#!/usr/bin/env python3
"""determinism_audit.py — determinism audit harness (validation battery arm).

Draws a seed-fixed sample of n items from a sanitized batch, writes it to a
sample JSONL under data/battery/, then runs pipeline/03_code/run_coders.py as
a SUBPROCESS twice on the identical sample, and reports per-dimension
exact-match rates between the two runs.

run_coders.py is never modified. Its outputs are hardwired to
data/coded/<sample-batch>_<coder>.jsonl with skip-existing resume logic, so
this harness separates the two runs purely by file moves:
  - the sample file gets a dedicated basename (det_<batch>_s<seed>), so the
    coded outputs never collide with real coding outputs;
  - any stale det outputs in data/coded are moved aside BEFORE run 1
    (to data/battery/det_stale_<ts>/ — nothing is deleted);
  - after each run, the fresh outputs are MOVED out of data/coded into
    data/battery/det_run1/ or det_run2/, so run 2 starts with no existing
    output file and skip-existing skips nothing.
Note: run_coders itself appends its mandatory batch summary to
data/coded/cost_log.md on every run (append-only audit trail; also in --smoke).

Comparison: joined on item_id; a pair counts only if both runs produced a
valid (non parse_fail) record. Exact-match rates per dimension (d1_step,
d2_direction, d3_strength, d4_type), all-4-dims joint, plus flags (sorted) and
confidence as auxiliary rows. Report JSON: data/battery/det_report_<...>.json.

Usage:
  python3 pipeline/04_battery/determinism_audit.py \
      --batch data/sanitized/pilot_rs2015.jsonl --n 20 --seed 7 [--coders a,b,c]
  python3 pipeline/04_battery/determinism_audit.py --smoke [--coders a,b,c]
      (2 built-in dummy items; real API calls via run_coders subprocess, no
       research item text; battery files under data/battery/smoke_det_*)
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

DIMENSIONS = ("d1_step", "d2_direction", "d3_strength", "d4_type")

# Built-in SYNTHETIC dummies for --smoke (written for this script; not real
# abstracts, not from data/raw|sanitized|coded).
SMOKE_ITEMS = [
    {
        "item_id": "SMOKE-DET-001",
        "text": (
            "This synthetic pipeline-validation abstract argues that newly "
            "fabricated tide-table measurements lend modest support to the claim "
            "that an imaginary archipelago's weather has an external cause rather "
            "than being a brute fact; the invented observational premise is "
            "load-bearing."
        ),
        "text_extra": None,
    },
    {
        "item_id": "SMOKE-DET-002",
        "text": (
            "A second synthetic validation abstract: it surveys made-up replies "
            "to a fictional argument from hedge-maze order to an external "
            "designer, and concludes, purely for testing, that the argument is "
            "question-begging."
        ),
        "text_extra": None,
    },
]


def move_aside(path: str, dest_dir: str):
    if os.path.exists(path):
        os.makedirs(dest_dir, exist_ok=True)
        dst = os.path.join(dest_dir, os.path.basename(path))
        if os.path.exists(dst):
            dst += "." + bc.utcnow().replace(":", "")
        shutil.move(path, dst)
        print(f"  [moved] {path} -> {dst}")


def run_once(run_idx: int, sample_path: str, sample_base: str, coders: list,
             run_dir: str, coded_dir: str) -> None:
    os.makedirs(run_dir, exist_ok=True)
    # anything already in run_dir for this base is from an older audit — keep it aside
    for c in coders:
        move_aside(os.path.join(run_dir, f"{sample_base}_{c}.jsonl"),
                   os.path.join(run_dir, "prev"))
    cmd = [sys.executable, bc.RUN_CODERS_PATH, "--batch", sample_path,
           "--coders", ",".join(coders)]
    print(f"[run {run_idx}] {' '.join(os.path.basename(x) if i == 1 else x for i, x in enumerate(cmd))}")
    proc = subprocess.run(cmd, cwd=bc.REPO_ROOT)
    # move outputs out of data/coded regardless of exit code (best effort),
    # so a partial run never contaminates the next one
    missing = []
    for c in coders:
        src = os.path.join(coded_dir, f"{sample_base}_{c}.jsonl")
        if os.path.exists(src):
            shutil.move(src, os.path.join(run_dir, os.path.basename(src)))
        else:
            missing.append(src)
    if proc.returncode != 0:
        bc.die(f"run {run_idx}: run_coders exited {proc.returncode} "
               f"(partial outputs, if any, are in {run_dir})", 5)
    if missing:
        bc.die(f"run {run_idx}: expected output(s) missing: {missing}", 5)


def load_valid(path: str):
    """-> (valid: {item_id: record}, parse_fail_ids: set)"""
    valid, fails = {}, set()
    if not os.path.exists(path):
        return valid, fails
    for rec in bc.read_jsonl(path):
        iid = rec.get("item_id")
        if not iid:
            continue
        if rec.get("parse_fail"):
            fails.add(iid)
        else:
            valid[iid] = rec
    return valid, fails


def norm_flags(v):
    if v is None:
        return []
    if isinstance(v, str):
        v = [v]
    return sorted(str(x) for x in v)


def compare_coder(run1_path: str, run2_path: str, sample_ids: list) -> dict:
    v1, f1 = load_valid(run1_path)
    v2, f2 = load_valid(run2_path)
    both = [iid for iid in sample_ids if iid in v1 and iid in v2]
    res = {
        "items_sampled": len(sample_ids),
        "both_valid": len(both),
        "parse_fail_run1": sorted(f1),
        "parse_fail_run2": sorted(f2),
        "missing_either_run": [iid for iid in sample_ids if iid not in v1 or iid not in v2],
        "dims": {},
    }
    for dim in DIMENSIONS:
        match = sum(1 for iid in both if v1[iid].get(dim) == v2[iid].get(dim))
        res["dims"][dim] = {"match": match, "total": len(both)}
    all4 = sum(1 for iid in both
               if all(v1[iid].get(d) == v2[iid].get(d) for d in DIMENSIONS))
    res["dims"]["all_4_dims"] = {"match": all4, "total": len(both)}
    res["dims"]["flags_sorted"] = {
        "match": sum(1 for iid in both
                     if norm_flags(v1[iid].get("flags")) == norm_flags(v2[iid].get("flags"))),
        "total": len(both)}
    res["dims"]["confidence"] = {
        "match": sum(1 for iid in both
                     if v1[iid].get("confidence") == v2[iid].get("confidence")),
        "total": len(both)}
    res["mismatched_items"] = sorted(
        iid for iid in both
        if any(v1[iid].get(d) != v2[iid].get(d) for d in DIMENSIONS))
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Determinism audit: run_coders x2 on a fixed sample.")
    ap.add_argument("--batch", help="sanitized JSONL to sample from")
    ap.add_argument("--n", type=int, default=20, help="sample size (default 20)")
    ap.add_argument("--seed", type=int, default=1, help="sampling seed (default 1)")
    ap.add_argument("--coders", default="a,b,c")
    ap.add_argument("--smoke", action="store_true",
                    help="2 built-in dummy items through the full subprocess path")
    args = ap.parse_args(argv)

    coders = bc.parse_families(args.coders)
    bc.ensure_battery_dir()
    m = bc.rc()
    coded_dir = m.CODED_DIR

    if args.smoke:
        sample_items = SMOKE_ITEMS
        sample_base = "smoke_det_dummy"
        run_dirs = [os.path.join(bc.BATTERY_DIR, "smoke_det_run1"),
                    os.path.join(bc.BATTERY_DIR, "smoke_det_run2")]
        report_path = os.path.join(bc.BATTERY_DIR, "smoke_det_report.json")
    else:
        if not args.batch:
            bc.die("--batch is required unless --smoke is given", 2)
        batch_path = m.resolve_path(args.batch)
        if not os.path.exists(batch_path):
            bc.die(f"batch file not found: {batch_path}", 2)
        items = bc.read_jsonl(batch_path)
        if not items:
            bc.die("batch is empty", 4)
        n = min(args.n, len(items))
        if n < args.n:
            print(f"[warn] batch has only {len(items)} item(s); sampling all of them",
                  file=sys.stderr)
        sample_items = random.Random(args.seed).sample(items, n)
        sample_base = f"det_{bc.batch_tag(batch_path)}_s{args.seed}"
        run_dirs = [os.path.join(bc.BATTERY_DIR, "det_run1"),
                    os.path.join(bc.BATTERY_DIR, "det_run2")]
        report_path = os.path.join(bc.BATTERY_DIR, f"det_report_{sample_base}.json")

    sample_path = os.path.join(bc.BATTERY_DIR, f"{sample_base}.jsonl")
    with open(sample_path, "w", encoding="utf-8") as f:
        for it in sample_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    sample_ids = [it["item_id"] for it in sample_items]
    print(f"[det] sample: {len(sample_ids)} item(s) (seed={args.seed}) -> {sample_path}")

    # stale det outputs in data/coded would be silently skip-resumed — move aside
    stale_dir = os.path.join(bc.BATTERY_DIR, f"det_stale_{bc.utcnow().replace(':', '')}")
    for c in coders:
        move_aside(os.path.join(coded_dir, f"{sample_base}_{c}.jsonl"), stale_dir)

    for run_idx, run_dir in enumerate(run_dirs, 1):
        run_once(run_idx, sample_path, sample_base, coders, run_dir, coded_dir)

    report = {
        "generated_at": bc.utcnow(),
        "sample_batch": sample_base,
        "sample_path": sample_path,
        "seed": args.seed,
        "n": len(sample_ids),
        "coders": {},
        "run_dirs": run_dirs,
        "note": ("exact-match rates between two identical run_coders invocations; "
                 "pairs counted only when both runs yielded a valid record"),
    }
    print(f"\n[det] determinism report ({len(sample_ids)} sampled item(s)):")
    for c in coders:
        p1 = os.path.join(run_dirs[0], f"{sample_base}_{c}.jsonl")
        p2 = os.path.join(run_dirs[1], f"{sample_base}_{c}.jsonl")
        res = compare_coder(p1, p2, sample_ids)
        report["coders"][c] = res
        print(f"  coder {c}: both_valid={res['both_valid']}/{res['items_sampled']} "
              f"parse_fail r1={len(res['parse_fail_run1'])} r2={len(res['parse_fail_run2'])}")
        for dim, d in res["dims"].items():
            print(f"    {dim:<14} {d['match']}/{d['total']}  {bc.pct(d['match'], d['total'])}")
        if res["mismatched_items"]:
            print(f"    mismatched item_ids: {', '.join(res['mismatched_items'])}")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[det] report written -> {report_path}")
    print("[det] note: run_coders appended its usual batch summaries to "
          "data/coded/cost_log.md (append-only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
