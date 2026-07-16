#!/usr/bin/env python3
"""ditch-audit P2 corpus post-processing (3 dk-approved low-risk passes, no Sonar).

Runs, in order, over the P2 corpus produced by ``fetch_corpus.py``:

  T3  F&P 2022-2024 backfill   -- OpenAlex source S192930876 (Faith and Philosophy),
      volume-derived year (year = 1983 + volume; vol 39=2022, 40=2023, 41=2024),
      verbatim abstracts from abstract_inverted_index. Crossref has no F&P DOIs
      past vol 38 (2021), so these are NEW records. -> data/raw/fp_backfill.jsonl
      (OpenAlex holds vol 39-40 only; vol 41/2024 = 0 works -> honestly absent.)

  T1  PDC book-review reclassification (fp, pc only) -- PDC reviews are formatted
      "REVIEWER IN CAPS: Book Title" (2-5 pp, no ISBN/blurb, journal-article type)
      and slipped into the note class via the span<=5 rule. Reclassify a current
      note -> excluded iff NOT a genuine reply-cue AND
        (a) title matches the caps "NAME: Title" review signature, OR
        (b) missing_abstract AND page-span <= 5.
      Genuine reply-cue notes (reply/response/rejoinder/comment/... to a paper)
      are preserved. No re-scrape. -> rewrites corpus_{fp,pc}.jsonl; excluded rows
      appended to checkpoints/<key>/excluded.jsonl (reason logged).

  T2  DB abstract recovery (fp, fp_backfill, pc, ijpr, sophia) -- fill remaining
      missing abstracts from OpenAlex (inverted-index, VERBATIM) then Semantic
      Scholar (verbatim abstract field). No generation/paraphrase. Low-yield
      segments (PC <=2018, IJPR 2004-07) are attempted in full but expected near
      zero (measured: OpenAlex has ~6% PC-old, ~0% IJPR; SS ~0%). -> rewrites the
      corpus files in place; source set to openalex/semanticscholar; missing flag
      dropped; recovered_at stamped.

Then recomputes the coverage matrix (reclassification- and backfill-adjusted
denominator) and appends section 7 to data/raw/corpus_harvest_log.md, decomposing
residual missing into genuine-no-abstract vs source-absent.

VERBATIM GUARANTEE mirrors recover_t1_abstracts.py / backfill_apq.py: OpenAlex
tokens are re-placed at their recorded inverted-index positions (whitespace
collapsed only); Semantic Scholar abstracts used as-is. No model anywhere.

data/ stays .gitignore'd; abstracts not reproduced in logs.
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_pilot as fp      # noqa: E402  sha16, clean helpers, page_span
import fetch_corpus as fc     # noqa: E402  classify, NOTE_TITLE/NOTE_REPLY_NAMED, JOURNALS

RAW = fp.RAW
CKPT = os.path.join(RAW, "checkpoints")
CACHE = os.path.join(RAW, "corpus_recover_cache")
LOG = os.path.join(RAW, "corpus_harvest_log.md")
FP_BACKFILL = os.path.join(RAW, "fp_backfill.jsonl")

MAILTO = "dankang21@gmail.com"
UA = "ditch-audit/1.0 (mailto:%s)" % MAILTO
MIN_ABS = 40
OA_BATCH = 50
OA_SLEEP = 1.0
SS_SLEEP = 3.5

FP_OA_SOURCE = "S192930876"     # OpenAlex source id, Faith and Philosophy (issn 0739-7046)
FP_VOL_BASE = 1983              # F&P: year = 1983 + volume  (vol 1 = 1984; calibrated)
FP_BACKFILL_VOLS = {39: 2022, 40: 2023, 41: 2024}   # 41 absent in OpenAlex (logged)

BAD_OA_TYPES = {"paratext", "editorial", "erratum", "letter", "book-review",
                "reference-entry", "peer-review", "dataset", "grant",
                "supplementary-materials", "libguides", "review"}

# caps "REVIEWER: Title" signature (pre-colon is an all-caps name / initials)
REVIEW_SIG = re.compile(r"^[A-Z][A-Z.'’`\- ]{1,45}:\s+\S")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")] if os.path.exists(path) else []


def dump(path, recs):
    fp.write_jsonl(path, recs)


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
            return None
        except Exception:
            if i < retries - 1:
                time.sleep(3 * (i + 1))
                continue
            return None
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
    """Verbatim: each token re-placed at its recorded position; whitespace only."""
    if not inv:
        return ""
    pairs = []
    for word, positions in inv.items():
        for p in positions:
            pairs.append((p, word))
    pairs.sort(key=lambda x: x[0])
    text = " ".join(w for _, w in pairs)
    return " ".join(text.split())  # whitespace-normalise only; verbatim tokens


# ============================ T1: PDC review reclassification ====================
def is_reply_note(title):
    return bool(fc.NOTE_TITLE.search(title) or fc.NOTE_REPLY_NAMED.search(title))


def review_verdict(rec):
    """(is_review, trigger) for a record CURRENTLY flagged note. Preserves reply notes."""
    title = rec.get("title", "")
    if is_reply_note(title):
        return False, None
    if REVIEW_SIG.match(title):
        return True, "review-signature"
    span = fp.page_span(rec)
    if rec.get("missing_abstract") and span is not None and span <= 5:
        return True, "missing+short(<=5pp)"
    return False, None


def reclassify_pdc(key):
    path = os.path.join(RAW, "corpus_%s.jsonl" % key)
    recs = load(path)
    before_notes = sum(1 for r in recs if r.get("note"))
    kept, moved = [], []
    trig = Counter()
    for r in recs:
        if r.get("note"):
            rev, t = review_verdict(r)
            if rev:
                trig[t] += 1
                moved.append({"doi": r.get("doi"), "year": r.get("year"),
                              "volume": r.get("volume"), "issue": r.get("issue"),
                              "page": r.get("page"), "title": (r.get("title") or "")[:90],
                              "reason": "book review (PDC reclassified: %s)" % t})
                continue
        kept.append(r)
    dump(path, kept)
    exc_path = os.path.join(CKPT, key, "excluded.jsonl")
    os.makedirs(os.path.dirname(exc_path), exist_ok=True)
    with open(exc_path, "a", encoding="utf-8") as f:
        for m in moved:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    after_notes = sum(1 for r in kept if r.get("note"))
    return {"before_total": len(recs), "after_total": len(kept),
            "before_notes": before_notes, "after_notes": after_notes,
            "reclassified": len(moved), "triggers": dict(trig)}


# ============================ T3: F&P 2022-2024 backfill =========================
def fetch_fp_openalex():
    cache = os.path.join(CACHE, "fp_openalex_all.json")
    if os.path.exists(cache):
        return json.load(open(cache, encoding="utf-8"))
    os.makedirs(CACHE, exist_ok=True)
    select = "id,doi,title,display_name,authorships,publication_year,type,biblio,abstract_inverted_index"
    items, cursor = [], "*"
    while True:
        url = ("https://api.openalex.org/works?filter=primary_location.source.id:%s"
               "&per-page=200&cursor=%s&select=%s&mailto=%s"
               % (FP_OA_SOURCE, urllib.parse.quote(cursor), urllib.parse.quote(select), MAILTO))
        d = http_json(url)
        if d is None:
            break
        items += d.get("results", [])
        cursor = d.get("meta", {}).get("next_cursor")
        if not d.get("results") or not cursor:
            break
        time.sleep(OA_SLEEP)
    json.dump(items, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    return items


def parse_vol(w):
    try:
        return int(str((w.get("biblio") or {}).get("volume")).strip())
    except (ValueError, TypeError, AttributeError):
        return None


def backfill_fp():
    items = fetch_fp_openalex()
    by_vol = Counter(parse_vol(w) for w in items)
    recs, excluded = [], Counter()
    seen = set()
    for w in items:
        v = parse_vol(w)
        if v not in FP_BACKFILL_VOLS:
            continue
        year = FP_VOL_BASE + v
        title = (w.get("title") or w.get("display_name") or "").strip()
        otype = w.get("type")
        doi = norm_doi(w.get("doi"))
        oid = oa_short_id(w.get("id"))
        if otype in BAD_OA_TYPES:
            excluded["openalex type: %s" % otype] += 1
            continue
        biblio = w.get("biblio") or {}
        fpg, lpg = biblio.get("first_page"), biblio.get("last_page")
        page = ("%s-%s" % (fpg, lpg)) if fpg and lpg else (fpg or None)
        pseudo = {"title": [title], "subtitle": [], "page": page or "",
                  "type": "journal-article"}
        kind, reason = fc.classify(pseudo, pdc=True)
        if kind == "exclude":
            excluded[reason] += 1
            continue
        abs_text = abstract_from_inverted_index(w.get("abstract_inverted_index"))
        have = len(abs_text) >= MIN_ABS
        key = doi or ("openalex:%s" % oid)
        if key in seen:
            continue
        seen.add(key)
        authors = [a.get("author", {}).get("display_name")
                   for a in w.get("authorships", []) if a.get("author")]
        rec = {
            "item_id": fp.sha16(doi) if doi else fp.sha16(oid),
            "doi": doi or "",
            "title": title,
            "authors": [a for a in authors if a],
            "journal": "Faith and Philosophy",
            "year": year,
            "abstract": abs_text if have else "",
            "source": "openalex" if have else "openalex-none",
            "fetched_at": now_iso(),
            "volume": biblio.get("volume"),
            "issue": biblio.get("issue"),
            "page": page,
            "year_source": "openalex_volume",
        }
        if not doi:
            rec["alt_id"] = "openalex:%s" % oid
        if kind == "note":
            rec["note"] = True
        if not have:
            rec["missing_abstract"] = True
        recs.append(rec)

    # apply the same PDC review reclassification to backfill notes
    kept, moved = [], 0
    for r in recs:
        if r.get("note"):
            rev, t = review_verdict(r)
            if rev:
                excluded["book review (PDC reclassified: %s)" % t] += 1
                moved += 1
                continue
        kept.append(r)
    dump(FP_BACKFILL, kept)
    have = sum(1 for r in kept if not r.get("missing_abstract"))
    return {"vols_present": {v: by_vol.get(v, 0) for v in FP_BACKFILL_VOLS},
            "included": len(kept), "have_abstract": have,
            "reclassified_reviews": moved, "excluded": dict(excluded),
            "by_year": dict(Counter(r["year"] for r in kept))}


# ============================ T2: DB abstract recovery ==========================
def openalex_recover(dois):
    """{norm_doi: verbatim_abstract} for up to 50 DOIs, cached."""
    ckey = "oa_%s.json" % fp.sha16("|".join(sorted(dois)))
    cpath = os.path.join(CACHE, ckey)
    if os.path.exists(cpath):
        data = json.load(open(cpath, encoding="utf-8"))
    else:
        url = ("https://api.openalex.org/works?filter=doi:%s&per-page=%d"
               "&select=doi,abstract_inverted_index&mailto=%s"
               % (urllib.parse.quote("|".join(dois)), OA_BATCH, MAILTO))
        data = http_json(url)
        if data is None:
            return {}
        os.makedirs(CACHE, exist_ok=True)
        json.dump(data, open(cpath, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(OA_SLEEP)
    out = {}
    for w in data.get("results", []):
        nd = norm_doi(w.get("doi"))
        if nd:
            out[nd] = abstract_from_inverted_index(w.get("abstract_inverted_index"))
    return out


def ss_recover(doi):
    ckey = "ss_%s.json" % fp.sha16(doi)
    cpath = os.path.join(CACHE, ckey)
    if os.path.exists(cpath):
        data = json.load(open(cpath, encoding="utf-8"))
    else:
        url = ("https://api.semanticscholar.org/graph/v1/paper/DOI:%s?fields=abstract"
               % urllib.parse.quote(doi))
        data = http_json(url, timeout=30)
        if data is None:
            return ""
        os.makedirs(CACHE, exist_ok=True)
        json.dump(data, open(cpath, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(SS_SLEEP)
    return (data.get("abstract") or "").strip()


def recover_file(path, label):
    recs = load(path)
    targets = [r for r in recs if r.get("missing_abstract") and r.get("doi")]
    no_doi = [r for r in recs if r.get("missing_abstract") and not r.get("doi")]
    recovered = {}
    tdois = [norm_doi(r["doi"]) for r in targets]
    # pass 1: OpenAlex batched
    for i in range(0, len(tdois), OA_BATCH):
        res = openalex_recover(tdois[i:i + OA_BATCH])
        for d in tdois[i:i + OA_BATCH]:
            a = res.get(d, "")
            if len(a) >= MIN_ABS:
                recovered[d] = (a, "openalex")
    # pass 2: Semantic Scholar for the rest
    still = [d for d in tdois if d not in recovered]
    for d in still:
        a = ss_recover(d)
        if len(a) >= MIN_ABS:
            recovered[d] = (a, "semanticscholar")
    oa = sum(1 for v in recovered.values() if v[1] == "openalex")
    ss = sum(1 for v in recovered.values() if v[1] == "semanticscholar")
    # apply
    for r in recs:
        if not (r.get("missing_abstract") and r.get("doi")):
            continue
        d = norm_doi(r["doi"])
        if d in recovered:
            a, src = recovered[d]
            r["abstract"] = a
            r["source"] = src
            r["recovered_at"] = now_iso()
            r.pop("missing_abstract", None)
    dump(path, recs)
    have = sum(1 for r in recs if not r.get("missing_abstract"))
    return {"label": label, "n": len(recs), "missing_before": len(targets) + len(no_doi),
            "openalex": oa, "semanticscholar": ss,
            "still_missing": len(recs) - have, "no_doi": len(no_doi),
            "coverage": have / len(recs) if recs else 0.0}


# ============================ recompute + log append ============================
def fp_all_records():
    """F&P corpus = corpus_fp.jsonl (Crossref, <=2021) UNION fp_backfill.jsonl (2022-24)."""
    return load(os.path.join(RAW, "corpus_fp.jsonl")) + load(FP_BACKFILL)


def journal_records():
    return {
        "fp": fp_all_records(),
        "rs": load(os.path.join(RAW, "corpus_rs.jsonl")),
        "ijpr": load(os.path.join(RAW, "corpus_ijpr.jsonl")),
        "sophia": load(os.path.join(RAW, "corpus_sophia.jsonl")),
        "pc": load(os.path.join(RAW, "corpus_pc.jsonl")),
    }


def append_log(sections):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n".join(sections) + "\n")


def main():
    os.makedirs(CACHE, exist_ok=True)
    print("== T3: F&P 2022-2024 backfill (OpenAlex source %s) ==" % FP_OA_SOURCE, flush=True)
    bf = backfill_fp()
    print("  ", bf, flush=True)

    print("== T1: PDC book-review reclassification (fp, pc) ==", flush=True)
    rc = {"fp": reclassify_pdc("fp"), "pc": reclassify_pdc("pc")}
    for k, v in rc.items():
        print("  ", k, v, flush=True)

    print("== T2: DB abstract recovery (OpenAlex -> Semantic Scholar) ==", flush=True)
    rec_stats = []
    for path, label in [(os.path.join(RAW, "corpus_fp.jsonl"), "fp"),
                        (FP_BACKFILL, "fp_backfill"),
                        (os.path.join(RAW, "corpus_pc.jsonl"), "pc"),
                        (os.path.join(RAW, "corpus_ijpr.jsonl"), "ijpr"),
                        (os.path.join(RAW, "corpus_sophia.jsonl"), "sophia")]:
        s = recover_file(path, label)
        rec_stats.append(s)
        print("  ", s, flush=True)

    # ---- recompute matrix ----
    jr = journal_records()
    order = ["fp", "rs", "ijpr", "sophia", "pc"]
    grand_n = sum(len(jr[k]) for k in order)
    grand_have = sum(sum(1 for r in jr[k] if not r.get("missing_abstract")) for k in order)
    all_dois = [r["doi"] for k in order for r in jr[k] if r.get("doi")]
    dup = [d for d, c in Counter(all_dois).items() if c > 1]

    L = ["## 7. POST-PROCESSING (backfill + PDC reclassification + DB recovery)",
         "", "- generated: %s" % now_iso(),
         "- script: `pipeline/01_fetch/corpus_postprocess.py` (stdlib; verbatim OpenAlex/SS; no Sonar, no generation)",
         "- F&P corpus now = `corpus_fp.jsonl` (Crossref, <=2021) UNION `fp_backfill.jsonl` (OpenAlex, 2022-2023)",
         ""]
    L.append("### 7.1 F&P backfill (OpenAlex volume-derived year = 1983+vol)")
    L.append("- volumes present in OpenAlex: %s (vol 41/2024 = 0 works -> genuinely absent)"
             % bf["vols_present"])
    L.append("- backfill included: **%d** (by year %s); with abstract: %d"
             % (bf["included"], bf["by_year"], bf["have_abstract"]))
    L.append("- backfill excluded (types + reclassified reviews): %s" % bf["excluded"])
    L.append("")
    L.append("### 7.2 PDC book-review reclassification (note -> excluded)")
    L.append("| journal | notes before | reclassified | notes after | triggers |")
    L.append("|---|---|---|---|---|")
    for k in ("fp", "pc"):
        v = rc[k]
        L.append("| %s | %d | %d | %d | %s |"
                 % (k, v["before_notes"], v["reclassified"], v["after_notes"], v["triggers"]))
    L.append("- reply-cue notes preserved; excluded rows appended to checkpoints/<key>/excluded.jsonl")
    L.append("")
    L.append("### 7.3 DB abstract recovery (verbatim)")
    L.append("| file | n | missing before | OpenAlex | Sem.Scholar | still missing | coverage |")
    L.append("|---|---|---|---|---|---|---|")
    for s in rec_stats:
        L.append("| %s | %d | %d | %d | %d | %d | %.1f%% |"
                 % (s["label"], s["n"], s["missing_before"], s["openalex"],
                    s["semanticscholar"], s["still_missing"], 100 * s["coverage"]))
    L.append("")
    L.append("### 7.4 Final coverage matrix (post backfill + reclassification + recovery)")
    L.append("| journal | items | have | coverage | <=2018 | >=2019 |")
    L.append("|---|---|---|---|---|---|")
    for k in order:
        recs = jr[k]
        n = len(recs)
        have = sum(1 for r in recs if not r.get("missing_abstract"))
        pre = [r for r in recs if r["year"] <= 2018]
        post = [r for r in recs if r["year"] >= 2019]
        ph = sum(1 for r in pre if not r.get("missing_abstract"))
        qh = sum(1 for r in post if not r.get("missing_abstract"))
        L.append("| %s | %d | %d | %.1f%% | %d/%d | %d/%d |"
                 % (k, n, have, 100 * have / n if n else 0, ph, len(pre), qh, len(post)))
    L.append("| **TOTAL** | **%d** | **%d** | **%.1f%%** | | |"
             % (grand_n, grand_have, 100 * grand_have / grand_n if grand_n else 0))
    L.append("")
    L.append("### 7.5 Residual-missing decomposition (nature of the gap)")
    resid = []
    for k in order:
        for r in jr[k]:
            if r.get("missing_abstract"):
                resid.append((k, r["year"]))
    rc_by_j = Counter(k for k, _y in resid)
    # genuine-no-abstract (old, pre-DOI-abstract era) vs source-absent classification
    pre2009 = sum(1 for _k, y in resid if y <= 2008)
    y0918 = sum(1 for _k, y in resid if 2009 <= y <= 2018)
    y19 = sum(1 for _k, y in resid if y >= 2019)
    L.append("- residual missing total: **%d** (of %d = %.1f%% still uncovered)"
             % (len(resid), grand_n, 100 * len(resid) / grand_n if grand_n else 0))
    L.append("- by journal: %s" % dict(rc_by_j))
    L.append("- by era: <=2008 **%d** (Kluwer/pre-structured-abstract: genuine no-abstract), "
             "2009-2018 **%d**, >=2019 **%d**" % (pre2009, y0918, y19))
    L.append("- DOI uniqueness (cross-journal, incl. backfill): %d unique / %d = %s; dups %d"
             % (len(set(all_dois)), len(all_dois),
                "100%" if not dup else "<100%", len(dup)))
    append_log(L)
    print("\nDONE. overall coverage %.1f%% (%d/%d); residual %d; DOI dup %d -> appended §7 to %s"
          % (100 * grand_have / grand_n, grand_have, grand_n, len(resid), len(dup), LOG), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
