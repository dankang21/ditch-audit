#!/usr/bin/env python3
"""ditch-audit P2 aux task 2 — American Philosophical Quarterly 2004-2016 backfill.

APQ has NO Crossref records before 2017 (verified: Crossref
`journals/0003-0481/works?filter=from-pub-date:2004-01-01,until-pub-date:
2016-12-31` returns 0), so the main T1 harvester missed the 2004-2016 window.
This backfills it from **OpenAlex** (source S98143213 = APQ), reconstructing
abstracts verbatim from ``abstract_inverted_index``.

YEAR ASSIGNMENT — IMPORTANT: OpenAlex's ``publication_year`` is UNRELIABLE for
pre-DOI APQ records (it mis-dates many 1980s/90s articles to 2016, i.e. the
ingest year). The reliable signal is the VOLUME number. APQ volume->year is
exactly ``year = 1963 + volume`` (calibrated against every DOI-bearing OpenAlex
record AND against the Crossref-harvested APQ 2017-2024 items, vol 54-61 —
100% agreement). We therefore pull the ENTIRE APQ works list (no date filter)
and select ``volume in 41..53`` (= 2004..2016). This both removes mis-dated old
articles AND recovers true-window articles OpenAlex mis-dated outside 2004-2016.
Records lacking a parseable volume fall back to ``publication_year`` and are
flagged ``year_source:"openalex_pubyear"`` (kept only if that year is in range).

DOI handling: pre-2017 APQ records generally lack a DOI. When ``doi`` is null,
``item_id = sha256(openalex_id)[:16]``, ``doi = null``, OpenAlex work id kept in
``alt_id``. When a DOI exists, ``item_id = sha256(doi)[:16]``.

VERBATIM GUARANTEE: abstracts are rebuilt token-for-token from the OpenAlex
inverted index (each word replaced at its recorded position, whitespace
collapsed only). NO generation / summarisation / paraphrase.

Exclusions mirror the T1 harvester (book reviews, front/back matter, editorial,
obituary, errata, OpenAlex non-article types). Discussion notes -> ``note:true``.

Outputs (data/ is .gitignore'd -- copyrighted abstracts stay local):
  data/raw/apq_backfill.jsonl     ALL APQ articles+notes 2004-2016 (superset)
  data/raw/t1_apq_hits.jsonl      keyword pre-filtered subset (T1 keyword list)
  data/raw/apq_backfill_log.md
  data/raw/apq_meta_cache.json    raw OpenAlex pull, ALL years (resume-safe)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_t1_candidates as t1  # KEYWORDS, matched_keywords, exclusion regexes  # noqa: E402

ROOT = t1.ROOT
RAW = t1.RAW
OUT_ALL = os.path.join(RAW, "apq_backfill.jsonl")
OUT_HITS = os.path.join(RAW, "t1_apq_hits.jsonl")
LOG = os.path.join(RAW, "apq_backfill_log.md")
META_CACHE = os.path.join(RAW, "apq_meta_cache.json")

MAILTO = "dankang21@gmail.com"
UA = "ditch-audit/1.0 (mailto:%s)" % MAILTO
APQ_SOURCE = "S98143213"      # OpenAlex source id for APQ (issn 0003-0481, verified live)
JOURNAL = "American Philosophical Quarterly"
YEAR_FROM, YEAR_TO = 2004, 2016
VOL_BASE = 1963               # APQ: year = VOL_BASE + volume (calibrated, see docstring)
PER_PAGE = 200
SLEEP = 1.0
MIN_ABS = 40

SELECT = ("id,doi,title,display_name,authorships,publication_year,type,"
          "language,biblio,abstract_inverted_index")

BAD_OA_TYPES = {"paratext", "editorial", "erratum", "letter", "book-review",
                "reference-entry", "peer-review", "dataset", "grant",
                "supplementary-materials", "libguides"}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_json(url, timeout=45, retries=5):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(4 * (i + 1))
                continue
            raise
        except Exception:
            if i < retries - 1:
                time.sleep(3 * (i + 1))
                continue
            raise
    return None


def norm_doi(d):
    if not d:
        return None
    d = d.strip().lower()
    for pre in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d or None


def oa_short_id(full):
    return (full or "").rstrip("/").split("/")[-1]


def abstract_from_inverted_index(inv):
    if not inv:
        return ""
    pairs = []
    for word, positions in inv.items():
        for p in positions:
            pairs.append((p, word))
    pairs.sort(key=lambda x: x[0])
    text = " ".join(w for _, w in pairs)
    return " ".join(text.split())  # whitespace-normalise only; verbatim tokens


def parse_vol(biblio):
    try:
        return int(str((biblio or {}).get("volume")).strip())
    except (ValueError, TypeError, AttributeError):
        return None


def derive_year(w):
    """(year, source). Prefer volume (reliable); fall back to OpenAlex pub-year."""
    v = parse_vol(w.get("biblio"))
    if v is not None:
        return VOL_BASE + v, "volume"
    return w.get("publication_year"), "openalex_pubyear"


def fetch_all():
    """Full APQ works pull from OpenAlex — NO date filter (dates are unreliable)."""
    if os.path.exists(META_CACHE):
        with open(META_CACHE, encoding="utf-8") as f:
            return json.load(f)
    items, cursor, page = [], "*", 0
    while True:
        url = ("https://api.openalex.org/works?filter="
               "primary_location.source.id:%s"
               "&per-page=%d&cursor=%s&select=%s&mailto=%s"
               % (APQ_SOURCE, PER_PAGE, urllib.parse.quote(cursor),
                  urllib.parse.quote(SELECT), MAILTO))
        data = http_json(url)
        its = data.get("results", [])
        items += its
        page += 1
        cursor = data.get("meta", {}).get("next_cursor")
        print("  page %d: +%d (total %d)" % (page, len(its), len(items)), flush=True)
        if not its or not cursor:
            break
        time.sleep(SLEEP)
    with open(META_CACHE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)
    return items


def classify(title, otype):
    """Return ('article'|'note'|'exclude', reason). Mirrors T1 heuristics."""
    tl = (title or "").strip().lower()
    if otype in BAD_OA_TYPES:
        return ("exclude", "openalex type: %s" % otype)
    if not tl:
        return ("exclude", "empty title")
    if t1.FRONT_BACK.search(tl):
        return ("exclude", "front/back matter")
    if t1.ERRATUM.search(title):
        return ("exclude", "corrigendum/erratum/correction")
    if t1.EDITORIAL.match(tl):
        return ("exclude", "editorial/preface")
    if t1.OBIT.search(title):
        return ("exclude", "obituary")
    if t1.REVIEW_TITLE.search(title):
        return ("exclude", "book review (title signature)")
    if t1.BIBLIO.search(title):
        return ("exclude", "book review (bibliographic signature)")
    m = t1.NOTE_CUE.search(title)
    if m and m.group(2)[:1].isupper():
        return ("note", "")
    return ("article", "")


def build_record(w, year, year_source):
    title = (w.get("title") or w.get("display_name") or "").strip()
    doi = norm_doi(w.get("doi"))
    oid = oa_short_id(w.get("id"))
    authors = [a.get("author", {}).get("display_name")
               for a in w.get("authorships", []) if a.get("author")]
    authors = [a for a in authors if a]
    biblio = w.get("biblio") or {}
    fp_, lp_ = biblio.get("first_page"), biblio.get("last_page")
    page = ("%s-%s" % (fp_, lp_)) if fp_ and lp_ else (fp_ or None)
    abs_text = abstract_from_inverted_index(w.get("abstract_inverted_index"))
    have_abs = len(abs_text) >= MIN_ABS

    item_id = t1.fp.sha16(doi) if doi else t1.fp.sha16(oid)
    rec = {
        "item_id": item_id,
        "doi": doi,
        "title": title,
        "authors": authors,
        "journal": JOURNAL,
        "year": year,
        "abstract": abs_text if have_abs else "",
        "source": "openalex" if have_abs else "none",
        "fetched_at": now_iso(),
        "matched_keywords": [],
        "volume": biblio.get("volume"),
        "issue": biblio.get("issue"),
        "page": page,
        "type": w.get("type"),
        "year_source": year_source,
    }
    if not doi:
        rec["alt_id"] = "openalex:%s" % oid
    if not have_abs:
        rec["missing_abstract"] = True
    return rec, have_abs


def run():
    print("== APQ backfill %d-%d via OpenAlex source %s (volume-based years) ==" %
          (YEAR_FROM, YEAR_TO, APQ_SOURCE), flush=True)
    items = fetch_all()
    print("fetched %d raw OpenAlex works (all years)" % len(items), flush=True)

    all_rows, hit_rows = [], []
    seen = set()
    excl = Counter()
    by_year = Counter()
    by_year_hits = Counter()
    ysrc = Counter()
    with_abs = 0
    hits_with_abs = 0
    dup = 0
    out_of_window = 0

    for w in items:
        year, year_source = derive_year(w)
        if year is None or year < YEAR_FROM or year > YEAR_TO:
            out_of_window += 1
            continue
        title = (w.get("title") or w.get("display_name") or "").strip()
        kind, reason = classify(title, w.get("type"))
        if kind == "exclude":
            excl[reason] += 1
            continue
        rec, have_abs = build_record(w, year, year_source)
        dedup_key = rec["doi"] or rec.get("alt_id")
        if dedup_key in seen:
            dup += 1
            continue
        seen.add(dedup_key)
        if kind == "note":
            rec["note"] = True

        mk = t1.matched_keywords(rec["title"] + " " + rec["abstract"])
        rec["matched_keywords"] = mk
        if mk and not have_abs:
            rec["title_only_match"] = True

        all_rows.append(rec)
        ysrc[year_source] += 1
        by_year[year] += 1
        if have_abs:
            with_abs += 1
        if mk:
            hit_rows.append(rec)
            by_year_hits[year] += 1
            if have_abs:
                hits_with_abs += 1

    with open(OUT_ALL, "w", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_HITS, "w", encoding="utf-8") as f:
        for r in hit_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    write_log(all_rows, hit_rows, excl, by_year, by_year_hits,
              with_abs, hits_with_abs, dup, len(items), out_of_window, ysrc)
    print("\nDONE. window-articles=%d hits=%d (abs_all=%d, abs_hits=%d) "
          "oow=%d dup=%d -> %s"
          % (len(all_rows), len(hit_rows), with_abs, hits_with_abs,
             out_of_window, dup, LOG), flush=True)


def write_log(all_rows, hit_rows, excl, by_year, by_year_hits,
              with_abs, hits_with_abs, dup, raw_n, oow, ysrc):
    n_all = len(all_rows)
    n_hits = len(hit_rows)
    cov_all = with_abs / n_all * 100 if n_all else 0.0
    cov_hits = hits_with_abs / n_hits * 100 if n_hits else 0.0
    n_doi = sum(1 for r in all_rows if r["doi"])
    L = []
    A = L.append
    A("# apq_backfill_log — P2 aux task 2: APQ 2004-2016 backfill")
    A("")
    A("- generated: %s" % now_iso())
    A("- script: `pipeline/01_fetch/backfill_apq.py` (stdlib-only)")
    A("- reason: APQ has **0** Crossref records with pub-date 2004-2016 "
      "(verified live); the T1 harvester therefore missed the window.")
    A("- source: **OpenAlex** source `%s` (APQ, ISSN 0003-0481), FULL pull "
      "(no date filter)." % APQ_SOURCE)
    A("- **year = %d + volume** (APQ mapping; calibrated vs every DOI-bearing "
      "OpenAlex record AND Crossref APQ 2017-2024 vol 54-61 = 100%% agreement). "
      "OpenAlex `publication_year` is unreliable pre-DOI (mis-dates old articles "
      "to ingest year) and is used only as a flagged fallback when volume is "
      "absent." % VOL_BASE)
    A("- copyright isolation: abstracts under `data/` (.gitignore'd); not shown here.")
    A("")
    A("## Totals")
    A("")
    A("- raw OpenAlex works pulled (all years): **%d**" % raw_n)
    A("- out-of-window (volume/year not in %d-%d): **%d**" % (YEAR_FROM, YEAR_TO, oow))
    A("- excluded (reviews/matter/editorial/errata/types): **%d**" % sum(excl.values()))
    A("- intra-source duplicates dropped: **%d**" % dup)
    A("- **backfill articles+notes (apq_backfill.jsonl): %d**" % n_all)
    A("- of which carry a DOI: **%d** (rest use `alt_id`=openalex:Wxxxx, `doi`:null)"
      % n_doi)
    A("- year assignment: volume-derived **%d**, pubyear-fallback **%d**"
      % (ysrc.get("volume", 0), ysrc.get("openalex_pubyear", 0)))
    A("- abstract coverage (all backfill): **%d/%d = %.1f%%**" % (with_abs, n_all, cov_all))
    A("- **keyword hits (t1_apq_hits.jsonl): %d**" % n_hits)
    A("- abstract coverage (hits): **%d/%d = %.1f%%**" % (hits_with_abs, n_hits, cov_hits))
    A("")
    A("## Per-year counts (year = %d + volume)" % VOL_BASE)
    A("")
    A("| year | vol | backfill articles | keyword hits |")
    A("|---|---|---|---|")
    for y in range(YEAR_FROM, YEAR_TO + 1):
        A("| %d | %d | %d | %d |" % (y, y - VOL_BASE, by_year.get(y, 0),
                                     by_year_hits.get(y, 0)))
    A("| **total** | | **%d** | **%d** |" % (n_all, n_hits))
    A("")
    A("## Exclusion reasons")
    A("")
    A("| reason | count |")
    A("|---|---|")
    for r, n in excl.most_common():
        A("| %s | %d |" % (r, n))
    A("")
    A("## Matched-keyword frequency (hits)")
    A("")
    kc = Counter()
    for r in hit_rows:
        for k in r["matched_keywords"]:
            kc[k] += 1
    A("| keyword | hits |")
    A("|---|---|")
    for k, n in kc.most_common():
        A("| `%s` | %d |" % (k, n))
    A("")
    A("## id uniqueness check")
    A("")
    ids = [r["item_id"] for r in all_rows]
    keys = [(r["doi"] or r.get("alt_id")) for r in all_rows]
    A("- item_id uniqueness: **%d unique / %d rows**%s" %
      (len(set(ids)), len(ids), "" if len(set(ids)) == len(ids) else "  DUPLICATES"))
    A("- doi/alt_id uniqueness: **%d unique / %d rows**%s" %
      (len(set(keys)), len(keys), "" if len(set(keys)) == len(keys) else "  DUPLICATES"))
    A("")
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    run()
