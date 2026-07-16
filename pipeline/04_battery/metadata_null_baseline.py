#!/usr/bin/env python3
"""metadata_null_baseline.py — B7b metadata-only null baseline (validation
battery §B7b; analysis-plan v1.1 §8 B7b / §9 row B7b; freeze-manifest
item 21: "Probe prompt templates: ... B7b metadata-only baseline").

A NON-CODER context assigns the four study codes from the bibliographic
record ALONE — no abstract, no article text. This quantifies the
prior-driven coding ceiling (how far metadata + model priors alone reproduce
the codes); it is report-only (NOTE class, §9 row B7b) and never enters any
confirmatory denominator.

Prompt discipline (frozen here, per the plan's item-21 wording):
  * the probe prompt below is a SEPARATE MINIMAL TEMPLATE — it is NOT the
    built coder prompt with metadata inserted (pipeline/03_code/
    coder_prompt.txt is never loaded or used by this script);
  * the OUTPUT SCHEMA is identical to the coding schema (run_coders.py
    SCHEMA_KEYS; records validate through run_coders.validate_record), so
    downstream analysis can compute baseline headline estimates on the same
    machinery;
  * metadata sent per item: title, authors, journal, year (bibliographic
    record only; the blinding of the real coding runs is untouched — this
    probe runs analysis-side, on metadata the coders never see).

Providers (pins/endpoints, retry/backoff, JSON extraction, schema
validation) are reused from pipeline/03_code/run_coders.py via
battery_common. Every call is fresh and independent.

Output: data/battery/metadata_null_<batch>.jsonl, one line per item×family:
the validated coding record (item_id force-overwritten) + {"family",
"parse_fail"?}. Existing (item_id, family) pairs are skipped on restart;
failed HTTP calls are not written (retried on rerun).

Pre-P4 this script is exercised with --smoke only (built-in dummy
bibliographic record; real API calls; writes only
data/battery/smoke_metadata_null.jsonl) and --selftest (offline, no network).

Usage:
  python3 pipeline/04_battery/metadata_null_baseline.py \
      --meta data/raw/<corpus>.jsonl [--families a,b,c] [--limit N]
  python3 pipeline/04_battery/metadata_null_baseline.py --smoke
  python3 pipeline/04_battery/metadata_null_baseline.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

# ---------------------------------------------------------------- template
# FROZEN PROBE TEMPLATE (manifest item 21). A minimal, self-contained
# schema description — NOT the built coder prompt. Hash of this file
# freezes it.
PROBE_PROMPT = """You are given ONLY the bibliographic record of a journal article (no
abstract, no text). From this record alone, give your best guess for the
four codes below. Guess from what the record itself suggests; if it
licenses no guess for a dimension, use the NA-style value stated for it.

D1 step (one of S1-S8, B, P, I, M, X) — the thesis the article most
directly bears on:
  S1 physical reality as a whole has an external cause or ground
  S2 that ground is an agent with intentions and will
  S3 the agent is unique, a se, uncreated; all else depends on it
  S4 the ultimate is perfectly good
  S5 the good ultimate acts specially in the world post-creation
  S6 the authentic bearer of special revelation is the Hebrew prophetic tradition
  S7 Jesus of Nazareth was bodily raised (~AD 30)
  S8 the resurrection shows Jesus is God incarnate; God is triune
  B bundled full-God conclusion argued directly
  P pragmatic grounds for belief (wager-type)
  I intra-theistic attribute puzzle
  M methodology of theistic/atheistic case-making itself
  X out of scope
D2 direction (pro | contra | neutral | NA) — net effect on the step thesis
  (NA if D1 is X or I).
D3 claim strength (DEF | POS | NA) — DEF: defends coherence/rebuts an
  objection or claims warrant without propositional evidence; POS: claims
  evidence supports or disconfirms the thesis; NA if D2 is neutral or D1 is
  X or I.
D4 load-bearing epistemic type (alpha | beta | gamma | NA) — alpha: a
  priori/conceptual; beta: empirical contact; gamma: historical-documentary;
  NA if D1 is X or I, or nothing load-bearing is inferable.

Return JSON only, exactly this schema:
{
  "item_id": "string",
  "d1_step": "S1|S2|S3|S4|S5|S6|S7|S8|B|P|I|M|X",
  "d2_direction": "pro|contra|neutral|NA",
  "d3_strength": "DEF|POS|NA",
  "d4_type": "alpha|beta|gamma|NA",
  "flags": [],
  "confidence": 0.0,
  "uncertain_dimensions": ["..."],
  "rationale": "string, <= 40 words"
}

BIBLIOGRAPHIC RECORD (this is ALL you get):
{{metadata}}"""

METADATA_FIELDS = ["title", "authors", "journal", "year"]
MAX_CONSECUTIVE_ERRORS = 3

# Built-in SYNTHETIC dummy for --smoke (fictional record; no research item).
SMOKE_META = [{
    "item_id": "SMOKE-META-001",
    "title": "Does the Lighthouse Argument Illuminate? A Fabricated Reply to Nobody",
    "authors": ["Quenby Smokestack"],
    "journal": "Journal of Nonexistent Results",
    "year": "2099",
}]


def metadata_block(item: dict) -> str:
    lines = []
    for k in METADATA_FIELDS:
        v = item.get(k)
        if v is None or v == "":
            continue
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v)
        lines.append(f"{k}: {v}")
    return "\n".join(lines)


def build_probe(item: dict) -> str:
    return PROBE_PROMPT.replace("{{metadata}}", metadata_block(item))


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
          "report-only NOTE class — §9 row B7b)")
    for fam in families:
        rows = [r for (iid, f), r in recs.items() if f == fam and iid in wanted]
        okrows = [r for r in rows if not r.get("parse_fail")]
        from collections import Counter
        d1 = Counter(r.get("d1_step") for r in okrows)
        model = providers[fam].model if fam in providers else "?"
        print(f"  family {fam} ({model}): coded={len(okrows)}/{len(rows)} "
              f"parse_fail={len(rows) - len(okrows)} "
              f"d1 dist={dict(sorted(d1.items()))}")


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    """Offline: template/schema discipline checks. No network, no writes."""
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    m = bc.rc()

    # schema identity with the coding runs
    for key in m.SCHEMA_KEYS:
        check(f"template names schema key {key!r}", f'"{key}"' in PROBE_PROMPT)
    check("template D1 values = run_coders D1_VALUES",
          all(v in PROBE_PROMPT for v in m.D1_VALUES))
    check("template D4 values = run_coders D4_VALUES",
          all(v in PROBE_PROMPT for v in m.D4_VALUES))

    # a well-formed answer validates through run_coders.validate_record
    good = {"item_id": "x", "d1_step": "S4", "d2_direction": "contra",
            "d3_strength": "POS", "d4_type": "beta", "flags": [],
            "confidence": 0.4, "uncertain_dimensions": ["d4_type"],
            "rationale": "metadata-only guess"}
    clean, err = m.validate_record(good)
    check("well-formed record validates via run_coders.validate_record",
          clean is not None and err is None)
    bad = dict(good, d3_strength="CS4")
    clean, err = m.validate_record(bad)
    check("legacy scale value rejected by the shared validator",
          clean is None and "d3_strength" in (err or ""))

    # metadata discipline: bibliographic fields only, no abstract
    item = {"item_id": "i1", "title": "T", "authors": ["A B", "C D"],
            "journal": "J", "year": "2010", "abstract": "MUST NOT APPEAR",
            "text": "MUST NOT APPEAR EITHER"}
    probe = build_probe(item)
    check("probe carries title/authors/journal/year",
          all(s in probe for s in ("title: T", "authors: A B; C D",
                                   "journal: J", "year: 2010")))
    check("probe NEVER carries abstract/text fields",
          "MUST NOT APPEAR" not in probe)
    check("placeholder fully substituted", "{{metadata}}" not in probe)
    check("missing fields are omitted, not fabricated",
          "journal:" not in build_probe({"item_id": "i2", "title": "T2"}))

    # structural: this probe never touches the built coder prompt — no
    # string constant in the executable AST (module docstring excluded)
    # references it, so no code path can open/load it
    import ast
    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    if (tree.body and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)):
        tree.body = tree.body[1:]  # drop the module docstring
    needle = "coder_" + "prompt"   # avoid matching this scan's own constants
    refs = [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and needle in n.value]
    check("no executable string constant references the built coder prompt",
          refs == [])
    check("probe is not the built prompt (no {{text}} placeholder)",
          "{{text}}" not in PROBE_PROMPT)

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="B7b metadata-only null baseline (bibliographic record -> "
                    "coding schema; report-only).")
    ap.add_argument("--meta", nargs="+",
                    help="raw corpus JSONL(s): bibliographic records to code")
    ap.add_argument("--families", default="a,b,c")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", help="output override "
                    "(default data/battery/metadata_null_<batch>.jsonl)")
    ap.add_argument("--smoke", action="store_true",
                    help="built-in dummy record; writes smoke_metadata_null.jsonl only")
    ap.add_argument("--selftest", action="store_true",
                    help="offline template/schema tests; no network")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    families = bc.parse_families(args.families)
    bc.ensure_battery_dir()
    m = bc.rc()

    if args.smoke:
        items = SMOKE_META
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_metadata_null.jsonl")
        if os.path.exists(out_path):
            os.remove(out_path)  # smoke runs are idempotent
    else:
        if not args.meta:
            bc.die("--meta is required unless --smoke/--selftest", 2)
        items = []
        for p in args.meta:
            rp = m.resolve_path(p)
            if not os.path.exists(rp):
                bc.die(f"file not found: {rp}", 2)
            items.extend(bc.read_jsonl(rp))
        out_path = args.out or os.path.join(
            bc.BATTERY_DIR,
            f"metadata_null_{bc.batch_tag(m.resolve_path(args.meta[0]))}.jsonl")

    if args.limit is not None:
        items = items[: args.limit]

    providers = bc.make_providers(families)  # fail fast on missing keys
    done = load_done_pairs(out_path)
    print(f"[probe] {len(items)} record(s) x families {','.join(families)} -> "
          f"{out_path} (resume: {len(done)} pair(s) already done)")
    print("[probe] coding prompt NOT loaded — separate minimal metadata template")

    errors = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for fam in families:
            provider = providers[fam]
            consecutive = 0
            for item in items:
                iid = item.get("item_id")
                if not iid or (iid, fam) in done:
                    continue
                probe = build_probe(item)
                try:
                    text, meta = bc.call_provider(provider, probe)
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
                obj = m.extract_json_block(text)
                clean, err = (m.validate_record(obj) if isinstance(obj, dict)
                              else (None, "no JSON object found in output"))
                if clean is not None:
                    clean["item_id"] = iid  # force-overwrite (run_coders rule)
                    rec = dict(clean, family=fam, _meta=meta)
                else:
                    rec = {"item_id": iid, "family": fam, "parse_fail": True,
                           "raw": (text or "")[:500], "error": err, "_meta": meta}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                done.add((iid, fam))
                if args.smoke:
                    if rec.get("parse_fail"):
                        print(f"[smoke:{fam}] {iid}: parse_fail ({rec['error']})")
                    else:
                        print(f"[smoke:{fam}] {iid}: d1={rec['d1_step']} "
                              f"d2={rec['d2_direction']} d3={rec['d3_strength']} "
                              f"d4={rec['d4_type']} conf={rec['confidence']}")

    summarize(out_path, [i.get("item_id") for i in items], families, providers)
    if errors:
        print(f"[probe] {errors} call error(s) — rerun to retry missing pairs",
              file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
