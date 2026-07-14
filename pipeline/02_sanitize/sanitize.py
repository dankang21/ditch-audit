#!/usr/bin/env python3
# Implements codebook-v1.md §2 (canonical). Prereqs: Python 3.10+, stdlib only.
# In:  data/raw/*.jsonl (harvester schema; contains author/title/journal/year/doi)
# Out: data/sanitized/<name>.jsonl        -> {"item_id","text","text_extra"}
#      data/sanitized/scrub_log.jsonl     -> {"item_id","rule","before","after"}
#      data/sanitized/exclusions.jsonl    -> {"item_id","reason"} (items dropped)
#
# Blindness contract (codebook §1/§2):
#   * Output carries ONLY {item_id, text, text_extra}; every metadata field is dropped.
#   * In-text self-identifiers are scrubbed: "in this journal", "as I (have) argued
#     in <year>", proper-name self-citations "<Author> (<year>)" and "my <year>
#     book/paper <Title>", the item's OWN journal name in a citation, and the item's
#     OWN author name used self-referentially (-> role tag "[the author]").
#   * Opponent / interlocutor names are CONTENT and are kept (rule §2.3).
#   * Author list + journal are read here to drive scrubs; they are NEVER emitted.
#   * Abstract < 60 words -> text_extra (null when no source paragraph held) + LOWTEXT.
#   * Missing/empty abstract -> item EXCLUDED from sanitized output (cannot code empty).
#   * Borderline self-identification is NOT auto-deleted; it is left in place and the
#     residual is surfaced by the caller's heuristic sweep for human (dk) judgement.
# Deterministic: same input -> same output (pure regex, stable ordering).

from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "data" / "raw"
OUT = REPO / "data" / "sanitized"

PAD = 28  # context chars kept on each side of a scrub in before/after snippets
LOWTEXT_WORDS = 60
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
NON_AUTHOR = {"the society of christian philosophers"}


def _snip(text: str, start: int, end: int, replacement: str) -> tuple[str, str]:
    """Return (before, after) snippets around a single scrub span in `text`."""
    left = text[max(0, start - PAD):start]
    right = text[end:end + PAD]
    before = (left + text[start:end] + right)
    after = (left + replacement + right)
    ws = re.compile(r"\s+")
    return ws.sub(" ", before).strip(), ws.sub(" ", after).strip()


def _surname(author: str) -> str | None:
    if author.strip().lower() in NON_AUTHOR:
        return None
    toks = [t for t in re.split(r"\s+", author.strip()) if t]
    toks = [t for t in toks if t.strip(".,").lower() not in SUFFIXES]
    return toks[-1].strip(".,") if toks else None


def _apply(text: str, pattern: re.Pattern, repl, item_id: str, rule: str, log: list) -> str:
    """Apply `pattern` left-to-right; log each match as its own scrub entry.

    `repl` is a string (may contain \\1 backrefs) or a callable(match)->str.
    Matching is done against the pre-substitution string of this pass so spans
    stay valid for snippet extraction.
    """
    src = text
    out = []
    cursor = 0
    for m in pattern.finditer(src):
        replacement = m.expand(repl) if isinstance(repl, str) else repl(m)
        before, after = _snip(src, m.start(), m.end(), replacement)
        log.append({"item_id": item_id, "rule": rule, "before": before, "after": after})
        out.append(src[cursor:m.start()])
        out.append(replacement)
        cursor = m.end()
    out.append(src[cursor:])
    return "".join(out)


def sanitize_record(rec: dict, log: list) -> tuple[dict | None, str | None]:
    """Return (sanitized_record | None, exclusion_reason | None)."""
    item_id = rec["item_id"]
    abstract = (rec.get("abstract") or "").strip()
    if not abstract or rec.get("missing_abstract"):
        return None, "missing_abstract"

    authors = rec.get("authors") or []
    journal = rec.get("journal")
    surnames = [s for s in (_surname(a) for a in authors) if s]
    full_matched = False
    text = abstract

    # R1 — venue self-identifier "in this journal" (§2.2). Drop the phrase.
    text = _apply(
        text,
        re.compile(r"\s+in this journal\b", re.IGNORECASE),
        "", item_id, "in_this_journal", log,
    )

    # R2 — "as I (have) argued in <year>" self-reference (§2.2).
    text = _apply(
        text,
        re.compile(r"\bas I (?:have )?argued in \(?\d{4}[a-z]?\)?", re.IGNORECASE),
        "as I argued elsewhere", item_id, "self_reference_year", log,
    )

    # R3 — proper-name self-citation "<OwnAuthor> (<year>)" (§2.2). Own authors only;
    # opponent citations like "Plantinga (2011)" are kept as content.
    for sn in surnames:
        text = _apply(
            text,
            re.compile(r"\b" + re.escape(sn) + r"\s*\(\d{4}[a-z]?\)", re.IGNORECASE),
            "earlier work", item_id, "self_citation", log,
        )

    # R4 — self book/paper citation "my <year> book/paper <Title>" (§2.2).
    text = _apply(
        text,
        re.compile(r"\bmy \d{4} (?:book|monograph|paper|article)\b[^.]*\.", re.IGNORECASE),
        "my earlier work.", item_id, "self_citation", log,
    )

    # R5 — item's OWN journal name leaked inside a citation parenthetical (§2.1/§2.2).
    # Collapse "( <Journal> , vol (YYYY), pp )" -> "(YYYY)"; discipline mentions of the
    # journal name outside a citation are left alone (no bare substitution).
    if journal:
        text = _apply(
            text,
            re.compile(r"\(\s*" + re.escape(journal) + r"\s*,[^()]*\((\d{4})\)[^()]*\)"),
            r"(\1)", item_id, "journal_name", log,
        )

    # R6 — item's OWN author name used self-referentially -> role tag (§2.3).
    # Replace the full name first; only if a full name matched (confident self-ref,
    # e.g. a 3rd-person blurb) do we also replace the bare surname, to avoid touching
    # a same-named third party.
    for author in authors:
        if author.strip().lower() in NON_AUTHOR:
            continue
        toks = [re.escape(t.strip(".,")) for t in re.split(r"\s+", author.strip())
                if t.strip(".,") and t.strip(".,").lower() not in SUFFIXES]
        if len(toks) < 2:
            continue
        full = r"\b" + r"\.?\s+".join(toks) + r"\.?" + r"(?:,?\s+(?:Jr|Sr|II|III|IV)\.?)?"
        pat = re.compile(full)
        if pat.search(text):
            text = _apply(text, pat, "[the author]", item_id, "self_name_role_tag", log)
            full_matched = True
    if full_matched:
        for sn in surnames:
            text = _apply(
                text,
                re.compile(r"\b" + re.escape(sn) + r"\b"),
                "[the author]", item_id, "self_name_role_tag", log,
            )

    text = re.sub(r"[ \t]{2,}", " ", text).strip()

    word_count = len(text.split())
    lowtext = word_count < LOWTEXT_WORDS
    # No source first/last paragraph is held in raw -> text_extra stays null even for
    # LOWTEXT items; the LOWTEXT flag is surfaced to the coder downstream.
    out = {"item_id": item_id, "text": text, "text_extra": None}
    if lowtext:
        out["_lowtext"] = True  # transient marker; stripped before write
    return out, None


def process(name: str, log: list, excluded: list, lowtext: list) -> int:
    src = RAW / f"{name}.jsonl"
    dst = OUT / f"{name}.jsonl"
    written = 0
    with src.open(encoding="utf-8") as fin, dst.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out, reason = sanitize_record(rec, log)
            if out is None:
                excluded.append({"item_id": rec["item_id"], "reason": reason})
                continue
            if out.pop("_lowtext", False):
                lowtext.append(out["item_id"])
            fout.write(json.dumps(out, ensure_ascii=False) + "\n")
            written += 1
    return written


def main(argv: list[str]) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    names = argv[1:] or ["pilot_rs2015", "gold_anchors"]
    log: list = []
    excluded: list = []
    lowtext: list = []
    counts = {}
    for name in names:
        counts[name] = process(name, log, excluded, lowtext)

    with (OUT / "scrub_log.jsonl").open("w", encoding="utf-8") as f:
        for e in log:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with (OUT / "exclusions.jsonl").open("w", encoding="utf-8") as f:
        for e in excluded:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print("=== sanitize summary ===")
    for name, n in counts.items():
        print(f"  {name}: {n} written")
    print(f"  scrub_log entries: {len(log)}")
    print(f"  excluded (missing abstract): {len(excluded)} -> "
          f"{[e['item_id'] for e in excluded]}")
    print(f"  LOWTEXT items: {len(lowtext)} -> {lowtext}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
