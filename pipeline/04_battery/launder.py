#!/usr/bin/env python3
"""launder.py — paraphrase-laundering arm (validation battery, pipeline/04_battery/).

Takes a sanitized batch plus the recognition-probe results and, for every item
that at least one selected coder family IDENTIFIED (recognition record
identified=true), asks family E (Perplexity Agent API, perplexity/glm-5.2,
"tools": []) for a meaning-preserving paraphrase: thesis, claim strength,
number and strength of hedging expressions, technical terms, personal names
(dialectical opponents), and argument structure are preserved; sentence
structure and surface wording change; no summarizing, no added content.

If an identified item carries a non-empty `text_extra` (e.g. gold first/last
paragraphs), BOTH fields are laundered in the SAME E call — two labeled
sections in, two labeled sections out (one model pass keeps the register
consistent) — because a verbatim text_extra would re-identify the item.
The paraphrased fields are written back to their respective keys.

E-call machinery (api_call with structural tools=[], extract_text,
no_search_proof, hedge lexicon HEDGE_RE) is REUSED by importing
pipeline/00_criterion/generate_synthetics.py as a module (import has no side
effects; that file is never modified). The no_search_proof record is stored
per item exactly as generate_synthetics stores it.

Cue-fidelity checks (script-side, deterministic; hedge lexicon = the 12
word-group lexicon from generate_synthetics.HEDGE_RE — battery_common carries
no hedge lexicon, that regex is the single source of truth). When text_extra
is laundered too, every count is taken over BOTH fields COMBINED
(text + text_extra), original vs paraphrase:
  - |hedges(paraphrase) - hedges(original)| <= 1
  - 0.8 <= wordcount(paraphrase) / wordcount(original) <= 1.25
  - |modals(paraphrase) - modals(original)| <= 2  (must/cannot/would/should)
  - format sanity: plain prose only (no labels/markdown); with text_extra,
    the response must parse into exactly the two labeled sections
Failure => E is re-called with the failures as feedback, at most 3 content
attempts per item (search-trace discards do not count; hard cap 6 calls).
3 content failures => the record is written with "launder_failed": true and
the ORIGINAL text/text_extra (flagged, so downstream can exclude or re-run).

Unidentified items are copied through verbatim with "laundered": false.

Output (default data/battery/laundered_<batch>.jsonl), one line per item,
input order, run_coders.py --batch compatible (verified on write by re-loading
through run_coders.load_batch; extra keys are ignored by run_coders):
  {"item_id":..., "text":..., "text_extra":...,
   "laundered": bool, "attempts": int, "cue_checks": {...}|null,
   "no_search_proof": {...}|null}
text_extra holds the laundered version for laundered items that had one, and
the original (kept as-is) for passthrough and launder_failed items.
Plus, where applicable: "launder_failed": true, "gen_model", "fail_reasons".
Checkpoint/resume: existing item_ids in the output file are skipped on restart.

Usage:
  python3 pipeline/04_battery/launder.py \
      --sanitized data/sanitized/gold_anchors.jsonl \
      --recognition data/battery/recognition_gold_anchors.jsonl \
      [--families a,b,c] [--limit N] \
      [--out data/battery/laundered_gold_anchors.jsonl]
  python3 pipeline/04_battery/launder.py --smoke
      (one built-in dummy item WITH a dummy text_extra, full two-field launder
       round-trip with real E calls; writes ONLY data/battery/smoke_laundered.jsonl)

stdlib only, Python 3.10+.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

GS_PATH = os.path.join(bc.REPO_ROOT, "pipeline", "00_criterion",
                       "generate_synthetics.py")

MAX_CONTENT_ATTEMPTS = 3   # cue-check / content failures per item
MAX_TOTAL_CALLS = 6        # hard cap incl. discarded search-trace outputs
MAX_OUTPUT_TOKENS = 8192
MAX_CONSECUTIVE_API_FAILS = 3  # items in a row with only API errors => abort

HEDGE_DIFF_MAX = 1
WORD_RATIO_LO, WORD_RATIO_HI = 0.8, 1.25
MODAL_DIFF_MAX = 2
MODAL_RE = re.compile(r"\b(?:must|cannot|would|should)\b", re.IGNORECASE)
MODAL_HUMAN = "must, cannot, would, should"

_FENCE_RE = re.compile(r"^```[a-zA-Z]*\s*|\s*```$")

# Two-field mode (item has text_extra): E must answer with exactly these two
# labeled sections, in this order.
SEC_TEXT = "[PARAPHRASED ABSTRACT]"
SEC_EXTRA = "[PARAPHRASED EXCERPT]"
_SECTION_RE = re.compile(
    re.escape(SEC_TEXT) + r"\s*(?P<t>.*?)\s*" + re.escape(SEC_EXTRA)
    + r"\s*(?P<x>.*?)\s*$",
    re.S | re.I)

# Built-in SYNTHETIC dummy for --smoke (written for this script; not sourced
# from data/raw|sanitized|coded, describes nothing real). It carries hedges
# (may, suggests, could, perhaps / may, suggests, could) and modals (would,
# cannot, should / should) across BOTH fields so the combined-count
# cue-fidelity path and the two-field round-trip are actually exercised.
SMOKE_ITEM = {
    "item_id": "SMOKE-LND-001",
    "text": (
        "This synthetic validation abstract, written purely to test a "
        "paraphrasing pipeline, argues that imaginary municipal lighthouse "
        "maintenance schedules may track seabird nesting density, and it "
        "suggests that the fabricated correlation could survive casual "
        "scrutiny. The argument holds that any invented ledger of forty "
        "coastal stations would exhibit the pattern, that a skeptic cannot "
        "dismiss it without inspecting the fictional records, and that the "
        "conclusion should perhaps be read as a caution about spurious "
        "correlation rather than as a discovery. No real study, place, or "
        "person is described anywhere in this text."
    ),
    "text_extra": (
        "In closing, this fabricated final paragraph restates, purely for "
        "pipeline testing, that the invented lighthouse ledger may mislead a "
        "hasty reader, and it suggests that the pattern could vanish under "
        "closer inspection; any lesson drawn from it should therefore be "
        "treated as fictional. Nothing in this paragraph describes real "
        "research, real data, or real people."
    ),
}

_gs_module = None


def gs():
    """Import pipeline/00_criterion/generate_synthetics.py exactly once.

    Import has no side effects (main() is __main__-guarded); the file is
    never modified. Gives us api_call (tools structurally []), extract_text,
    no_search_proof, load_env_key, HEDGE_RE, GEN_MODEL.
    """
    global _gs_module
    if _gs_module is None:
        spec = importlib.util.spec_from_file_location("generate_synthetics",
                                                      GS_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot import {GS_PATH}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _gs_module = mod
    return _gs_module


# --------------------------------------------------------------- cue fidelity

def word_count(text: str) -> int:
    return len((text or "").split())


def hedge_count(text: str) -> int:
    return len(gs().HEDGE_RE.findall(text or ""))


def modal_count(text: str) -> int:
    return len(MODAL_RE.findall(text or ""))


def normalize_output(text: str) -> str:
    """Light mechanical normalization only: strip code fences + whitespace."""
    t = (text or "").strip()
    t = _FENCE_RE.sub("", t).strip()
    return t


def parse_two_sections(raw: str):
    """Parse the two-field response. -> (para_text, para_extra) or None."""
    m = _SECTION_RE.search(raw or "")
    if not m:
        return None
    para_text, para_extra = m.group("t").strip(), m.group("x").strip()
    if not para_text or not para_extra:
        return None
    if "[PARAPHRASED" in para_text.upper() or "[PARAPHRASED" in para_extra.upper():
        return None  # duplicated / repeated section labels
    return para_text, para_extra


def cue_check(original: str, paraphrase: str, two_field: bool = False) -> tuple:
    """-> (checks: dict, failures: list[str]). Deterministic, script-side.

    In two-field mode the caller passes text + text_extra CONCATENATED for
    both `original` and `paraphrase`: all counts are combined over the two
    fields, per the combined-basis rule."""
    failures = []
    scope = " (counted over the abstract and the excerpt together)" if two_field else ""
    ow, pw = word_count(original), word_count(paraphrase)
    oh, ph = hedge_count(original), hedge_count(paraphrase)
    om, pm = modal_count(original), modal_count(paraphrase)
    ratio = (pw / ow) if ow else 0.0

    if abs(ph - oh) > HEDGE_DIFF_MAX:
        failures.append(
            f"hedge-lexicon count{scope} is {ph} in the paraphrase but {oh} "
            f"in the original; the difference must be at most {HEDGE_DIFF_MAX}. "
            f"Preserve the hedging of the original. Hedge lexicon "
            f"(case-insensitive): {gs().HEDGE_LEXICON_HUMAN}")
    if not (WORD_RATIO_LO <= ratio <= WORD_RATIO_HI):
        failures.append(
            f"paraphrase is {pw} words vs {ow} in the original{scope} "
            f"(ratio {ratio:.2f}); it must stay between {WORD_RATIO_LO}x and "
            f"{WORD_RATIO_HI}x of the original length — do not summarize, "
            f"compress, or pad")
    if abs(pm - om) > MODAL_DIFF_MAX:
        failures.append(
            f"strong-modal count ({MODAL_HUMAN}){scope} is {pm} in the "
            f"paraphrase but {om} in the original; the difference must be at "
            f"most {MODAL_DIFF_MAX} — preserve the modal strength of each claim")
    if re.match(r"^\s*(abstract\b|title\b|paraphrase\b|#)", paraphrase, re.I) \
            or "**" in paraphrase:
        failures.append(
            "output must be ONLY the plain paraphrased text: no "
            "'Abstract:'/'Paraphrase:' label, no title, no markdown")

    checks = {
        "basis": "text+text_extra" if two_field else "text",
        "orig_words": ow, "para_words": pw, "word_ratio": round(ratio, 3),
        "word_ratio_band": [WORD_RATIO_LO, WORD_RATIO_HI],
        "orig_hedges": oh, "para_hedges": ph, "hedge_diff_max": HEDGE_DIFF_MAX,
        "orig_modals": om, "para_modals": pm, "modal_diff_max": MODAL_DIFF_MAX,
        "pass": not failures,
    }
    return checks, failures


# ------------------------------------------------------------- prompt building

LAUNDER_INSTRUCTIONS = (
    "You are an expert academic editor producing meaning-preserving paraphrases "
    "of scholarly texts for a methodological validation study. You preserve "
    "the thesis, the strength of every claim, the number and strength of hedging "
    "expressions, all technical terminology, all personal names (including "
    "dialectical opponents and cited figures), and the argumentative structure. "
    "You change the sentence structure and the surface vocabulary. You never "
    "summarize, compress, or add content. You output only the paraphrased text, "
    "formatted exactly as instructed: continuous prose, no titles, no markdown, "
    "no commentary.")


def build_launder_input(text: str, extra, feedback_history: list) -> str:
    two_field = bool(extra)
    what = ("the following academic abstract AND the additional excerpt from "
            "the same paper" if two_field else "the following academic abstract")
    lines = [
        f"Paraphrase {what}, preserving the meaning.",
        "",
        "REQUIREMENTS:",
        "- Preserve the thesis and every claim exactly; do not strengthen or "
        "weaken any claim.",
        "- Preserve hedging: keep the number and the strength of hedging "
        "expressions (e.g. may, might, perhaps, suggests, seems, could, "
        "possibly) the same as in the original.",
        "- Preserve all technical terms and all personal names (opponents, "
        "cited figures) exactly as written.",
        "- Preserve the argument structure: the order and role of every "
        "argumentative move.",
        "- Change the sentence structure and the surface vocabulary: do not "
        "reuse the original sentence shapes or distinctive phrasing.",
        "- Do NOT summarize or compress: each paraphrase must be about the "
        "same length as its original.",
        "- Do NOT add content, examples, or claims absent from the original.",
    ]
    if two_field:
        lines += [
            "- Paraphrase the two passages separately: do not merge them, "
            "reorder them, or move content between them.",
            "",
            "[ORIGINAL ABSTRACT]",
            text,
            "",
            "[ORIGINAL ADDITIONAL EXCERPT FROM THE SAME PAPER]",
            extra,
            "",
            "OUTPUT FORMAT — exactly these two labeled sections and nothing "
            "else (keep the bracketed labels verbatim, each on its own line):",
            SEC_TEXT,
            "<the paraphrased abstract>",
            SEC_EXTRA,
            "<the paraphrased excerpt>",
            "No other labels, no quotation marks around the texts, no notes.",
        ]
    else:
        lines += [
            "",
            "[ORIGINAL ABSTRACT]",
            text,
            "",
            "OUTPUT: the paraphrased abstract text only — no labels, no "
            "quotation marks around the whole text, no notes.",
        ]
    if feedback_history:
        prev_text, prev_failures = feedback_history[-1]
        lines += ["", "=" * 40,
                  "YOUR PREVIOUS PARAPHRASE FAILED VALIDATION.",
                  "Previous paraphrase:", prev_text, "",
                  "Validation failures to fix:"]
        lines += [f"- {f}" for f in prev_failures]
        lines += ["",
                  "Write a corrected paraphrase that fixes ALL listed failures "
                  "while still meeting every requirement above. Do not simply "
                  "resubmit the previous text."]
    return "\n".join(lines)


# --------------------------------------------------------------- per-item run

def launder_item(item: dict) -> dict:
    """Launder one identified item via E. Returns the output record.

    Items with a non-empty text_extra are laundered two-field: both passages
    go into the SAME E call and come back as two labeled sections; cue checks
    run on the combined counts. Retry caps and no_search_proof handling are
    identical in both modes."""
    g = gs()
    iid = item["item_id"]
    original = item.get("text") or ""
    orig_extra = item.get("text_extra") or None
    two_field = bool(orig_extra)
    orig_combined = original + ("\n\n" + orig_extra if two_field else "")
    feedback_history = []
    content_attempts = 0
    total_calls = 0
    last_checks = None
    last_proof = None
    api_error_only = True

    while content_attempts < MAX_CONTENT_ATTEMPTS and total_calls < MAX_TOTAL_CALLS:
        total_calls += 1
        try:
            resp = g.api_call(g.GEN_MODEL, LAUNDER_INSTRUCTIONS,
                              build_launder_input(original, orig_extra,
                                                  feedback_history),
                              MAX_OUTPUT_TOKENS)
        except RuntimeError as e:
            content_attempts += 1
            print(f"  [error] {iid} call {total_calls}: API error: {e}",
                  file=sys.stderr)
            feedback_history.append(("(no text produced)", [f"API error: {e}"]))
            continue

        api_error_only = False
        clean, proof = g.no_search_proof(resp, g.GEN_MODEL)
        if not clean:
            # same policy as generate_synthetics: discard, does not count as
            # a content attempt (hard total-call cap still applies)
            print(f"  [warn] {iid} call {total_calls}: search traces in "
                  f"response — output discarded, re-calling", file=sys.stderr)
            last_proof = proof
            continue
        last_proof = proof

        raw = normalize_output(g.extract_text(resp))
        content_attempts += 1
        if not raw:
            feedback_history.append(
                ("(empty output)",
                 ["the response contained no text; output the paraphrased "
                  "text only, in the required format"]))
            continue

        if two_field:
            parsed = parse_two_sections(raw)
            if parsed is None:
                print(f"  [cue-fail] {iid} attempt {content_attempts}: "
                      f"two-section format not parseable", file=sys.stderr)
                feedback_history.append(
                    (raw,
                     [f"the output must consist of exactly two labeled "
                      f"sections in this order and nothing else: a line "
                      f"'{SEC_TEXT}' followed by the paraphrased abstract, "
                      f"then a line '{SEC_EXTRA}' followed by the paraphrased "
                      f"excerpt; both sections must be non-empty and the "
                      f"labels must appear exactly once"]))
                continue
            para_text, para_extra = parsed
            para_combined = para_text + "\n\n" + para_extra
        else:
            para_text, para_extra = raw, None
            para_combined = raw

        checks, failures = cue_check(orig_combined, para_combined, two_field)
        last_checks = checks
        if failures:
            print(f"  [cue-fail] {iid} attempt {content_attempts}: "
                  f"{failures[0][:100]}", file=sys.stderr)
            feedback_history.append((raw, failures))
            continue

        return {
            "item_id": iid,
            "text": para_text,
            "text_extra": para_extra if two_field else item.get("text_extra"),
            "laundered": True,
            "attempts": content_attempts,
            "cue_checks": checks,
            "no_search_proof": proof,
            "gen_model": g.GEN_MODEL,
        }

    # 3 content failures (or call cap): flag; keep the ORIGINAL text and
    # text_extra so the record stays uniform/codable — downstream must
    # exclude or re-run these.
    rec = {
        "item_id": iid,
        "text": original,
        "text_extra": item.get("text_extra"),
        "laundered": False,
        "launder_failed": True,
        "attempts": content_attempts,
        "cue_checks": last_checks,
        "no_search_proof": last_proof,
        "gen_model": g.GEN_MODEL,
        "fail_reasons": [f for _, fs in feedback_history for f in fs][-3:],
    }
    rec["_api_error_only"] = api_error_only  # internal, stripped before write
    return rec


def passthrough_record(item: dict) -> dict:
    return {
        "item_id": item["item_id"],
        "text": item.get("text"),
        "text_extra": item.get("text_extra"),
        "laundered": False,
        "attempts": 0,
        "cue_checks": None,
        "no_search_proof": None,
    }


# -------------------------------------------------------------- identification

def identified_ids(recognition_path: str, families: list) -> set:
    """item_ids identified by ANY selected family (last record wins per
    (item_id, family), mirroring recognition_probe.summarize)."""
    last = {}
    for rec in bc.read_jsonl(recognition_path):
        iid, fam = rec.get("item_id"), rec.get("family")
        if iid and fam:
            last[(iid, fam)] = bool(rec.get("identified"))
    return {iid for (iid, fam), ident in last.items()
            if ident and fam in families}


def recognition_coverage(recognition_path: str, families: list) -> set:
    covered = set()
    for rec in bc.read_jsonl(recognition_path):
        if rec.get("item_id") and rec.get("family") in families:
            covered.add(rec["item_id"])
    return covered


# ------------------------------------------------------------------------ main

def verify_run_coders_compat(out_path: str):
    """Re-load the output through run_coders.load_batch (same check as
    make_stubs): guarantees --batch compatibility."""
    n = len(bc.rc().load_batch(out_path))
    print(f"[verify] {out_path}: {n} record(s) re-loaded via "
          f"run_coders.load_batch — --batch compatible")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Paraphrase-launder recognition-identified items via "
                    "family E (search structurally off).")
    ap.add_argument("--sanitized", help="sanitized JSONL (items to process)")
    ap.add_argument("--recognition",
                    help="recognition-probe results JSONL (identified flags)")
    ap.add_argument("--families", default="a,b,c",
                    help="families whose identified=true marks an item for "
                         "laundering (any-of); default a,b,c")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out",
                    help="output override (default data/battery/laundered_<batch>.jsonl)")
    ap.add_argument("--smoke", action="store_true",
                    help="one built-in dummy text, full launder round-trip; "
                         "writes only data/battery/smoke_laundered.jsonl")
    args = ap.parse_args(argv)

    bc.ensure_battery_dir()
    g = gs()

    if args.smoke:
        g.API_KEY = g.load_env_key("PERPLEXITY_API_KEY")  # value never printed
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_laundered.jsonl")
        if os.path.exists(out_path):
            os.remove(out_path)  # smoke runs are idempotent
        print(f"[smoke] laundering 1 dummy item (text + text_extra, one call) "
              f"via {g.GEN_MODEL} (tools=[]) -> {out_path}")
        rec = launder_item(SMOKE_ITEM)
        rec.pop("_api_error_only", None)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok = bool(
            rec.get("laundered")
            and (rec.get("cue_checks") or {}).get("pass")
            and (rec.get("no_search_proof") or {}).get("clean")
            and rec.get("text") and rec.get("text") != SMOKE_ITEM["text"]
            and rec.get("text_extra")
            and rec.get("text_extra") != SMOKE_ITEM["text_extra"])
        print(f"[smoke] laundered={rec.get('laundered')} "
              f"attempts={rec.get('attempts')} "
              f"cue_checks={json.dumps(rec.get('cue_checks'))} "
              f"no_search_clean={ (rec.get('no_search_proof') or {}).get('clean') }")
        if rec.get("laundered"):
            print(f"[smoke] paraphrased text: {rec['text']}")
            print(f"[smoke] paraphrased text_extra: {rec['text_extra']}")
        verify_run_coders_compat(out_path)
        print(f"[smoke] {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1

    if not args.sanitized or not args.recognition:
        bc.die("--sanitized and --recognition are both required unless --smoke", 2)
    m = bc.rc()
    san_path = m.resolve_path(args.sanitized)
    rec_path = m.resolve_path(args.recognition)
    for p in (san_path, rec_path):
        if not os.path.exists(p):
            bc.die(f"file not found: {p}", 2)
    families = bc.parse_families(args.families)

    items = bc.read_jsonl(san_path)
    if args.limit is not None:
        items = items[: args.limit]
    for it in items:
        if not it.get("item_id"):
            bc.die(f"{san_path}: item missing item_id", 4)

    targets = identified_ids(rec_path, families)
    covered = recognition_coverage(rec_path, families)
    missing = [it["item_id"] for it in items if it["item_id"] not in covered]
    if missing:
        print(f"  [warn] {len(missing)} item(s) have no recognition record for "
              f"families {','.join(families)} (treated as unidentified — "
              f"probe incomplete?): {', '.join(missing[:10])}"
              f"{' ...' if len(missing) > 10 else ''}", file=sys.stderr)

    out_path = args.out or os.path.join(
        bc.BATTERY_DIR, f"laundered_{bc.batch_tag(san_path)}.jsonl")
    done = set()
    if os.path.exists(out_path):
        for rec in bc.read_jsonl(out_path):
            if rec.get("item_id"):
                done.add(rec["item_id"])

    n_target = sum(1 for it in items if it["item_id"] in targets)
    print(f"[launder] {len(items)} item(s), {n_target} identified by any of "
          f"families {{{','.join(families)}}} -> launder via {g.GEN_MODEL}; "
          f"rest copied verbatim")
    print(f"[launder] out={out_path} (resume: {len(done)} already done)")

    if any(it["item_id"] in targets and it["item_id"] not in done
           for it in items):
        g.API_KEY = g.load_env_key("PERPLEXITY_API_KEY")  # value never printed

    n_laundered = n_copied = n_failed = 0
    consecutive_api_fails = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for item in items:
            iid = item["item_id"]
            if iid in done:
                continue
            if iid in targets:
                rec = launder_item(item)
                api_only = rec.pop("_api_error_only", False)
                if rec.get("launder_failed"):
                    n_failed += 1
                    consecutive_api_fails = consecutive_api_fails + 1 if api_only else 0
                    print(f"  [launder_failed] {iid} after "
                          f"{rec['attempts']} attempt(s)", file=sys.stderr)
                    if consecutive_api_fails >= MAX_CONSECUTIVE_API_FAILS:
                        print(f"  [abort] {consecutive_api_fails} consecutive "
                              f"items with API errors only — stopping; rerun "
                              f"to resume", file=sys.stderr)
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        f.flush()
                        break
                else:
                    n_laundered += 1
                    consecutive_api_fails = 0
                    print(f"  [ok] {iid}: laundered in {rec['attempts']} "
                          f"attempt(s), wc {rec['cue_checks']['orig_words']}"
                          f"->{rec['cue_checks']['para_words']}, hedges "
                          f"{rec['cue_checks']['orig_hedges']}"
                          f"->{rec['cue_checks']['para_hedges']}")
            else:
                rec = passthrough_record(item)
                n_copied += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            done.add(iid)

    print(f"[launder] done: laundered={n_laundered} copied={n_copied} "
          f"failed={n_failed} (total in file: {len(done)}/{len(items)})")
    if n_failed:
        print(f"[launder] {n_failed} launder_failed item(s) kept ORIGINAL "
              f"text — exclude or re-run before using this arm", file=sys.stderr)
    verify_run_coders_compat(out_path)
    return 1 if n_failed else 0


if __name__ == "__main__":
    sys.exit(main())
