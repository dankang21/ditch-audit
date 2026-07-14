#!/usr/bin/env python3
"""recognition_probe.py — recognition probe (validation battery arm).

Asks each of the three coder families (a=Anthropic claude-sonnet-5,
b=Google gemini-3.5-flash, c=OpenAI gpt-5.5-2026-04-23 — pins and endpoints
reused from pipeline/03_code/run_coders.py) to IDENTIFY the bibliographic
source of a sanitized abstract. This is a probe, NOT a coding run: the coding
prompt (coder_prompt.txt) is never used or loaded. Every call is fresh and
independent (single user message, no conversation state).

Scoring (script-side, deterministic):
  identified = (any true author's family name appears as a token in the
                response's author field, falling back to the whole response
                if no JSON author field was parseable)
            OR (>= 60% of the true title's major words — stopwords removed,
                len >= 3 — appear in the response's title field / whole
                response fallback).
  A bare UNKNOWN reply is never identified.

Output: data/battery/recognition_<batch>.jsonl, one line per item x family:
  {"item_id": ..., "family": "a"|"b"|"c", "response": <full text>, "identified": bool}
Failed calls are NOT written (they are retried on the next invocation);
existing (item_id, family) pairs are skipped on restart (checkpoint/resume).
Summary (identification rate per family) goes to stdout.

Usage:
  python3 pipeline/04_battery/recognition_probe.py \
      --sanitized data/sanitized/gold_anchors.jsonl --raw data/raw/gold_anchors.jsonl \
      [--families a,b,c] [--limit N]
  python3 pipeline/04_battery/recognition_probe.py --smoke
      (built-in dummy abstract + dummy answer key; real API calls, no research
       item text; writes only data/battery/smoke_recognition.jsonl)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

PROBE_PROMPT = (
    "The following is a sanitized journal-article abstract. Name the author(s), "
    "title, journal, and year of the paper it comes from. If you cannot identify "
    "it, reply exactly UNKNOWN. Respond as JSON: "
    '{"author":..., "title":..., "journal":..., "year":...} or "UNKNOWN".'
)

TITLE_OVERLAP_THRESHOLD = 0.60
MAX_CONSECUTIVE_ERRORS = 3

_NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}

# Built-in SYNTHETIC dummies for --smoke (no research item text; the "answer
# key" is fictional, so the scoring path runs but nothing real is probed).
SMOKE_SANITIZED = [
    {
        "item_id": "SMOKE-REC-001",
        "text": (
            "This synthetic validation abstract examines whether municipal "
            "lighthouse maintenance schedules correlate with seabird nesting "
            "density, using a fabricated dataset of forty coastal stations. "
            "It exists only to exercise a pipeline and describes no real study."
        ),
        "text_extra": None,
    },
    {
        "item_id": "SMOKE-REC-002",
        "text": (
            "We present an invented framework for classifying imaginary garden "
            "mazes by hedge topology and argue, purely for pipeline testing, "
            "that no such classification can be complete."
        ),
        "text_extra": None,
    },
]
SMOKE_RAW = [
    {
        "item_id": "SMOKE-REC-001",
        "title": "Lighthouse Maintenance and Seabird Nesting: A Fabricated Correlational Study",
        "authors": ["Quenby Smokestack"],
        "journal": "Journal of Nonexistent Results",
        "year": "2099",
    },
    {
        "item_id": "SMOKE-REC-002",
        "title": "Hedge Topology and the Incompleteness of Imaginary Maze Classification",
        "authors": ["Testa Dummyfield"],
        "journal": "Annals of Pipeline Validation",
        "year": "2098",
    },
]


def build_probe(item: dict) -> str:
    msg = PROBE_PROMPT + "\n\n[ABSTRACT]\n" + (item.get("text") or "")
    extra = item.get("text_extra")
    if extra:
        msg += "\n\n[ADDITIONAL EXCERPT FROM THE SAME PAPER]\n" + extra
    return msg


def is_unknown(response: str) -> bool:
    s = (response or "").strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s).strip()
    return s.strip(" \"'.`").casefold() == "unknown"


def family_names(authors) -> list:
    """Family (last) name per author, suffixes (Jr/III/...) dropped, casefolded."""
    fams = []
    for a in authors or []:
        toks = re.findall(r"[A-Za-z][A-Za-z'’-]*", str(a))
        toks = [t for t in toks if t.casefold().strip(".") not in _NAME_SUFFIXES]
        if toks:
            fams.append(re.sub(r"[^a-z0-9]", "", toks[-1].casefold()))
    return [f for f in fams if f]


def title_major_words(title: str) -> list:
    return [w for w in bc.tokens(title) if len(w) >= 3 and w not in bc.STOPWORDS]


def score_response(response: str, truth: dict):
    """-> (identified: bool, detail: dict) against the raw answer key."""
    if is_unknown(response):
        return False, {"unknown": True, "author_hit": False, "title_overlap": 0.0}
    obj = bc.rc().extract_json_block(response)
    resp_author = resp_title = None
    if isinstance(obj, dict):
        ra = obj.get("author") or obj.get("authors")
        if ra is not None:
            resp_author = ra if isinstance(ra, str) else json.dumps(ra, ensure_ascii=False)
        rt = obj.get("title")
        if rt is not None:
            resp_title = rt if isinstance(rt, str) else json.dumps(rt, ensure_ascii=False)

    hay_author = set(bc.tokens(resp_author if resp_author else response))
    hay_title = set(bc.tokens(resp_title if resp_title else response))

    fams = family_names(truth.get("authors"))
    author_hit = any(f in hay_author for f in fams)

    major = title_major_words(truth.get("title") or "")
    overlap = (sum(1 for w in major if w in hay_title) / len(major)) if major else 0.0

    identified = author_hit or overlap >= TITLE_OVERLAP_THRESHOLD
    return identified, {"unknown": False, "author_hit": author_hit,
                        "title_overlap": round(overlap, 3)}


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
    print(f"\n[summary] {os.path.basename(out_path)} ({len(wanted)} item(s))")
    for fam in families:
        rows = [r for (iid, f), r in recs.items() if f == fam and iid in wanted]
        ident = sum(1 for r in rows if r.get("identified"))
        model = providers[fam].model if fam in providers else "?"
        print(f"  family {fam} ({model}): identified {ident}/{len(rows)} "
              f"({bc.pct(ident, len(rows))}) missing={len(wanted) - len(rows)}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Recognition probe (identification, not coding).")
    ap.add_argument("--sanitized", help="sanitized JSONL (probe input)")
    ap.add_argument("--raw", help="matching raw JSONL (answer key: authors/title)")
    ap.add_argument("--families", default="a,b,c")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", help="output override (default data/battery/recognition_<batch>.jsonl)")
    ap.add_argument("--smoke", action="store_true",
                    help="built-in dummy item + dummy answer key; writes smoke_recognition.jsonl")
    args = ap.parse_args(argv)

    families = bc.parse_families(args.families)
    bc.ensure_battery_dir()
    m = bc.rc()

    if args.smoke:
        items, raw_items = SMOKE_SANITIZED, SMOKE_RAW
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_recognition.jsonl")
        if os.path.exists(out_path):
            os.remove(out_path)  # smoke runs are idempotent
    else:
        if not args.sanitized or not args.raw:
            bc.die("--sanitized and --raw are both required unless --smoke", 2)
        san_path, raw_path = m.resolve_path(args.sanitized), m.resolve_path(args.raw)
        for p in (san_path, raw_path):
            if not os.path.exists(p):
                bc.die(f"file not found: {p}", 2)
        items = bc.read_jsonl(san_path)
        raw_items = bc.read_jsonl(raw_path)
        out_path = args.out or os.path.join(
            bc.BATTERY_DIR, f"recognition_{bc.batch_tag(san_path)}.jsonl")

    if args.limit is not None:
        items = items[: args.limit]
    truth = {r["item_id"]: r for r in raw_items if r.get("item_id")}

    providers = bc.make_providers(families)  # fail fast on missing keys
    done = load_done_pairs(out_path)
    print(f"[probe] {len(items)} item(s) x families {','.join(families)} -> {out_path}"
          f" (resume: {len(done)} pair(s) already done)")
    print("[probe] coding prompt NOT loaded — probe prompt only")

    errors = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for fam in families:
            provider = providers[fam]
            consecutive = 0
            for item in items:
                iid = item["item_id"]
                if (iid, fam) in done:
                    continue
                if iid not in truth:
                    print(f"  [warn] {iid}: no raw answer-key record — skipped", file=sys.stderr)
                    continue
                probe = build_probe(item)
                try:
                    text, _meta = bc.call_provider(provider, probe)
                except m.HTTPCallError as e:
                    errors += 1
                    consecutive += 1
                    print(f"  [error] {iid} family={fam}: HTTP {e.status}: {e.body[:200]}",
                          file=sys.stderr)
                    if consecutive >= MAX_CONSECUTIVE_ERRORS:
                        print(f"  [abort] family {fam}: {consecutive} consecutive errors",
                              file=sys.stderr)
                        break
                    continue
                consecutive = 0
                identified, detail = score_response(text, truth[iid])
                rec = {"item_id": iid, "family": fam, "response": text,
                       "identified": identified}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                done.add((iid, fam))
                if args.smoke:
                    print(f"[smoke:{fam}] {iid}: identified={identified} detail={detail}")

    summarize(out_path, [i["item_id"] for i in items], families, providers)
    if errors:
        print(f"[probe] {errors} call error(s) — rerun to retry missing pairs", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
