#!/usr/bin/env python3
"""make_stubs.py — cue-ablation stub generator (validation battery arm; LOCAL
ONLY, zero API calls).

For each sanitized item, builds an argument-free stub:
  (a) the first clause of the first sentence, capped at --max-words (12) words
      — nothing of the original text after that first clause is ever emitted;
  (b) one line "Topic keywords: k1, k2, ..." — TF-top tokens (<= --topk, 5)
      from the item's `text` field after removing stopwords + academic
      boilerplate (len >= 3, alphanumeric). `text_extra` (gold last paragraphs)
      is deliberately excluded from keyword extraction: it carries conclusion
      content and the ablation is meant to be strict.

Deterministic: sentence/clause splitting is pure string processing; keyword
ties break by (count desc, token asc); output order = input order. Any early
false sentence break (e.g. an abbreviation period) only SHORTENS the stub —
errors always fall on the safe (less-leakage) side.

Output schema per line: {"item_id": ..., "text": <stub>, "text_extra": null}
— directly usable as run_coders.py --batch input (verified on write by
re-loading through run_coders.load_batch).

Usage:
  python3 pipeline/04_battery/make_stubs.py --batch data/sanitized/pilot_rs2015.jsonl
      -> data/battery/stubs_pilot_rs2015.jsonl
  python3 pipeline/04_battery/make_stubs.py --smoke
      -> data/battery/smoke_stubs.jsonl (built-in dummy texts only)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

MAX_HEAD_WORDS = 12
TOPK = 5

# Sentence end: . ! or ? followed by whitespace or end-of-text.
_SENT_END_RE = re.compile(r"[.!?](?=\s|$)")
# Clause boundary inside the first sentence: comma/semicolon/colon, or a
# spaced dash (em/en/double-hyphen). A hyphen inside a word never matches.
_CLAUSE_RE = re.compile(r"[,;:]|\s[—–]\s?|\s--\s?|\s-\s")

# Built-in SYNTHETIC dummies for --smoke. Written for this script; not sourced
# from data/raw|sanitized|coded and not real abstracts.
SMOKE_ITEMS = [
    {
        "item_id": "SMOKE-STUB-001",
        "text": (
            "This synthetic validation abstract, written solely for pipeline "
            "testing, contends that municipal lighthouse maintenance schedules "
            "track seabird nesting density; the fabricated dataset covers forty "
            "coastal stations. No real study is described here. The lighthouse "
            "keepers, the seabirds, and the maintenance ledger are all invented."
        ),
        "text_extra": None,
    },
    {
        "item_id": "SMOKE-STUB-002",
        "text": (
            "A short dummy text with a first sentence that runs well past the "
            "twelve word cap before any clause boundary ever appears in it. "
            "Second sentence adds fake keywords: topiary topiary topiary maze "
            "maze hedge hedge hedge classification classification."
        ),
        "text_extra": "This extra field must be ignored by keyword extraction.",
    },
]


def first_clause(text: str, max_words: int = MAX_HEAD_WORDS) -> str:
    """First clause of the first sentence, capped at max_words words."""
    t = " ".join((text or "").split())  # normalize whitespace
    m = _SENT_END_RE.search(t)
    sentence = t[: m.start()] if m else t
    m2 = _CLAUSE_RE.search(sentence)
    clause = sentence[: m2.start()] if m2 else sentence
    words = clause.split()
    return " ".join(words[:max_words]).strip()


def topic_keywords(text: str, k: int = TOPK) -> list:
    """TF-top <=k topic tokens; stopwords/boilerplate removed; deterministic."""
    drop = bc.STOPWORDS | bc.BOILERPLATE
    counts = {}
    for tok in bc.tokens(text):
        if len(tok) < 3 or tok in drop or tok.isdigit():
            continue
        counts[tok] = counts.get(tok, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [tok for tok, _ in ranked[:k]]


def build_stub(item: dict, max_words: int, topk: int) -> dict:
    head = first_clause(item.get("text") or "", max_words)
    kws = topic_keywords(item.get("text") or "", topk)
    stub_text = head + " ..."
    if kws:
        stub_text += "\nTopic keywords: " + ", ".join(kws)
    return {"item_id": item["item_id"], "text": stub_text, "text_extra": None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Cue-ablation stub generator (local only, no API).")
    ap.add_argument("--batch", help="sanitized JSONL, e.g. data/sanitized/pilot_rs2015.jsonl")
    ap.add_argument("--out", help="output path override (default data/battery/stubs_<batch>.jsonl)")
    ap.add_argument("--max-words", type=int, default=MAX_HEAD_WORDS)
    ap.add_argument("--topk", type=int, default=TOPK)
    ap.add_argument("--smoke", action="store_true",
                    help="built-in dummy texts only -> data/battery/smoke_stubs.jsonl")
    args = ap.parse_args(argv)

    bc.ensure_battery_dir()
    if args.smoke:
        items = SMOKE_ITEMS
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_stubs.jsonl")
    else:
        if not args.batch:
            bc.die("--batch is required unless --smoke is given", 2)
        batch_path = bc.rc().resolve_path(args.batch)
        if not os.path.exists(batch_path):
            bc.die(f"batch file not found: {batch_path}", 2)
        items = bc.read_jsonl(batch_path)
        out_path = args.out or os.path.join(bc.BATTERY_DIR, f"stubs_{bc.batch_tag(batch_path)}.jsonl")

    stubs = []
    for it in items:
        if not it.get("item_id"):
            bc.die("input item missing item_id", 4)
        stub = build_stub(it, args.max_words, args.topk)
        # invariants: head <= max_words words; nothing beyond first clause
        head_line = stub["text"].split("\n", 1)[0]
        assert len(head_line.replace(" ...", "").split()) <= args.max_words
        stubs.append(stub)

    with open(out_path, "w", encoding="utf-8") as f:
        for s in stubs:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # compatibility check: output must load as a run_coders --batch input
    loaded = bc.rc().load_batch(out_path)
    if len(loaded) != len(stubs):
        bc.die("round-trip check failed: run_coders.load_batch item count mismatch", 5)

    print(f"[stubs] wrote {len(stubs)} stub(s) -> {out_path}")
    print("[stubs] run_coders.load_batch round-trip: OK "
          f"(schema keys: item_id, text, text_extra)")
    if args.smoke:
        for s in stubs:
            print(f"[stubs:smoke] {s['item_id']}: {json.dumps(s['text'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
