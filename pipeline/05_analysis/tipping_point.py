#!/usr/bin/env python3
"""tipping_point.py — frozen tipping-point searches (analysis-plan v1.1;
freeze-manifest item 11: "the §4.2 tipping-point search ... script").

Two subcommands, both deterministic, stdlib-only:

`missing` — §4.2(b) missingness tipping points TP_pos / TP_free:
  For a hypothesis, the MINIMUM number of missing-stratum items that overturns
  the decision rule (moves the 95% CI to include 1, or — H1 only — the point OR
  below the registered magnitude 3) when allocated adversarially over ALL free
  margins: direction, D4 type, strength (POS and DEF), and tier for H2 —
  subject only to each missing item's known venue fixing its venue/tier row
  (hence the per-tier pools --missing-t12/--missing-t3; H1 imputation is
  restricted to the missing stratum's T1∪T2 portion, §4.2(b) last line).
  The search is the plan's own frozen mechanism: GREEDY adversarial cell
  allocation ("the search is mechanical (greedy adversarial cell allocation;
  stdlib script, hash in manifest item 11)"). Each statistic is read against
  its 95% UCL comparator (Wilson upper bounds):
    TP_pos  vs  N_missing_relevant × UCL[P(S)] × UCL[P(POS|S)]
    TP_free vs  N_missing_relevant × UCL[P(S)]
  (the plan prints the whole-stratum 462 in the formula; the script
  parameterizes N_missing_relevant = the tier pools actually admissible for
  the hypothesis — T1∪T2 portion for H1, both portions for H2 — recorded in
  the output as an interpretation note). Margins pass (§4.2 claim consequence
  (iii)) iff TP exceeds its comparator; a never-overturned search passes
  trivially and is reported as such.
  For H1, DEF/non-chain allocations cannot enter DEN-H1 (§3.1 condition 4), so
  they are inert; a MINIMAL adversary never spends an item on them and
  TP_free(H1) = TP_pos(H1) as a count — only the comparator differs.

`flips` — §5.2 first bullet (published diagnostic): for each headline effect
  (OR_H1, OR_pro, OR_contra, ROR), the minimum number (and identity pattern)
  of 2-1 adjudicated items in analysis-critical cells whose flip moves the
  95% CI to include 1; reported as a count and as a fraction of all 2-1
  resolutions in those cells. Candidates come from a JSON file produced by the
  adjudication pipeline: each candidate = {"id", "from": <cell-key>, "to":
  <cell-key or null>} — null "to" = the flip removes the item from the
  denominator (§3.4 membership re-evaluation). Deterministic greedy: at each
  step flip the candidate that minimizes the include-1 margin; ties break by
  canonical candidate order (id).

Statistics (plan §2.2/§2.3/§2.5, implemented 1:1):
  OR_H1 = [n(pro,α)·n(contra,β∪γ)] / [n(pro,β∪γ)·n(contra,α)], Woolf 95% CI.
  OR_pro / OR_contra = tier-conditional POS odds ratios from the 2×2×2 table;
  ROR = OR_pro/OR_contra with Woolf on the three-way term
  (SE = sqrt of the sum of reciprocals over all 8 cells).
  Haldane–Anscombe +0.5 on all cells of the estimate's table if any cell = 0;
  raw and corrected both carried; `haldane_used` flagged (a confirmatory
  verdict may not rest on a Haldane-corrected analysis-critical cell — §2.5;
  this script only reports the flag, it assigns no verdicts).
  Decision rules: H1 met iff LCL > 1 AND point OR >= 3 (§2.2);
  H2 met iff LCL(OR_pro) > 1 AND LCL(ROR) > 1 (§2.3), or LCL(OR_pro) > 1 alone
  under --h2-scope orpro (§12 item 16 re-scope).

Cell-table JSON keys:
  H1 (4): pro_a, pro_bg, contra_a, contra_bg          (a = alpha, bg = beta∪gamma)
  H2 (8): {t3,t12}_{pro,contra}_{pos,def}
Fractional (expected) counts are admissible (§4.2(c) fractional allocation).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from statistics import NormalDist

Z95 = NormalDist().inv_cdf(0.975)

H1_CELLS = ["pro_a", "pro_bg", "contra_a", "contra_bg"]
H2_CELLS = [f"{t}_{d}_{s}" for t in ("t3", "t12") for d in ("pro", "contra")
            for s in ("pos", "def")]


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


# ------------------------------------------------------------ core statistics
def _haldane(vals):
    if any(v == 0 for v in vals):
        return [v + 0.5 for v in vals], True
    return list(vals), False


def or_ci(a, b, c, d):
    """Odds ratio a·d/(b·c) with Woolf (logit) 95% CI; Haldane +0.5 on all four
    cells if any cell = 0 (plan §2.2/§2.5). Returns raw and corrected."""
    raw = (a * d / (b * c)) if b * c > 0 else (math.inf if a * d > 0 else math.nan)
    (a2, b2, c2, d2), hald = _haldane([a, b, c, d])
    pt = a2 * d2 / (b2 * c2)
    se = math.sqrt(1 / a2 + 1 / b2 + 1 / c2 + 1 / d2)
    lo, hi = math.log(pt) - Z95 * se, math.log(pt) + Z95 * se
    return {"or": pt, "lcl": math.exp(lo), "ucl": math.exp(hi),
            "raw_or": raw, "haldane_used": hald}


def h1_effect(t):
    return or_ci(t["pro_a"], t["pro_bg"], t["contra_a"], t["contra_bg"])


def h2_effects(t):
    """OR_pro, OR_contra (Woolf per 2×2) and ROR with Woolf on the three-way
    term: SE(log ROR) = sqrt(Σ 1/n over all 8 cells) (plan §2.3). Haldane is
    applied to the 8-cell table as a whole if any cell = 0 (§2.5)."""
    vals = [t[k] for k in H2_CELLS]
    corr, hald = _haldane(vals)
    tc = dict(zip(H2_CELLS, corr))
    op = or_ci(tc["t3_pro_pos"], tc["t3_pro_def"], tc["t12_pro_pos"], tc["t12_pro_def"])
    oc = or_ci(tc["t3_contra_pos"], tc["t3_contra_def"],
               tc["t12_contra_pos"], tc["t12_contra_def"])
    ror_pt = op["or"] / oc["or"]
    se = math.sqrt(sum(1 / v for v in corr))
    ror = {"or": ror_pt, "lcl": math.exp(math.log(ror_pt) - Z95 * se),
           "ucl": math.exp(math.log(ror_pt) + Z95 * se), "haldane_used": hald}
    for e in (op, oc):
        e["haldane_used"] = e["haldane_used"] or hald
    return {"or_pro": op, "or_contra": oc, "ror": ror, "haldane_used": hald}


def h1_rule(t, magnitude=3.0):
    """§2.2 decision semantics: supported at registered magnitude iff
    LCL > 1 and point OR >= 3. Margin < 0 <=> rule overturned."""
    e = h1_effect(t)
    margin = min(e["lcl"] - 1.0, e["or"] - magnitude)
    return {"met": e["lcl"] > 1.0 and e["or"] >= magnitude, "margin": margin,
            "effect": e}


def h2_rule(t, scope="full"):
    """§2.3 decision semantics: LCL(OR_pro) > 1 AND LCL(ROR) > 1 (scope=full);
    §12 item 16 re-scope: LCL(OR_pro) > 1 only (scope=orpro)."""
    e = h2_effects(t)
    if scope == "orpro":
        margin = e["or_pro"]["lcl"] - 1.0
        met = e["or_pro"]["lcl"] > 1.0
    else:
        margin = min(e["or_pro"]["lcl"] - 1.0, e["ror"]["lcl"] - 1.0)
        met = e["or_pro"]["lcl"] > 1.0 and e["ror"]["lcl"] > 1.0
    return {"met": met, "margin": margin, "effect": e}


def wilson_ucl(k, n):
    """95% Wilson score upper bound (two-sided z)."""
    if n <= 0:
        die("Wilson UCL: n must be positive")
    p = k / n
    z2 = Z95 * Z95
    return (p + z2 / (2 * n) + Z95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) \
        / (1 + z2 / n)


# ------------------------------------------------- §4.2(b) missingness search
def tp_moves(hyp, mode, pools):
    """Admissible adversarial single-item allocations. Each move =
    (pool_key, cell_key). Canonical (sorted) order fixes greedy tie-breaks."""
    moves = []
    if hyp == "h1":
        if pools.get("t12", 0) > 0:
            cells = H1_CELLS  # POS in-chain allocations; DEF is inert for DEN-H1
            moves = [("t12", c) for c in cells]
    else:
        strengths = ("pos",) if mode == "pos" else ("pos", "def")
        for tier in ("t12", "t3"):
            if pools.get(tier, 0) > 0:
                moves += [(tier, f"{tier}_{d}_{s}")
                          for d in ("pro", "contra") for s in strengths]
    return sorted(moves)


def tp_search(hyp, table, pools, mode, scope):
    """Greedy adversarial allocation (frozen mechanism, §4.2(b)). Returns
    (tp_count_or_None, trace). Deterministic: candidate moves evaluated in
    canonical order; strict improvement required to displace the incumbent."""
    rule = (lambda t: h1_rule(t)) if hyp == "h1" else (lambda t: h2_rule(t, scope))
    t = dict(table)
    pools = dict(pools)
    trace = []
    base = rule(t)
    if not base["met"]:
        return 0, [{"note": "decision rule not met at baseline; TP = 0"}]
    count = 0
    while sum(pools.values()) > 0:
        best = None
        for pool, cell in tp_moves(hyp, mode, pools):
            t2 = dict(t)
            t2[cell] = t2.get(cell, 0) + 1
            m = rule(t2)["margin"]
            if best is None or m < best[0]:
                best = (m, pool, cell)
        if best is None:
            break
        _, pool, cell = best
        t[cell] = t.get(cell, 0) + 1
        pools[pool] -= 1
        count += 1
        r = rule(t)
        trace.append({"step": count, "pool": pool, "cell": cell,
                      "margin": r["margin"], "met": r["met"]})
        if not r["met"]:
            return count, trace
    return None, trace


def run_missing(args):
    table = load_cells(args.cells, args.hypothesis)
    pools = {"t12": args.missing_t12,
             "t3": args.missing_t3 if args.hypothesis == "h2" else 0}
    n_rel = pools["t12"] + (pools["t3"] if args.hypothesis == "h2" else 0)
    ucl_ps = wilson_ucl(*args.ps)
    ucl_ppos = wilson_ucl(*args.ppos)
    out = {"spec": "plan v1.1 §4.2(b) TP_pos/TP_free (manifest item 11)",
           "hypothesis": args.hypothesis, "h2_scope": args.h2_scope,
           "baseline": (h1_rule(table) if args.hypothesis == "h1"
                        else h2_rule(table, args.h2_scope)),
           "pools": pools,
           "anchor_rates": {"p_s": {"k": args.ps[0], "n": args.ps[1], "ucl": ucl_ps},
                            "p_pos_given_s": {"k": args.ppos[0], "n": args.ppos[1],
                                              "ucl": ucl_ppos}},
           "interpretation_notes": [
               "N_missing_relevant = admissible tier pools for the hypothesis "
               "(H1: T1∪T2 portion only, §4.2(b) last line); the plan's formula "
               "prints the whole-stratum 462.",
               "H1: DEF/non-chain allocations are inert for DEN-H1, so "
               "TP_free(H1) = TP_pos(H1) as a count; comparators differ.",
           ]}
    for mode in ("pos", "free"):
        tp, trace = tp_search(args.hypothesis, table, pools, mode, args.h2_scope)
        comparator = (n_rel * ucl_ps * ucl_ppos) if mode == "pos" else (n_rel * ucl_ps)
        out[f"tp_{mode}"] = {
            "tp": tp,
            "overturnable_within_stratum": tp is not None,
            "ucl_comparator": comparator,
            "margin_met": (tp is None) or (tp > comparator),
            "trace": trace if args.trace else trace[-3:],
        }
    return out


# ------------------------------------------------------ §5.2 2-1 flip search
def include1_margin(e):
    """Distance from CI-includes-1; <= 0 <=> CI includes 1 (overturned)."""
    if e["lcl"] > 1.0:
        return e["lcl"] - 1.0
    if e["ucl"] < 1.0:
        return 1.0 - e["ucl"]
    return 0.0


def effect_of(effect_name, table):
    if effect_name == "or_h1":
        return h1_effect(table)
    return h2_effects(table)[effect_name]


def apply_flip(table, cand):
    t = dict(table)
    if cand.get("from"):
        t[cand["from"]] = t.get(cand["from"], 0) - 1
        if t[cand["from"]] < 0:
            die(f"flip {cand['id']}: cell {cand['from']} would go negative")
    if cand.get("to"):
        t[cand["to"]] = t.get(cand["to"], 0) + 1
    return t


def run_flips(args):
    effect_name = args.effect
    hyp = "h1" if effect_name == "or_h1" else "h2"
    table = load_cells(args.cells, hyp)
    blob = json.load(open(args.flips, encoding="utf-8"))
    cands = sorted(blob["candidates"], key=lambda c: c["id"])
    total = len(cands)
    valid_cells = set(H1_CELLS if hyp == "h1" else H2_CELLS)
    for c in cands:
        for k in ("from", "to"):
            if c.get(k) is not None and c[k] not in valid_cells:
                die(f"candidate {c['id']}: unknown cell {c[k]!r} for {hyp}")
    t = dict(table)
    flipped, trace = [], []
    e0 = effect_of(effect_name, t)
    remaining = list(cands)
    while remaining:
        e = effect_of(effect_name, t)
        if include1_margin(e) <= 0.0:
            break
        best = None
        for c in remaining:
            m = include1_margin(effect_of(effect_name, apply_flip(t, c)))
            if best is None or m < best[0]:
                best = (m, c)
        m, c = best
        t = apply_flip(t, c)
        remaining.remove(c)
        flipped.append(c["id"])
        trace.append({"step": len(flipped), "id": c["id"], "from": c.get("from"),
                      "to": c.get("to"), "include1_margin": m})
    e_final = effect_of(effect_name, t)
    overturned = include1_margin(e_final) <= 0.0
    return {"spec": "plan v1.1 §5.2 tipping point (published diagnostic)",
            "effect": effect_name,
            "baseline_effect": e0,
            "n_candidates_2_1": total,
            "tipping_count": len(flipped) if overturned else None,
            "tipping_fraction_of_2_1": (len(flipped) / total
                                        if (overturned and total) else None),
            "overturned": overturned,
            "identity_pattern": flipped,
            "final_effect": e_final,
            "trace": trace}


# --------------------------------------------------------------------- misc
def load_cells(path, hyp):
    blob = json.load(open(path, encoding="utf-8"))
    if hyp in blob:
        blob = blob[hyp]
    keys = H1_CELLS if hyp == "h1" else H2_CELLS
    missing = [k for k in keys if k not in blob]
    if missing:
        die(f"cells file lacks {hyp} keys: {missing}")
    return {k: float(blob[k]) for k in keys}


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    # Woolf OR on a known table: (30,10,10,30) -> OR 9, CI excludes 1
    e = or_ci(30, 10, 10, 30)
    check("OR point = 9", abs(e["or"] - 9.0) < 1e-12)
    se = math.sqrt(1 / 30 + 1 / 10 + 1 / 10 + 1 / 30)
    check("Woolf LCL matches closed form",
          abs(e["lcl"] - math.exp(math.log(9) - Z95 * se)) < 1e-12)
    check("no Haldane on positive cells", not e["haldane_used"])
    e0 = or_ci(5, 0, 10, 10)
    check("Haldane fires on a zero cell and raw OR is inf",
          e0["haldane_used"] and e0["raw_or"] == math.inf and e0["or"] > 0)

    # Wilson UCLs against plan §7.0 published intervals
    check("Wilson UCL 59/150 ≈ .473 (plan §7.0)", abs(wilson_ucl(59, 150) - 0.473) < 2e-3)
    check("Wilson UCL 10/59 ≈ .285 (plan §7.0)", abs(wilson_ucl(10, 59) - 0.285) < 2e-3)

    # H2 effects on a symmetric table: OR_pro = OR_contra = ROR = 1
    t8 = {k: 20.0 for k in H2_CELLS}
    h = h2_effects(t8)
    check("null 2x2x2 -> OR_pro = ROR = 1",
          abs(h["or_pro"]["or"] - 1) < 1e-12 and abs(h["ror"]["or"] - 1) < 1e-12)
    se8 = math.sqrt(8 / 20)
    check("ROR SE = sqrt(Σ 1/n) over 8 cells",
          abs(h["ror"]["ucl"] - math.exp(Z95 * se8)) < 1e-9)

    # H1 TP search: strong table overturns; replay confirms minimality property
    t4 = {"pro_a": 60, "pro_bg": 15, "contra_a": 10, "contra_bg": 40}
    base = h1_rule(t4)
    check("H1 baseline rule met (OR=16)", base["met"] and abs(base["effect"]["or"] - 16) < 1e-9)
    tp, trace = tp_search("h1", t4, {"t12": 500}, "pos", "full")
    check("H1 TP_pos found", isinstance(tp, int) and tp >= 1)
    check("rule fails exactly at TP", trace[-1]["met"] is False
          and all(s["met"] for s in trace[:-1]))
    tp2, trace2 = tp_search("h1", t4, {"t12": 500}, "pos", "full")
    check("TP search deterministic", tp == tp2 and trace == trace2)
    tpf, _ = tp_search("h1", t4, {"t12": 500}, "free", "full")
    check("H1 TP_free = TP_pos (DEF inert)", tpf == tp)
    tpn, _ = tp_search("h1", t4, {"t12": 1}, "pos", "full")
    check("pool exhaustion -> not overturnable (None)", tpn is None)

    # H2 TP search: free margins at least as adversarial as POS-only
    t8s = {"t3_pro_pos": 30, "t3_pro_def": 20, "t12_pro_pos": 10, "t12_pro_def": 60,
           "t3_contra_pos": 8, "t3_contra_def": 25, "t12_contra_pos": 12,
           "t12_contra_def": 35}
    b2 = h2_rule(t8s, "full")
    check("H2 baseline rule met", b2["met"])
    tpp, _ = tp_search("h2", t8s, {"t12": 400, "t3": 100}, "pos", "full")
    tpf2, _ = tp_search("h2", t8s, {"t12": 400, "t3": 100}, "free", "full")
    check("H2 TPs found", tpp is not None and tpf2 is not None)
    check("H2 TP_free <= TP_pos (more margins, stronger adversary)", tpf2 <= tpp)
    tpo, _ = tp_search("h2", t8s, {"t12": 400, "t3": 100}, "pos", "orpro")
    check("orpro re-scope also searchable", tpo is None or tpo >= 1)

    # flips subcommand end-to-end via temp files
    import tempfile, os as _os
    with tempfile.TemporaryDirectory(prefix="tp_selftest_") as td:
        cpath = _os.path.join(td, "cells.json")
        json.dump({"h1": t4}, open(cpath, "w"))
        fpath = _os.path.join(td, "flips.json")
        cands = ([{"id": f"x{i:02d}", "from": "pro_a", "to": "pro_bg"} for i in range(25)]
                 + [{"id": f"y{i:02d}", "from": "contra_bg", "to": "contra_a"}
                    for i in range(25)]
                 + [{"id": "z00", "from": "pro_a", "to": None}])
        json.dump({"candidates": cands}, open(fpath, "w"))
        ns = argparse.Namespace(effect="or_h1", cells=cpath, flips=fpath)
        r = run_flips(ns)
        check("flip TP overturns CI to include 1", r["overturned"]
              and r["final_effect"]["lcl"] <= 1.0 <= r["final_effect"]["ucl"])
        check("flip TP count and fraction reported",
              isinstance(r["tipping_count"], int)
              and abs(r["tipping_fraction_of_2_1"]
                      - r["tipping_count"] / len(cands)) < 1e-12)
        check("flip TP is minimal along the greedy path: last step crossed",
              r["trace"][-1]["include1_margin"] <= 0.0
              and all(s["include1_margin"] > 0.0 for s in r["trace"][:-1]))
        r2 = run_flips(ns)
        check("flip search deterministic", r == r2)
        # membership-removal flip ("to": null) is admissible
        json.dump({"candidates": [{"id": "z00", "from": "pro_a", "to": None}] * 1},
                  open(fpath, "w"))
        r3 = run_flips(argparse.Namespace(effect="or_h1", cells=cpath, flips=fpath))
        check("null-destination flip shrinks the from-cell",
              r3["trace"][0]["to"] is None if r3["trace"] else not r3["overturned"])
    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Frozen tipping-point searches (plan §4.2(b)/§5.2).")
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    mp = sub.add_parser("missing", help="§4.2(b) TP_pos/TP_free")
    mp.add_argument("--hypothesis", choices=["h1", "h2"], required=True)
    mp.add_argument("--cells", required=True, help="observed cell-count JSON")
    mp.add_argument("--missing-t12", type=int, required=True,
                    help="missing-stratum items in T1∪T2 venues")
    mp.add_argument("--missing-t3", type=int, default=0,
                    help="missing-stratum items in T3 venues (H2 only)")
    mp.add_argument("--ps", type=int, nargs=2, metavar=("K", "N"), required=True,
                    help="P(S) anchor counts (frozen anchor: checkpoint tranche, §4.2(c))")
    mp.add_argument("--ppos", type=int, nargs=2, metavar=("K", "N"), required=True,
                    help="P(POS|S) anchor counts")
    mp.add_argument("--h2-scope", choices=["full", "orpro"], default="full")
    mp.add_argument("--trace", action="store_true", help="emit the full greedy trace")
    mp.add_argument("--out")
    fp_ = sub.add_parser("flips", help="§5.2 2-1 flip tipping point")
    fp_.add_argument("--effect", choices=["or_h1", "or_pro", "or_contra", "ror"],
                     required=True)
    fp_.add_argument("--cells", required=True)
    fp_.add_argument("--flips", required=True,
                     help='JSON {"candidates": [{"id","from","to"}...]} '
                          "= ALL 2-1 resolutions in the analysis-critical cells")
    fp_.add_argument("--out")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.cmd == "missing":
        out = run_missing(args)
    elif args.cmd == "flips":
        out = run_flips(args)
    else:
        ap.print_help()
        return 2
    blob = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False,
                      default=str) + "\n"
    if getattr(args, "out", None):
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"[tipping-point] -> {args.out}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
