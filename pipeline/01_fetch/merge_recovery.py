#!/usr/bin/env python3
"""Merge Asbury-PDF (F&P) + pdcnet-og (PC) recovery results into the corpus.

Applies the source-confirmed verdicts recorded by recover_fp_full.py /
recover_pc_full.py:

  review      -> row removed from corpus, appended to checkpoints/<key>/excluded.jsonl
                 (extends the P2 book-review reclassification with a SOURCE-confirmed
                 signature, catching the 6-7pp leak the metadata <=5pp rule missed)
  abstract    -> verbatim abstract written; source = asbury-pdf | pdcnet-og;
                 recovered_at stamped; ocr_suspect carried through; missing flag dropped
  otherwise   -> stays honestly missing (no fabrication)

Then recomputes the coverage matrix (reclassification-reflected denominator),
stratified by journal x era and by venue tier (T2 = fp/rs/ijpr/sophia,
T3 = pc; F&P is the R2 T2<->T3 flip axis), decomposes residual missing, and
appends section 8 to corpus_harvest_log.md. No abstract text is written to the log.
"""
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_pilot as FP  # noqa: E402

RAW = FP.RAW
CKPT = os.path.join(RAW, "checkpoints")
LOG = os.path.join(RAW, "corpus_harvest_log.md")
FP_BACKFILL = os.path.join(RAW, "fp_backfill.jsonl")

TIER = {"fp": "T2", "rs": "T2", "ijpr": "T2", "sophia": "T2", "pc": "T3"}
ORDER = ["fp", "rs", "ijpr", "sophia", "pc"]


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_doi(d):
    if not d:
        return None
    d = d.strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if d.startswith(p):
            d = d[len(p):]
    return d or None


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")] if os.path.exists(path) else []


def dump(path, recs):
    FP.write_jsonl(path, recs)


def load_results(path):
    m = {}
    for l in open(path, encoding="utf-8"):
        r = json.loads(l)
        m[r["key"]] = r          # last write wins (resume-safe)
    return m


def apply_fp(fpmap):
    stats = {}
    for path, sf, src in [(os.path.join(RAW, "corpus_fp.jsonl"), "fp", "asbury-pdf"),
                          (FP_BACKFILL, "bf", "asbury-pdf")]:
        recs = load(path)
        before_missing = sum(1 for r in recs if r.get("missing_abstract"))
        kept, moved = [], []
        vv = Counter()
        for r in recs:
            if not r.get("missing_abstract"):
                kept.append(r)
                continue
            key = norm_doi(r.get("doi")) or r.get("item_id")
            res = fpmap.get(key)
            if not res:
                kept.append(r)
                vv["unprocessed"] += 1
                continue
            v = res["verdict"]
            vv[v] += 1
            if v == "review":
                moved.append({"doi": r.get("doi"), "year": r.get("year"),
                              "volume": r.get("volume"), "issue": r.get("issue"),
                              "page": r.get("page"), "title": (r.get("title") or "")[:90],
                              "reason": "book review (Asbury PDF source-confirmed: %s)" % res["trigger"]})
                continue
            if v == "abstract":
                r["abstract"] = res["abstract"]
                r["source"] = src
                r["recovered_at"] = now()
                if res.get("ocr_suspect"):
                    r["ocr_suspect"] = True
                r.pop("missing_abstract", None)
            kept.append(r)
        dump(path, kept)
        exc = os.path.join(CKPT, "fp", "excluded.jsonl")
        os.makedirs(os.path.dirname(exc), exist_ok=True)
        with open(exc, "a", encoding="utf-8") as f:
            for m in moved:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")
        after_missing = sum(1 for r in kept if r.get("missing_abstract"))
        stats[sf] = {"n_after": len(kept), "missing_before": before_missing,
                     "missing_after": after_missing, "reviews_excluded": len(moved),
                     "verdicts": dict(vv),
                     "ocr_suspect": sum(1 for r in kept if r.get("ocr_suspect"))}
    return stats


def apply_pc(pcmap):
    path = os.path.join(RAW, "corpus_pc.jsonl")
    recs = load(path)
    before_missing = sum(1 for r in recs if r.get("missing_abstract"))
    kept, moved = [], []
    vv = Counter()
    rev_with_abs = 0
    for r in recs:
        if not r.get("missing_abstract"):
            kept.append(r)
            continue
        key = norm_doi(r.get("doi")) or r.get("item_id")
        res = pcmap.get(key)
        if not res:
            kept.append(r)
            vv["unprocessed"] += 1
            continue
        v = res["verdict"]
        vv[v] += 1
        if v == "review":
            if res.get("had_abstract"):
                rev_with_abs += 1
            moved.append({"doi": r.get("doi"), "year": r.get("year"),
                          "volume": r.get("volume"), "issue": r.get("issue"),
                          "page": r.get("page"), "title": (r.get("title") or "")[:90],
                          "reason": "book review (pdcnet source-confirmed: %s)" % res["trigger"]})
            continue
        if v == "abstract":
            r["abstract"] = res["abstract"]
            r["source"] = "pdcnet-og"
            r["recovered_at"] = now()
            r.pop("missing_abstract", None)
        kept.append(r)
    dump(path, kept)
    exc = os.path.join(CKPT, "pc", "excluded.jsonl")
    os.makedirs(os.path.dirname(exc), exist_ok=True)
    with open(exc, "a", encoding="utf-8") as f:
        for m in moved:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    after_missing = sum(1 for r in kept if r.get("missing_abstract"))
    return {"n_after": len(kept), "missing_before": before_missing,
            "missing_after": after_missing, "reviews_excluded": len(moved),
            "reviews_excluded_with_abstract": rev_with_abs, "verdicts": dict(vv)}


def journal_records():
    return {"fp": load(os.path.join(RAW, "corpus_fp.jsonl")) + load(FP_BACKFILL),
            "rs": load(os.path.join(RAW, "corpus_rs.jsonl")),
            "ijpr": load(os.path.join(RAW, "corpus_ijpr.jsonl")),
            "sophia": load(os.path.join(RAW, "corpus_sophia.jsonl")),
            "pc": load(os.path.join(RAW, "corpus_pc.jsonl"))}


def band(y):
    return "<=2008" if y <= 2008 else ("2009-2018" if y <= 2018 else "2019-2024")


def cov(recs):
    n = len(recs)
    have = sum(1 for r in recs if not r.get("missing_abstract"))
    return have, n


def main():
    fpmap = load_results(os.path.join(RAW, "fp_recover_results.jsonl"))
    pcmap = load_results(os.path.join(RAW, "pc_recover_results.jsonl"))
    fp_stats = apply_fp(fpmap)
    pc_stats = apply_pc(pcmap)

    jr = journal_records()
    bands = ["<=2008", "2009-2018", "2019-2024"]

    L = ["## 8. G2 RECOVERY: Asbury-PDF (F&P) + pdcnet-og (PC) + source-confirmed review reclassification",
         "", "- generated: %s" % now(),
         "- scripts: `recover_fp_full.py` (source: asbury-pdf), `recover_pc_full.py` (source: pdcnet-og), "
         "`merge_recovery.py`; verbatim (whitespace-collapse only), no model, no Sonar.",
         "- data/ stays .gitignore'd; abstract text not reproduced here.", ""]

    L.append("### 8.1 Recovery by source (this pass)")
    L.append("| target | processed | reviews->excluded | abstracts recovered | still missing | ocr_suspect |")
    L.append("|---|---|---|---|---|---|")
    fpc = fp_stats["fp"]; bfc = fp_stats["bf"]
    for lbl, s in [("F&P corpus_fp (asbury-pdf)", fpc), ("F&P fp_backfill (asbury-pdf)", bfc)]:
        rec = s["verdicts"].get("abstract", 0)
        L.append("| %s | %d | %d | %d | %d | %d |"
                 % (lbl, sum(s["verdicts"].values()), s["reviews_excluded"], rec,
                    s["missing_after"], s["ocr_suspect"]))
    rec_pc = pc_stats["verdicts"].get("abstract", 0)
    L.append("| PC corpus_pc (pdcnet-og) | %d | %d | %d | %d | - |"
             % (sum(pc_stats["verdicts"].values()), pc_stats["reviews_excluded"], rec_pc,
                pc_stats["missing_after"]))
    L.append("")
    L.append("- F&P verdict detail corpus_fp: %s" % fpc["verdicts"])
    L.append("- F&P verdict detail fp_backfill: %s" % bfc["verdicts"])
    L.append("- PC verdict detail: %s" % pc_stats["verdicts"])
    L.append("- PC reviews excluded that carried an abstract (review essays, reversible): %d"
             % pc_stats["reviews_excluded_with_abstract"])
    L.append("")

    L.append("### 8.2 Coverage matrix (reclassification-reflected denominator), by journal x era")
    L.append("| journal | tier | items | have | coverage | <=2008 | 2009-2018 | 2019-2024 |")
    L.append("|---|---|---|---|---|---|---|---|")
    grand_h = grand_n = 0
    tier_acc = {"T2": [0, 0], "T3": [0, 0]}
    for k in ORDER:
        recs = jr[k]
        have, n = cov(recs)
        grand_h += have; grand_n += n
        tier_acc[TIER[k]][0] += have; tier_acc[TIER[k]][1] += n
        cells = []
        for b in bands:
            sub = [r for r in recs if band(r["year"]) == b]
            h2, n2 = cov(sub)
            cells.append("%d/%d" % (h2, n2))
        L.append("| %s | %s | %d | %d | %.1f%% | %s | %s | %s |"
                 % (k, TIER[k], n, have, 100 * have / n if n else 0, *cells))
    L.append("| **T2 (fp/rs/ijpr/sophia)** | T2 | %d | %d | %.1f%% | | | |"
             % (tier_acc["T2"][1], tier_acc["T2"][0],
                100 * tier_acc["T2"][0] / tier_acc["T2"][1] if tier_acc["T2"][1] else 0))
    L.append("| **T3 (pc)** | T3 | %d | %d | %.1f%% | | | |"
             % (tier_acc["T3"][1], tier_acc["T3"][0],
                100 * tier_acc["T3"][0] / tier_acc["T3"][1] if tier_acc["T3"][1] else 0))
    L.append("| **TOTAL** | - | %d | %d | %.1f%% | | | |"
             % (grand_n, grand_h, 100 * grand_h / grand_n if grand_n else 0))
    # F&P flip: recompute T2/T3 with F&P moved to T3
    fp_h, fp_n = cov(jr["fp"])
    t2f_h = tier_acc["T2"][0] - fp_h; t2f_n = tier_acc["T2"][1] - fp_n
    t3f_h = tier_acc["T3"][0] + fp_h; t3f_n = tier_acc["T3"][1] + fp_n
    L.append("- R2 F&P flip (F&P->T3): T2 %.1f%% (%d/%d), T3 %.1f%% (%d/%d)"
             % (100 * t2f_h / t2f_n if t2f_n else 0, t2f_h, t2f_n,
                100 * t3f_h / t3f_n if t3f_n else 0, t3f_h, t3f_n))
    L.append("")

    L.append("### 8.3 Residual-missing decomposition (nature of the remaining gap)")
    resid = [(k, r["year"]) for k in ORDER for r in jr[k] if r.get("missing_abstract")]
    by_j = Counter(k for k, _ in resid)
    by_era = Counter(band(y) for _, y in resid)
    L.append("- residual missing total: **%d** (of %d = %.1f%%)"
             % (len(resid), grand_n, 100 * len(resid) / grand_n if grand_n else 0))
    L.append("- by journal: %s" % dict(by_j))
    L.append("- by era: %s" % dict(by_era))
    # nature: from recovery verdicts (source-authoritative no-abstract vs fetch-failure)
    def nat(mp):
        c = Counter()
        for r in mp.values():
            if r["verdict"] in ("no_abstract",):
                c["source_confirmed_no_abstract"] += 1
            elif r["verdict"] in ("no_landing", "no_pdf", "no_imuse", "no_doi", "error"):
                c["fetch_failure(%s)" % r["verdict"]] += 1
        return dict(c)
    L.append("- F&P residual nature (recovery verdicts): %s" % nat(fpmap))
    L.append("- PC residual nature (recovery verdicts): %s" % nat(pcmap))
    L.append("- interpretation: 'source_confirmed_no_abstract' = journal never printed/exposed an "
             "abstract (pre-abstract-era tail, honest missing); 'fetch_failure' = retryable.")
    L.append("")

    all_dois = [r["doi"] for k in ORDER for r in jr[k] if r.get("doi")]
    dup = [d for d, c in Counter(all_dois).items() if c > 1]
    L.append("- DOI uniqueness (cross-journal, incl. backfill): %d unique / %d = %s; dups %d"
             % (len(set(all_dois)), len(all_dois), "100%" if not dup else "<100%", len(dup)))

    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n".join(L) + "\n")

    summary = {"fp": fp_stats, "pc": pc_stats,
               "overall_coverage": round(100 * grand_h / grand_n, 1),
               "grand": [grand_h, grand_n], "residual": len(resid),
               "residual_by_journal": dict(by_j), "dup": len(dup)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
