#!/usr/bin/env python3
# Implements codebook-v1.md §2 (canonical). Prereqs: Python 3.10+, stdlib only.
# In:  data/raw/*.jsonl (harvester schema; contains author/title/journal/year/doi)
# Out: data/sanitized/<name>.jsonl        -> {"item_id","text","text_extra"}
#      data/sanitized/scrub_log.jsonl     -> {"item_id","rule","before","after"}
#      data/sanitized/exclusions.jsonl    -> {"item_id","reason"} (items dropped)
#
# Blindness contract (codebook §1/§2):
#   * Output carries ONLY {item_id, text, text_extra}; every metadata field is dropped.
#   * Text mapping:
#       - abstract present            -> text = abstract,   text_extra = null
#       - abstract absent, first_para -> text = first_para, text_extra = last_para
#       - neither                     -> item EXCLUDED (cannot code empty)
#     (first/last-paragraph excerpts substitute for a missing abstract; the coder then
#      sees both ends of the paper. Provenance fields text_source/_url/_edition and
#      excerpt_fetched_at are never emitted.)
#   * Scrubs run on BOTH text and text_extra. In-text self-identifiers removed:
#       - "in this journal"; "as I (have) argued in <year>";
#       - proper-name self-citations "<OwnAuthor> (<year>)" and "my <year> book <Title>";
#       - the item's OWN journal name (citation parenthetical, or a venue reference such
#         as "special issue of <Journal>"); guarded so common-word / single-token journal
#         names in ordinary prose (e.g. "in mind" for journal "Mind") are NOT touched;
#       - the item's OWN author name used self-referentially -> role tag "[the author]".
#     Opponent / interlocutor names are CONTENT and kept (Plantinga, Rowe, Craig, Mackie,
#     Hume, Swinburne, ... when they are not the item's own author) — codebook §2.3.
#   * Author list + journal are read here to drive scrubs; they are NEVER emitted.
#   * Abstract < 60 words -> text_extra (null when no source paragraph held) + LOWTEXT.
#   * Borderline self-identification is NOT auto-deleted; it is left in place and the
#     residual is surfaced by the caller's heuristic sweep for human (dk) judgement.
# Deterministic: same input -> same output (pure regex, stable ordering). scrub_log is
# regenerated from scratch each run (no double-loading on re-run).

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
    ws = re.compile(r"\s+")
    before = ws.sub(" ", left + text[start:end] + right).strip()
    after = ws.sub(" ", left + replacement + right).strip()
    return before, after


def _surname(author: str) -> str | None:
    if author.strip().lower() in NON_AUTHOR:
        return None
    toks = [t for t in re.split(r"\s+", author.strip()) if t]
    toks = [t for t in toks if t.strip(".,").lower() not in SUFFIXES]
    return toks[-1].strip(".,") if toks else None


def _apply(text, pattern, repl, item_id, rule, log, guard=None):
    """Apply `pattern` left-to-right; log each accepted match as its own scrub entry.

    `repl`  : replacement string (may contain \\1 backrefs) or callable(match)->str.
    `guard` : optional predicate(match)->bool; when it returns False the match is left
              untouched and not logged (used to skip common-word false positives).
    Matching is done against the pre-substitution string of this pass so spans stay
    valid for snippet extraction.
    """
    src = text
    out = []
    cursor = 0
    for m in pattern.finditer(src):
        if guard is not None and not guard(m):
            continue
        replacement = m.expand(repl) if isinstance(repl, str) else repl(m)
        before, after = _snip(src, m.start(), m.end(), replacement)
        log.append({"item_id": item_id, "rule": rule, "before": before, "after": after})
        out.append(src[cursor:m.start()])
        out.append(replacement)
        cursor = m.end()
    out.append(src[cursor:])
    return "".join(out)


def scrub_field(text: str, item_id: str, authors: list, journal: str | None,
                surnames: list, log: list) -> str:
    """Run the full §2 scrub pass over one text field. Deterministic."""
    if not text:
        return text

    # R1 — venue self-identifier "in this journal" (§2.2). Drop the phrase.
    text = _apply(text, re.compile(r"\s+in this journal\b", re.IGNORECASE),
                  "", item_id, "in_this_journal", log)

    # R2 — "as I (have) argued in <year>" self-reference (§2.2).
    text = _apply(text, re.compile(r"\bas I (?:have )?argued in \(?\d{4}[a-z]?\)?", re.IGNORECASE),
                  "as I argued elsewhere", item_id, "self_reference_year", log)

    # R3 — proper-name self-citation "<OwnAuthor> (<year>)" (§2.2). Own authors only;
    # opponent citations like "Plantinga (2011)" or "Alvin Plantinga (1983)" are kept.
    for sn in surnames:
        text = _apply(text, re.compile(r"\b" + re.escape(sn) + r"\s*\(\d{4}[a-z]?\)", re.IGNORECASE),
                      "earlier work", item_id, "self_citation", log)

    # R4 — self book/paper citation "my <year> book/paper <Title>" (§2.2).
    text = _apply(text, re.compile(r"\bmy \d{4} (?:book|monograph|paper|article)\b[^.]*\.", re.IGNORECASE),
                  "my earlier work.", item_id, "self_citation", log)

    # R5 — item's OWN journal name leaked in the text (§2.1/§2.2).
    if journal:
        # R5a: citation parenthetical "( <Journal> , vol (YYYY), pp )" -> "(YYYY)".
        text = _apply(text, re.compile(r"\(\s*" + re.escape(journal) + r"\s*,[^()]*\((\d{4})\)[^()]*\)"),
                      r"(\1)", item_id, "journal_name", log)
        # R5b: venue reference to a multi-word journal name. Guarded to fire only when
        # the matched journal text is NOT all-lowercase (i.e. a proper-noun reference),
        # so ordinary prose using the journal's constituent common words is untouched
        # (e.g. journal "Mind" vs. "carbon-based life in mind").
        jtoks = [re.escape(t) for t in journal.split()]
        if len(jtoks) >= 2:
            jpat = r"\b" + r"\s+".join(jtoks) + r"\b"
            # R5b-1: "<prep> <Journal>" (e.g. "of Faith and Philosophy") -> drop.
            text = _apply(text, re.compile(r"(\s+(?:of|in|from|for)\s+)(" + jpat + r")", re.IGNORECASE),
                          "", item_id, "journal_name", log,
                          guard=lambda m: not m.group(2).islower())
            # R5b-2: bare "<Journal>" fallback -> "this journal".
            text = _apply(text, re.compile(jpat, re.IGNORECASE),
                          "this journal", item_id, "journal_name", log,
                          guard=lambda m: not m.group(0).islower())

    # R6 — item's OWN author name used self-referentially -> role tag (§2.3).
    # Replace the full name first; only if a full name matched (confident self-reference,
    # e.g. a 3rd-person blurb) do we also replace the bare surname, to avoid touching a
    # same-named third party.
    full_matched = False
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
            text = _apply(text, re.compile(r"\b" + re.escape(sn) + r"\b"),
                          "[the author]", item_id, "self_name_role_tag", log)

    return re.sub(r"[ \t]{2,}", " ", text).strip()


def sanitize_record(rec: dict, log: list) -> tuple[dict | None, str | None]:
    """Return (sanitized_record | None, exclusion_reason | None)."""
    item_id = rec["item_id"]
    abstract = (rec.get("abstract") or "").strip()
    first = (rec.get("first_para") or "").strip()
    last = (rec.get("last_para") or "").strip()

    if abstract:
        text_src, extra_src = abstract, None
    elif first:
        text_src, extra_src = first, (last or None)
    else:
        return None, "no_abstract_or_paragraphs"

    authors = rec.get("authors") or []
    journal = rec.get("journal")
    surnames = [s for s in (_surname(a) for a in authors) if s]

    text = scrub_field(text_src, item_id, authors, journal, surnames, log)
    text_extra = (scrub_field(extra_src, item_id, authors, journal, surnames, log)
                  if extra_src else None)

    out = {"item_id": item_id, "text": text, "text_extra": text_extra}
    if len(text.split()) < LOWTEXT_WORDS:
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
    print(f"  excluded: {len(excluded)} -> {[e['item_id'] for e in excluded]}")
    print(f"  LOWTEXT items: {len(lowtext)} -> {lowtext}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
