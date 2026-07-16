#!/usr/bin/env python3
"""build_locks.py — machine-readable corpus-lock id lists (analysis-plan v1.1
§11 freeze-manifest item 12: "review-exclusion list (620), review-essay list
(15), missingness-stratum item list (672 items; 210 missing), ...
machine-readable confirmatory-exclusion id list (89 pilot-phase = 69 real +
20 gold; §3.8)").

Writes four JSON files under data/raw/locks/ (data/ stays .gitignore'd —
absolute rule 3; the freeze manifest records their SHA256):

  review_exclusions.json    — every book-review exclusion row of the F&P and
      PC checkpoints (checkpoints/{fp,pc}/excluded.jsonl, reason contains
      "review", case-insensitive), keyed by DOI. These are the source-
      confirmed review exclusions behind the §1.2 T2∪T3 denominator
      ("after 620 source-confirmed review exclusions" — the plan's 620 is a
      nominal round figure; the mechanical extraction count and its
      per-reason decomposition are recorded in this file).
  review_essays.json        — the 15 reversibly-excluded abstract-bearing PC
      review essays (§1.2, §12 item 6): rows of pc_recover_results.jsonl with
      verdict = "review" and abs_len > 0 (source-authoritative
      Item_Data_Type = Book Review that nonetheless carried a printed
      abstract). A subset of review_exclusions by DOI (asserted).
  missingness_stratum.json  — the preregistered pre-2008 missingness stratum
      (§4.0/§4.1): every item of the locked T2∪T3 corpus files with
      year <= 2008 (672 expected), each flagged missing_abstract when the
      abstract field is absent/empty (210 expected).
  confirmatory_exclusions.json — the 89 pilot-phase item ids excluded from
      all confirmatory denominators (§3.8): pilot_rs2015 (35) +
      pilot_ijpr2015 (34) + gold_anchors (20).

Every file carries `generation_rule` and `sources` (path -> SHA256) fields,
contains ids/bibliographic pointers only (no abstract text — absolute
rule 3), embeds no timestamp, and is written with sorted keys and sorted item
order, so re-runs over unchanged inputs are byte-identical (§2.5 standard).

The real run verifies the plan §1.2/§3.8 registered counts
(672/210, 15, 89) and dies without writing on mismatch (the locks certify
the gated corpus; a drifted corpus must not be silently re-locked).

stdlib-only, Python 3.10+, deterministic. --selftest runs on synthetic
fixtures only (no repo data needed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# Locked T2∪T3 corpus of record (plan §1.2; same union as
# build_checkpoint_tranche.py minus the T1 file — the missingness stratum is
# a T2∪T3 construct, §4.0).
T23_CORPUS = [
    ("fp", "data/raw/corpus_fp.jsonl"),
    ("fp", "data/raw/fp_backfill.jsonl"),
    ("rs", "data/raw/corpus_rs.jsonl"),
    ("ijpr", "data/raw/corpus_ijpr.jsonl"),
    ("sophia", "data/raw/corpus_sophia.jsonl"),
    ("pc", "data/raw/corpus_pc.jsonl"),
]
REVIEW_EXCLUDED_FILES = [
    ("fp", "data/raw/checkpoints/fp/excluded.jsonl"),
    ("pc", "data/raw/checkpoints/pc/excluded.jsonl"),
]
PC_RECOVER_RESULTS = "data/raw/pc_recover_results.jsonl"
CONFIRMATORY_SETS = [
    ("pilot_rs2015", "data/raw/pilot_rs2015.jsonl"),
    ("pilot_ijpr2015", "data/raw/pilot_ijpr2015.jsonl"),
    ("gold_anchors", "data/raw/gold_anchors.jsonl"),
]
OUT_DIR = "data/raw/locks"

PRE2008_MAX_YEAR = 2008          # §4.0: "pre-2008" = the <= 2008 era stratum
EXPECT = {                       # registered counts (plan §1.2 / §3.8)
    "missingness_total": 672,
    "missingness_missing": 210,
    "review_essays": 15,
    "confirmatory": 89,
}


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: str) -> list:
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                die(f"{path}:{n}: invalid JSON ({e})", 4)
    return out


def is_review_reason(reason) -> bool:
    return "review" in (reason or "").casefold()


def has_abstract(rec) -> bool:
    return bool((rec.get("abstract") or "").strip())


# ------------------------------------------------------------- lock builders
def build_review_exclusions(rows_by_venue: dict, sources: dict) -> dict:
    items, reasons = [], {}
    for venue in sorted(rows_by_venue):
        for r in rows_by_venue[venue]:
            if not is_review_reason(r.get("reason")):
                continue
            items.append({"doi": r.get("doi"), "venue": venue,
                          "year": int(r["year"]) if r.get("year") is not None else None,
                          "reason": r.get("reason")})
            reasons[r.get("reason")] = reasons.get(r.get("reason"), 0) + 1
    items.sort(key=lambda x: (x["venue"], x["doi"] or ""))
    dois = [x["doi"] for x in items]
    if len(set(dois)) != len(dois) or not all(dois):
        die("review_exclusions: missing or duplicate DOI in excluded rows")
    return {
        "lock": "review_exclusions",
        "spec": "plan v1.1 §11 item 12 — review-exclusion list (nominal 620)",
        "generation_rule": (
            "all rows of data/raw/checkpoints/{fp,pc}/excluded.jsonl whose "
            "`reason` contains 'review' (case-insensitive), keyed by DOI, "
            "sorted by (venue, doi). The plan's '620 source-confirmed review "
            "exclusions' (§1.2) is a nominal figure for the post-harvest "
            "source-confirmed passes; this lock is the exhaustive mechanical "
            "extraction (initial-harvest signature rows included) and its "
            "count is authoritative for manifest item 12."),
        "sources": sources,
        "count": len(items),
        "count_by_reason": dict(sorted(reasons.items())),
        "items": items,
    }


def build_review_essays(recover_rows: list, review_dois: set, sources: dict) -> dict:
    items = []
    for r in recover_rows:
        if r.get("verdict") == "review" and (r.get("abs_len") or 0) > 0:
            items.append({"item_id": r.get("item_id"), "doi": r.get("doi"),
                          "year": r.get("year")})
    items.sort(key=lambda x: x["doi"] or "")
    missing = [x["doi"] for x in items if x["doi"] not in review_dois]
    if missing:
        die(f"review_essays: {len(missing)} essay DOI(s) not in the "
            f"review-exclusion lock (e.g. {missing[:3]})")
    return {
        "lock": "review_essays",
        "spec": "plan v1.1 §11 item 12 — review-essay list (15; §12 item 6 "
                "resolution: exclusion sustained, reversible)",
        "generation_rule": (
            "rows of data/raw/pc_recover_results.jsonl with verdict='review' "
            "and abs_len>0 (pdcnet source-confirmed Item_Data_Type=Book "
            "Review carrying a printed abstract), sorted by doi; asserted a "
            "subset of review_exclusions.json by DOI."),
        "sources": sources,
        "count": len(items),
        "items": items,
    }


def build_missingness_stratum(corpus_rows: list, sources: dict) -> dict:
    items = []
    for venue, r in corpus_rows:
        try:
            year = int(r.get("year"))
        except (TypeError, ValueError):
            die(f"missingness_stratum: unparseable year in item "
                f"{r.get('item_id')!r}")
        if year > PRE2008_MAX_YEAR:
            continue
        items.append({"item_id": r.get("item_id"), "doi": r.get("doi"),
                      "venue": venue, "year": year,
                      "missing_abstract": not has_abstract(r)})
    items.sort(key=lambda x: (x["venue"], x["item_id"] or ""))
    ids = [x["item_id"] for x in items]
    if len(set(ids)) != len(ids) or not all(ids):
        die("missingness_stratum: missing or duplicate item_id")
    n_missing = sum(1 for x in items if x["missing_abstract"])
    per_venue = {}
    for x in items:
        pv = per_venue.setdefault(x["venue"], {"items": 0, "missing": 0})
        pv["items"] += 1
        pv["missing"] += 1 if x["missing_abstract"] else 0
    return {
        "lock": "missingness_stratum",
        "spec": "plan v1.1 §11 item 12 — missingness-stratum item list "
                "(672 items; 210 missing; §4.0 preregistered stratum)",
        "generation_rule": (
            "every item of the locked T2∪T3 corpus files (corpus_fp + "
            "fp_backfill + corpus_rs + corpus_ijpr + corpus_sophia + "
            "corpus_pc) with int(year) <= 2008; missing_abstract = abstract "
            "field absent/empty after strip; sorted by (venue, item_id)."),
        "sources": sources,
        "count": len(items),
        "count_missing_abstract": n_missing,
        "count_by_venue": dict(sorted(per_venue.items())),
        "items": items,
    }


def build_confirmatory_exclusions(sets_rows: dict, sources: dict) -> dict:
    items = []
    for set_name in sorted(sets_rows):
        for r in sets_rows[set_name]:
            items.append({"item_id": r.get("item_id"), "doi": r.get("doi"),
                          "set": set_name})
    items.sort(key=lambda x: (x["set"], x["item_id"] or ""))
    ids = [x["item_id"] for x in items]
    if len(set(ids)) != len(ids) or not all(ids):
        die("confirmatory_exclusions: missing or duplicate item_id")
    per_set = {s: sum(1 for x in items if x["set"] == s) for s in sets_rows}
    return {
        "lock": "confirmatory_exclusions",
        "spec": "plan v1.1 §11 item 12 / §3.8 — machine-readable "
                "confirmatory-exclusion id list (89 pilot-phase = 69 real + "
                "20 gold)",
        "generation_rule": (
            "all item_ids of data/raw/pilot_rs2015.jsonl + "
            "data/raw/pilot_ijpr2015.jsonl + data/raw/gold_anchors.jsonl; "
            "these items are excluded from ALL confirmatory denominators "
            "(§3.8: pilot data per outline §4.7; anchors are curated and "
            "memorization-suspect); sorted by (set, item_id)."),
        "sources": sources,
        "count": len(items),
        "count_by_set": dict(sorted(per_set.items())),
        "items": items,
    }


# ------------------------------------------------------------------- driver
def write_lock(out_dir: str, name: str, blob: dict) -> str:
    path = os.path.join(out_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(blob, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    return path


def run(root: str, out_dir: str, enforce_expect: bool = True) -> dict:
    def ap(rel):
        return os.path.join(root, rel)

    # review exclusions (fp + pc checkpoints)
    rex_sources, rows_by_venue = {}, {}
    for venue, rel in REVIEW_EXCLUDED_FILES:
        p = ap(rel)
        rex_sources[rel] = sha256_file(p)
        rows_by_venue.setdefault(venue, []).extend(read_jsonl(p))
    review_exclusions = build_review_exclusions(rows_by_venue, rex_sources)

    # review essays (pc recovery results; subset check vs review exclusions)
    ress_p = ap(PC_RECOVER_RESULTS)
    review_essays = build_review_essays(
        read_jsonl(ress_p),
        {x["doi"] for x in review_exclusions["items"]},
        {PC_RECOVER_RESULTS: sha256_file(ress_p)})

    # missingness stratum (T2∪T3 corpus, year <= 2008)
    ms_sources, corpus_rows = {}, []
    for venue, rel in T23_CORPUS:
        p = ap(rel)
        ms_sources[rel] = sha256_file(p)
        corpus_rows.extend((venue, r) for r in read_jsonl(p))
    missingness = build_missingness_stratum(corpus_rows, ms_sources)

    # confirmatory exclusions (pilot 69 + gold 20)
    cf_sources, sets_rows = {}, {}
    for set_name, rel in CONFIRMATORY_SETS:
        p = ap(rel)
        cf_sources[rel] = sha256_file(p)
        sets_rows[set_name] = read_jsonl(p)
    confirmatory = build_confirmatory_exclusions(sets_rows, cf_sources)

    if enforce_expect:
        checks = [
            ("missingness stratum total", missingness["count"],
             EXPECT["missingness_total"]),
            ("missingness stratum missing", missingness["count_missing_abstract"],
             EXPECT["missingness_missing"]),
            ("review essays", review_essays["count"], EXPECT["review_essays"]),
            ("confirmatory exclusions", confirmatory["count"],
             EXPECT["confirmatory"]),
        ]
        bad = [f"{n}: got {g}, registered {e}" for n, g, e in checks if g != e]
        if bad:
            die("registered-count mismatch (plan §1.2/§3.8) — locks NOT "
                "written:\n  " + "\n  ".join(bad), 5)

    os.makedirs(out_dir, exist_ok=True)
    written = {}
    for name, blob in (("review_exclusions", review_exclusions),
                       ("review_essays", review_essays),
                       ("missingness_stratum", missingness),
                       ("confirmatory_exclusions", confirmatory)):
        path = write_lock(out_dir, name, blob)
        written[name] = {"path": path, "sha256": sha256_file(path),
                         "count": blob["count"]}
        print(f"[lock] {name}: {blob['count']} item(s) -> {path}")
        print(f"       sha256={written[name]['sha256']}")
    return written


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    def wj(path, rows):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")

    with tempfile.TemporaryDirectory(prefix="locks_selftest_") as td:
        # synthetic fixture tree mirroring the real relative layout
        wj(os.path.join(td, "data/raw/checkpoints/fp/excluded.jsonl"), [
            {"doi": "10.1/fp1", "year": 2010, "title": "t",
             "reason": "book review (bibliographic signature)"},
            {"doi": "10.1/fp2", "year": 2011, "title": "t", "reason": "editorial"},
            {"doi": "10.1/fp3", "year": 2012, "title": "t",
             "reason": "book review (PDC reclassified: missing+short(<=5pp))"},
        ])
        wj(os.path.join(td, "data/raw/checkpoints/pc/excluded.jsonl"), [
            {"doi": "10.1/pc1", "year": 2009, "title": "t",
             "reason": "book review (pdcnet source-confirmed: Item_Data_Type=Book Review)"},
            {"doi": "10.1/pc2", "year": 2004, "title": "t", "reason": "announcement"},
        ])
        wj(os.path.join(td, "data/raw/pc_recover_results.jsonl"), [
            {"item_id": "e1", "doi": "10.1/pc1", "year": 2009,
             "verdict": "review", "abs_len": 812},
            {"item_id": "e2", "doi": "10.1/pcX", "year": 2010,
             "verdict": "review", "abs_len": 0},         # no abstract -> not essay
            {"item_id": "e3", "doi": "10.1/pcY", "year": 2010,
             "verdict": "abstract", "abs_len": 900},     # not a review
        ])
        corpus = {
            "corpus_fp.jsonl": [
                {"item_id": "f1", "doi": "10.1/a", "year": "2008", "abstract": "x"},
                {"item_id": "f2", "doi": "10.1/b", "year": "2009", "abstract": "x"},
                {"item_id": "f3", "doi": "10.1/c", "year": "2004", "abstract": "  "},
            ],
            "fp_backfill.jsonl": [
                {"item_id": "f4", "doi": "10.1/d", "year": "2022", "abstract": ""}],
            "corpus_rs.jsonl": [
                {"item_id": "r1", "doi": "10.1/e", "year": "2005", "abstract": "x"}],
            "corpus_ijpr.jsonl": [
                {"item_id": "i1", "doi": "10.1/f", "year": "2008"}],
            "corpus_sophia.jsonl": [
                {"item_id": "s1", "doi": "10.1/g", "year": "2009", "abstract": "x"}],
            "corpus_pc.jsonl": [
                {"item_id": "p1", "doi": "10.1/h", "year": "2006", "abstract": "x"}],
        }
        for fn, rows in corpus.items():
            wj(os.path.join(td, "data/raw", fn), rows)
        wj(os.path.join(td, "data/raw/pilot_rs2015.jsonl"),
           [{"item_id": f"pr{i}", "doi": f"10.2/{i}"} for i in range(3)])
        wj(os.path.join(td, "data/raw/pilot_ijpr2015.jsonl"),
           [{"item_id": f"pi{i}", "doi": f"10.3/{i}"} for i in range(2)])
        wj(os.path.join(td, "data/raw/gold_anchors.jsonl"),
           [{"item_id": f"A{i:02d}", "doi": f"10.4/{i}"} for i in range(2)])

        out_dir = os.path.join(td, "data/raw/locks")
        written = run(td, out_dir, enforce_expect=False)

        rex = json.load(open(os.path.join(out_dir, "review_exclusions.json")))
        check("review filter keeps 'review' reasons only (3 of 5 rows)",
              rex["count"] == 3
              and {x["doi"] for x in rex["items"]}
              == {"10.1/fp1", "10.1/fp3", "10.1/pc1"})
        check("per-reason decomposition recorded",
              sum(rex["count_by_reason"].values()) == 3)

        ess = json.load(open(os.path.join(out_dir, "review_essays.json")))
        check("essays = review verdict AND abs_len>0 only",
              ess["count"] == 1 and ess["items"][0]["item_id"] == "e1")

        ms = json.load(open(os.path.join(out_dir, "missingness_stratum.json")))
        check("pre-2008 boundary includes 2008, excludes 2009+",
              ms["count"] == 5
              and {x["item_id"] for x in ms["items"]}
              == {"f1", "f3", "r1", "i1", "p1"})
        check("missing flag: absent or whitespace-only abstracts",
              ms["count_missing_abstract"] == 2
              and {x["item_id"] for x in ms["items"] if x["missing_abstract"]}
              == {"f3", "i1"})

        cf = json.load(open(os.path.join(out_dir, "confirmatory_exclusions.json")))
        check("confirmatory union covers pilot+gold with set labels",
              cf["count"] == 7 and cf["count_by_set"]
              == {"gold_anchors": 2, "pilot_ijpr2015": 2, "pilot_rs2015": 3})

        check("all locks carry generation_rule + sources hashes",
              all("generation_rule" in b and b["sources"]
                  for b in (rex, ess, ms, cf)))

        # determinism: byte-identical re-run
        h1 = {k: v["sha256"] for k, v in written.items()}
        written2 = run(td, out_dir, enforce_expect=False)
        h2 = {k: v["sha256"] for k, v in written2.items()}
        check("re-run byte-identical (no timestamps)", h1 == h2)

        # registered-count enforcement fires on the (mismatching) fixture
        import subprocess
        r = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--root", td,
             "--out-dir", out_dir],
            capture_output=True, text=True)
        check("registered-count mismatch dies without writing",
              r.returncode == 5 and "registered-count mismatch" in r.stderr)

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Build the manifest item-12 corpus-lock id lists.")
    ap.add_argument("--root", default=REPO_ROOT,
                    help="repo root holding data/raw (default: this repo)")
    ap.add_argument("--out-dir", help="output dir (default <root>/data/raw/locks)")
    ap.add_argument("--no-expect", action="store_true",
                    help="skip the registered-count enforcement (fixtures only; "
                         "the freeze run MUST enforce)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    out_dir = args.out_dir or os.path.join(args.root, OUT_DIR)
    run(args.root, out_dir, enforce_expect=not args.no_expect)
    return 0


if __name__ == "__main__":
    sys.exit(main())
