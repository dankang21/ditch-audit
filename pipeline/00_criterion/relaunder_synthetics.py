#!/usr/bin/env python3
"""Style-relaunder the 60 synthetic criterion items (round 1 of max 3).

Context: discriminator gate failed (balanced acc A 0.88 / B 0.87 / C 0.99 vs
criterion <=0.60); diagnosed cue = sentence-length profile (gen mean 27.5 words
vs pilot 23.4). This script asks the SAME author model E (perplexity/glm-5.2,
tools:[]) for a style-only rewrite of each item: shorter sentences (mean ~23,
hard cap mean <=25), content/claims/hedge-count/numeric figures preserved.

Reuses (unmodified) from generate_synthetics.py: api_call, no_search_proof,
extract_text, mech_check, hedge lexicon, blacklist, spec loading.
The harness never writes or edits item text; only E authors text.
Kimi re-check is SKIPPED this round by prereg'd decision (style-only transform);
its substitute is the mechanical invariance check: hedge count and the exact
multiset of digit strings must be unchanged from v1.

stdlib only.
"""
import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_synthetics as gs  # noqa: E402  (reused, not modified)

# Slow-API hardening (2026-07-14 pm: E latency degraded to 200-2000 s/call).
# gs.api_call reads these module globals at call time; the module file itself
# is untouched. Read timeout 600 s; timeouts stay inside the retry+backoff loop.
gs.HTTP_TIMEOUT = 600


def append_fsync(path, obj):
    """Durable per-item checkpoint: append + flush + fsync immediately."""
    with gs._file_lock:
        with open(path, "a") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

OUT_DIR = gs.OUT_DIR
V1_DEV = OUT_DIR / "synthetic_dev.jsonl"
V1_VAULT = OUT_DIR / "synthetic_vault.jsonl"
V2_DEV = OUT_DIR / "synthetic_dev_v2.jsonl"
V2_VAULT = OUT_DIR / "synthetic_vault_v2.jsonl"
WORK_PATH = OUT_DIR / "relaunder_results.jsonl"
ATTEMPTS_PATH = OUT_DIR / "relaunder_attempts.jsonl"

RESTYLE_ROUND = 1
MAX_ATTEMPTS = 3          # content attempts per item
MAX_TOTAL_CALLS = 6       # incl. search-trace discards
MEAN_SENT_CAP = 25.0
MEAN_SENT_TARGET = 23

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
DIGIT_TOKEN = re.compile(r"\d+(?:\.\d+)?")


def sent_stats(text):
    sents = [s for s in SENT_SPLIT.split(text) if s.strip()]
    lens = [len(s.split()) for s in sents]
    mean = sum(lens) / len(lens) if lens else 0.0
    return round(mean, 2), len(sents)


def relaunder_checks(spec, v1_text, v2_text):
    """Full v1 mechanical battery + round-1 style/invariance additions."""
    checks, failures = gs.mech_check(spec, v2_text)

    mean_len, n_sents = sent_stats(v2_text)
    checks["mean_sentence_len"] = mean_len
    checks["n_sentences"] = n_sents
    if mean_len > MEAN_SENT_CAP:
        failures.append(
            f"mean sentence length is {mean_len} words; it must be at most "
            f"{MEAN_SENT_CAP:.0f} (target about {MEAN_SENT_TARGET}) — break long "
            f"sentences into shorter ones without cutting content")

    v1_h = len(gs.HEDGE_RE.findall(v1_text))
    v2_h = len(gs.HEDGE_RE.findall(v2_text))
    checks["hedge_count_v1"] = v1_h
    checks["hedge_invariant"] = (v1_h == v2_h)
    if v1_h != v2_h:
        failures.append(
            f"hedge-lexicon count changed: original has exactly {v1_h}, rewrite has "
            f"{v2_h}; the total must remain exactly {v1_h} "
            f"(lexicon: {gs.HEDGE_LEXICON_HUMAN})")

    v1_nums = Counter(DIGIT_TOKEN.findall(v1_text))
    v2_nums = Counter(DIGIT_TOKEN.findall(v2_text))
    checks["digit_strings_v1"] = sorted(v1_nums.elements())
    checks["digit_strings_v2"] = sorted(v2_nums.elements())
    checks["numbers_invariant"] = (v1_nums == v2_nums)
    if v1_nums != v2_nums:
        failures.append(
            f"numeric figures changed: original digit strings "
            f"{sorted(v1_nums.elements())}, rewrite has "
            f"{sorted(v2_nums.elements())}; keep exactly the original figures, "
            f"no more and no fewer")

    checks["pass"] = not failures
    return checks, failures


def build_restyle_input(spec, item, feedback_history):
    lo, hi = spec["length_band"]
    quota = len(gs.HEDGE_RE.findall(item["text"]))
    is_cs5 = spec["target"].get("d3_strength") == "CS5"
    figs = sorted(set(DIGIT_TOKEN.findall(item["text"])))

    lines = []
    lines.append("Restyle the following synthetic academic abstract. This is a "
                 "STYLE-ONLY rewrite: keep the content, the line of argument, and "
                 "every claim at exactly its original strength. Do not summarize, do "
                 "not add material, do not drop material, do not reorder the argument.")
    lines.append("")
    lines.append("PRESERVE EXACTLY:")
    lines.append("- every claim, premise, qualification, and its strength")
    lines.append(f"- the total count of hedge-lexicon words: exactly {quota} "
                 f"occurrence(s) from this lexicon (case-insensitive; these surface "
                 f"forms only): {gs.HEDGE_LEXICON_HUMAN}. You may relocate them or "
                 f"swap one lexicon word for another, but the total must stay "
                 f"exactly {quota}. Count before finalizing.")
    if is_cs5:
        lines.append(f"- the explicit numeric figure(s), verbatim in digits: "
                     f"{', '.join(figs)}. Introduce no other digits.")
    else:
        lines.append("- the absence of digits: the rewrite must contain NO digits; "
                     "keep all quantities spelled out in words.")
    lines.append(f"- overall length within {lo}-{hi} words (whitespace-separated "
                 f"tokens)")
    lines.append("")
    lines.append("CHANGE:")
    lines.append(f"- sentence rhythm: break long sentences into shorter ones. Target "
                 f"a mean sentence length of about {MEAN_SENT_TARGET} words; the mean "
                 f"MUST be at most {MEAN_SENT_CAP:.0f} words. Mix shorter and longer "
                 f"sentences so the abstract reads with the natural rhythm of a "
                 f"published journal abstract, not a list of clauses.")
    lines.append("- you may adjust connectives, punctuation, and clause order within "
                 "sentences as needed for the new rhythm, provided meaning and claim "
                 "strength are untouched.")
    lines.append("")
    lines.append("PROHIBITIONS (unchanged from the original brief): no real author "
                 "names, real works, real journals, real institutions; no new claims; "
                 "no meta-commentary.")
    lines.append("")
    lines.append("OUTPUT: the restyled abstract text only — no title, no label, no "
                 "quotation marks around it, no notes.")
    lines.append("")
    lines.append("ORIGINAL ABSTRACT:")
    lines.append(item["text"])

    if feedback_history:
        prev_text, prev_failures = feedback_history[-1]
        lines.append("")
        lines.append("=" * 40)
        lines.append("YOUR PREVIOUS REWRITE FAILED VALIDATION.")
        lines.append("Previous rewrite:")
        lines.append(prev_text)
        lines.append("")
        lines.append("Validation failures to fix:")
        for f in prev_failures:
            lines.append(f"- {f}")
        lines.append("")
        lines.append("Produce a corrected rewrite that fixes ALL listed failures "
                     "while still meeting every requirement above.")
    return "\n".join(lines)


def run_item(item, spec):
    sid = item["item_id"]
    feedback_history = []
    attempts = 0
    total_calls = 0
    t0 = time.time()

    while attempts < MAX_ATTEMPTS and total_calls < MAX_TOTAL_CALLS:
        total_calls += 1
        try:
            resp = gs.api_call(gs.GEN_MODEL, gs.GEN_INSTRUCTIONS,
                               build_restyle_input(spec, item, feedback_history), 8192)
        except RuntimeError as e:
            attempts += 1
            append_fsync(ATTEMPTS_PATH, {"item_id": sid, "call": total_calls,
                                            "phase": "restyle", "error": str(e)})
            gs.log(f"[{sid}] restyle call {total_calls}: API error: {e}")
            feedback_history.append(("(no text produced)", [f"API error: {e}"]))
            continue

        if not isinstance(resp, dict):
            # api_call can yield None on some degraded-API paths instead of raising;
            # treat exactly like an API error (retryable), never abort the run.
            attempts += 1
            append_fsync(ATTEMPTS_PATH, {"item_id": sid, "call": total_calls,
                                            "phase": "restyle",
                                            "error": f"non-dict response: {type(resp).__name__}"})
            gs.log(f"[{sid}] restyle call {total_calls}: non-dict response ({type(resp).__name__}) -> retry")
            feedback_history.append(("(no text produced)", ["API returned no usable response"]))
            continue

        clean, proof = gs.no_search_proof(resp, gs.GEN_MODEL)
        text = gs.extract_text(resp)
        usage = resp.get("usage", {})
        rec = {"item_id": sid, "call": total_calls, "phase": "restyle",
               "model": gs.GEN_MODEL, "text": text, "no_search_proof": proof,
               "usage": {k: usage.get(k) for k in
                         ("input_tokens", "output_tokens", "total_tokens")}}

        if not clean:
            rec["outcome"] = "discarded_search_traces"
            append_fsync(ATTEMPTS_PATH, rec)
            gs.log(f"[{sid}] call {total_calls}: SEARCH TRACES -> discard & re-call")
            continue
        if not text:
            attempts += 1
            rec["outcome"] = "empty_output"
            append_fsync(ATTEMPTS_PATH, rec)
            feedback_history.append(("(empty output)",
                                     ["the response contained no abstract text"]))
            continue

        attempts += 1
        checks, failures = relaunder_checks(spec, item["text"], text)
        rec["mech_checks"] = checks
        if failures:
            rec["outcome"] = "mech_fail"
            rec["mech_failures"] = failures
            append_fsync(ATTEMPTS_PATH, rec)
            gs.log(f"[{sid}] attempt {attempts}: fail: {failures[0][:90]}")
            feedback_history.append((text, failures))
            continue

        rec["outcome"] = "accepted"
        append_fsync(ATTEMPTS_PATH, rec)
        out = dict(item)  # same schema as v1 record
        out.update({
            "text": text,
            "gen_attempts": attempts,          # this round's E calls
            "no_search_proof": {"generator": proof,
                                "checker": item["no_search_proof"]["checker"]},
            "mech_checks": checks,
            "restyle_round": RESTYLE_ROUND,
            # kimi_verdict carried over from v1 (content-invariant transform;
            # Kimi re-check skipped this round per coordinator instruction)
        })
        append_fsync(WORK_PATH, out)
        m, n = checks["mean_sentence_len"], checks["n_sentences"]
        gs.log(f"[{sid}] OK in {attempts} attempt(s), {time.time()-t0:.0f}s, "
               f"wc={checks['word_count']}, meansent={m} ({n} sents)")
        return out

    out = dict(item)
    out.update({"restyle_round": RESTYLE_ROUND, "restyle_failed": True,
                "gen_attempts": attempts})
    append_fsync(WORK_PATH, out)
    gs.log(f"[{sid}] RESTYLE FAILED after {attempts} attempts — keeping v1 text")
    return out


def load_work():
    """Read per-item checkpoints from disk; last record per item_id wins."""
    done = {}
    if WORK_PATH.exists():
        for line in WORK_PATH.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["item_id"]] = r
    return done


def assemble_v2(specs):
    """Build v2 dev/vault files purely from the on-disk work file."""
    done = load_work()
    order = {s: i for i, s in enumerate(specs)}
    results = sorted(done.values(), key=lambda r: order.get(r["item_id"], 999))
    with open(V2_DEV, "w") as fd, open(V2_VAULT, "w") as fv:
        for r in results:
            line = json.dumps(r, ensure_ascii=False) + "\n"
            (fd if r["half"] == "dev" else fv).write(line)
    ok = [r for r in results if not r.get("restyle_failed")]
    failed = [r["item_id"] for r in results if r.get("restyle_failed")]
    return len(ok), failed, len(results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", help="comma-separated item_ids (default: all 60)")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--fresh", action="store_true",
                    help="ignore existing checkpoints (default: resume)")
    args = ap.parse_args()

    gs.API_KEY = gs.load_env_key("PERPLEXITY_API_KEY")

    specs = {s["spec_id"]: s for s in
             json.loads(gs.SPECS_PATH.read_text())["specs"]}
    items = []
    for p in (V1_DEV, V1_VAULT):
        for line in p.read_text().splitlines():
            if line.strip():
                items.append(json.loads(line))
    assert len(items) == 60, f"expected 60 v1 items, got {len(items)}"

    if args.items:
        wanted = set(args.items.split(","))
        items = [i for i in items if i["item_id"] in wanted]

    # resume is the DEFAULT: any item_id already checkpointed is skipped
    if not args.fresh:
        done = load_work()
        items = [i for i in items if i["item_id"] not in done]
        gs.log(f"resume: {len(done)} checkpointed, {len(items)} to run")

    exit_code = 0
    try:
        # results are NOT accumulated in memory; run_item checkpoints each
        # item to WORK_PATH (append+flush+fsync) the moment it finishes
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(run_item, it, specs[it["item_id"]]): it["item_id"]
                    for it in items}
            for fut in concurrent.futures.as_completed(futs):
                fut.result()
    except BaseException as e:
        exit_code = 1
        gs.log(f"run aborted: {type(e).__name__}: {e}")
    finally:
        n_ok, failed, n_total = assemble_v2(specs)
        n_missing = 60 - n_total
        if (failed or n_missing) and exit_code == 0:
            exit_code = 1
        gs.log(f"done: restyled={n_ok} failed={len(failed)} ({failed}) "
               f"missing={n_missing}")
        gs.log(f"EXIT code={exit_code} restyled={n_ok} failed={len(failed)} "
               f"missing={n_missing} of 60")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
