#!/usr/bin/env python3
"""checkpoint_stats.py — P4 confirmatory-checkpoint dual statistic + sub-audits.

Implements, 1:1, the FROZEN definitions of analysis-plan v1.1 (this script is
post-freeze operational tooling — the *definitions* are frozen in the plan;
this implementation's hash is recorded in guardian_log at first checkpoint
use, per the §11 item-11 convention for the other analysis scripts):

  §6 Statistic 1 (point)   min pairwise Krippendorff α over {(A,B),(A,C),(B,C)}
                           ≥ .70 on every dimension (D1/D2/D4 nominal; D3
                           nominal ≡ ordinal at 2 levels; NA on D3 = missing).
  §6 Statistic 2 (interval) per dimension, bootstrap the min-pairwise α — the
                           per-dimension minimum over the three pairs
                           recomputed inside every replicate; percentile 95%
                           lower bound ≥ .667. FOUR interval quantities, not
                           twelve. Bootstrap per §2.5: nonparametric
                           percentile, B = 1,000, item-level resampling,
                           single global RNG (seed = OSF registration date
                           YYYYMMDD), one shared draw per replicate
                           (pair-outer/dim-inner computation within it);
                           nearest-rank bounds (sorted[ceil(p·B)-1], p=.025),
                           identical to headline_effects.py's convention.
  §9 B1b                   consolidated run-split rate (run_unstable_dims) per
                           coder per dimension: ≤ 2% floor, 5% alarm.
  §9 B1c (b1c mode)        consolidated exact-match between two full
                           majority-of-3 pipeline re-runs, per dimension per
                           coder, ≥ 95%.
  §6.3                     conditional-agreement diagnostic P(B=C | A≠B) per
                           dimension; watch trigger ≥ .90 with n(A≠B) ≥ 20.

α computation is IMPORTED from the frozen scripts/alpha.py (manifest item 11)
— no reimplementation. Deterministic: no timestamps; identical inputs + seed
reproduce byte-identical reports. stdlib-only, Python 3.10+.

Usage:
  dual: checkpoint_stats.py dual --coded A.jsonl B.jsonl C.jsonl --seed YYYYMMDD
          [--b 1000] [--point-gate 0.70] [--lb-floor 0.667] [--label raw]
          [--out report.json]
  b1c:  checkpoint_stats.py b1c --run1-prefix data/coded/ckpt_b1c_p1
          --run2-prefix data/coded/ckpt_b1c_p2 [--coders a,b,c]
          [--min-match 0.95] [--out report.json]
  self: checkpoint_stats.py selftest
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
import alpha  # noqa: E402  FROZEN α harness (manifest item 11) — imported, never edited

DIMS = alpha.DIMS  # {"d1_step": "nominal", ..., "d3_strength": "ordinal"}
PAIRS = [(0, 1, "AB"), (0, 2, "AC"), (1, 2, "BC")]


def percentile_nearest_rank(sorted_vals, p):
    n = len(sorted_vals)
    idx = max(0, math.ceil(p * n) - 1)
    return sorted_vals[idx]


def get_val(rec, dim):
    """Record value for α purposes: D3 'NA' = missing (pairwise exclusion)."""
    if rec is None:
        return None
    v = rec.get(dim)
    if DIMS[dim] == "ordinal" and v == "NA":
        return None
    return v


def d3_order(coders):
    seen = {r.get("d3_strength") for c in coders for r in c.values()} - {None, "NA"}
    return alpha.D3_ORDER if seen <= set(alpha.D3_ORDER) else alpha.CS_ORDER


def pair_alpha(triples, i, j, metric, order):
    units = [[t[i], t[j]] for t in triples]
    return alpha.krippendorff(units, metric, order)


def dual_stats(coders, seed, b=1000, point_gate=0.70, lb_floor=0.667, label="raw"):
    """coders: [dict_a, dict_b, dict_c] of {item_id: record}. Returns report dict."""
    id_sets = [set(c) for c in coders]
    ids = sorted(set.union(*id_sets))
    id_mismatch = {f"coder_{'abc'[k]}_missing": sorted(set(ids) - id_sets[k])
                   for k in range(3) if set(ids) - id_sets[k]}
    order3 = d3_order(coders)
    # per-dim triples over the fixed universe (None = missing / D3-NA)
    triples = {dim: [tuple(get_val(c.get(i), dim) for c in coders) for i in ids]
               for dim in DIMS}

    # ---- Statistic 1: point min-pairwise per dimension
    point = {}
    for dim, metric in DIMS.items():
        order = order3 if dim == "d3_strength" else None
        per_pair = {}
        for i, j, name in PAIRS:
            a = pair_alpha(triples[dim], i, j, metric, order)
            per_pair[name] = a
        vals = [v for v in per_pair.values() if v is not None]
        point[dim] = {
            "pairwise": per_pair,
            "min": min(vals) if len(vals) == 3 else None,
        }
    stat1_pass = all(p["min"] is not None and p["min"] >= point_gate for p in point.values())

    # ---- Statistic 2: bootstrap min-pairwise per dimension (§2.5 convention)
    rng = random.Random(seed)
    n = len(ids)
    boot = {dim: [] for dim in DIMS}
    degenerate = {dim: 0 for dim in DIMS}
    for _ in range(b):
        idx = [rng.randrange(n) for _ in range(n)]  # ONE shared draw per replicate
        for dim, metric in DIMS.items():
            order = order3 if dim == "d3_strength" else None
            tri = triples[dim]
            mins = []
            for i, j, _name in PAIRS:
                units = [[tri[k][i], tri[k][j]] for k in idx]
                a = alpha.krippendorff(units, metric, order)
                if a is None:
                    mins = None
                    break
                mins.append(a)
            if mins is None:
                degenerate[dim] += 1
            else:
                boot[dim].append(min(mins))
    interval = {}
    for dim in DIMS:
        sv = sorted(boot[dim])
        interval[dim] = {
            "b_effective": len(sv),
            "degenerate_replicates": degenerate[dim],
            "lb95": percentile_nearest_rank(sv, 0.025) if sv else None,
            "median": percentile_nearest_rank(sv, 0.5) if sv else None,
            "ub95": percentile_nearest_rank(sv, 0.975) if sv else None,
        }
    stat2_pass = all(iv["lb95"] is not None and iv["lb95"] >= lb_floor for iv in interval.values())

    # ---- §6.3 conditional-agreement diagnostic P(B=C | A≠B)
    condagree = {}
    for dim in DIMS:
        n_cond = n_bc = 0
        for c_a, c_b, c_c in ((coders[0].get(i), coders[1].get(i), coders[2].get(i)) for i in ids):
            if c_a is None or c_b is None or c_c is None:
                continue
            va, vb, vc = c_a.get(dim), c_b.get(dim), c_c.get(dim)
            if va is None or vb is None or vc is None:
                continue
            if va != vb:
                n_cond += 1
                if vb == vc:
                    n_bc += 1
        p = (n_bc / n_cond) if n_cond else None
        condagree[dim] = {
            "p_bc_given_a_neq_b": p,
            "n_a_neq_b": n_cond,
            "watch_trigger": bool(p is not None and n_cond >= 20 and p >= 0.90),
        }

    # ---- §9 B1b consolidated run-split rate per coder per dimension
    b1b = {}
    for k, cname in enumerate("abc"):
        recs = coders[k]
        total = len(recs)
        rates = {}
        for dim in DIMS:
            m = sum(1 for r in recs.values() if dim in (r.get("run_unstable_dims") or []))
            rate = m / total if total else None
            rates[dim] = {
                "rate": rate,
                "n_unstable": m,
                "over_floor_2pct": bool(rate is not None and rate > 0.02),
                "alarm_5pct": bool(rate is not None and rate > 0.05),
            }
        b1b[cname] = rates
    b1b_ok = not any(d["over_floor_2pct"] for c in b1b.values() for d in c.values())

    return {
        "artifact": "P4 checkpoint dual statistic (plan §6; §2.5 bootstrap; §6.3; §9 B1b)",
        "arm_label": label,
        "n_items": n,
        "id_mismatch": id_mismatch,
        "seed": seed,
        "b": b,
        "d3_order": order3,
        "statistic1_point": point,
        "statistic1_pass": stat1_pass,
        "point_gate": point_gate,
        "statistic2_interval": interval,
        "statistic2_pass": stat2_pass,
        "lb_floor": lb_floor,
        "dual_pass": bool(stat1_pass and stat2_pass),
        "condagree_6_3": condagree,
        "b1b_run_split": b1b,
        "b1b_all_within_2pct": b1b_ok,
    }


def b1c_stats(run1, run2, coders="abc", min_match=0.95):
    """run1/run2: {coder: {item_id: record}}. Exact-match per dim per coder."""
    out = {"artifact": "B1c consolidated-output determinism (plan §6/§9 B1c)",
           "min_match": min_match, "coders": {}}
    all_ok = True
    for c in coders:
        r1, r2 = run1[c], run2[c]
        common = sorted(set(r1) & set(r2))
        only1, only2 = sorted(set(r1) - set(r2)), sorted(set(r2) - set(r1))
        dims = {}
        for dim in DIMS:
            match = sum(1 for i in common if r1[i].get(dim) == r2[i].get(dim))
            rate = match / len(common) if common else None
            ok = bool(rate is not None and rate >= min_match)
            all_ok &= ok
            dims[dim] = {"exact_match": rate, "n": len(common), "pass": ok}
        out["coders"][c] = {"dims": dims, "n_common": len(common),
                            "only_run1": only1, "only_run2": only2}
    out["b1c_pass"] = all_ok
    return out


def print_dual(rep):
    print(f"=== checkpoint dual statistic — arm: {rep['arm_label']} "
          f"(n={rep['n_items']}, seed={rep['seed']}, B={rep['b']}) ===")
    if rep["id_mismatch"]:
        print(f"  WARNING id mismatch across coders: {rep['id_mismatch']}")
    print(f"{'dim':<14}{'AB':>8}{'AC':>8}{'BC':>8}{'min':>8}{'lb95':>8}{'med':>8}  verdict")
    for dim in DIMS:
        p = rep["statistic1_point"][dim]
        iv = rep["statistic2_interval"][dim]
        f = lambda v: "  n/a " if v is None else f"{v:7.4f}"
        s1 = p["min"] is not None and p["min"] >= rep["point_gate"]
        s2 = iv["lb95"] is not None and iv["lb95"] >= rep["lb_floor"]
        v = "PASS" if (s1 and s2) else ("FAIL-pt" if not s1 else "FAIL-lb")
        print(f"{dim:<14}{f(p['pairwise']['AB'])}{f(p['pairwise']['AC'])}"
              f"{f(p['pairwise']['BC'])}{f(p['min'])}{f(iv['lb95'])}{f(iv['median'])}  {v}")
    print(f"Statistic1 (all min >= {rep['point_gate']}): {'PASS' if rep['statistic1_pass'] else 'FAIL'}")
    print(f"Statistic2 (all lb95 >= {rep['lb_floor']}): {'PASS' if rep['statistic2_pass'] else 'FAIL'}")
    print(f"DUAL: {'PASS' if rep['dual_pass'] else 'FAIL'}")
    print("--- §6.3 P(B=C | A≠B) ---")
    for dim, d in rep["condagree_6_3"].items():
        pv = "n/a" if d["p_bc_given_a_neq_b"] is None else f"{d['p_bc_given_a_neq_b']:.3f}"
        print(f"  {dim:<14}{pv}  n={d['n_a_neq_b']}"
              f"{'  WATCH-TRIGGER' if d['watch_trigger'] else ''}")
    print("--- §9 B1b run-split rate (floor 2%, alarm 5%) ---")
    for c, dims in rep["b1b_run_split"].items():
        cells = "  ".join(
            f"{dim}:{'n/a' if d['rate'] is None else format(d['rate'], '.3f')}"
            f"{'!' if d['over_floor_2pct'] else ''}{'!!' if d['alarm_5pct'] else ''}"
            for dim, d in dims.items())
        print(f"  coder {c}: {cells}")


def print_b1c(rep):
    print(f"=== B1c consolidated determinism (floor {rep['min_match']:.2f}) ===")
    for c, info in rep["coders"].items():
        cells = "  ".join(
            f"{dim}:{'n/a' if d['exact_match'] is None else format(d['exact_match'], '.3f')}"
            f"{'' if d['pass'] else '<FAIL'}" for dim, d in info["dims"].items())
        extra = "" if not (info["only_run1"] or info["only_run2"]) else \
            f"  [id diff: {len(info['only_run1'])}/{len(info['only_run2'])}]"
        print(f"  coder {c} (n={info['n_common']}): {cells}{extra}")
    print(f"B1c: {'PASS' if rep['b1c_pass'] else 'FAIL (k-raise 3->5 + full re-consolidation rule fires)'}")


def selftest():
    def mk(vals):  # vals: {item: (d1,d2,d3,d4)}
        return {i: {"d1_step": v[0], "d2_direction": v[1],
                    "d3_strength": v[2], "d4_type": v[3]} for i, v in vals.items()}

    # T1 nearest-rank convention
    assert percentile_nearest_rank(list(range(1, 1001)), 0.025) == 25
    assert percentile_nearest_rank(list(range(1, 1001)), 0.975) == 975

    # T2 perfect agreement -> point 1.0, lb 1.0, dual PASS
    base = {f"i{k:03d}": ("S1" if k % 2 else "S2", "pro" if k % 3 else "contra",
                          "DEF" if k % 2 else "POS", "alpha" if k % 4 else "beta")
            for k in range(60)}
    a = mk(base)
    rep = dual_stats([a, mk(base), mk(base)], seed=20260717, b=200)
    assert rep["dual_pass"] and rep["statistic1_pass"] and rep["statistic2_pass"]
    for dim in DIMS:
        assert rep["statistic1_point"][dim]["min"] == 1.0
        assert rep["statistic2_interval"][dim]["lb95"] == 1.0

    # T3 injected noise -> alpha in (0,1), lb <= point-min, deterministic under seed
    noisy = dict(base)
    for k in range(0, 30):
        v = base[f"i{k:03d}"]
        noisy[f"i{k:03d}"] = ("S3", v[1], v[2], v[3])  # coder c disagrees on d1
    r1 = dual_stats([a, mk(base), mk(noisy)], seed=20260717, b=200)
    r2 = dual_stats([a, mk(base), mk(noisy)], seed=20260717, b=200)
    r3 = dual_stats([a, mk(base), mk(noisy)], seed=19990101, b=200)
    d1 = r1["statistic1_point"]["d1_step"]
    assert d1["pairwise"]["AB"] == 1.0 and 0 < d1["min"] < 1
    assert json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
    assert r1["statistic2_interval"]["d1_step"]["lb95"] <= d1["min"] + 1e-12
    assert (r3["statistic2_interval"]["d1_step"]["lb95"]
            != r1["statistic2_interval"]["d1_step"]["lb95"])

    # T4 cross-check point pairwise vs frozen alpha.py on the same units
    tri = [tuple(get_val(c.get(i), "d1_step") for c in (a, mk(base), mk(noisy)))
           for i in sorted(base)]
    direct = alpha.krippendorff([[t[0], t[2]] for t in tri], "nominal")
    assert abs(direct - d1["pairwise"]["AC"]) < 1e-12

    # T5 §6.3: B=C whenever A≠B -> p=1.0, trigger (n=30 >= 20)
    ca = r1["condagree_6_3"]["d1_step"]
    assert ca["n_a_neq_b"] == 0  # A agrees with B here; use A-noisy seating instead
    r4 = dual_stats([mk(noisy), mk(base), mk(base)], seed=20260717, b=10)
    ca = r4["condagree_6_3"]["d1_step"]
    assert ca["n_a_neq_b"] == 30 and ca["p_bc_given_a_neq_b"] == 1.0 and ca["watch_trigger"]

    # T6 B1b: 3/60 unstable on d2 for coder a -> 5.0% -> over floor AND at alarm boundary edge
    a_unst = mk(base)
    for k in range(3):
        a_unst[f"i{k:03d}"]["run_unstable_dims"] = ["d2_direction"]
    r5 = dual_stats([a_unst, mk(base), mk(base)], seed=20260717, b=10)
    cell = r5["b1b_run_split"]["a"]["d2_direction"]
    assert cell["n_unstable"] == 3 and cell["over_floor_2pct"] and not cell["alarm_5pct"]
    assert not r5["b1b_all_within_2pct"]

    # T7 D3 'NA' pairwise exclusion feeds None into alpha (not a category)
    na = dict(base)
    na["i000"] = (base["i000"][0], base["i000"][1], "NA", base["i000"][3])
    r6 = dual_stats([mk(na), mk(base), mk(base)], seed=20260717, b=10)
    assert r6["statistic1_point"]["d3_strength"]["min"] == 1.0  # NA excluded, not a mismatch

    # T8 b1c: identical -> 1.0 PASS; 4/50 flipped on d4 -> 0.92 FAIL
    fifty = {f"j{k:02d}": ("S1", "pro", "DEF", "alpha") for k in range(50)}
    p1 = {c: mk(fifty) for c in "abc"}
    p2 = {c: mk(fifty) for c in "abc"}
    rb = b1c_stats(p1, p2)
    assert rb["b1c_pass"]
    flip = mk(fifty)
    for k in range(4):
        flip[f"j{k:02d}"]["d4_type"] = "beta"
    p2b = {"a": flip, "b": mk(fifty), "c": mk(fifty)}
    rb2 = b1c_stats(p1, p2b)
    assert not rb2["b1c_pass"]
    assert abs(rb2["coders"]["a"]["dims"]["d4_type"]["exact_match"] - 0.92) < 1e-12

    print("selftest PASS (T1 nearest-rank, T2 perfect, T3 noise+determinism, "
          "T4 alpha.py cross-check, T5 condagree, T6 B1b, T7 D3-NA, T8 b1c)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    d = sub.add_parser("dual")
    d.add_argument("--coded", nargs=3, required=True, metavar=("A", "B", "C"))
    d.add_argument("--seed", type=int, required=True, help="OSF registration date YYYYMMDD")
    d.add_argument("--b", type=int, default=1000)
    d.add_argument("--point-gate", type=float, default=0.70)
    d.add_argument("--lb-floor", type=float, default=0.667)
    d.add_argument("--label", default="raw")
    d.add_argument("--out")
    c = sub.add_parser("b1c")
    c.add_argument("--run1-prefix", required=True)
    c.add_argument("--run2-prefix", required=True)
    c.add_argument("--coders", default="a,b,c")
    c.add_argument("--min-match", type=float, default=0.95)
    c.add_argument("--out")
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.mode == "selftest":
        return selftest()
    if args.mode == "dual":
        coders = [alpha.load_jsonl(p) for p in args.coded]
        rep = dual_stats(coders, seed=args.seed, b=args.b, point_gate=args.point_gate,
                         lb_floor=args.lb_floor, label=args.label)
        print_dual(rep)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(rep, f, ensure_ascii=False, indent=1, sort_keys=True)
            print(f"[report] -> {args.out}")
        return 0 if rep["dual_pass"] else 1
    if args.mode == "b1c":
        coders = args.coders.split(",")
        run1 = {c: alpha.load_jsonl(f"{args.run1_prefix}_{c}.jsonl") for c in coders}
        run2 = {c: alpha.load_jsonl(f"{args.run2_prefix}_{c}.jsonl") for c in coders}
        rep = b1c_stats(run1, run2, coders=coders, min_match=args.min_match)
        print_b1c(rep)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(rep, f, ensure_ascii=False, indent=1, sort_keys=True)
            print(f"[report] -> {args.out}")
        return 0 if rep["b1c_pass"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
