#!/usr/bin/env python3
"""ditch-audit P2 corpus harvester — T2 + T3 journals, 2004-2024 (research articles).

Generalizes the P1 pilot harvester (``fetch_pilot.py``) to the full preregistered
tier set. Reuses the pilot helpers WITHOUT modifying them (Crossref REST paging,
cleaners, schema, doi.org publisher fallback, coverage, write_jsonl).

Preregistered target (outline v0.4 §4.1; CONTEXT.md D-1/D-2):
  T2 (window 2004-2024, research articles):
    fp     Faith and Philosophy                              ISSN 0739-7046 (PDC/SCP)
    rs     Religious Studies                                 ISSN 0034-4125 (CUP)   -verified
    ijpr   International Journal for Philosophy of Religion   ISSN 0020-7047 (Springer) -verified
    sophia Sophia                                            ISSN 0038-1527 (Springer)
  T3:
    pc     Philosophia Christi                               ISSN 1529-1634 (PDC)

Year assignment = the *issue year* (published-print preferred, then online, then
issued). We fetch a wide Crossref window (2002-2026) and filter client-side on
that year in [2004, 2024]; this reproduces the pilot's volume-based "annual TOC"
semantics while absorbing online-first drift (an article printed 2016 but posted
online 2015 is assigned 2016, not double-counted).

Abstract fallback (3 attempts, then honest ``missing_abstract`` -- never fabricated):
  1. Crossref JATS abstract.
  2. doi.org landing: Springer JSON-LD / Cambridge Core citation_abstract /
     Springer Abs1-content / generic abstract div / bepress id="abstract"
     (Digital Commons) / DC.Description meta.
  3. one landing retry (Springer/CUP) ; PDC journals get a single attempt because
     F&P->Asbury landings rarely carry a deposited abstract for <=2018 and
     PC->pdcnet.org returns HTTP 403 (both are source-absence, not scrape failure;
     flagged missing_abstract for Sonar harvest-aid triage, battery B0).

Diagnostics established before build (2026-07-15, this window):
  - Crossref has-abstract share: RS ~65-70% all years; F&P ~0 pre-2014, ~83% 2019+;
    IJPR ~0 pre-2019; Sophia ~0 pre-2019; PC ~0 pre-2019, ~97% 2019+.
  - IJPR/Sophia gap filled by Springer JSON-LD landing (pilot: IJPR 2015 -> 100%).
  - RS gap filled by Cambridge Core citation_abstract.
  - PDC pre-2019 (F&P/PC) is the coverage floor: abstracts largely absent at source.

Checkpointing (resumable after process death):
  data/raw/checkpoints/<key>/toc.jsonl        raw Crossref window items (metadata pass)
  data/raw/checkpoints/<key>/excluded.jsonl   excluded records w/ reason
  data/raw/checkpoints/<key>/part_<year>.jsonl in-progress resolved records
  data/raw/checkpoints/<key>/out_<year>.jsonl  finalized resolved records
  data/raw/checkpoints/<key>/done_<year>       marker (year fully resolved)
Re-running skips finished journals' TOC fetch, finished years, and resolved DOIs.

Reuse of pilot output (do NOT re-scrape): RS 2015 <- pilot_rs2015.jsonl,
IJPR 2015 <- pilot_ijpr2015.jsonl (curated note flags + 100% coverage preserved).

Outputs (data/ is .gitignore'd -- copyrighted abstracts stay local):
  data/raw/corpus_{fp,rs,ijpr,sophia,pc}.jsonl
  data/raw/corpus_harvest_log.md
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_pilot as fp  # noqa: E402  (reuse helpers; import runs no I/O)

RAW = fp.RAW
CKPT = os.path.join(RAW, "checkpoints")

YEAR_FROM, YEAR_TO = 2004, 2024
WIN_FROM, WIN_UNTIL = "2002-01-01", "2026-12-31"   # brackets the issue-year window
CROSSREF_SLEEP = 1.0
POLITE = 2.0                                        # between landing scrapes

# --- journal config table --------------------------------------------------------
JOURNALS = [
    {"key": "fp",     "issn": "0739-7046", "name": "Faith and Philosophy",
     "landing_attempts": 1, "pdc": True},
    {"key": "rs",     "issn": "0034-4125", "name": "Religious Studies",
     "landing_attempts": 2, "pdc": False, "reuse": {2015: "pilot_rs2015.jsonl"}},
    {"key": "ijpr",   "issn": "0020-7047", "name": "International Journal for Philosophy of Religion",
     "landing_attempts": 2, "pdc": False, "reuse": {2015: "pilot_ijpr2015.jsonl"}},
    {"key": "sophia", "issn": "0038-1527", "name": "Sophia",
     "landing_attempts": 2, "pdc": False},
    {"key": "pc",     "issn": "1529-1634", "name": "Philosophia Christi",
     "landing_attempts": 1, "pdc": True},
]
JMAP = {j["key"]: j for j in JOURNALS}


# --- classification (generalizes fetch_pilot.classify + fetch_ijpr.classify_ijpr) --
BLURB = re.compile(
    r"(?i)(\b(19|20)\d{2}\b.*(\bpp\b|\bpages\b|\bp\.\b))"
    r"|([$£€]\s?\d)"
    r"|\b(University Press|Univ\. Press|Publishing|Publishers|Blackwell|Wiley|Springer|"
    r"Palgrave|Routledge|Peeters|Ashgate|Lexington|Bloomsbury|Eerdmans|Baker Academic|"
    r"InterVarsity|Zondervan|Crossway|Brill|Continuum|T&T Clark|"
    r"Indiana University|Columbia University|Oxford University|Cambridge University|"
    r"Notre Dame Press|Cornell University|Yale University|Harvard University)\b")
FRONT_BACK = re.compile(r"(?i)(cover and (front|back) matter|^front matter$|^back matter$"
                        r"|^table of contents$|^index$|^contents$|^issue information$)")
EDITORIAL = re.compile(r"(?i)^(editorial\b|editor'?s (introduction|note|preface|page)"
                       r"|from the editor|preface\b|introduction to the special issue$)")
ANNOUNCE = re.compile(r"(?i)^(news and announcements?|announcements?|call for papers|"
                      r"in this issue|acknowledgment of reviewers|essay prize|"
                      r"books received|advertisement)")
OBIT = re.compile(r"(?i)\b(in memoriam|obituary|obituaries|memorial minute)\b")
NOTE_TITLE = re.compile(r"(?i)\b(reply to|reply\b|response to|rejoinder|comment on|"
                        r"in reply to|revisited|a note on|postscript)\b")
NOTE_REPLY_NAMED = re.compile(r"\b(reply to|response to|rejoinder to|comment on|in reply to)\s+[A-Z]")


def _clean(item):
    return fp.clean_title(item)


def classify(item, pdc=False):
    """Return (kind, reason). kind in {'article','note','exclude'}."""
    title = _clean(item)
    tl = title.lower().strip()
    page = (item.get("page") or "").lower()
    subs = item.get("subtitle") or []
    sub = subs[0] if subs else ""
    typ = item.get("type") or ""

    if not tl:
        return "exclude", "empty title (front/back matter)"
    if re.match(r"^[bf]\d", page) or FRONT_BACK.search(tl):
        return "exclude", "front/back matter"
    if "corrigendum" in tl or "erratum" in tl or "correction to" in tl or tl.startswith("retraction"):
        return "exclude", "corrigendum/erratum"
    if EDITORIAL.match(tl):
        return "exclude", "editorial"
    if ANNOUNCE.match(tl):
        return "exclude", "announcement"
    if OBIT.search(tl):
        return "exclude", "obituary"
    if typ in ("book-review", "editorial", "other"):
        return "exclude", "book review/editorial (crossref type)"
    if sub and BLURB.search(sub):
        return "exclude", "book review (publisher blurb subtitle)"
    if re.search(r"\bISBN\b", title) or re.search(r"\bPp\.\s", title) or re.search(r"\bpp\.\s?[ivxlcdm0-9]", title):
        return "exclude", "book review (bibliographic signature)"
    # PDC review/critical-notice signature: "Review of ...", "Critical Notice: ..."
    if pdc and re.match(r"(?i)^(review of|critical notice|book note|review essay:)\b", tl):
        return "exclude", "book review (title signature)"

    span = fp.page_span(item)
    # note = reply to a *specific prior paper* (named target) OR short piece (<=5pp)
    if NOTE_REPLY_NAMED.search(title) or NOTE_TITLE.search(title) or (span is not None and span <= 5):
        return "note", ""
    return "article", ""


# --- abstract resolution (superset extractor; reuses fetch_pilot internals) -------
def corpus_landing_abstract(doi):
    """Fetch the doi.org landing once and try every extractor we know, incl.
    bepress/Digital Commons (F&P->Asbury) and DC.Description. Reuses
    fetch_pilot._jsonld_descriptions / clean_abstract / http_get."""
    try:
        _final, body = fp.http_get("https://doi.org/" + doi, timeout=45)
    except Exception:
        return ""
    text = body.decode("utf-8", "replace")
    for d in fp._jsonld_descriptions(text):                 # Springer et al.
        return fp.clean_abstract(d)
    m = re.search(r'(?is)<meta[^>]+name="citation_abstract"[^>]+content="([^"]{60,})"', text)
    if m:                                                    # Cambridge Core / HighWire / bepress
        return fp.clean_abstract(m.group(1))
    m = re.search(r'(?is)id="Abs1-content"[^>]*>(.*?)</(?:div|section)>', text)
    if m:                                                    # Springer abstract block
        t = fp.clean_abstract(m.group(1))
        if len(t) > 60:
            return t
    m = re.search(r'(?is)<div[^>]+id="abstract"[^>]*>(.*?)</div>', text)
    if m:                                                    # bepress/Digital Commons block
        t = fp.clean_abstract(m.group(1))
        if len(t) > 60 and not re.match(r"(?i)^\s*by .+ published on", t):
            return t
    m = re.search(r'(?is)<div[^>]+class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>', text)
    if m:                                                    # generic abstract div
        t = fp.clean_abstract(m.group(1))
        if len(t) > 60:
            return t
    m = re.search(r'(?is)<meta[^>]+name="DC\.Description"[^>]+content="([^"]{60,})"', text)
    if m:
        t = fp.clean_abstract(m.group(1))
        if not re.match(r"(?i)^\s*by .+ published on", t):
            return t
    return ""


def resolve_abstract(doi, cr_item, landing_attempts):
    """Crossref -> landing (n attempts). Returns (text, source)."""
    a = fp.clean_abstract((cr_item or {}).get("abstract"))
    if len(a) > 40:
        return a, "crossref"
    if not doi:
        return "", ""
    for _ in range(max(1, landing_attempts)):
        time.sleep(POLITE)
        a = corpus_landing_abstract(doi)
        if len(a) > 40:
            return a, "publisher-page"
    return "", ""


# --- Crossref metadata pass (checkpointed per journal) ----------------------------
def fetch_toc(journal):
    """Page the full Crossref window for a journal; cache to checkpoints/<key>/toc.jsonl."""
    key, issn = journal["key"], journal["issn"]
    d = os.path.join(CKPT, key)
    os.makedirs(d, exist_ok=True)
    toc_path = os.path.join(d, "toc.jsonl")
    if os.path.exists(toc_path) and os.path.getsize(toc_path) > 0:
        items = [json.loads(l) for l in open(toc_path, encoding="utf-8")]
        print("  [%s] TOC cache hit: %d Crossref items" % (key, len(items)))
        return items

    items, cursor, pages = [], "*", 0
    while True:
        url = ("https://api.crossref.org/journals/%s/works?"
               "filter=from-pub-date:%s,until-pub-date:%s&rows=100&cursor=%s"
               "&select=DOI,title,subtitle,type,volume,issue,page,author,abstract,"
               "container-title,published-print,published-online,issued"
               % (issn, WIN_FROM, WIN_UNTIL, urllib.parse.quote(cursor)))
        try:
            msg = fp.crossref_message(url)
        except urllib.error.HTTPError as e:
            print("  [%s] Crossref HTTP %s on page %d; retrying once after 5s" % (key, e.code, pages))
            time.sleep(5)
            msg = fp.crossref_message(url)
        its = msg["items"]
        items += its
        pages += 1
        cursor = msg.get("next-cursor")
        if not its or not cursor:
            break
        time.sleep(CROSSREF_SLEEP)
    with open(toc_path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print("  [%s] TOC fetched: %d Crossref items over %d pages" % (key, len(items), pages))
    return items


def year_of(item):
    for kkey in ("published-print", "published-online", "issued", "published"):
        dp = (item.get(kkey) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return None


def build_record(doi, it, journal, kind, year, abs_text, src):
    rec = {
        "item_id": fp.sha16(doi),
        "doi": doi,
        "title": _clean(it),
        "authors": fp.authors_from(it),
        "journal": (it.get("container-title") or [journal["name"]])[0],
        "year": year,
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
    return rec


# --- per-journal harvest ----------------------------------------------------------
def harvest_journal(journal, only_years=None):
    key = journal["key"]
    d = os.path.join(CKPT, key)
    os.makedirs(d, exist_ok=True)
    print("== %s (%s) ==" % (journal["name"], journal["issn"]))
    toc = fetch_toc(journal)

    # classify + bucket by issue-year
    per_year = defaultdict(list)          # year -> list of (doi, crossref item, kind)
    excluded = []
    seen = set()
    for it in toc:
        doi = it.get("DOI")
        if not doi:
            continue
        y = year_of(it)
        if y is None or y < YEAR_FROM or y > YEAR_TO:
            continue
        kind, reason = classify(it, pdc=journal.get("pdc"))
        if kind == "exclude":
            excluded.append({"doi": doi, "year": y, "volume": it.get("volume"),
                             "issue": it.get("issue"), "page": it.get("page"),
                             "title": _clean(it)[:90], "reason": reason})
            continue
        if doi in seen:                    # intra-journal DOI dedup
            continue
        seen.add(doi)
        per_year[y].append((doi, it, kind))
    # persist excluded (overwrite: deterministic from cached TOC)
    with open(os.path.join(d, "excluded.jsonl"), "w", encoding="utf-8") as f:
        for e in excluded:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    reuse = journal.get("reuse", {})
    for year in range(YEAR_FROM, YEAR_TO + 1):
        if only_years and year not in only_years:
            continue
        done_marker = os.path.join(d, "done_%d" % year)
        out_path = os.path.join(d, "out_%d.jsonl" % year)
        if os.path.exists(done_marker) and os.path.exists(out_path):
            continue

        # reuse pilot output for pre-collected journal-years
        if year in reuse:
            src_file = os.path.join(RAW, reuse[year])
            recs = [json.loads(l) for l in open(src_file, encoding="utf-8")]
            fp.write_jsonl(out_path, recs)
            open(done_marker, "w").write(fp.now_iso())
            print("  [%s %d] reused %s (%d records, no re-scrape)" % (key, year, reuse[year], len(recs)))
            continue

        bucket = per_year.get(year, [])
        # resume: load already-resolved DOIs from partial
        part_path = os.path.join(d, "part_%d.jsonl" % year)
        resolved = {}
        if os.path.exists(part_path):
            for l in open(part_path, encoding="utf-8"):
                r = json.loads(l)
                resolved[r["doi"]] = r
        pf = open(part_path, "a", encoding="utf-8")
        for i, (doi, it, kind) in enumerate(bucket):
            if doi in resolved:
                continue
            abs_text, src = resolve_abstract(doi, it, journal["landing_attempts"])
            rec = build_record(doi, it, journal, kind, year, abs_text, src)
            resolved[doi] = rec
            pf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            pf.flush()
        pf.close()

        recs = [resolved[doi] for (doi, _it, _k) in bucket]
        fp.write_jsonl(out_path, recs)
        open(done_marker, "w").write(fp.now_iso())
        have = sum(1 for r in recs if not r.get("missing_abstract"))
        print("  [%s %d] %d items, abstract %d/%d (%.0f%%)"
              % (key, year, len(recs), have, len(recs),
                 100 * have / len(recs) if recs else 0))

    # concatenate finalized years -> corpus_<key>.jsonl
    all_recs = []
    for year in range(YEAR_FROM, YEAR_TO + 1):
        p = os.path.join(d, "out_%d.jsonl" % year)
        if os.path.exists(p):
            all_recs += [json.loads(l) for l in open(p, encoding="utf-8")]
    fp.write_jsonl(os.path.join(RAW, "corpus_%s.jsonl" % key), all_recs)
    return all_recs, excluded


# --- harvest log + final validation ----------------------------------------------
def finalize_log():
    print("\n== FINALIZE: corpus_harvest_log.md ==")
    journals_data = {}
    for j in JOURNALS:
        p = os.path.join(RAW, "corpus_%s.jsonl" % j["key"])
        recs = [json.loads(l) for l in open(p, encoding="utf-8")] if os.path.exists(p) else []
        exc_p = os.path.join(CKPT, j["key"], "excluded.jsonl")
        exc = [json.loads(l) for l in open(exc_p, encoding="utf-8")] if os.path.exists(exc_p) else []
        journals_data[j["key"]] = (recs, exc)

    # cross-journal DOI dedup check
    all_dois = []
    for recs, _ in journals_data.values():
        all_dois += [r["doi"] for r in recs]
    dup = [doi for doi, c in Counter(all_dois).items() if c > 1]

    lines = []
    lines.append("# corpus_harvest_log — P2 corpus (T2 + T3, 2004-2024, research articles)\n")
    lines.append("- generated: %s" % fp.now_iso())
    lines.append("- harvester: `pipeline/01_fetch/fetch_corpus.py` (stdlib-only; "
                 "Crossref REST + doi.org publisher fallback; checkpointed)")
    lines.append("- window: issue-year in [2004, 2024] (published-print preferred); "
                 "Crossref fetch window %s..%s" % (WIN_FROM, WIN_UNTIL))
    lines.append("- copyright isolation: outputs under `data/` (.gitignore'd); "
                 "abstracts NOT reproduced here (counts + provenance only).\n")

    # 1. per-journal totals
    lines.append("## 1. Per-journal totals\n")
    lines.append("| journal | key | ISSN | included | articles | notes | excluded | "
                 "abstract cov | missing |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    grand_inc = grand_have = grand_exc = 0
    for j in JOURNALS:
        recs, exc = journals_data[j["key"]]
        n = len(recs)
        notes = sum(1 for r in recs if r.get("note"))
        have = sum(1 for r in recs if not r.get("missing_abstract"))
        grand_inc += n; grand_have += have; grand_exc += len(exc)
        lines.append("| %s | %s | %s | %d | %d | %d | %d | %.1f%% | %d |"
                     % (j["name"], j["key"], j["issn"], n, n - notes, notes, len(exc),
                        100 * have / n if n else 0, n - have))
    lines.append("| **TOTAL** | | | **%d** | | | **%d** | **%.1f%%** | **%d** |"
                 % (grand_inc, grand_exc, 100 * grand_have / grand_inc if grand_inc else 0,
                    grand_inc - grand_have))

    # 2. journal x year count matrix (included)
    lines.append("\n## 2. Journal x year matrix (included research items)\n")
    header = "| year | " + " | ".join(j["key"] for j in JOURNALS) + " | row |"
    lines.append(header)
    lines.append("|" + "---|" * (len(JOURNALS) + 2))
    year_counts = {j["key"]: Counter(r["year"] for r in journals_data[j["key"]][0]) for j in JOURNALS}
    for year in range(YEAR_FROM, YEAR_TO + 1):
        row = [str(year_counts[j["key"]].get(year, 0)) for j in JOURNALS]
        lines.append("| %d | %s | %d |" % (year, " | ".join(row), sum(int(x) for x in row)))
    tot_row = [str(sum(year_counts[j["key"]].values())) for j in JOURNALS]
    lines.append("| **tot** | %s | %d |" % (" | ".join("**%s**" % x for x in tot_row),
                                            sum(int(x) for x in tot_row)))
    lines.append("\n(Zero-count years, if any, are flagged below with cause: unpublished vs harvest gap.)")
    zero_notes = []
    for j in JOURNALS:
        for year in range(YEAR_FROM, YEAR_TO + 1):
            if year_counts[j["key"]].get(year, 0) == 0:
                toc_p = os.path.join(CKPT, j["key"], "toc.jsonl")
                zero_notes.append("- %s %d: 0 included (verify TOC — see checkpoints/%s/toc.jsonl)"
                                  % (j["key"], year, j["key"]))
    if zero_notes:
        lines.append("\n**Zero-count years:**")
        lines += zero_notes
    else:
        lines.append("\nNo zero-count journal-years.")

    # 3. abstract coverage by journal x year
    lines.append("\n## 3. Abstract coverage by journal x year (have/total)\n")
    lines.append(header.replace(" row ", " overall "))
    lines.append("|" + "---|" * (len(JOURNALS) + 2))
    for year in range(YEAR_FROM, YEAR_TO + 1):
        cells = []
        for j in JOURNALS:
            yr = [r for r in journals_data[j["key"]][0] if r["year"] == year]
            h = sum(1 for r in yr if not r.get("missing_abstract"))
            cells.append("%d/%d" % (h, len(yr)) if yr else "-")
        lines.append("| %d | %s |  |" % (year, " | ".join(cells)))

    # 4. abstract source breakdown
    lines.append("\n## 4. Abstract source breakdown (per journal)\n")
    for j in JOURNALS:
        recs = journals_data[j["key"]][0]
        src = Counter(r["source"] for r in recs)
        lines.append("- **%s**: %s" % (j["key"], dict(src)))

    # 5. exclusion reasons
    lines.append("\n## 5. Exclusion reasons (per journal)\n")
    for j in JOURNALS:
        exc = journals_data[j["key"]][1]
        lines.append("- **%s** (%d excluded): %s"
                     % (j["key"], len(exc), dict(Counter(e["reason"] for e in exc))))

    # 6. dedup + G2
    lines.append("\n## 6. DOI uniqueness + G2 pre-tally\n")
    lines.append("- total included rows: %d" % grand_inc)
    lines.append("- unique DOIs (cross-journal): %d" % len(set(all_dois)))
    lines.append("- cross-journal duplicate DOIs: %d %s"
                 % (len(dup), ("(%s)" % dup[:5] if dup else "")))
    lines.append("- **overall abstract coverage: %.1f%% (%d/%d)** — G2 threshold 90%%"
                 % (100 * grand_have / grand_inc if grand_inc else 0, grand_have, grand_inc))
    pdc_recs = sum(len(journals_data[k][0]) for k in ("fp", "pc"))
    pdc_have = sum(sum(1 for r in journals_data[k][0] if not r.get("missing_abstract"))
                   for k in ("fp", "pc"))
    non_pdc_recs = grand_inc - pdc_recs
    non_pdc_have = grand_have - pdc_have
    lines.append("- non-PDC (rs/ijpr/sophia) coverage: %.1f%% (%d/%d)"
                 % (100 * non_pdc_have / non_pdc_recs if non_pdc_recs else 0, non_pdc_have, non_pdc_recs))
    lines.append("- PDC (fp/pc) coverage: %.1f%% (%d/%d) — Sonar harvest-aid candidate pool"
                 % (100 * pdc_have / pdc_recs if pdc_recs else 0, pdc_have, pdc_recs))

    with open(os.path.join(RAW, "corpus_harvest_log.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("  wrote corpus_harvest_log.md")
    print("  overall coverage: %.1f%% (%d/%d); unique DOIs %d/%d; cross-journal dups %d"
          % (100 * grand_have / grand_inc if grand_inc else 0, grand_have, grand_inc,
             len(set(all_dois)), len(all_dois), len(dup)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--journals", default="", help="comma keys (default: all)")
    ap.add_argument("--year-from", type=int, default=None)
    ap.add_argument("--year-to", type=int, default=None)
    ap.add_argument("--finalize-only", action="store_true")
    args = ap.parse_args()

    os.makedirs(CKPT, exist_ok=True)
    if args.finalize_only:
        finalize_log()
        return 0

    keys = [k for k in (args.journals.split(",") if args.journals else JMAP) if k in JMAP]
    only_years = None
    if args.year_from or args.year_to:
        only_years = set(range(args.year_from or YEAR_FROM, (args.year_to or YEAR_TO) + 1))
    for k in keys:
        harvest_journal(JMAP[k], only_years=only_years)
    finalize_log()
    return 0


if __name__ == "__main__":
    sys.exit(main())
