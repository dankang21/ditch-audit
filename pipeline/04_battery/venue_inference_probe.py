#!/usr/bin/env python3
"""venue_inference_probe.py — B9 venue-register control probe (validation
battery §B9; analysis-plan v1.1 §9 row B9; freeze-manifest item 21:
"Probe prompt templates: ... B9 venue-inference probe").

Each coder family (a=Anthropic, b=Google, c=OpenAI — pins/endpoints reused
from pipeline/03_code/run_coders.py) classifies the venue TIER of a sanitized
abstract from the text alone and returns a probability that the venue is T3.
This is a probe, NOT a coding run: coder_prompt.txt is never used or loaded.
Every call is fresh and independent (single user message, no state).

Scoring (script-side, deterministic):
  * truth label = frozen venue-tier table (manifest item 9) joined on the
    RAW metadata's journal field (D5 is metadata-joined, never coded);
  * per-family AUC on T3-vs-rest by the Mann–Whitney rank statistic over the
    reported p_t3 scores (ties count 1/2). Records whose p_t3 is missing or
    unparseable fall back to the hard tier label (T3 -> 1.0, else 0.0);
    fully unparseable responses are excluded from the AUC and counted
    `invalid`;
  * §9 row B9 trigger read: MAX over the three families' AUCs > 0.65
    (most conservative aggregation, frozen v1.3). The trigger's consequences
    (laundered-arm switch, §6 eligibility rule) live in the plan/battery, not
    here — this script measures and reports.

Run phase: P4 (battery §B9 — the P1 pilot corpus is single-tier, so
T3-vs-rest AUC is not estimable earlier). Pre-P4 this script is exercised
with --smoke only (built-in dummy items with dummy tier labels; real API
calls; writes only data/battery/smoke_venue_inference.jsonl) and --selftest
(offline, no network).

Output: data/battery/venue_inference_<batch>.jsonl, one line per item×family:
  {"item_id", "family", "tier_true", "tier_pred", "p_t3", "response"}
Existing (item_id, family) pairs are skipped on restart; failed calls are not
written (retried on rerun). Summary (per-family AUC + trigger read) on stdout.

Usage:
  python3 pipeline/04_battery/venue_inference_probe.py \
      --sanitized data/sanitized/<batch>.jsonl --meta data/raw/<corpus>.jsonl... \
      [--families a,b,c] [--limit N] [--tiers overrides.json]
  python3 pipeline/04_battery/venue_inference_probe.py --smoke
  python3 pipeline/04_battery/venue_inference_probe.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

# ---------------------------------------------------------------- template
# FROZEN PROBE TEMPLATE (manifest item 21). Hash of this file freezes it.
PROBE_PROMPT = (
    "You will read one sanitized journal-article abstract from a philosophy-"
    "of-religion study corpus. Judge, from the TEXT ALONE, the register of "
    "the venue it most likely appeared in:\n"
    "  T1 = elite general philosophy journal (broad-scope analytic "
    "philosophy; religion is one topic among many).\n"
    "  T2 = mainstream specialist philosophy-of-religion journal "
    "(analytic, non-confessional).\n"
    "  T3 = confessional or apologetics-adjacent journal (faith-committed "
    "editorial identity).\n"
    "Do not try to identify the specific paper, author, or journal; judge "
    "register, style, and framing only. Respond as JSON only:\n"
    '{"tier": "T1"|"T2"|"T3", "p_t3": <number in [0,1], your probability '
    'that the venue is T3>, "rationale": "<= 25 words"}'
)

VALID_TIERS = {"T1", "T2", "T3"}
AUC_TRIGGER = 0.65          # §9 row B9 frozen trigger (MAX over families)
MAX_CONSECUTIVE_ERRORS = 3

# Frozen venue-tier assignment table (manifest item 9; F&P = T2 primary,
# the R2 flip is a preregistered sensitivity via --tiers).
DEFAULT_TIERS = {
    "mind": "T1", "analysis": "T1", "the philosophical quarterly": "T1",
    "philosophical quarterly": "T1", "philosophical studies": "T1",
    "noûs": "T1", "nous": "T1", "american philosophical quarterly": "T1",
    "religious studies": "T2", "international journal for philosophy of religion": "T2",
    "sophia": "T2", "faith and philosophy": "T2",
    "philosophia christi": "T3",
}

# Built-in SYNTHETIC dummies for --smoke (machine-written for this script;
# the tier labels are dummy fixtures, no research item text).
SMOKE_SANITIZED = [
    {"item_id": "SMOKE-VEN-001",
     "text": ("This synthetic validation abstract argues, for pipeline "
              "testing only, that an invented modal principle entails an "
              "invented conclusion about grounding, with no empirical "
              "premise anywhere.")},
    {"item_id": "SMOKE-VEN-002",
     "text": ("A second machine-written placeholder abstract, defending a "
              "fabricated tradition-internal doctrinal harmony claim purely "
              "to exercise a venue-register classifier.")},
]
SMOKE_META = [
    {"item_id": "SMOKE-VEN-001", "journal": "Mind"},
    {"item_id": "SMOKE-VEN-002", "journal": "Philosophia Christi"},
]


def build_probe(item: dict) -> str:
    return PROBE_PROMPT + "\n\n[ABSTRACT]\n" + (item.get("text") or "")


def parse_response(response: str):
    """-> (tier_pred or None, p_t3 or None). Deterministic, script-side."""
    obj = bc.rc().extract_json_block(response or "")
    if not isinstance(obj, dict):
        return None, None
    tier = obj.get("tier")
    tier = tier.strip().upper() if isinstance(tier, str) else None
    if tier not in VALID_TIERS:
        tier = None
    p = obj.get("p_t3")
    try:
        p = float(p)
    except (TypeError, ValueError):
        p = None
    if p is not None and not (0.0 <= p <= 1.0):
        p = None
    return tier, p


def score_of(rec):
    """AUC score for one record: p_t3 if present, else hard-label fallback;
    None if fully unparseable (excluded from AUC, counted invalid)."""
    if rec.get("p_t3") is not None:
        return float(rec["p_t3"])
    if rec.get("tier_pred") in VALID_TIERS:
        return 1.0 if rec["tier_pred"] == "T3" else 0.0
    return None


def auc_t3_vs_rest(pairs):
    """Mann–Whitney AUC. pairs = [(score, is_t3_bool)]; ties count 1/2.
    Returns None if either class is empty."""
    pos = sorted(s for s, y in pairs if y)
    neg = sorted(s for s, y in pairs if not y)
    if not pos or not neg:
        return None
    import bisect
    wins = 0.0
    for s in pos:
        lo = bisect.bisect_left(neg, s)
        hi = bisect.bisect_right(neg, s)
        wins += lo + 0.5 * (hi - lo)
    return wins / (len(pos) * len(neg))


def tier_of(meta_rec, tiers_tab):
    j = " ".join((meta_rec.get("journal") or "").split()).casefold()
    return tiers_tab.get(j)


def load_done_pairs(path: str) -> set:
    done = set()
    if os.path.exists(path):
        for rec in bc.read_jsonl(path):
            if rec.get("item_id") and rec.get("family"):
                done.add((rec["item_id"], rec["family"]))
    return done


def summarize(out_path: str, item_ids: list, families: list, providers: dict):
    recs = {}
    if os.path.exists(out_path):
        for rec in bc.read_jsonl(out_path):
            recs[(rec.get("item_id"), rec.get("family"))] = rec  # last wins
    wanted = set(item_ids)
    print(f"\n[summary] {os.path.basename(out_path)} ({len(wanted)} item(s); "
          f"B9 trigger = MAX family AUC > {AUC_TRIGGER}, T3-vs-rest)")
    aucs = {}
    for fam in families:
        rows = [r for (iid, f), r in recs.items() if f == fam and iid in wanted]
        pairs, invalid = [], 0
        for r in rows:
            s = score_of(r)
            if s is None:
                invalid += 1
            elif r.get("tier_true") in VALID_TIERS:
                pairs.append((s, r["tier_true"] == "T3"))
        auc = auc_t3_vs_rest(pairs)
        aucs[fam] = auc
        acc_n = sum(1 for r in rows if r.get("tier_pred") and r.get("tier_true"))
        acc_k = sum(1 for r in rows if r.get("tier_pred")
                    and r.get("tier_pred") == r.get("tier_true"))
        model = providers[fam].model if fam in providers else "?"
        auc_s = "n/a (single class or no data)" if auc is None else f"{auc:.3f}"
        print(f"  family {fam} ({model}): n={len(rows)} AUC(T3-vs-rest)={auc_s} "
              f"tier-acc={bc.pct(acc_k, acc_n)} invalid={invalid}")
    known = [a for a in aucs.values() if a is not None]
    if known:
        mx = max(known)
        print(f"  MAX family AUC = {mx:.3f} -> B9 trigger "
              f"{'FIRES' if mx > AUC_TRIGGER else 'does not fire'} "
              f"(consequences per plan §9 row B9 / §6 eligibility rule)")
    return aucs


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    """Offline: parsing, AUC, tier join. No network, no writes."""
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    t, p = parse_response('{"tier": "t3", "p_t3": 0.82, "rationale": "r"}')
    check("parses tier (case-normalized) + p_t3", t == "T3" and p == 0.82)
    t, p = parse_response('```json\n{"tier":"T1","p_t3":"0.1"}\n```')
    check("parses fenced JSON and numeric strings", t == "T1" and p == 0.1)
    t, p = parse_response('{"tier":"T9","p_t3":1.7}')
    check("rejects bad tier and out-of-range p", t is None and p is None)
    t, p = parse_response("no json here")
    check("unparseable -> (None, None)", t is None and p is None)

    check("score fallback: hard label when p_t3 missing",
          score_of({"p_t3": None, "tier_pred": "T3"}) == 1.0
          and score_of({"p_t3": None, "tier_pred": "T2"}) == 0.0
          and score_of({"p_t3": None, "tier_pred": None}) is None)

    # AUC: perfect separation, ties, known hand value
    check("AUC perfect separation = 1",
          auc_t3_vs_rest([(0.9, True), (0.8, True), (0.2, False)]) == 1.0)
    check("AUC all-tied scores = 0.5",
          auc_t3_vs_rest([(0.5, True), (0.5, False), (0.5, False)]) == 0.5)
    # hand computation: pos {0.9, 0.4}, neg {0.6, 0.4, 0.1}
    # 0.9 beats 3; 0.4 beats 0.1, ties 0.4 -> 1.5; AUC = 4.5/6
    check("AUC hand value 4.5/6",
          abs(auc_t3_vs_rest([(0.9, True), (0.4, True),
                              (0.6, False), (0.4, False), (0.1, False)])
              - 4.5 / 6) < 1e-12)
    check("AUC single-class -> None",
          auc_t3_vs_rest([(0.9, True)]) is None)

    check("frozen tier table joins journals (whitespace/case-insensitive)",
          tier_of({"journal": "  Philosophia   Christi "}, DEFAULT_TIERS) == "T3"
          and tier_of({"journal": "MIND"}, DEFAULT_TIERS) == "T1"
          and tier_of({"journal": "Unknown Venue"}, DEFAULT_TIERS) is None)

    check("probe template mentions all three tiers and requests p_t3",
          all(s in PROBE_PROMPT for s in ("T1", "T2", "T3", "p_t3")))
    check("probe never loads the coding prompt (structural)",
          "coder_prompt" not in PROBE_PROMPT)

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="B9 venue-inference probe (tier from sanitized text; AUC).")
    ap.add_argument("--sanitized", help="sanitized JSONL (probe input)")
    ap.add_argument("--meta", nargs="+",
                    help="raw corpus JSONL(s) with journal metadata (truth join)")
    ap.add_argument("--tiers", help="JSON journal->tier overrides "
                    "(default: frozen tier table; use for the R2 F&P flip)")
    ap.add_argument("--families", default="a,b,c")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", help="output override "
                    "(default data/battery/venue_inference_<batch>.jsonl)")
    ap.add_argument("--smoke", action="store_true",
                    help="built-in dummy items + dummy tier labels; writes "
                         "smoke_venue_inference.jsonl only")
    ap.add_argument("--selftest", action="store_true",
                    help="offline scoring/parsing tests; no network")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    families = bc.parse_families(args.families)
    bc.ensure_battery_dir()
    m = bc.rc()

    tiers_tab = dict(DEFAULT_TIERS)
    if args.tiers:
        for k, v in json.load(open(args.tiers, encoding="utf-8")).items():
            tiers_tab[" ".join(k.split()).casefold()] = v

    if args.smoke:
        items, meta_items = SMOKE_SANITIZED, SMOKE_META
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_venue_inference.jsonl")
        if os.path.exists(out_path):
            os.remove(out_path)  # smoke runs are idempotent
    else:
        if not args.sanitized or not args.meta:
            bc.die("--sanitized and --meta are both required unless --smoke/--selftest", 2)
        san_path = m.resolve_path(args.sanitized)
        if not os.path.exists(san_path):
            bc.die(f"file not found: {san_path}", 2)
        items = bc.read_jsonl(san_path)
        meta_items = []
        for p in args.meta:
            rp = m.resolve_path(p)
            if not os.path.exists(rp):
                bc.die(f"file not found: {rp}", 2)
            meta_items.extend(bc.read_jsonl(rp))
        out_path = args.out or os.path.join(
            bc.BATTERY_DIR, f"venue_inference_{bc.batch_tag(san_path)}.jsonl")

    if args.limit is not None:
        items = items[: args.limit]
    truth = {}
    for r in meta_items:
        if r.get("item_id"):
            truth.setdefault(r["item_id"], tier_of(r, tiers_tab))

    providers = bc.make_providers(families)  # fail fast on missing keys
    done = load_done_pairs(out_path)
    print(f"[probe] {len(items)} item(s) x families {','.join(families)} -> "
          f"{out_path} (resume: {len(done)} pair(s) already done)")
    print("[probe] coding prompt NOT loaded — venue-register probe prompt only")

    errors = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for fam in families:
            provider = providers[fam]
            consecutive = 0
            for item in items:
                iid = item["item_id"]
                if (iid, fam) in done:
                    continue
                if truth.get(iid) not in VALID_TIERS:
                    print(f"  [warn] {iid}: no venue-tier truth label — skipped",
                          file=sys.stderr)
                    continue
                try:
                    text, _meta = bc.call_provider(provider, build_probe(item))
                except m.HTTPCallError as e:
                    errors += 1
                    consecutive += 1
                    print(f"  [error] {iid} family={fam}: HTTP {e.status}: "
                          f"{e.body[:200]}", file=sys.stderr)
                    if consecutive >= MAX_CONSECUTIVE_ERRORS:
                        print(f"  [abort] family {fam}: {consecutive} "
                              "consecutive errors", file=sys.stderr)
                        break
                    continue
                consecutive = 0
                tier_pred, p_t3 = parse_response(text)
                rec = {"item_id": iid, "family": fam,
                       "tier_true": truth[iid], "tier_pred": tier_pred,
                       "p_t3": p_t3, "response": text}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                done.add((iid, fam))
                if args.smoke:
                    print(f"[smoke:{fam}] {iid}: true={rec['tier_true']} "
                          f"pred={tier_pred} p_t3={p_t3}")

    summarize(out_path, [i["item_id"] for i in items], families, providers)
    if errors:
        print(f"[probe] {errors} call error(s) — rerun to retry missing pairs",
              file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
