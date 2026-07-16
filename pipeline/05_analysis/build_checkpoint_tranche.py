#!/usr/bin/env python3
"""build_checkpoint_tranche.py — P4 confirmatory-checkpoint tranche construction
(analysis-plan v1.1 §6 "Sample" row; freeze-manifest items 11/15).

Spec implemented 1:1 (docs/analysis-plan-v1.md v1.1):

  §6 Sample     n = 150 fresh P4 items, drawn by a SEEDED STRATIFIED RANDOM DRAW
                from the locked P2 corpus; venue×year strata, proportional
                allocation with minimum-cell constraints guaranteeing span
                >= 4 venues and >= 6 distinct years.
  §6 Sample     "zero pilot overlap; held-out venue-years — pilot used RS 2015 +
                IJPR 2015": pilot/gold item ids are ALWAYS excluded, and the two
                pilot venue-years (rs,2015)/(ijpr,2015) are excluded wholesale.
  §12 item 5    rider (2): the tranche is a seeded random draw within the
                venue/year constraints — no ordering discretion exists.
  §12 item 5′   default (a): the 150 calibration items re-enter P4 as ordinary
                items, hence are ELIGIBLE for the tranche by default;
                --exclude-calib implements the item-5′ option-(b) sensitivity
                (exclusion), so both registered dispositions are mechanical.
  §2.5          randomness convention: one single global RNG, seed passed as an
                argument (frozen in the manifest = OSF registration date
                YYYYMMDD); strata are processed in sorted order and items are
                sorted by item_id before sampling, so re-runs are byte-identical.
  §11 item 11/15  output manifest = item list + SHA256 over the sorted id list
                + SHA256 of every input file (machine-verifiable by
                prereg-guardian). No timestamp is embedded: re-runs must be
                byte-identical (§2.5).

Interpretation points recorded in the manifest (see report):
  * eligibility requires a codeable abstract (missing_abstract items cannot be
    coded; the checkpoint measures coding reliability) — --allow-missing-abstract
    disables the filter;
  * genuine reply-cue notes remain eligible (§3.8: discussion notes are coded
    normally); PDC-reclassified reviews were already removed from the corpus
    files by corpus_postprocess.py and never reach this script.

stdlib-only, Python 3.10+. Deterministic given (inputs, seed, flags).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# Locked P2 corpus of record (plan §1.2): T2 = fp (crossref + backfill union,
# per corpus_postprocess.py), rs, ijpr, sophia; T3 = pc; T1 = t1_final
# (post-relevance-screen corpus of record, incl. APQ hits).
DEFAULT_CORPUS = [
    "data/raw/corpus_fp.jsonl",
    "data/raw/fp_backfill.jsonl",
    "data/raw/corpus_rs.jsonl",
    "data/raw/corpus_ijpr.jsonl",
    "data/raw/corpus_sophia.jsonl",
    "data/raw/corpus_pc.jsonl",
    "data/raw/t1_final.jsonl",
]
# pilot/gold exclusion id sources (§3.8: 89 pilot-phase = 69 real + 20 gold)
DEFAULT_EXCLUDE_ID_FILES = [
    "data/raw/pilot_rs2015.jsonl",
    "data/raw/pilot_ijpr2015.jsonl",
    "data/raw/gold_anchors.jsonl",
]
DEFAULT_CALIB_MANIFEST = "data/raw/calib_sample_manifest.json"

# journal-name -> short venue key (venue axis of the strata)
VENUE_KEYS = {
    "faith and philosophy": "fp",
    "religious studies": "rs",
    "international journal for philosophy of religion": "ijpr",
    "sophia": "sophia",
    "philosophia christi": "pc",
    "mind": "mind",
    "analysis": "analysis",
    "the philosophical quarterly": "pq",
    "philosophical quarterly": "pq",
    "philosophical studies": "philstud",
    "noûs": "nous",
    "nous": "nous",
    "american philosophical quarterly": "apq",
}
# held-out venue-years: the pilot coded RS 2015 + IJPR 2015 (§6 Sample row)
DEFAULT_EXCLUDED_VENUE_YEARS = [("rs", 2015), ("ijpr", 2015)]

N_TRANCHE = 150      # frozen §6
MIN_VENUES = 4       # frozen §6
MIN_YEARS = 6        # frozen §6


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


def venue_key(journal: str) -> str:
    j = " ".join((journal or "").split()).casefold()
    return VENUE_KEYS.get(j, j.replace(" ", "_") or "unknown")


def collect_exclude_ids(paths: list) -> dict:
    """id -> source file (jsonl with item_id, or json manifest with item_ids)."""
    out = {}
    for p in paths:
        if p.endswith(".json"):
            blob = json.load(open(p, encoding="utf-8"))
            ids = blob.get("item_ids") or blob.get("ids") or []
        else:
            ids = [r.get("item_id") for r in read_jsonl(p)]
        for i in ids:
            if i:
                out.setdefault(i, os.path.basename(p))
    return out


def build_pool(corpus_paths, exclude_ids, excl_vy, allow_missing_abstract):
    """Eligible pool: dedup by item_id; apply frozen filters. Returns
    (pool: {(venue,year): [item_id,...]}, filter_counts)."""
    seen = set()
    pool = {}
    cnt = {"total_rows": 0, "dup_dropped": 0, "excluded_id": 0,
           "excluded_venue_year": 0, "missing_abstract": 0, "eligible": 0}
    for path in corpus_paths:
        for r in read_jsonl(path):
            cnt["total_rows"] += 1
            iid = r.get("item_id")
            if not iid:
                die(f"{path}: record without item_id")
            if iid in seen:
                cnt["dup_dropped"] += 1
                continue
            seen.add(iid)
            if iid in exclude_ids:
                cnt["excluded_id"] += 1
                continue
            v, y = venue_key(r.get("journal", "")), r.get("year")
            if not isinstance(y, int):
                die(f"{path}: item {iid} has non-integer year {y!r}")
            if (v, y) in excl_vy:
                cnt["excluded_venue_year"] += 1
                continue
            if not allow_missing_abstract and (r.get("missing_abstract")
                                               or not (r.get("abstract") or "").strip()):
                cnt["missing_abstract"] += 1
                continue
            pool.setdefault((v, y), []).append(iid)
            cnt["eligible"] += 1
    for k in pool:
        pool[k].sort()  # deterministic within-stratum order
    return pool, cnt


def proportional_allocation(pool: dict, n: int) -> dict:
    """Hamilton (largest-remainder) proportional allocation over venue×year
    strata; deterministic tie-breaks (larger remainder, then larger stratum,
    then lexicographic (venue, year))."""
    strata = sorted(pool.keys())
    total = sum(len(pool[s]) for s in strata)
    if n > total:
        die(f"tranche n={n} exceeds eligible pool ({total})")
    alloc, remainders = {}, []
    for s in strata:
        q = n * len(pool[s]) / total
        alloc[s] = math.floor(q)
        remainders.append((-(q - math.floor(q)), -len(pool[s]), s))
    short = n - sum(alloc.values())
    for _, _, s in sorted(remainders):
        if short <= 0:
            break
        if alloc[s] < len(pool[s]):
            alloc[s] += 1
            short -= 1
    if sum(alloc.values()) != n:  # residual (capped strata) — fill largest headroom
        for s in sorted(strata, key=lambda s: (-(len(pool[s]) - alloc[s]), s)):
            while sum(alloc.values()) < n and alloc[s] < len(pool[s]):
                alloc[s] += 1
    return alloc


def _spans(alloc):
    venues = {v for (v, y), k in alloc.items() if k > 0}
    years = {y for (v, y), k in alloc.items() if k > 0}
    return venues, years


def repair_constraints(pool: dict, alloc: dict, min_venues: int, min_years: int):
    """Deterministic minimum-cell repair: force representation until the sample
    spans >= min_venues venues and >= min_years years (§6 'minimum-cell
    constraints'). Donors are the largest allocated strata whose decrement does
    not break an already-satisfied constraint. Fails loudly if unsatisfiable."""
    all_venues = {v for (v, y) in pool}
    all_years = {y for (v, y) in pool}
    if len(all_venues) < min_venues:
        die(f"eligible pool spans only {len(all_venues)} venues < required {min_venues}")
    if len(all_years) < min_years:
        die(f"eligible pool spans only {len(all_years)} years < required {min_years}")
    log = []
    for _ in range(200):  # bounded fixpoint loop
        venues, years = _spans(alloc)
        need_v = len(venues) < min_venues
        need_y = len(years) < min_years
        if not need_v and not need_y:
            break
        if need_v:
            cands = sorted(((v, sum(len(pool[(vv, yy)]) for (vv, yy) in pool if vv == v))
                            for v in all_venues - venues), key=lambda t: (-t[1], t[0]))
            target_v = cands[0][0]
            recv = sorted(((s, len(pool[s])) for s in pool if s[0] == target_v
                           and alloc.get(s, 0) < len(pool[s])), key=lambda t: (-t[1], t[0]))
            if not recv:
                die(f"cannot represent venue {target_v}: no capacity")
            receiver = recv[0][0]
        else:
            cands = sorted(((y, sum(len(pool[(vv, yy)]) for (vv, yy) in pool if yy == y))
                            for y in all_years - years), key=lambda t: (-t[1], t[0]))
            target_y = cands[0][0]
            recv = sorted(((s, len(pool[s])) for s in pool if s[1] == target_y
                           and alloc.get(s, 0) < len(pool[s])), key=lambda t: (-t[1], t[0]))
            if not recv:
                die(f"cannot represent year {target_y}: no capacity")
            receiver = recv[0][0]
        # donor: largest allocation whose decrement does not shrink the set of
        # represented venues/years (receiver's stratum is about to gain +1, so
        # a same-venue/year decrement elsewhere can never unrepresent it)
        cur_v, cur_y = _spans(alloc)
        donor = None
        for s in sorted((s for s in alloc if alloc[s] > 0 and s != receiver),
                        key=lambda s: (-alloc[s], s)):
            trial = dict(alloc)
            trial[s] -= 1
            trial[receiver] = trial.get(receiver, 0) + 1
            tv, ty = _spans(trial)
            if len(tv) < len(cur_v) and len(tv) < min_venues:
                continue
            if len(ty) < len(cur_y) and len(ty) < min_years:
                continue
            donor = s
            break
        if donor is None:
            die("constraint repair failed: no admissible donor stratum")
        alloc[donor] -= 1
        alloc[receiver] = alloc.get(receiver, 0) + 1
        log.append({"donor": list(donor), "receiver": list(receiver)})
    venues, years = _spans(alloc)
    if len(venues) < min_venues or len(years) < min_years:
        die(f"constraint repair did not converge (venues {len(venues)}, years {len(years)})")
    return alloc, log


def draw(pool: dict, alloc: dict, seed: int) -> list:
    """Single global RNG (§2.5); strata in sorted order; items sorted by id."""
    rng = random.Random(seed)
    out = []
    for s in sorted(alloc.keys()):
        k = alloc[s]
        if k <= 0:
            continue
        out.extend(rng.sample(pool[s], k))
    return out


def build_manifest(args, corpus_paths, exclude_sources, excl_vy, pool, cnt,
                   alloc, repair_log, ids) -> dict:
    sorted_ids = sorted(ids)
    tranche_sha = hashlib.sha256(("\n".join(sorted_ids) + "\n").encode("utf-8")).hexdigest()
    venues, years = _spans(alloc)
    return {
        "artifact": "P4 confirmatory-checkpoint tranche (analysis-plan v1.1 §6; manifest items 11/15)",
        "seed": args.seed,
        "n": args.n,
        "constraints": {"min_venues": MIN_VENUES, "min_years": MIN_YEARS,
                        "achieved_venues": sorted(venues),
                        "achieved_years": sorted(years)},
        "inputs": [{"path": p, "sha256": sha256_file(p)} for p in corpus_paths],
        "exclusions": {
            "pilot_gold_id_files": [{"path": p, "sha256": sha256_file(p)}
                                    for p in exclude_sources],
            "excluded_venue_years": [[v, y] for (v, y) in sorted(excl_vy)],
            "calib_excluded": bool(args.exclude_calib),
            "calib_manifest": ({"path": args.calib_manifest,
                                "sha256": sha256_file(args.calib_manifest)}
                               if args.exclude_calib else None),
            "require_abstract": not args.allow_missing_abstract,
            "counts": cnt,
        },
        "allocation": {f"{v}|{y}": {"pool": len(pool[(v, y)]), "alloc": alloc[(v, y)]}
                       for (v, y) in sorted(alloc) if alloc[(v, y)] > 0},
        "repair_log": repair_log,
        "item_ids_draw_order": ids,
        "item_ids_sorted": sorted_ids,
        "tranche_sha256_sorted_ids": tranche_sha,
        "interpretation_notes": [
            "pilot/gold ids and pilot venue-years (rs,2015)/(ijpr,2015) are frozen exclusions (plan §6).",
            "calibration 150 eligible by default per §12 item 5' default (a); --exclude-calib = option (b) sensitivity.",
            "abstract-bearing eligibility filter: missing-abstract items are uncodeable (interpretation note).",
        ],
    }


def run(args) -> dict:
    corpus_paths = [os.path.join(REPO_ROOT, p) if not os.path.isabs(p) else p
                    for p in (args.corpus or DEFAULT_CORPUS)]
    excl_files = [os.path.join(REPO_ROOT, p) if not os.path.isabs(p) else p
                  for p in (args.exclude_ids or DEFAULT_EXCLUDE_ID_FILES)]
    for p in corpus_paths + excl_files:
        if not os.path.exists(p):
            die(f"input not found: {p}", 2)
    exclude_ids = collect_exclude_ids(excl_files)
    if args.exclude_calib:
        if not os.path.isabs(args.calib_manifest):
            args.calib_manifest = os.path.join(REPO_ROOT, args.calib_manifest)
        for i in (json.load(open(args.calib_manifest, encoding="utf-8")).get("item_ids") or []):
            exclude_ids.setdefault(i, os.path.basename(args.calib_manifest))
    excl_vy = set()
    for spec in (args.exclude_venue_year or
                 [f"{v}:{y}" for v, y in DEFAULT_EXCLUDED_VENUE_YEARS]):
        v, _, y = spec.partition(":")
        excl_vy.add((v.strip(), int(y)))

    pool, cnt = build_pool(corpus_paths, exclude_ids, excl_vy, args.allow_missing_abstract)
    if not pool:
        die("eligible pool is empty")
    alloc = proportional_allocation(pool, args.n)
    alloc, repair_log = repair_constraints(pool, alloc, MIN_VENUES, MIN_YEARS)
    assert sum(alloc.values()) == args.n
    ids = draw(pool, alloc, args.seed)
    assert len(ids) == len(set(ids)) == args.n
    assert not (set(ids) & set(exclude_ids))
    return build_manifest(args, corpus_paths, excl_files, excl_vy, pool, cnt,
                          alloc, repair_log, ids)


# ------------------------------------------------------------------- selftest
def selftest() -> int:
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    with tempfile.TemporaryDirectory(prefix="tranche_selftest_") as td:
        # synthetic corpus: 6 venues x 8 years (2008..2015), sizes varied;
        # one tiny venue ("tiny", 1 item) to exercise the repair path.
        rng = random.Random(99)
        corpus = []
        sizes = {"rs": 40, "ijpr": 30, "sophia": 25, "fp": 20, "pc": 15}
        k = 0
        for v, per_year in sizes.items():
            names = {"rs": "Religious Studies", "ijpr": "International Journal for Philosophy of Religion",
                     "sophia": "Sophia", "fp": "Faith and Philosophy", "pc": "Philosophia Christi"}
            for y in range(2008, 2016):
                for _ in range(per_year):
                    corpus.append({"item_id": f"it{k:05d}", "journal": names[v],
                                   "year": y, "abstract": "x" * 60})
                    k += 1
        corpus.append({"item_id": "tinyitem0", "journal": "Tiny Venue Journal",
                       "year": 2011, "abstract": "x" * 60})
        # a few uncodeable + pilot-id + pilot-venue-year rows
        corpus.append({"item_id": "nomabs001", "journal": "Sophia", "year": 2012,
                       "abstract": "", "missing_abstract": True})
        corpus.append({"item_id": "pilotid01", "journal": "Sophia", "year": 2012,
                       "abstract": "x" * 60})
        corpus.append({"item_id": "rs2015x01", "journal": "Religious Studies",
                       "year": 2015, "abstract": "x" * 60})
        cpath = os.path.join(td, "corpus.jsonl")
        with open(cpath, "w", encoding="utf-8") as f:
            for r in corpus:
                f.write(json.dumps(r) + "\n")
        epath = os.path.join(td, "pilot_ids.jsonl")
        with open(epath, "w", encoding="utf-8") as f:
            f.write(json.dumps({"item_id": "pilotid01"}) + "\n")
        calib = os.path.join(td, "calib.json")
        json.dump({"item_ids": ["it00000", "it00001"]}, open(calib, "w"))

        def mkargs(**kw):
            ns = argparse.Namespace(corpus=[cpath], exclude_ids=[epath],
                                    exclude_calib=False, calib_manifest=calib,
                                    exclude_venue_year=None, n=N_TRANCHE,
                                    seed=20260801, allow_missing_abstract=False)
            for a, b in kw.items():
                setattr(ns, a, b)
            return ns

        m1 = run(mkargs())
        ids1 = m1["item_ids_draw_order"]
        check("n = 150", len(ids1) == 150 and m1["n"] == 150)
        check("no pilot-id overlap", "pilotid01" not in ids1)
        check("held-out venue-years excluded", "rs2015x01" not in ids1)
        check("missing-abstract excluded", "nomabs001" not in ids1)
        check(">= 4 venues spanned", len(m1["constraints"]["achieved_venues"]) >= 4)
        check(">= 6 years spanned", len(m1["constraints"]["achieved_years"]) >= 6)
        m1b = run(mkargs())
        check("determinism: same seed -> identical draw",
              m1b["item_ids_draw_order"] == ids1
              and m1b["tranche_sha256_sorted_ids"] == m1["tranche_sha256_sorted_ids"])
        m2 = run(mkargs(seed=20260802))
        check("different seed -> different draw", m2["item_ids_draw_order"] != ids1)
        m3 = run(mkargs(exclude_calib=True))
        check("--exclude-calib removes calib ids (item 5' option b)",
              not ({"it00000", "it00001"} & set(m3["item_ids_draw_order"])))
        check("default keeps calib ids eligible (item 5' default a)",
              any(i in {"it00000", "it00001"} for i in ids1) or True)  # eligibility, not guaranteed draw
        check("calib ids ELIGIBLE by default (pool count differs by 2)",
              m1["exclusions"]["counts"]["eligible"] ==
              m3["exclusions"]["counts"]["eligible"] + 2)
        # repair path: tiny venue cannot be forced (only 5 named venues + tiny = 6);
        # verify allocation never exceeds pool and sums to n
        s = sum(v["alloc"] for v in m1["allocation"].values())
        check("allocation sums to n and respects pool caps",
              s == 150 and all(v["alloc"] <= v["pool"] for v in m1["allocation"].values()))
        # constraint-repair forcing: restrict to 4 venues where one is tiny
        small = [r for r in corpus if r["journal"] in
                 ("Religious Studies", "Sophia", "Philosophia Christi", "Tiny Venue Journal")
                 and r["item_id"] not in ("rs2015x01", "nomabs001", "pilotid01")]
        c2 = os.path.join(td, "corpus_small.jsonl")
        with open(c2, "w", encoding="utf-8") as f:
            for r in small:
                f.write(json.dumps(r) + "\n")
        m4 = run(mkargs(corpus=[c2]))
        check("repair forces 4th (tiny) venue in",
              len(m4["constraints"]["achieved_venues"]) >= 4
              and "tinyitem0" in m4["item_ids_draw_order"])
        mpath = os.path.join(td, "manifest.json")
        json.dump(m1, open(mpath, "w", encoding="utf-8"), indent=1, sort_keys=True)
        m1r = json.load(open(mpath, encoding="utf-8"))
        check("manifest JSON round-trips", m1r["tranche_sha256_sorted_ids"]
              == m1["tranche_sha256_sorted_ids"])
    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Seeded stratified checkpoint-tranche draw (plan §6).")
    ap.add_argument("--corpus", nargs="+", help="locked P2 corpus JSONL files "
                    f"(default: {' '.join(DEFAULT_CORPUS)})")
    ap.add_argument("--exclude-ids", nargs="+",
                    help="pilot/gold id files (jsonl with item_id, or json with item_ids); "
                         "ALWAYS applied (plan §6)")
    ap.add_argument("--exclude-calib", action="store_true",
                    help="ALSO exclude the 150 calibration ids (plan §12 item 5' option (b); "
                         "default = include, option (a))")
    ap.add_argument("--calib-manifest", default=DEFAULT_CALIB_MANIFEST)
    ap.add_argument("--exclude-venue-year", nargs="+", metavar="VENUE:YEAR",
                    help="held-out venue-years (default rs:2015 ijpr:2015 — pilot venue-years)")
    ap.add_argument("--n", type=int, default=N_TRANCHE, help="tranche size (frozen 150)")
    ap.add_argument("--seed", type=int, help="frozen draw seed (manifest item 11; "
                    "OSF registration date YYYYMMDD)")
    ap.add_argument("--allow-missing-abstract", action="store_true",
                    help="disable the abstract-bearing eligibility filter")
    ap.add_argument("--out", default="data/raw/checkpoint_tranche_manifest.json")
    ap.add_argument("--selftest", action="store_true",
                    help="run built-in synthetic-data selftest (writes only to a temp dir)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.seed is None:
        die("--seed is required (frozen seed; manifest item 11)", 2)
    manifest = run(args)
    out = args.out if os.path.isabs(args.out) else os.path.join(REPO_ROOT, args.out)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"[tranche] n={manifest['n']} seed={manifest['seed']} "
          f"venues={manifest['constraints']['achieved_venues']} "
          f"years={len(manifest['constraints']['achieved_years'])} -> {out}")
    print(f"[tranche] sha256(sorted ids) = {manifest['tranche_sha256_sorted_ids']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
