#!/usr/bin/env python3
"""ditch-audit P1 pilot expansion — International Journal for Philosophy of
Religion (IJPR), 2015 annual (research articles).

Reuses the RS harvester helpers from ``fetch_pilot.py`` (Crossref REST +
doi.org/Springer publisher-page abstract fallback, cleaners, schema) WITHOUT
modifying the RS code path. Only the target population, ISSN, volume filter and
classifier are IJPR-specific.

Target population = the 2015 *annual table of contents*. IJPR publishes two
volumes per calendar year: **volume 77 (issues 1-3)** and **volume 78
(issues 1-3)**, both dated 2015 (verified via Crossref published-print).
A ``pub-date:2015`` filter would also catch online-first articles belonging to
later volumes, so we fetch a wide date window and filter client-side on
``volume in {77, 78}`` (same discipline as the RS vol.51 filter).

Crossref holds NO abstracts for these Springer volumes, so every included
abstract is recovered via the doi.org -> Springer JSON-LD / Abs1-content
fallback already implemented in ``fetch_pilot.publisher_abstract`` (3 attempts,
then ``missing_abstract`` — never fabricated).

Exclusions: editorial prefaces (editorial), book reviews (bibliographic
signature), obituaries, errata/corrigenda. discussion notes/replies -> note:true
(none present in IJPR 2015: no reply-to-a-named-paper titles, no <=5pp pieces).

Output (data/ is .gitignore'd — copyrighted abstracts stay local):
  data/raw/pilot_ijpr2015.jsonl
"""

import os
import re
import sys
import time
import urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_pilot as fp  # noqa: E402  (reuse helpers; import runs no I/O)

ISSN = "0020-7047"                 # International Journal for Philosophy of Religion (print)
VOLUMES = {"77", "78"}             # the two 2015 volumes
WIN_FROM, WIN_UNTIL = "2014-01-01", "2016-12-31"  # brackets vols 77-78, excludes online-first drift
JOURNAL = "International Journal for Philosophy of Religion"

RAW = fp.RAW
OUT = os.path.join(RAW, "pilot_ijpr2015.jsonl")

# --- classification (IJPR-specific) ------------------------------------------
# Book-review signature: IJPR reviews carry a Crossref *subtitle* that is a
# publisher blurb ("City: Publisher, YEAR, NNN pp, $PRICE"). All 16 vol.77/78
# subtitled records are reviews; no research article in these volumes has a
# subtitle. Double-guarded: subtitle present AND matches the blurb pattern.
BLURB = re.compile(
    r"(?i)(\b(19|20)\d{2}\b.*(\bpp\b|\bpages\b|\bp\.\b))"
    r"|([$£€]\s?\d)"
    r"|\b(University Press|Publishing|Publishers|Blackwell|Wiley|Springer|"
    r"Palgrave|Routledge|Peeters|Ashgate|Lexington Books|Bloomsbury|"
    r"Indiana University|Columbia University|Oxford University|Cambridge University)\b"
)
EDITORIAL = re.compile(r"(?i)^(editorial\b|editorial preface|preface\b|introduction to the special issue$)")
OBIT = re.compile(r"(?i)\b(in memoriam|obituary|obituaries)\b")
# discussion-note cue: a *reply to a specific prior paper* names its target, so
# require the cue to be followed by a capitalized proper name (e.g. "reply to
# Landau"). A bare topical phrase ("response to horrendous evils") in a
# full-length article is NOT a note-cue (same rule the RS log records for
# 'critique of'). No IJPR 2015 record matches -> notes: 0 (all 34 are articles).
NOTE_CUE = re.compile(r"\b(reply to|response to|rejoinder to|comment on|in reply to)\s+[A-Z]")


def classify_ijpr(item):
    """Return (kind, reason). kind in {'article','note','exclude'}."""
    title = fp.clean_title(item)
    tl = title.lower()
    subs = item.get("subtitle") or []
    sub = subs[0] if subs else ""

    if EDITORIAL.match(tl):
        return "exclude", "editorial preface"
    if OBIT.search(tl):
        return "exclude", "obituary"
    if "corrigendum" in tl or "erratum" in tl or "correction to" in tl:
        return "exclude", "corrigendum/erratum"
    if item.get("type") == "book-review":
        return "exclude", "book review (crossref type)"
    # book review by subtitle blurb, or by bibliographic signature in the title
    if sub and BLURB.search(sub):
        return "exclude", "book review (publisher blurb subtitle)"
    if re.search(r"\bISBN\b", title) or re.search(r"\bPp\.\s", title):
        return "exclude", "book review (bibliographic signature)"

    span = fp.page_span(item)
    if NOTE_CUE.search(title) or (span is not None and span <= 5):
        return "note", ""
    return "article", ""


def fetch_ijpr_records():
    items, cursor = [], "*"
    while True:
        url = ("https://api.crossref.org/journals/%s/works?"
               "filter=from-pub-date:%s,until-pub-date:%s&rows=100&cursor=%s"
               "&select=DOI,title,subtitle,type,volume,issue,page,author,abstract,"
               "container-title,published-print,published-online"
               % (ISSN, WIN_FROM, WIN_UNTIL, urllib.parse.quote(cursor)))
        msg = fp.crossref_message(url)
        its = msg["items"]
        items += its
        cursor = msg.get("next-cursor")
        if not its or not cursor:
            break
        time.sleep(fp.CROSSREF_SLEEP)

    vv = [it for it in items if it.get("volume") in VOLUMES]
    records, excluded, seen = [], [], set()
    for it in sorted(vv, key=lambda x: (x.get("volume"), int(x.get("issue") or 0),
                                        x.get("page") or "")):
        kind, reason = classify_ijpr(it)
        doi = it["DOI"]
        if kind == "exclude":
            excluded.append({"doi": doi, "volume": it.get("volume"),
                             "issue": it.get("issue"), "page": it.get("page"),
                             "title": fp.clean_title(it), "reason": reason})
            continue
        if doi in seen:
            continue
        seen.add(doi)
        abs_text, src = fp.resolve_abstract(doi, it)
        rec = {
            "item_id": fp.sha16(doi),
            "doi": doi,
            "title": fp.clean_title(it),
            "authors": fp.authors_from(it),
            "journal": (it.get("container-title") or [JOURNAL])[0],
            "year": fp.year_from(it, 2015),
            "abstract": abs_text,
            "source": src or "crossref",
            "fetched_at": fp.now_iso(),
            "volume": it.get("volume"),
            "issue": it.get("issue"),
            "page": it.get("page"),
        }
        if kind == "note":
            rec["note"] = True
        if not abs_text:
            rec["missing_abstract"] = True
        records.append(rec)
    return records, excluded


def main():
    os.makedirs(RAW, exist_ok=True)
    print("== PILOT (expansion): IJPR vols 77-78 (2015) ==")
    recs, excluded = fetch_ijpr_records()
    fp.write_jsonl(OUT, recs)

    have, n, cov = fp.coverage(recs)
    notes = [r for r in recs if r.get("note")]
    dois = [r["doi"] for r in recs]
    print("  included items      :", n, "(articles %d + notes %d)" % (n - len(notes), len(notes)))
    print("  excluded            :", len(excluded))
    print("  excluded by reason  :", dict(Counter(e["reason"] for e in excluded)))
    per_vi = Counter((r["volume"], r["issue"]) for r in recs)
    print("  included by vol/issue:", dict(sorted(per_vi.items())))
    exc_vi = Counter((e["volume"], e["issue"]) for e in excluded)
    print("  excluded by vol/issue:", dict(sorted(exc_vi.items())))
    print("  DOI uniqueness      :", "%d unique / %d rows" % (len(set(dois)), len(dois)))
    print("  abstract coverage   :", "%d/%d = %.1f%%" % (have, n, cov * 100))
    print("  by source           :", dict(Counter(r["source"] for r in recs)))
    if cov < 0.90:
        print("  *** HARD STOP: IJPR abstract coverage < 90% ***")
        print("  missing:", [(r["doi"], r["page"]) for r in recs if r.get("missing_abstract")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
