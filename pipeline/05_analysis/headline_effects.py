#!/usr/bin/env python3
"""headline_effects.py — primary H1/H2 headline estimator (analysis-plan v1.1
§2.2/§2.3/§2.5 + §3 denominators; freeze-manifest item 11: "the H1/H2 analysis
and bootstrap scripts to be added pre-freeze").

Implements the plan 1:1:

  DEN-H1 (§3.1): tier ∈ {T1,T2}; adjudicated D1 ∈ {S1..S8}; D2 ∈ {pro,contra};
    D3 = POS; D4 ∈ {alpha,beta,gamma}; no `unresolved` on D1–D4.
    Cells: D2 × (alpha vs beta∪gamma).
  DEN-H2 (§3.2): tier ∈ {T1,T2,T3}; D1 ∈ {S1..S8} (+B under --include-b, the
    preregistered B-inclusion sensitivity); D2 ∈ {pro,contra};
    D3 ∈ {DEF,POS}; D4 NOT required; no `unresolved` on D1–D3 (v1.1
    condition-6 exception). Cells: (T3 vs T1∪T2) × D3 × D2.
  Adjudication (§3.3): per dimension majority-of-three over the coders'
    consolidated codes; 3-way -> `unresolved` (excluded per §3.4 primary rule).
  `run_unstable` (§3.5): included in the primary with the consolidated value;
    --exclude-run-unstable implements the preregistered sensitivity.

  H1 (§2.2): OR_H1 = [n(pro,α)·n(contra,β∪γ)]/[n(pro,β∪γ)·n(contra,α)] with
    Woolf (logit) 95% CI; Haldane–Anscombe +0.5 on all cells if any cell = 0
    (raw and corrected both reported; `haldane_used` flagged); two-sided
    Fisher exact test reported alongside. Registered prediction OR_H1 ≥ 3.
  H2 (§2.3): saturated log-linear fit of the 2×2×2 tier×strength×direction
    table by stdlib IPF; OR_pro, OR_contra, ROR = OR_pro/OR_contra with Woolf
    on the three-way term (SE = sqrt Σ 1/n over the 8 cells); the IPF-derived
    three-way u-term is cross-checked against the direct ratio (they must
    agree — the saturated MLE reproduces the observed table), and the
    interaction contrast additionally carries the G² likelihood-ratio test of
    the no-three-way model [TD][TS][DS] (fit by the same IPF; df = 1).
  Decision rows (§2.2/§2.3 tables, frozen): H1 supported-at-registered-
    magnitude / directionally-supported / null; H2 supported / partially
    supported / null; contra-control met / not-met / not-evaluable (both
    contra tier-cells at adjudicated n ≥ 15). §5.3 n-floor (n ≥ 15 per
    analysis-critical cell) and the §2.5 Haldane rider are reported per
    hypothesis: `verdict_confirmatory` = rule met AND all cell floors met AND
    NOT haldane_used. (The FULL confirmatory gate chain §2.4 has further
    items adjudicated outside this script; this script's flags are §2.4
    items 6 and 10 plus the §2.5 rider only.)
  Bootstrap (§2.5 convention): nonparametric percentile, B = 1,000 default,
    ITEM-level resampling over the adjudicated item set (denominator
    membership re-evaluated inside every replicate), single global RNG,
    seed = OSF registration date (YYYYMMDD) passed as --seed, replicate-outer
    loop; both hypotheses' tables are rebuilt from the SAME replicate draw.
    Percentile bounds use the nearest-rank convention
    (sorted[ceil(p·B)-1]). Reported alongside the Woolf CIs (the Woolf CI is
    the decision-rule CI of record; the bootstrap CI is published with it).

Verdict vocabulary is instrument-relative (§2.6): the registered sentence
form is "H1 [H2] supported, as measured by the frozen, preregistered
multi-family LLM instrument"; this script emits verdict keys, not prose.

Denominators and effect statistics are SELF-CONTAINED here per the freeze
instruction (no imports from other analysis scripts in the run path); the
selftest imports adversarial_flip.py to prove NUMERIC IDENTITY with that
script's self-contained implementation on shared fixtures.

Firewall note: consumes coded outputs and venue metadata only; never
coder-facing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
from collections import Counter
from statistics import NormalDist

Z95 = NormalDist().inv_cdf(0.975)

DIMS = ["d1_step", "d2_direction", "d3_strength", "d4_type"]
CODERS = ["a", "b", "c"]
HYP_DIMS = {"h1": ["d1_step", "d2_direction", "d3_strength", "d4_type"],
            "h2": ["d1_step", "d2_direction", "d3_strength"]}
S_STEPS = {f"S{i}" for i in range(1, 9)}
UNRESOLVED = "__unresolved__"
H1_CELLS = ["pro_a", "pro_bg", "contra_a", "contra_bg"]
H2_CELLS = [f"{t}_{d}_{s}" for t in ("t3", "t12") for d in ("pro", "contra")
            for s in ("pos", "def")]
N_FLOOR = 15                  # §5.3 frozen n-floor
REGISTERED_MAGNITUDE = 3.0    # §2.2 registered prediction OR_H1 >= 3
CONTRA_EVAL_FLOOR = 15        # §2.3 contra-control evaluability floor
BOOT_DEFAULT = 1000           # §2.5 frozen B

# Frozen venue-tier assignment table (manifest item 9; F&P = T2 primary,
# the R2 flip is a separate preregistered sensitivity run via --tiers).
DEFAULT_TIERS = {
    "mind": "T1", "analysis": "T1", "the philosophical quarterly": "T1",
    "philosophical quarterly": "T1", "philosophical studies": "T1",
    "noûs": "T1", "nous": "T1", "american philosophical quarterly": "T1",
    "religious studies": "T2", "international journal for philosophy of religion": "T2",
    "sophia": "T2", "faith and philosophy": "T2",
    "philosophia christi": "T3",
}


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def read_jsonl(path: str) -> dict:
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                die(f"{path}:{n}: invalid JSON ({e})", 4)
            out[r["item_id"]] = r
    return out


# ----------------------------------------------------------- §2 statistics
def _haldane(vals):
    if any(v == 0 for v in vals):
        return [v + 0.5 for v in vals], True
    return list(vals), False


def or_ci(a, b, c, d):
    """OR = a·d/(b·c) with Woolf (logit) 95% CI; Haldane +0.5 on all four
    cells if any cell = 0 (§2.2/§2.5). Raw and corrected both carried."""
    raw = (a * d / (b * c)) if b * c > 0 else (math.inf if a * d > 0 else math.nan)
    (a2, b2, c2, d2), hald = _haldane([a, b, c, d])
    pt = a2 * d2 / (b2 * c2)
    se = math.sqrt(1 / a2 + 1 / b2 + 1 / c2 + 1 / d2)
    return {"or": pt, "lcl": math.exp(math.log(pt) - Z95 * se),
            "ucl": math.exp(math.log(pt) + Z95 * se),
            "raw_or": raw, "haldane_used": hald}


def fisher_exact_two_sided(a, b, c, d):
    """Two-sided Fisher exact p for the 2×2 table [[a,b],[c,d]] (raw integer
    counts; §2.2 "two-sided Fisher exact test reported alongside").
    Convention: sum of hypergeometric probabilities of all tables (with the
    observed margins) whose probability <= the observed table's probability
    (relative tolerance 1e-9). Degenerate margins -> p = 1.0."""
    for v in (a, b, c, d):
        if v != int(v) or v < 0:
            die("Fisher exact requires non-negative integer cells")
    a, b, c, d = int(a), int(b), int(c), int(d)
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2
    if n == 0 or r1 == 0 or r2 == 0 or c1 == 0 or c1 == n:
        return 1.0
    denom = math.comb(n, c1)
    lo, hi = max(0, c1 - r2), min(r1, c1)
    p_obs = math.comb(r1, a) * math.comb(r2, c1 - a) / denom
    p = 0.0
    for k in range(lo, hi + 1):
        pk = math.comb(r1, k) * math.comb(r2, c1 - k) / denom
        if pk <= p_obs * (1 + 1e-9):
            p += pk
    return min(1.0, p)


def h1_effect(t):
    return or_ci(t["pro_a"], t["pro_bg"], t["contra_a"], t["contra_bg"])


def h2_effects(t):
    """OR_pro, OR_contra (Woolf per 2×2) and ROR with Woolf on the three-way
    term (SE = sqrt Σ 1/n over the 8 cells). Haldane on the 8-cell table as a
    whole if any cell = 0 (§2.5). NUMERICALLY IDENTICAL to
    adversarial_flip.h2_effects / tipping_point.h2_effects (selftest-proven)."""
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


# ------------------------------------------------------------- IPF log-linear
# 2×2×2 axes: T (t3=0, t12=1) × D (pro=0, contra=1) × S (pos=0, def=1).
_AXES = (("t3", "t12"), ("pro", "contra"), ("pos", "def"))


def _cube(table):
    """H2 cell dict -> nested [t][d][s] list."""
    return [[[table[f"{t}_{d}_{s}"] for s in _AXES[2]] for d in _AXES[1]]
            for t in _AXES[0]]


def _margin(cube, axes):
    """Sum of the 2×2×2 cube over the axes NOT in `axes`; returns a dict
    keyed by the index tuple on `axes`."""
    out = {}
    for i in range(2):
        for j in range(2):
            for k in range(2):
                key = tuple(idx for ax, idx in zip((0, 1, 2), (i, j, k))
                            if ax in axes)
                out[key] = out.get(key, 0.0) + cube[i][j][k]
    return out


def ipf_fit(table, generators, tol=1e-10, max_iter=10000):
    """Iterative proportional fitting of a hierarchical log-linear model for
    the 2×2×2 table (stdlib; §2.3 "saturated log-linear model (stdlib IPF
    implementation)"). `generators` = list of axis tuples, e.g.
    [(0,1),(0,2),(1,2)] for the no-three-way model, [(0,1,2)] for the
    saturated model. Requires strictly positive observed cells (apply the
    §2.5 Haldane correction first if any cell = 0). Returns (fitted_cube,
    n_iterations)."""
    obs = _cube(table)
    if any(obs[i][j][k] <= 0 for i in range(2) for j in range(2) for k in range(2)):
        die("ipf_fit requires strictly positive cells (Haldane-correct first)")
    targets = {g: _margin(obs, g) for g in generators}
    fit = [[[1.0] * 2 for _ in range(2)] for _ in range(2)]
    it = 0
    for it in range(1, max_iter + 1):
        delta = 0.0
        for g in generators:
            cur = _margin(fit, g)
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        key = tuple(idx for ax, idx in zip((0, 1, 2), (i, j, k))
                                    if ax in g)
                        fit[i][j][k] *= targets[g][key] / cur[key]
        for g in generators:
            cur = _margin(fit, g)
            delta = max(delta, max(abs(cur[key] - targets[g][key])
                                   for key in cur))
        if delta < tol:
            break
    return fit, it


def loglinear_three_way(fit):
    """Effect-coded three-way u-term of a strictly positive fitted cube;
    log ROR = 8·u_TDS = Σ s_t·s_d·s_s·ln m (signs +1 for index 0)."""
    total = 0.0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                sign = (1 if i == 0 else -1) * (1 if j == 0 else -1) \
                    * (1 if k == 0 else -1)
                total += sign * math.log(fit[i][j][k])
    return total / 8.0


def g2_of(obs_cube, fit_cube):
    return 2.0 * sum(
        obs_cube[i][j][k] * math.log(obs_cube[i][j][k] / fit_cube[i][j][k])
        for i in range(2) for j in range(2) for k in range(2)
        if obs_cube[i][j][k] > 0)


def chi2_1_sf(x):
    """Survival function of chi-square(1): P(X > x) = erfc(sqrt(x/2))."""
    return math.erfc(math.sqrt(max(x, 0.0) / 2.0))


def h2_ipf_block(table):
    """Saturated IPF fit + three-way contrast + no-three-way G² test (§2.3).
    Works on the Haldane-corrected table if any cell = 0 (§2.5)."""
    vals = [table[k] for k in H2_CELLS]
    corr, hald = _haldane(vals)
    tcorr = dict(zip(H2_CELLS, corr))
    sat_fit, sat_iter = ipf_fit(tcorr, [(0, 1, 2)])
    obs = _cube(tcorr)
    sat_max_dev = max(abs(sat_fit[i][j][k] - obs[i][j][k])
                      for i in range(2) for j in range(2) for k in range(2))
    log_ror = 8.0 * loglinear_three_way(sat_fit)
    red_fit, red_iter = ipf_fit(tcorr, [(0, 1), (0, 2), (1, 2)])
    g2 = g2_of(obs, red_fit)
    se = math.sqrt(sum(1 / v for v in corr))  # Woolf on the three-way term
    return {
        "haldane_used": hald,
        "saturated": {"iterations": sat_iter,
                      "fitted_equals_observed_max_dev": sat_max_dev},
        "three_way_contrast": {
            "log_ror": log_ror,
            "ror": math.exp(log_ror),
            "se_woolf": se,
            "lcl": math.exp(log_ror - Z95 * se),
            "ucl": math.exp(log_ror + Z95 * se),
        },
        "no_three_way_model": {
            "generators": "[TD][TS][DS]",
            "iterations": red_iter,
            "g2": g2, "df": 1, "p": chi2_1_sf(g2),
            "fitted_cells": {f"{t}_{d}_{s}": red_fit[i][j][k]
                             for i, t in enumerate(_AXES[0])
                             for j, d in enumerate(_AXES[1])
                             for k, s in enumerate(_AXES[2])},
        },
    }


# ------------------------------------------------- §3 adjudication + denominators
def adjudicate_item(recs: dict) -> dict:
    """recs: coder -> record. Per dimension: adopted value (or UNRESOLVED),
    verdict, minority value (2-1 only) — plan §3.3."""
    out = {}
    for d in DIMS:
        vals = [recs[c][d] for c in CODERS]
        ct = Counter(vals)
        top, n = ct.most_common(1)[0]
        if n == 3:
            out[d] = {"adopted": top, "verdict": "agree", "minority": None}
        elif n == 2:
            minority = next(v for v in vals if v != top)
            out[d] = {"adopted": top, "verdict": "majority", "minority": minority}
        else:
            out[d] = {"adopted": UNRESOLVED, "verdict": "unresolved", "minority": None}
    return out


def cell_of(hyp: str, codes: dict, tier: str, include_b: bool = False):
    """§3.1/§3.2 denominator membership + cell assignment from adjudicated
    codes. None = not in denominator. IDENTICAL logic to
    adversarial_flip.cell_of (selftest-proven)."""
    dims = HYP_DIMS[hyp]
    if any(codes[d] == UNRESOLVED for d in dims):
        return None
    d1, d2, d3 = codes["d1_step"], codes["d2_direction"], codes["d3_strength"]
    if hyp == "h1":
        if tier not in ("T1", "T2"):
            return None
        if d1 not in S_STEPS or d2 not in ("pro", "contra") or d3 != "POS":
            return None
        d4 = codes["d4_type"]
        if d4 not in ("alpha", "beta", "gamma"):
            return None
        return f"{d2}_{'a' if d4 == 'alpha' else 'bg'}"
    if tier not in ("T1", "T2", "T3"):
        return None
    d1_ok = S_STEPS | ({"B"} if include_b else set())
    if d1 not in d1_ok or d2 not in ("pro", "contra") or d3 not in ("DEF", "POS"):
        return None
    return f"{'t3' if tier == 'T3' else 't12'}_{d2}_{d3.lower()}"


def build_table(hyp, adj, tiers_of, include_b, multiplicity=None):
    """Cell counts from adjudicated codes; `multiplicity` (item_id -> weight)
    supports the item-level bootstrap resample (§2.5). Returns
    (table, per-item cells)."""
    keys = H1_CELLS if hyp == "h1" else H2_CELLS
    table = {k: 0 for k in keys}
    cells = {}
    for iid in sorted(adj):
        w = 1 if multiplicity is None else multiplicity.get(iid, 0)
        if w == 0:
            cells[iid] = None if multiplicity is None else cells.get(iid)
            continue
        codes = {d: adj[iid][d]["adopted"] for d in DIMS}
        c = cell_of(hyp, codes, tiers_of.get(iid, ""), include_b)
        cells[iid] = c
        if c is not None:
            table[c] += w
    return table, cells


def cell_floor_report(table):
    return {k: {"n": v, "n_floor_15_met": v >= N_FLOOR}
            for k, v in sorted(table.items())}


# ------------------------------------------------------------- decision rows
def h1_decision(table):
    """§2.2 decision semantics (frozen at P3) + §5.3 n-floor + §2.5 rider."""
    e = h1_effect(table)
    if e["lcl"] > 1.0 and e["or"] >= REGISTERED_MAGNITUDE:
        verdict = "supported_at_registered_magnitude"
    elif e["lcl"] > 1.0 and 1.0 < e["or"] < REGISTERED_MAGNITUDE:
        verdict = "directionally_supported_registered_magnitude_not_met"
    else:
        verdict = "null"
    floors = cell_floor_report(table)
    floors_met = all(v["n_floor_15_met"] for v in floors.values())
    ints = all(float(table[k]).is_integer() for k in H1_CELLS)
    fisher = (fisher_exact_two_sided(*(int(table[k]) for k in H1_CELLS))
              if ints else None)
    return {
        "effects": {"or_h1": e},
        "fisher_exact_two_sided_p": fisher,
        "registered_magnitude": REGISTERED_MAGNITUDE,
        "verdict": verdict,
        "rule_met": verdict == "supported_at_registered_magnitude",
        "kill_criterion_input_h1_null": verdict == "null",
        "cell_floors": floors,
        "n_floor_all_met": floors_met,
        "haldane_used": e["haldane_used"],
        "verdict_confirmatory": (verdict == "supported_at_registered_magnitude"
                                 and floors_met and not e["haldane_used"]),
    }


def h2_decision(table, scope="full"):
    """§2.3 decision semantics (frozen at P3) incl. the contra-control row,
    the v1.1 cell-integrity riders (§5.3 n-floor over all 8 cells; §2.5
    Haldane rider), and the §12 item 16 orpro re-scope."""
    e = h2_effects(table)
    lcl_pro, ror = e["or_pro"]["lcl"], e["ror"]
    if scope == "orpro":
        verdict = "supported" if lcl_pro > 1.0 else "null"
        scope_note = ("§12 item 16 re-scope active: confirmatory element = "
                      "OR_pro only; ROR reported as registered estimation "
                      "(CI, no supported/null verdict)")
    else:
        if lcl_pro > 1.0 and ror["lcl"] > 1.0:
            verdict = "supported"
        elif lcl_pro > 1.0 and ror["lcl"] <= 1.0 <= ror["ucl"]:
            verdict = "partially_supported"
        else:
            verdict = "null"
        scope_note = None
    # contra-control (§2.3): evaluable iff both contra tier-cells n >= 15
    n_t3_contra = table["t3_contra_pos"] + table["t3_contra_def"]
    n_t12_contra = table["t12_contra_pos"] + table["t12_contra_def"]
    evaluable = (n_t3_contra >= CONTRA_EVAL_FLOOR
                 and n_t12_contra >= CONTRA_EVAL_FLOOR)
    if not evaluable:
        contra = "not_evaluable"   # never "met" (§2.3 v1.1)
    else:
        contra = "met" if e["or_contra"]["lcl"] <= 1.0 else "not_met"
    floors = cell_floor_report(table)
    floors_met = all(v["n_floor_15_met"] for v in floors.values())
    return {
        "effects": e,
        "h2_scope": scope,
        "scope_note": scope_note,
        "verdict": verdict,
        "rule_met": verdict == "supported",
        "partially_supported_counts_as_supported_for_kill": False,  # §2.3
        "kill_criterion_input_h2_null": verdict == "null",
        "contra_control": {
            "status": contra,
            "evaluable": evaluable,
            "n_t3_contra": n_t3_contra,
            "n_t12_contra": n_t12_contra,
            "floor": CONTRA_EVAL_FLOOR,
            "exempt_from_b6_stability_block": True,  # §2.3/§5.1 v1.1
        },
        "cell_floors": floors,
        "n_floor_all_met": floors_met,
        "haldane_used": e["haldane_used"],
        "verdict_confirmatory": (verdict == "supported" and floors_met
                                 and not e["haldane_used"]),
    }


# ---------------------------------------------------------------- bootstrap
def percentile_nearest_rank(sorted_vals, p):
    n = len(sorted_vals)
    idx = max(0, math.ceil(p * n) - 1)
    return sorted_vals[idx]


def bootstrap_effects(adj, tiers_of, include_b, hyps, b, seed):
    """§2.5 convention: nonparametric percentile, item-level resampling,
    single global RNG (seed = OSF registration date YYYYMMDD), replicate-outer
    loop; both hypotheses share each replicate's draw."""
    ids = sorted(adj)
    n = len(ids)
    rng = random.Random(seed)
    effects = {"h1": ["or_h1"], "h2": ["or_pro", "or_contra", "ror"]}
    samples = {name: [] for h in hyps for name in effects[h]}
    hald_count = {name: 0 for h in hyps for name in effects[h]}
    for _ in range(b):
        mult = Counter(ids[rng.randrange(n)] for _ in range(n))
        for h in hyps:
            t, _cells = build_table(h, adj, tiers_of, include_b, multiplicity=mult)
            if h == "h1":
                e = h1_effect(t)
                samples["or_h1"].append(e["or"])
                hald_count["or_h1"] += 1 if e["haldane_used"] else 0
            else:
                es = h2_effects(t)
                for name in ("or_pro", "or_contra", "ror"):
                    samples[name].append(es[name]["or"])
                    hald_count[name] += 1 if es[name]["haldane_used"] else 0
    out = {}
    for name, vals in samples.items():
        sv = sorted(vals)
        out[name] = {
            "b": b, "seed": seed,
            "lcl": percentile_nearest_rank(sv, 0.025),
            "ucl": percentile_nearest_rank(sv, 0.975),
            "median": percentile_nearest_rank(sv, 0.5),
            "haldane_replicates": hald_count[name],
        }
    return out


# ------------------------------------------------------------------- driver
def run(args) -> dict:
    coded = {c: read_jsonl(p) for c, p in zip(CODERS, args.coded)}
    tiers_tab = dict(DEFAULT_TIERS)
    if args.tiers:
        for k, v in json.load(open(args.tiers, encoding="utf-8")).items():
            tiers_tab[" ".join(k.split()).casefold()] = v
    tiers_of = {}
    for p in args.meta:
        for iid, r in read_jsonl(p).items():
            j = " ".join((r.get("journal") or "").split()).casefold()
            tiers_of.setdefault(iid, tiers_tab.get(j, ""))

    common = set(coded["a"]) & set(coded["b"]) & set(coded["c"])
    run_unstable_ids = sorted(
        iid for iid in common
        if any("run_unstable" in (coded[c][iid].get("flags") or [])
               for c in CODERS))
    if args.exclude_run_unstable:   # §3.5 preregistered sensitivity
        common -= set(run_unstable_ids)
    adj = {iid: adjudicate_item({c: coded[c][iid] for c in CODERS})
           for iid in sorted(common)}

    hyps = ["h1", "h2"] if args.hypothesis == "both" else [args.hypothesis]
    incb = args.include_b
    unresolved_dim_counts = {
        d: sum(1 for iid in adj if adj[iid][d]["verdict"] == "unresolved")
        for d in DIMS}

    out = {
        "spec": ("plan v1.1 §2.2/§2.3 headline effects (primary estimator; "
                 "freeze-manifest item 11)"),
        "estimator": "E4 majority-of-three (§5.1 primary)",
        "hypotheses": hyps,
        "h2_scope": args.h2_scope,
        "include_b": incb,
        "exclude_run_unstable": bool(args.exclude_run_unstable),
        "n_items_adjudicated": len(adj),
        "n_run_unstable": len(run_unstable_ids),
        "unresolved_counts_per_dimension": unresolved_dim_counts,
        "interpretation_notes": [
            "adjudicated majority input (§3.3); `unresolved` excluded per "
            "§3.4 primary rule (the §3.4 min/max resolution envelope is a "
            "separate registered sensitivity, not computed here).",
            "contra-control evaluability (§2.3): 'both contra tier-cells' "
            "read as the two tier-marginal contra cells (T3-contra and "
            "T1∪T2-contra, POS+DEF pooled), each at adjudicated n >= 15.",
            "verdict_confirmatory covers §2.4 items 6 and 10 plus the §2.5 "
            "Haldane rider ONLY; the remaining §2.4 chain items are "
            "adjudicated by their own scripts/gates.",
            "bootstrap (§2.5): replicate-outer loop, single global RNG, "
            "item-level resampling with denominator membership re-evaluated "
            "per replicate; percentile bounds by nearest rank "
            "(sorted[ceil(p*B)-1]); Woolf CIs remain the decision-rule CIs.",
            "IPF saturated fit reproduces the observed table (MLE identity); "
            "the three-way u-term contrast equals the direct OR_pro/OR_contra "
            "ratio — both are asserted at runtime to 1e-9.",
        ],
        "script_sha256": hashlib.sha256(
            open(os.path.abspath(__file__), "rb").read()).hexdigest(),
    }

    tables = {}
    for h in hyps:
        table, cells = build_table(h, adj, tiers_of, incb)
        tables[h] = table
        n_in = sum(1 for v in cells.values() if v is not None)
        n_unres = sum(
            1 for iid in adj
            if any(adj[iid][d]["verdict"] == "unresolved" for d in HYP_DIMS[h]))
        block = {"table": table, "n_in_denominator": n_in,
                 "n_items_unresolved_on_denominator_dims": n_unres}
        if h == "h1":
            block["decision"] = h1_decision(table)
        else:
            block["decision"] = h2_decision(table, args.h2_scope)
            ipf = h2_ipf_block(table)
            direct = block["decision"]["effects"]["ror"]["or"]
            via_ipf = ipf["three_way_contrast"]["ror"]
            if not math.isclose(direct, via_ipf, rel_tol=1e-9, abs_tol=1e-12):
                die(f"IPF three-way contrast {via_ipf} != direct ROR {direct}")
            if ipf["saturated"]["fitted_equals_observed_max_dev"] > 1e-6:
                die("saturated IPF fit failed to reproduce the observed table")
            block["ipf_loglinear"] = ipf
        out[h] = block

    if args.boot > 0:
        if args.seed is None:
            die("--seed is required for the bootstrap (§2.5: OSF registration "
                "date YYYYMMDD); pass --boot 0 to skip", 2)
        out["bootstrap"] = bootstrap_effects(adj, tiers_of, incb, hyps,
                                             args.boot, args.seed)

    if args.export_cells:
        with open(args.export_cells, "w", encoding="utf-8") as f:
            json.dump({h: tables[h] for h in hyps}, f, indent=1, sort_keys=True)
        out["exported_cells"] = args.export_cells
    return out


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    import importlib.util
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    # cross-check module: adversarial_flip.py (self-contained sibling; the
    # freeze requires numeric identity between the two implementations)
    af_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "adversarial_flip.py")
    spec = importlib.util.spec_from_file_location("adversarial_flip", af_path)
    af = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(af)

    # --- unit: or_ci identity with adversarial_flip on assorted tables
    tabs = [(30, 10, 10, 30), (5, 0, 10, 10), (14, 4, 2, 8), (1, 1, 1, 1),
            (120, 33, 17, 240)]
    same = True
    for t4 in tabs:
        e1, e2 = or_ci(*t4), af.or_ci(*t4)
        same &= all(
            (isinstance(e1[k], float) and isinstance(e2[k], float)
             and (e1[k] == e2[k] or (math.isnan(e1[k]) and math.isnan(e2[k]))))
            or e1[k] == e2[k] for k in e1)
    check("or_ci numerically identical to adversarial_flip.or_ci", same)

    # --- unit: h2_effects identity
    t8 = {"t3_pro_pos": 12, "t3_pro_def": 18, "t12_pro_pos": 6,
          "t12_pro_def": 40, "t3_contra_pos": 3, "t3_contra_def": 16,
          "t12_contra_pos": 6, "t12_contra_def": 30}
    h_me, h_af = h2_effects(t8), af.h2_effects(t8)
    check("h2_effects numerically identical to adversarial_flip.h2_effects",
          all(h_me[e][k] == h_af[e][k]
              for e in ("or_pro", "or_contra", "ror") for k in h_me[e]))
    check("OR_pro = (12/18)/(6/40)",
          abs(h_me["or_pro"]["or"] - (12 / 18) / (6 / 40)) < 1e-12)

    # --- unit: Fisher exact (tea-tasting 2×2: [[3,1],[1,3]] -> 34/70)
    check("Fisher two-sided p = 34/70 on [[3,1],[1,3]]",
          abs(fisher_exact_two_sided(3, 1, 1, 3) - 34 / 70) < 1e-12)
    check("Fisher degenerate margin -> 1.0",
          fisher_exact_two_sided(0, 0, 5, 5) == 1.0)

    # --- unit: IPF saturated reproduces table; contrast equals direct ratio
    ipf = h2_ipf_block(t8)
    direct_ror = h_me["ror"]["or"]
    check("saturated IPF reproduces observed cells",
          ipf["saturated"]["fitted_equals_observed_max_dev"] < 1e-9)
    check("IPF three-way contrast == direct ROR",
          math.isclose(ipf["three_way_contrast"]["ror"], direct_ror,
                       rel_tol=1e-9))
    check("IPF Woolf CI == direct ROR CI",
          math.isclose(ipf["three_way_contrast"]["lcl"], h_me["ror"]["lcl"],
                       rel_tol=1e-9)
          and math.isclose(ipf["three_way_contrast"]["ucl"], h_me["ror"]["ucl"],
                           rel_tol=1e-9))
    check("no-three-way G² >= 0 with df 1",
          ipf["no_three_way_model"]["g2"] >= 0
          and ipf["no_three_way_model"]["df"] == 1)
    flat = {k: 20 for k in H2_CELLS}
    ipf0 = h2_ipf_block(flat)
    check("symmetric table -> ROR = 1, G² = 0, p = 1",
          abs(ipf0["three_way_contrast"]["ror"] - 1.0) < 1e-9
          and abs(ipf0["no_three_way_model"]["g2"]) < 1e-9
          and abs(ipf0["no_three_way_model"]["p"] - 1.0) < 1e-9)
    zero = dict(t8, t3_contra_pos=0)
    ipfz = h2_ipf_block(zero)
    check("zero cell -> Haldane inside IPF block, still consistent",
          ipfz["haldane_used"]
          and math.isclose(ipfz["three_way_contrast"]["ror"],
                           h2_effects(zero)["ror"]["or"], rel_tol=1e-9))
    check("chi2_1 sf at 3.841 ≈ .05", abs(chi2_1_sf(3.841458820694124) - 0.05) < 1e-6)

    # --- decision rows (§2.2/§2.3 semantics)
    d_sup = h1_decision({"pro_a": 60, "pro_bg": 15, "contra_a": 16, "contra_bg": 64})
    check("H1 supported at registered magnitude (OR=16, floors met)",
          d_sup["verdict"] == "supported_at_registered_magnitude"
          and d_sup["n_floor_all_met"] and d_sup["verdict_confirmatory"])
    d_dir = h1_decision({"pro_a": 200, "pro_bg": 100, "contra_a": 100, "contra_bg": 100})
    check("H1 directional-only (OR=2, LCL>1, < magnitude)",
          d_dir["verdict"] == "directionally_supported_registered_magnitude_not_met"
          and not d_dir["rule_met"] and not d_dir["kill_criterion_input_h1_null"])
    d_null = h1_decision({"pro_a": 20, "pro_bg": 20, "contra_a": 20, "contra_bg": 20})
    check("H1 null (OR=1)", d_null["verdict"] == "null"
          and d_null["kill_criterion_input_h1_null"])
    d_floor = h1_decision({"pro_a": 60, "pro_bg": 15, "contra_a": 10, "contra_bg": 40})
    check("H1 n-floor violation blocks confirmatory but not the verdict row",
          d_floor["verdict"] == "supported_at_registered_magnitude"
          and not d_floor["n_floor_all_met"] and not d_floor["verdict_confirmatory"])
    d_hald = h1_decision({"pro_a": 60, "pro_bg": 0, "contra_a": 16, "contra_bg": 64})
    check("§2.5 Haldane rider strips confirmatory status",
          d_hald["haldane_used"] and not d_hald["verdict_confirmatory"]
          and d_hald["fisher_exact_two_sided_p"] is not None)

    strong = {"t3_pro_pos": 60, "t3_pro_def": 40, "t12_pro_pos": 25,
              "t12_pro_def": 100, "t3_contra_pos": 15, "t3_contra_def": 45,
              "t12_contra_pos": 30, "t12_contra_def": 90}
    d2 = h2_decision(strong)
    check("H2 decision row computes with contra-control evaluable",
          d2["contra_control"]["evaluable"]
          and d2["contra_control"]["status"] in ("met", "not_met")
          and d2["verdict"] in ("supported", "partially_supported", "null"))
    thin = dict(strong, t3_contra_pos=2, t3_contra_def=4)
    d2t = h2_decision(thin)
    check("thin contra tier-cell -> contra-control not_evaluable, never met",
          d2t["contra_control"]["status"] == "not_evaluable"
          and not d2t["n_floor_all_met"] and not d2t["verdict_confirmatory"])
    d2o = h2_decision(strong, scope="orpro")
    check("orpro re-scope keys the verdict to OR_pro alone",
          d2o["scope_note"] is not None
          and d2o["verdict"] == ("supported" if d2o["effects"]["or_pro"]["lcl"] > 1
                                 else "null"))

    # --- end-to-end vs adversarial_flip on a shared synthetic fixture
    def rec(iid, d1, d2v, d3, d4, flags=None):
        return {"item_id": iid, "d1_step": d1, "d2_direction": d2v,
                "d3_strength": d3, "d4_type": d4, "flags": flags or []}

    full = {c: {} for c in CODERS}
    meta = []
    k = 0

    def add(d1, d2v, d3, d4, n, journal="Religious Studies", twist=None):
        nonlocal k
        for _ in range(n):
            iid = f"it{k:03d}"
            k += 1
            for c in CODERS:
                full[c][iid] = rec(iid, d1, d2v, d3, d4)
            if twist == "d4_21":
                full["c"][iid] = rec(iid, d1, d2v, d3, "beta")
            elif twist == "d2_3way":
                full["a"][iid] = rec(iid, d1, "pro", d3, d4)
                full["b"][iid] = rec(iid, d1, "contra", d3, d4)
                full["c"][iid] = rec(iid, d1, "neutral", d3, d4)
            elif twist == "unstable":
                for c in CODERS:
                    full[c][iid]["flags"] = ["run_unstable"]
            meta.append({"item_id": iid, "journal": journal, "year": 2019})

    add("S4", "pro", "POS", "alpha", 12)
    add("S4", "pro", "POS", "alpha", 6, twist="d4_21")
    add("S2", "contra", "POS", "beta", 8)
    add("S4", "pro", "POS", "beta", 4)
    add("S1", "contra", "POS", "alpha", 2)
    add("S4", "pro", "POS", "alpha", 1, twist="d2_3way")   # unresolved -> excluded
    add("S4", "pro", "POS", "alpha", 1, twist="unstable")  # run_unstable flagged
    add("X", "NA", "NA", "NA", 1)
    add("S4", "pro", "POS", "alpha", 3, journal="Philosophia Christi")
    add("S4", "pro", "DEF", "alpha", 5, journal="Philosophia Christi")
    add("S4", "contra", "POS", "beta", 1, journal="Philosophia Christi")
    add("S4", "contra", "DEF", "beta", 4, journal="Philosophia Christi")
    add("S4", "pro", "DEF", "alpha", 20)
    add("S4", "contra", "DEF", "beta", 10)

    with tempfile.TemporaryDirectory(prefix="headline_selftest_") as td:
        paths = {}
        for c in CODERS:
            paths[c] = os.path.join(td, f"coded_{c}.jsonl")
            with open(paths[c], "w") as f:
                for r in full[c].values():
                    f.write(json.dumps(r) + "\n")
        mpath = os.path.join(td, "meta.jsonl")
        with open(mpath, "w") as f:
            for r in meta:
                f.write(json.dumps(r) + "\n")

        def mkargs(**kw):
            ns = argparse.Namespace(
                coded=[paths[c] for c in CODERS], meta=[mpath], tiers=None,
                hypothesis="both", h2_scope="full", include_b=False,
                exclude_run_unstable=False, boot=0, seed=None,
                export_cells=None)
            for a, b in kw.items():
                setattr(ns, a, b)
            return ns

        r = run(mkargs())
        # identity vs adversarial_flip baselines on the same fixture
        for hyp in ("h1", "h2"):
            af_args = argparse.Namespace(
                coded=[paths[c] for c in CODERS], stubs=None, meta=[mpath],
                tiers=None, hypothesis=hyp, h2_scope="full", include_b=False,
                full_set=False, export_flips=None)
            base = af.run(af_args)["baseline"]
            check(f"{hyp} table identical to adversarial_flip baseline",
                  base["table"] == r[hyp]["table"])
            if hyp == "h1":
                mine = r["h1"]["decision"]["effects"]["or_h1"]
                theirs = base["rule"]["effects"]["or_h1"]
            else:
                mine = r["h2"]["decision"]["effects"]["ror"]
                theirs = base["rule"]["effects"]["ror"]
            check(f"{hyp} headline effect numerically identical",
                  all(mine[q] == theirs[q] for q in ("or", "lcl", "ucl")))
        check("run_unstable items included in primary and counted",
              r["n_run_unstable"] == 1
              and r["h1"]["table"]["pro_a"] == 12 + 6 + 1)
        r_x = run(mkargs(exclude_run_unstable=True))
        check("§3.5 sensitivity drops run_unstable items",
              r_x["h1"]["table"]["pro_a"] == r["h1"]["table"]["pro_a"] - 1
              and r_x["n_items_adjudicated"] == r["n_items_adjudicated"] - 1)
        check("unresolved item excluded and reported",
              r["h1"]["n_items_unresolved_on_denominator_dims"] == 1
              and r["unresolved_counts_per_dimension"]["d2_direction"] == 1)

        # bootstrap: determinism + sanity
        rb1 = run(mkargs(boot=200, seed=20260720))
        rb2 = run(mkargs(boot=200, seed=20260720))
        check("bootstrap deterministic under fixed seed",
              rb1["bootstrap"] == rb2["bootstrap"])
        rb3 = run(mkargs(boot=200, seed=20260721))
        check("bootstrap responds to the seed",
              rb1["bootstrap"] != rb3["bootstrap"])
        bh1 = rb1["bootstrap"]["or_h1"]
        check("bootstrap CI brackets the point estimate (strong H1 table)",
              bh1["lcl"] <= r["h1"]["decision"]["effects"]["or_h1"]["or"]
              <= bh1["ucl"])
        check("bootstrap covers all four headline effects",
              set(rb1["bootstrap"]) == {"or_h1", "or_pro", "or_contra", "ror"})

        # cells export for tipping_point.py interop
        cpath = os.path.join(td, "cells.json")
        r_e = run(mkargs(export_cells=cpath))
        exported = json.load(open(cpath))
        check("exported cells match computed tables (tipping_point interop)",
              exported["h1"] == r_e["h1"]["table"]
              and exported["h2"] == r_e["h2"]["table"])

        # determinism of the whole run
        check("full run deterministic", run(mkargs()) == r)

        # nearest-rank percentile convention
        vals = sorted(range(1, 101))
        check("nearest-rank percentile convention",
              percentile_nearest_rank(vals, 0.025) == 3
              and percentile_nearest_rank(vals, 0.975) == 98)

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Primary H1/H2 headline estimator (plan §2, frozen).")
    ap.add_argument("--coded", nargs=3, metavar=("A", "B", "C"),
                    help="consolidated coder files (a b c)")
    ap.add_argument("--meta", nargs="+", help="corpus JSONL(s) for the venue join")
    ap.add_argument("--tiers", help="JSON journal->tier overrides "
                    "(default: frozen tier table; use for the R2 F&P flip)")
    ap.add_argument("--hypothesis", choices=["h1", "h2", "both"], default="both")
    ap.add_argument("--h2-scope", choices=["full", "orpro"], default="full",
                    help="§12 item 16 re-scope switch")
    ap.add_argument("--include-b", action="store_true",
                    help="DEN-H2 B-inclusion sensitivity (§3.2)")
    ap.add_argument("--exclude-run-unstable", action="store_true",
                    help="§3.5 preregistered sensitivity (primary includes them)")
    ap.add_argument("--boot", type=int, default=BOOT_DEFAULT,
                    help=f"bootstrap replicates (§2.5 frozen B = {BOOT_DEFAULT}; "
                         "0 skips)")
    ap.add_argument("--seed", type=int,
                    help="bootstrap seed = OSF registration date YYYYMMDD "
                         "(§2.5; required when --boot > 0)")
    ap.add_argument("--export-cells", metavar="PATH",
                    help="write {h1,h2} cell tables for tipping_point.py")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not (args.coded and args.meta):
        die("required: --coded A B C, --meta ...", 2)
    out = run(args)
    blob = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"[headline-effects] {'/'.join(out['hypotheses'])} -> {args.out}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
