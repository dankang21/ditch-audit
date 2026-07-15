#!/usr/bin/env python3
"""ditch-audit P2 T1 candidate harvester — keyword pre-filter stage.

Collects Crossref metadata (title + abstract, when deposited) for the six T1
*general* philosophy journals, 2004-2024, and applies a **recall-first keyword
pre-filter** (case-insensitive substring match over title UNION abstract). Only
filter HITS are written to ``data/raw/t1_candidates.jsonl``; per journal x year
RAW record counts are logged as population-size evidence.

This is a candidate-generation stage. NO relevance judgement is made here (that
is the next stage's job). Over-inclusion is intended; the only hard commitment
is "do not drop a genuine research article".

Reuses the pilot harvester helpers (``fetch_pilot.py``): Crossref REST client,
title/abstract cleaners, author/year extractors, doi.org publisher-page abstract
fallback, JSONL writer. Nothing in the RS/IJPR code paths is modified.

Design notes
------------
* One paginated Crossref pass per journal over 2004-01-01..2024-12-31; the raw
  metadata is cached under ``data/raw/t1_meta_cache/<issn>.json`` so a re-run
  never re-fetches metadata. Records are then bucketed client-side by computed
  publication year (``year_from``), giving deterministic year assignment with no
  cross-boundary double counting.
* Checkpoint granularity = journal x year (``data/raw/t1_checkpoint.json``); a
  completed cell is skipped on resume. The output JSONL is globally deduped by
  DOI (existing DOIs are loaded at startup -> resume-safe + 100% DOI-unique).
* Filter target is METADATA ONLY. A record with no deposited abstract is filtered
  on its title alone and flagged ``title_only_match`` (we do NOT fetch abstracts
  for non-hits -- too expensive at ~11.5k records). Abstract fallback runs ONLY
  for hits that lack a Crossref abstract.
* OUP journals (Mind, Analysis, The Philosophical Quarterly) frequently bot-block
  the doi.org landing page; such failures are honestly flagged ``missing_abstract``
  and counted (never fabricated).

Schema (one JSON object per line, hits only):
  {"item_id": sha256(doi)[:16], "doi","title","authors","journal","year",
   "abstract","source","fetched_at","matched_keywords":[...],
   "volume","issue","page","type"}
  optional flags: "title_only_match", "missing_abstract", "note".

Outputs (data/ is .gitignore'd -- copyrighted abstracts stay local):
  data/raw/t1_candidates.jsonl
  data/raw/t1_harvest_log.md
  data/raw/t1_checkpoint.json      (resume state + per-cell stats)
  data/raw/t1_meta_cache/*.json    (raw Crossref metadata cache)
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_pilot as fp  # noqa: E402  (reuse helpers; import runs no I/O)

# ------------------------------------------------------------------ config -----
# ISSNs all verified live against Crossref /journals/<issn> (title match) before
# use, 2026-07-15. Second ISSN in each pair is the electronic ISSN (not queried).
JOURNALS = OrderedDict([
    ("0026-4423", "Mind"),
    ("0029-4624", "Noûs"),
    ("0031-8094", "The Philosophical Quarterly"),
    ("0003-0481", "American Philosophical Quarterly"),
    ("0003-2638", "Analysis"),
    ("0031-8116", "Philosophical Studies"),
])
# OUP-published (doi.org landing page tends to bot-block scraping) -- flagged in log.
OUP = {"0026-4423", "0031-8094", "0003-2638"}  # Mind, PQ, Analysis (OUP era)

YEAR_FROM, YEAR_TO = 2004, 2024
WIN_FROM = "%d-01-01" % YEAR_FROM
WIN_UNTIL = "%d-12-31" % YEAR_TO

CROSSREF_SLEEP = 1.0     # between Crossref metadata pages
POLITE = 2.0            # before each publisher-page scrape (hits w/o crossref abstract)
PUB_ATTEMPTS = 1        # publisher-page attempts per missing-abstract hit (mass stage)

ROOT = fp.ROOT
RAW = fp.RAW
OUT = os.path.join(RAW, "t1_candidates.jsonl")
LOG = os.path.join(RAW, "t1_harvest_log.md")
CKPT = os.path.join(RAW, "t1_checkpoint.json")
META_DIR = os.path.join(RAW, "t1_meta_cache")

SELECT = ("DOI,title,subtitle,type,volume,issue,page,author,abstract,"
          "container-title,published-print,published-online,issued")

# --------------------------------------------------------------- keywords ------
# Recall-first substring pre-filter (matches inflections via partial substrings,
# e.g. "atheis" -> atheism/atheist/atheistic; "trinit" -> trinity/trinitarian).
# Case-insensitive; matched over (title + " " + abstract).lower(). Kept verbatim
# from the P2 T1 spec.
KEYWORDS = [
    "god", "theism", "theist", "atheis", "divine", "deity", "theodicy",
    "problem of evil", "hiddenness", "cosmological", "fine-tun", "fine tun",
    "teleological", "design argument", "ontological", "kalam",
    "necessary being", "perfect being", "miracle", "resurrection",
    "incarnation", "trinit", "omnipoten", "omniscien", "religious experience",
    "religious belief", "natural theology", "philosophy of religion", "creator",
    "providence", "petitionary prayer", "pascal", "properly basic",
    "reformed epistemology", "afterlife", "divine command",
]


def matched_keywords(text):
    tl = text.lower()
    return [k for k in KEYWORDS if k in tl]


# ----------------------------------------------------------- classification ----
# Same spirit as the pilot/T2 exclusion heuristics, tuned for GENERAL journals.
# Deliberately conservative: only clear reviews / front-back matter / editorial /
# errata / issue-containers are excluded, to protect recall of research articles.
# NOTE: the page-span<=5 note heuristic is NOT applied here -- in these journals a
# short paper is a normal research article (esp. Analysis), so it would mislabel.
FRONT_BACK = re.compile(r"(?i)(cover and (front|back) matter|^front matter$|"
                        r"^back matter$|^issue information$|^title page$|"
                        r"^editorial board$|^table of contents$|books received)")
REVIEW_TITLE = re.compile(r"(?i)(^review of\b|^book review\b|\bbook reviews\b|"
                          r"^critical notice\b|\bcritical notice of\b|"
                          r"^review essay\b|^review article\b)")
BIBLIO = re.compile(r"(?i)(\bISBN\b|\bPp\.\s|\bpp\.\)|"
                    r"[$£€]\s?\d|\b(19|20)\d{2}\b[^.]{0,40}\bpp\b)")
EDITORIAL = re.compile(r"(?i)^(editorial|preface)\b")
OBIT = re.compile(r"(?i)\b(in memoriam|obituary|obituaries)\b")
ERRATUM = re.compile(r"(?i)(corrigendum|erratum|errata|^correction\b|"
                     r"^correction to\b|^retraction\b|^retraction of\b)")
NOTE_CUE = re.compile(r"(?i)\b(reply to|response to|rejoinder to|comment on|"
                      r"in reply to|replies to)\s+(\S+)")
BAD_TYPES = {"book-review", "journal-issue", "book", "monograph", "report",
             "dataset", "peer-review", "grant", "component", "journal-volume"}


def classify(item):
    """Return (kind, reason). kind in {'article','note','exclude'}."""
    title = fp.clean_title(item)
    tl = title.strip().lower()
    typ = item.get("type")
    subs = item.get("subtitle") or []
    sub = subs[0] if subs else ""

    if typ in BAD_TYPES:
        return "exclude", "crossref type: %s" % typ
    if not tl:
        return "exclude", "empty title"
    if FRONT_BACK.search(tl):
        return "exclude", "front/back matter"
    if ERRATUM.search(title):
        return "exclude", "corrigendum/erratum/correction"
    if EDITORIAL.match(tl):
        return "exclude", "editorial/preface"
    if OBIT.search(title):
        return "exclude", "obituary"
    if REVIEW_TITLE.search(title):
        return "exclude", "book review (title signature)"
    if (sub and BIBLIO.search(sub)) or BIBLIO.search(title):
        return "exclude", "book review (bibliographic signature)"

    m = NOTE_CUE.search(title)
    if m and m.group(2)[:1].isupper():   # cue + Capitalized proper name = reply/note
        return "note", ""
    return "article", ""


# --------------------------------------------------------- crossref client -----
def cr_get(url, retries=4):
    """crossref_message with backoff on transient 5xx / network errors."""
    for i in range(retries):
        try:
            return fp.crossref_message(url)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(3 * (i + 1))
                continue
            raise
        except urllib.error.URLError:
            if i < retries - 1:
                time.sleep(3 * (i + 1))
                continue
            raise
    return {"items": []}


def fetch_journal_meta(issn):
    """Full paginated Crossref pull for one journal (cached to disk)."""
    cache = os.path.join(META_DIR, "%s.json" % issn)
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f)
    items, cursor = [], "*"
    page = 0
    while True:
        url = ("https://api.crossref.org/journals/%s/works?"
               "filter=from-pub-date:%s,until-pub-date:%s&rows=100&cursor=%s"
               "&select=%s"
               % (issn, WIN_FROM, WIN_UNTIL, urllib.parse.quote(cursor),
                  urllib.parse.quote(SELECT)))
        msg = cr_get(url)
        its = msg.get("items", [])
        items += its
        page += 1
        cursor = msg.get("next-cursor")
        if page % 10 == 0:
            print("    [%s] fetched %d records..." % (issn, len(items)), flush=True)
        if not its or not cursor:
            break
        time.sleep(CROSSREF_SLEEP)
    os.makedirs(META_DIR, exist_ok=True)
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    return items


# ------------------------------------------------------------ abstract res -----
def resolve_hit_abstract(doi, cr_item):
    """crossref -> (up to PUB_ATTEMPTS) publisher-page. Returns (text, source)."""
    a = fp.clean_abstract((cr_item or {}).get("abstract"))
    if len(a) > 40:
        return a, "crossref"
    if not doi:
        return "", ""
    for _ in range(PUB_ATTEMPTS):
        time.sleep(POLITE)
        a = fp.publisher_abstract(doi)
        if len(a) > 40:
            return a, "publisher-page"
    return "", ""


# ------------------------------------------------------------ checkpointing ----
def load_ckpt():
    if os.path.exists(CKPT):
        with open(CKPT, encoding="utf-8") as f:
            return json.load(f)
    return {"cells": {}, "journal_meta_done": {}}


def save_ckpt(ck):
    tmp = CKPT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ck, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CKPT)


def load_seen_dois():
    seen = set()
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    seen.add(json.loads(line)["doi"])
                except Exception:
                    pass
    return seen


# --------------------------------------------------------------- main run ------
def run():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(META_DIR, exist_ok=True)
    ck = load_ckpt()
    seen = load_seen_dois()
    out_f = open(OUT, "a", encoding="utf-8")

    for issn, jname in JOURNALS.items():
        print("== %s (%s) ==" % (jname, issn), flush=True)
        items = fetch_journal_meta(issn)
        ck["journal_meta_done"][issn] = True

        # bucket by computed publication year
        by_year = {}
        out_of_range = 0
        for it in items:
            y = fp.year_from(it)
            if y is None or y < YEAR_FROM or y > YEAR_TO:
                out_of_range += 1
                continue
            by_year.setdefault(y, []).append(it)
        ck["cells"].setdefault("_oor", {})[issn] = out_of_range

        for year in range(YEAR_FROM, YEAR_TO + 1):
            key = "%s|%d" % (issn, year)
            if key in ck["cells"]:
                continue
            cell_items = by_year.get(year, [])
            raw = len(cell_items)
            excl_reasons = Counter()
            eligible = []
            for it in cell_items:
                kind, reason = classify(it)
                if kind == "exclude":
                    excl_reasons[reason] += 1
                else:
                    eligible.append((it, kind))

            hits = 0
            hits_abs = 0
            hits_title_only = 0
            by_source = Counter()
            oup_fail = 0
            new_rows = []
            for it, kind in eligible:
                doi = (it.get("DOI") or "").lower()
                if not doi:
                    continue
                title = fp.clean_title(it)
                cr_abs = fp.clean_abstract(it.get("abstract"))
                have_cr_abs = len(cr_abs) > 40
                filter_text = title + (" " + cr_abs if have_cr_abs else "")
                mk = matched_keywords(filter_text)
                if not mk:
                    continue
                hits += 1
                title_only = not have_cr_abs
                if title_only:
                    hits_title_only += 1

                if doi in seen:            # global dedup / resume-safety
                    continue

                abs_text, src = resolve_hit_abstract(doi, it)
                rec = {
                    "item_id": fp.sha16(doi),
                    "doi": doi,
                    "title": title,
                    "authors": fp.authors_from(it),
                    "journal": (it.get("container-title") or [jname])[0],
                    "year": fp.year_from(it, year),
                    "abstract": abs_text,
                    "source": src or "none",
                    "fetched_at": fp.now_iso(),
                    "matched_keywords": mk,
                    "volume": it.get("volume"),
                    "issue": it.get("issue"),
                    "page": it.get("page"),
                    "type": it.get("type"),
                }
                if kind == "note":
                    rec["note"] = True
                if title_only:
                    rec["title_only_match"] = True
                if abs_text:
                    hits_abs += 1
                    by_source[src] += 1
                else:
                    rec["missing_abstract"] = True
                    if issn in OUP:
                        oup_fail += 1
                seen.add(doi)
                new_rows.append(rec)

            for rec in new_rows:
                out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out_f.flush()

            ck["cells"][key] = {
                "journal": jname, "year": year, "raw": raw,
                "excluded": int(sum(excl_reasons.values())),
                "eligible": len(eligible), "hits": hits,
                "hits_written": len(new_rows),
                "hits_with_abstract": hits_abs,
                "hits_title_only": hits_title_only,
                "oup_fail": oup_fail,
                "by_source": dict(by_source),
                "excl_reasons": dict(excl_reasons),
            }
            save_ckpt(ck)
            print("   %d: raw=%3d excl=%2d elig=%3d hits=%2d written=%2d abs=%2d "
                  "(title_only=%d oup_fail=%d)"
                  % (year, raw, sum(excl_reasons.values()), len(eligible), hits,
                     len(new_rows), hits_abs, hits_title_only, oup_fail), flush=True)

    out_f.close()
    write_log(ck)
    print("\nDONE. log -> %s" % LOG, flush=True)


# ------------------------------------------------------------- log writer ------
def _kw_frequency():
    c = Counter()
    if not os.path.exists(OUT):
        return c
    with open(OUT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                for k in json.loads(line).get("matched_keywords", []):
                    c[k] += 1
            except Exception:
                pass
    return c


def write_log(ck):
    cells = ck["cells"]
    lines = []
    A = lines.append
    A("# t1_harvest_log — P2 T1 candidate keyword pre-filter")
    A("")
    A("- generated: %s" % fp.now_iso())
    A("- harvester: `pipeline/01_fetch/fetch_t1_candidates.py` "
      "(stdlib-only; reuses `fetch_pilot.py` helpers)")
    A("- stage: **candidate generation** — recall-first keyword pre-filter. "
      "NO relevance judgement made here (next stage). Over-inclusion is intended.")
    A("- window: %d–%d, research articles + discussion notes (`note:true`)."
      % (YEAR_FROM, YEAR_TO))
    A("- copyright isolation: outputs under `data/` (.gitignore'd); "
      "abstracts not reproduced here.")
    A("")
    A("## 1. Journals (ISSNs live-verified against Crossref, 2026-07-15)")
    A("")
    A("| journal | ISSN (print) | publisher-page fallback |")
    A("|---|---|---|")
    for issn, jname in JOURNALS.items():
        note = "OUP — landing page often bot-blocks (honest `missing_abstract`)" \
            if issn in OUP else "Wiley/Springer/PDC — usually scrapable"
        A("| %s | %s | %s |" % (jname, issn, note))
    A("")
    A("## 2. Keyword pre-filter (recall-first, case-insensitive substring)")
    A("")
    A("Match target = (title ∪ abstract). Records lacking a deposited abstract are "
      "filtered on **title only** (`title_only_match:true`); abstracts are NOT "
      "fetched for non-hits. Keywords (%d): %s" % (len(KEYWORDS),
                                                   ", ".join("`%s`" % k for k in KEYWORDS)))
    A("")
    A("Exclusion (before filtering) = crossref bad types, front/back matter, "
      "editorial/preface, obituary, corrigendum/erratum/correction, book-review "
      "(title or bibliographic signature). The page-span≤5 note heuristic is "
      "**not** applied (short paper = normal article in these venues); `note` = "
      "title reply-cue only.")
    A("")
    A("## 3. Population vs hits — per journal × year (raw = all Crossref records)")
    A("")
    grand = Counter()
    for issn, jname in JOURNALS.items():
        A("### %s (%s)" % (jname, issn))
        A("")
        A("| year | raw | excluded | eligible | hits | hits w/abstract | title-only |")
        A("|---|---|---|---|---|---|---|")
        jt = Counter()
        for year in range(YEAR_FROM, YEAR_TO + 1):
            key = "%s|%d" % (issn, year)
            c = cells.get(key)
            if not c:
                continue
            A("| %d | %d | %d | %d | %d | %d | %d |" %
              (year, c["raw"], c["excluded"], c["eligible"], c["hits"],
               c["hits_with_abstract"], c["hits_title_only"]))
            for k in ("raw", "excluded", "eligible", "hits", "hits_written",
                      "hits_with_abstract", "hits_title_only", "oup_fail"):
                jt[k] += c.get(k, 0)
        oor = ck["cells"].get("_oor", {}).get(issn, 0)
        cov = (jt["hits_with_abstract"] / jt["hits"] * 100) if jt["hits"] else 0.0
        A("| **total** | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |" %
          (jt["raw"], jt["excluded"], jt["eligible"], jt["hits"],
           jt["hits_with_abstract"], jt["hits_title_only"]))
        A("")
        A("- hit abstract coverage: **%d/%d = %.1f%%** "
          "(written rows: %d; OUP fallback failures: %d; "
          "out-of-window records dropped: %d)"
          % (jt["hits_with_abstract"], jt["hits"], cov, jt["hits_written"],
             jt["oup_fail"], oor))
        A("")
        for k in jt:
            grand[k] += jt[k]
    A("## 4. Grand totals")
    A("")
    gcov = (grand["hits_with_abstract"] / grand["hits"] * 100) if grand["hits"] else 0.0
    A("- raw Crossref records (all journals, in-window): **%d**" % grand["raw"])
    A("- excluded (reviews/matter/editorial/errata/types): **%d**" % grand["excluded"])
    A("- eligible (article/note): **%d**" % grand["eligible"])
    A("- keyword hits: **%d**" % grand["hits"])
    A("- hit rows written (DOI-deduped): **%d**" % grand["hits_written"])
    A("- **hit abstract coverage: %d/%d = %.1f%%**"
      % (grand["hits_with_abstract"], grand["hits"], gcov))
    A("- title-only-matched hits (no abstract at filter time): **%d**"
      % grand["hits_title_only"])
    A("- OUP publisher-page fallback failures: **%d**" % grand["oup_fail"])
    A("")
    # DOI uniqueness check on the written file
    dois = []
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        dois.append(json.loads(line)["doi"])
                    except Exception:
                        pass
    A("- output DOI uniqueness: **%d unique / %d rows**%s"
      % (len(set(dois)), len(dois), "" if len(set(dois)) == len(dois) else "  ⚠ DUPLICATES"))
    A("")
    A("## 5. Exclusion reasons (aggregate)")
    A("")
    er = Counter()
    for key, c in cells.items():
        if key == "_oor":
            continue
        for r, n in c.get("excl_reasons", {}).items():
            er[r] += n
    A("| reason | count |")
    A("|---|---|")
    for r, n in er.most_common():
        A("| %s | %d |" % (r, n))
    A("")
    A("## 6. Abstract source breakdown (written hits)")
    A("")
    bs = Counter()
    for key, c in cells.items():
        if key == "_oor":
            continue
        for s, n in c.get("by_source", {}).items():
            bs[s] += n
    A("| source | count |")
    A("|---|---|")
    for s, n in bs.most_common():
        A("| %s | %d |" % (s, n))
    A("")
    A("## 7. Matched-keyword frequency (written hits)")
    A("")
    A("| keyword | hits |")
    A("|---|---|")
    for k, n in _kw_frequency().most_common():
        A("| `%s` | %d |" % (k, n))
    A("")
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    if "--regen-log" in sys.argv:
        write_log(load_ckpt())
        print("log regenerated -> %s" % LOG)
        return 0
    run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
