#!/usr/bin/env python3
"""adversarial_flip.py — §5.2 adversarial folklore-flip test (analysis-plan v1.1;
BLOCK-class per §2.4 item 8 / §12 item 15; freeze-manifest item 11: "the §5.2
adversarial-flip search script").

Frozen test, implemented 1:1 with plan §5.2 (v1.1 definitions):

  * Candidate set: 2-1 adjudicated resolutions, on the hypothesis's
    denominator-relevant dimensions (H1: D1/D2/D3/D4; H2: D1/D2/D3), of items
    currently inside the hypothesis's analysis-critical cells (= inside
    DEN-H1 / DEN-H2 — the frozen §5.3 cell lists tile the denominators).
  * Stub-congruence (§5.2 v1.1 definition): a 2-1 resolution is stub-congruent
    iff the adopted majority value equals the MAJORITY of the three families'
    B2 stub-arm codes on that dimension (stub majority = 2-1 or 3-0; a 3-way
    stub split — or missing stub coverage — means no stub majority -> not
    stub-congruent).
  * m = number of stub-congruent 2-1 resolutions in the hypothesis's
    analysis-critical cells. Flip the adversarially-selected ceil(0.25·m) of
    them (frozen fraction, §12 item 15) — the subset whose joint flip moves
    the headline effect furthest toward 1 — by DETERMINISTIC GREEDY search
    (frozen mechanism; ties break on canonical (item_id, dim) order), with
    denominator membership re-evaluated per §3.4 on every flip (a flipped
    value can remove an item from the denominator entirely, e.g. a minority
    D1 = X, not merely move its cell).
  * PASS iff the hypothesis's decision rule (§2.2/§2.3) is still met after the
    flips; FAIL blocks the confirmatory claim for that hypothesis.
  * --full-set: the §5.2 sensitivity-note variant — every stub-congruent 2-1
    resolution flipped to its minority value; survival reported (never blocks).

Greedy objective (interpretation point, recorded in output): §5.2 says "moves
the headline effect furthest toward 1" while the scored outcome is "the
hypothesis's decision rule must still be met". For H1 these coincide (one
effect); for H2 the decision rule spans OR_pro AND ROR, so the deterministic
operationalization used here is the DECISION-RULE MARGIN (min over the rule's
LCL−1 terms; H1 additionally min'd with OR−3): each greedy step flips the
candidate minimizing that margin, i.e. moving the rule-relevant effects
furthest toward failure.

Denominators and effect statistics are SELF-CONTAINED here per the freeze
instruction (no imports from other analysis scripts), implementing plan
§3.1/§3.2/§3.3/§3.4 and §2.2/§2.3/§2.5 exactly:

  DEN-H1 (§3.1): tier ∈ {T1,T2}; adjudicated D1 ∈ {S1..S8}; D2 ∈ {pro,contra};
    D3 = POS; D4 ∈ {alpha,beta,gamma}; no `unresolved` on D1–D4.
    Cells: D2 × (alpha vs beta∪gamma).
  DEN-H2 (§3.2): tier ∈ {T1,T2,T3}; D1 ∈ {S1..S8} (+B under --include-b, the
    preregistered B-inclusion sensitivity); D2 ∈ {pro,contra};
    D3 ∈ {DEF,POS}; D4 NOT required; no `unresolved` on D1–D3 (v1.1
    condition-6 exception). Cells: (T3 vs T1∪T2) × D3 × D2.
  Adjudication (§3.3): per dimension majority-of-three; 3-way -> `unresolved`.
  OR_H1 (§2.2): [n(pro,α)·n(contra,β∪γ)]/[n(pro,β∪γ)·n(contra,α)], Woolf 95% CI.
  OR_pro/OR_contra/ROR (§2.3): tier-conditional POS odds ratios; ROR CI by
    Woolf on the three-way term (SE = sqrt Σ 1/n over the 8 cells).
  Haldane–Anscombe +0.5 on all cells of an estimate's table if any cell = 0
    (§2.5); `haldane_used` flagged — §2.5 v1.1: no confirmatory verdict may
    rest on a Haldane-corrected analysis-critical cell, so the report carries
    `rule_met_confirmatory` = rule_met AND NOT haldane_on_critical_cell.
  §5.3 n-floor: per-cell adjudicated n and the n ≥ 15 floor flag are reported
    (informational here; the floor's BLOCK lives in the gate chain, §2.4 item 6).

Firewall note: consumes coded outputs, stub-arm outputs and venue metadata
only; never coder-facing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
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
N_FLOOR = 15          # §5.3 frozen n-floor
FROZEN_FRACTION = 0.25  # §5.2 / §12 item 15

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
    raw = (a * d / (b * c)) if b * c > 0 else (math.inf if a * d > 0 else math.nan)
    (a2, b2, c2, d2), hald = _haldane([a, b, c, d])
    pt = a2 * d2 / (b2 * c2)
    se = math.sqrt(1 / a2 + 1 / b2 + 1 / c2 + 1 / d2)
    return {"or": pt, "lcl": math.exp(math.log(pt) - Z95 * se),
            "ucl": math.exp(math.log(pt) + Z95 * se),
            "raw_or": raw, "haldane_used": hald}


def h1_effect(t):
    return or_ci(t["pro_a"], t["pro_bg"], t["contra_a"], t["contra_bg"])


def h2_effects(t):
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


def rule_h1(t, magnitude=3.0):
    e = h1_effect(t)
    return {"met": e["lcl"] > 1.0 and e["or"] >= magnitude,
            "margin": min(e["lcl"] - 1.0, e["or"] - magnitude),
            "haldane_used": e["haldane_used"], "effects": {"or_h1": e}}


def rule_h2(t, scope="full"):
    e = h2_effects(t)
    if scope == "orpro":
        met, margin = e["or_pro"]["lcl"] > 1.0, e["or_pro"]["lcl"] - 1.0
    else:
        met = e["or_pro"]["lcl"] > 1.0 and e["ror"]["lcl"] > 1.0
        margin = min(e["or_pro"]["lcl"] - 1.0, e["ror"]["lcl"] - 1.0)
    return {"met": met, "margin": margin, "haldane_used": e["haldane_used"],
            "effects": e}


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


def stub_majority(recs: dict, dim: str):
    """Majority of the three families' stub-arm codes (2-1 or 3-0), else None."""
    if recs is None:
        return None
    vals = [recs[c][dim] for c in CODERS]
    top, n = Counter(vals).most_common(1)[0]
    return top if n >= 2 else None


def cell_of(hyp: str, codes: dict, tier: str, include_b: bool = False):
    """§3.1/§3.2 denominator membership + cell assignment from adjudicated
    codes (with any flip overrides already applied). None = not in denominator.
    Every §3 condition is re-applied on each call (§3.4 membership
    re-evaluation)."""
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


def build_table(hyp, adj, tiers_of, flips, include_b):
    """flips: {(item_id, dim): flipped_value}. Returns (table, per-item cells)."""
    keys = H1_CELLS if hyp == "h1" else H2_CELLS
    table = {k: 0 for k in keys}
    cells = {}
    for iid in sorted(adj):
        codes = {d: adj[iid][d]["adopted"] for d in DIMS}
        for d in DIMS:
            if (iid, d) in flips:
                codes[d] = flips[(iid, d)]
        c = cell_of(hyp, codes, tiers_of.get(iid, ""), include_b)
        cells[iid] = c
        if c is not None:
            table[c] += 1
    return table, cells


# ------------------------------------------------------------- flip search
def candidates(hyp, adj, stub, base_cells):
    """Stub-congruent 2-1 resolutions inside the hypothesis's analysis-critical
    cells (§5.2). Returns (congruent, all_2_1_in_cells)."""
    cong, all21 = [], []
    for iid in sorted(adj):
        if base_cells.get(iid) is None:
            continue
        for d in HYP_DIMS[hyp]:
            a = adj[iid][d]
            if a["verdict"] != "majority":
                continue
            entry = {"item_id": iid, "dim": d, "adopted": a["adopted"],
                     "minority": a["minority"],
                     "stub_majority": stub_majority(stub.get(iid), d)}
            entry["stub_congruent"] = (entry["stub_majority"] is not None
                                       and entry["stub_majority"] == a["adopted"])
            all21.append(entry)
            if entry["stub_congruent"]:
                cong.append(entry)
    return cong, all21


def greedy_flip(hyp, adj, tiers_of, cong, budget, scope, include_b):
    rule = (lambda t: rule_h1(t)) if hyp == "h1" else (lambda t: rule_h2(t, scope))
    flips = {}
    remaining = sorted(cong, key=lambda c: (c["item_id"], c["dim"]))
    trace = []
    for step in range(budget):
        best = None
        for c in remaining:
            trial = dict(flips)
            trial[(c["item_id"], c["dim"])] = c["minority"]
            t, _ = build_table(hyp, adj, tiers_of, trial, include_b)
            m = rule(t)["margin"]
            if best is None or m < best[0]:
                best = (m, c)
        if best is None:
            break
        m, c = best
        flips[(c["item_id"], c["dim"])] = c["minority"]
        remaining = [x for x in remaining
                     if (x["item_id"], x["dim"]) != (c["item_id"], c["dim"])]
        trace.append({"step": step + 1, "item_id": c["item_id"], "dim": c["dim"],
                      "adopted": c["adopted"], "flipped_to": c["minority"],
                      "margin_after": m})
    return flips, trace


def cell_floor_report(table):
    return {k: {"n": v, "n_floor_15_met": v >= N_FLOOR} for k, v in sorted(table.items())}


def run(args) -> dict:
    coded = {c: read_jsonl(p) for c, p in zip(CODERS, args.coded)}
    stub_files = ({c: read_jsonl(p) for c, p in zip(CODERS, args.stubs)}
                  if args.stubs else {c: {} for c in CODERS})
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
    adj = {iid: adjudicate_item({c: coded[c][iid] for c in CODERS})
           for iid in sorted(common)}
    stub = {}
    for iid in common:
        if all(iid in stub_files[c] for c in CODERS):
            stub[iid] = {c: stub_files[c][iid] for c in CODERS}

    hyp, scope, incb = args.hypothesis, args.h2_scope, args.include_b
    rule = (lambda t: rule_h1(t)) if hyp == "h1" else (lambda t: rule_h2(t, scope))
    base_table, base_cells = build_table(hyp, adj, tiers_of, {}, incb)
    base_rule = rule(base_table)
    cong, all21 = candidates(hyp, adj, stub, base_cells)
    m = len(cong)
    budget = m if args.full_set else math.ceil(FROZEN_FRACTION * m)
    if args.full_set:
        flips = {(c["item_id"], c["dim"]): c["minority"] for c in cong}
        trace = [{"note": "full-set sensitivity: all stub-congruent 2-1 flipped"}]
    else:
        flips, trace = greedy_flip(hyp, adj, tiers_of, cong, budget, scope, incb)
    final_table, _ = build_table(hyp, adj, tiers_of, flips, incb)
    final_rule = rule(final_table)

    out = {
        "spec": ("plan v1.1 §5.2 adversarial folklore-flip (BLOCK, §2.4 item 8)"
                 if not args.full_set else
                 "plan v1.1 §5.2 full-set flip (sensitivity-note)"),
        "hypothesis": hyp, "h2_scope": scope, "include_b": incb,
        "n_items_adjudicated": len(adj),
        "n_in_denominator": sum(1 for v in base_cells.values() if v is not None),
        "baseline": {"table": base_table, "rule": base_rule,
                     "cell_floors": cell_floor_report(base_table)},
        "n_2_1_in_critical_cells": len(all21),
        "m_stub_congruent": m,
        "frozen_fraction": FROZEN_FRACTION,
        "flip_budget": budget,
        "flips_applied": len(flips),
        "flip_trace": trace,
        "final": {"table": final_table, "rule": final_rule,
                  "cell_floors": cell_floor_report(final_table)},
        "survives": bool(final_rule["met"]),
        "rule_met_confirmatory": bool(final_rule["met"]
                                      and not final_rule["haldane_used"]),
        "interpretation_notes": [
            "greedy objective = decision-rule margin (see module docstring; "
            "H1 coincides with 'furthest toward 1').",
            "items without full three-family stub coverage have no stub "
            "majority -> never stub-congruent (§5.2 v1.1 definition).",
            "rule_met_confirmatory applies the §2.5 Haldane rider "
            "(no confirmatory verdict on a Haldane-corrected critical cell).",
        ],
        "script_sha256": hashlib.sha256(
            open(os.path.abspath(__file__), "rb").read()).hexdigest(),
    }
    if args.export_flips:
        cands = []
        for c in all21:
            iid, d = c["item_id"], c["dim"]
            codes = {dd: adj[iid][dd]["adopted"] for dd in DIMS}
            frm = cell_of(hyp, codes, tiers_of.get(iid, ""), incb)
            codes[d] = c["minority"]
            to = cell_of(hyp, codes, tiers_of.get(iid, ""), incb)
            cands.append({"id": f"{iid}|{d}", "from": frm, "to": to,
                          "stub_congruent": c["stub_congruent"]})
        with open(args.export_flips, "w", encoding="utf-8") as f:
            json.dump({"hypothesis": hyp, "candidates": cands}, f, indent=1,
                      sort_keys=True)
        out["exported_flips"] = args.export_flips
    return out


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    def rec(iid, d1, d2, d3, d4):
        return {"item_id": iid, "d1_step": d1, "d2_direction": d2,
                "d3_strength": d3, "d4_type": d4}

    # --- unit: denominators (plan §3.1/§3.2)
    ok_codes = {"d1_step": "S4", "d2_direction": "pro", "d3_strength": "POS",
                "d4_type": "alpha"}
    check("DEN-H1 cell pro_a", cell_of("h1", ok_codes, "T2") == "pro_a")
    check("DEN-H1 rejects T3", cell_of("h1", ok_codes, "T3") is None)
    check("DEN-H1 rejects DEF", cell_of("h1", {**ok_codes, "d3_strength": "DEF"}, "T2") is None)
    check("DEN-H1 rejects neutral D2", cell_of("h1", {**ok_codes, "d2_direction": "neutral"}, "T2") is None)
    check("DEN-H1 rejects D4=NA", cell_of("h1", {**ok_codes, "d4_type": "NA"}, "T2") is None)
    check("DEN-H1 rejects unresolved D1",
          cell_of("h1", {**ok_codes, "d1_step": UNRESOLVED}, "T2") is None)
    check("DEN-H2 keeps DEF and T3",
          cell_of("h2", {**ok_codes, "d3_strength": "DEF"}, "T3") == "t3_pro_def")
    check("DEN-H2 ignores D4-unresolved (v1.1 condition-6 exception)",
          cell_of("h2", {**ok_codes, "d4_type": UNRESOLVED}, "T2") == "t12_pro_pos")
    check("DEN-H2 rejects B by default",
          cell_of("h2", {**ok_codes, "d1_step": "B"}, "T2") is None)
    check("DEN-H2 B-inclusion sensitivity admits B",
          cell_of("h2", {**ok_codes, "d1_step": "B"}, "T2", include_b=True) == "t12_pro_pos")

    # --- end-to-end synthetic H1 run
    # unanimity base: 12 pro/alpha, 8 contra/bg, 4 pro/bg, 2 contra/alpha -> OR=12
    # + 6 pro/alpha items with a 2-1 on d4 (minority beta), stub-congruent
    # + 1 pro/alpha item with 2-1 on d1 (minority X: flip removes membership)
    # + 1 item with 3-way d2 split -> unresolved -> excluded
    # + 1 X item (out of chain)
    full = {c: {} for c in CODERS}
    stubf = {c: {} for c in CODERS}
    meta = []
    k = 0

    def add(d1, d2, d3, d4, n, journal="Religious Studies", twist=None):
        nonlocal k
        for _ in range(n):
            iid = f"it{k:03d}"
            k += 1
            for c in CODERS:
                full[c][iid] = rec(iid, d1, d2, d3, d4)
                stubf[c][iid] = rec(iid, d1, d2, d3, d4)  # stub agrees with majority
            if twist == "d4_21":
                full["c"][iid] = rec(iid, d1, d2, d3, "beta")
            elif twist == "d1_21_X":
                full["c"][iid] = rec(iid, "X", d2, d3, d4)
            elif twist == "d2_3way":
                full["a"][iid] = rec(iid, d1, "pro", d3, d4)
                full["b"][iid] = rec(iid, d1, "contra", d3, d4)
                full["c"][iid] = rec(iid, d1, "neutral", d3, d4)
            elif twist == "stub_3way":
                full["c"][iid] = rec(iid, d1, d2, d3, "beta")
                stubf["a"][iid] = rec(iid, d1, d2, d3, "alpha")
                stubf["b"][iid] = rec(iid, d1, d2, d3, "beta")
                stubf["c"][iid] = rec(iid, d1, d2, d3, "gamma")
            meta.append({"item_id": iid, "journal": journal, "year": 2019})

    add("S4", "pro", "POS", "alpha", 6)
    add("S4", "pro", "POS", "alpha", 6, twist="d4_21")        # congruent 2-1 (d4)
    add("S4", "pro", "POS", "alpha", 1, twist="d1_21_X")      # congruent 2-1 (d1, minority X)
    add("S4", "pro", "POS", "alpha", 1, twist="stub_3way")    # 2-1 but NOT congruent
    add("S2", "contra", "POS", "beta", 8)
    add("S4", "pro", "POS", "beta", 4)
    add("S1", "contra", "POS", "alpha", 2)
    add("S4", "pro", "POS", "alpha", 1, twist="d2_3way")      # unresolved -> excluded
    add("X", "NA", "NA", "NA", 1)

    with tempfile.TemporaryDirectory(prefix="advflip_selftest_") as td:
        paths = {}
        for c in CODERS:
            paths[("coded", c)] = os.path.join(td, f"coded_{c}.jsonl")
            paths[("stub", c)] = os.path.join(td, f"stub_{c}.jsonl")
            with open(paths[("coded", c)], "w") as f:
                for r in full[c].values():
                    f.write(json.dumps(r) + "\n")
            with open(paths[("stub", c)], "w") as f:
                for r in stubf[c].values():
                    f.write(json.dumps(r) + "\n")
        mpath = os.path.join(td, "meta.jsonl")
        with open(mpath, "w") as f:
            for r in meta:
                f.write(json.dumps(r) + "\n")

        def mkargs(**kw):
            ns = argparse.Namespace(
                coded=[paths[("coded", c)] for c in CODERS],
                stubs=[paths[("stub", c)] for c in CODERS],
                meta=[mpath], tiers=None, hypothesis="h1", h2_scope="full",
                include_b=False, full_set=False, export_flips=None)
            for a, b in kw.items():
                setattr(ns, a, b)
            return ns

        r = run(mkargs())
        bt = r["baseline"]["table"]
        # 6+6+1 pro_a (twists adjudicate to alpha/S4), 4 pro_bg, 2 contra_a, 8 contra_bg
        check("baseline table correct",
              bt == {"pro_a": 14, "pro_bg": 4, "contra_a": 2, "contra_bg": 8})
        check("unresolved item excluded from denominator",
              r["n_in_denominator"] == 28)
        check("baseline OR = 14 and rule met",
              abs(r["baseline"]["rule"]["effects"]["or_h1"]["or"] - 14.0) < 1e-9
              and r["baseline"]["rule"]["met"])
        # congruent candidates: 6 d4-twists + 1 d1-X twist (stub majority ==
        # adopted in both); stub_3way item is 2-1 but not congruent
        check("m counts stub-congruent 2-1 only", r["m_stub_congruent"] == 7
              and r["n_2_1_in_critical_cells"] == 8)
        check("budget = ceil(0.25 * 7) = 2", r["flip_budget"] == 2
              and r["flips_applied"] == 2)
        check("greedy trace deterministic", run(mkargs()) == r)
        # membership re-evaluation: flipping the d1 candidate to X must shrink
        # the denominator, not move a cell — force via full-set
        rf = run(mkargs(full_set=True))
        ft = rf["final"]["table"]
        check("full-set flips all 7", rf["flips_applied"] == 7)
        check("§3.4 membership re-evaluation: D1->X flip removes an item",
              sum(ft.values()) == sum(rf["baseline"]["table"].values()) - 1)
        check("d4 flips moved pro_a -> pro_bg",
              ft["pro_bg"] == 4 + 6 and ft["pro_a"] == 14 - 7)
        check("full-set is the NOTE variant, reported not blocking",
              "sensitivity-note" in rf["spec"])
        # n-floor flags present (§5.3)
        check("cell n-floor reported",
              r["baseline"]["cell_floors"]["contra_a"]["n_floor_15_met"] is False)
        # export interface for tipping_point.py flips
        ep = os.path.join(td, "flips.json")
        r2 = run(mkargs(export_flips=ep))
        exported = json.load(open(ep))
        check("exported flip candidates carry from/to cells",
              len(exported["candidates"]) == r2["n_2_1_in_critical_cells"]
              and any(c["to"] is None for c in exported["candidates"]))

        # --- H2 end-to-end (T3 venue + DEF strength + B-inclusion)
        full2 = {c: {} for c in CODERS}
        meta2 = []
        k2 = 0

        def add2(d1, d2, d3, journal, n):
            nonlocal k2
            for _ in range(n):
                iid = f"h2{k2:03d}"
                k2 += 1
                for c in CODERS:
                    full2[c][iid] = rec(iid, d1, d2, d3, "alpha")
                meta2.append({"item_id": iid, "journal": journal, "year": 2019})

        add2("S4", "pro", "POS", "Philosophia Christi", 12)
        add2("S4", "pro", "DEF", "Philosophia Christi", 18)
        add2("S4", "pro", "POS", "Religious Studies", 6)
        add2("S4", "pro", "DEF", "Religious Studies", 40)
        add2("S4", "contra", "POS", "Philosophia Christi", 3)
        add2("S4", "contra", "DEF", "Philosophia Christi", 16)
        add2("S4", "contra", "POS", "Religious Studies", 6)
        add2("S4", "contra", "DEF", "Religious Studies", 30)
        add2("B", "pro", "POS", "Religious Studies", 5)   # B: only under --include-b
        for c in CODERS:
            with open(os.path.join(td, f"h2_{c}.jsonl"), "w") as f:
                for rr in full2[c].values():
                    f.write(json.dumps(rr) + "\n")
        m2 = os.path.join(td, "meta2.jsonl")
        with open(m2, "w") as f:
            for rr in meta2:
                f.write(json.dumps(rr) + "\n")
        a2 = mkargs(coded=[os.path.join(td, f"h2_{c}.jsonl") for c in CODERS],
                    stubs=None, meta=[m2], hypothesis="h2")
        rh2 = run(a2)
        t = rh2["baseline"]["table"]
        check("H2 8-cell table correct",
              t == {"t3_pro_pos": 12, "t3_pro_def": 18, "t12_pro_pos": 6,
                    "t12_pro_def": 40, "t3_contra_pos": 3, "t3_contra_def": 16,
                    "t12_contra_pos": 6, "t12_contra_def": 30})
        opro = rh2["baseline"]["rule"]["effects"]["or_pro"]["or"]
        check("OR_pro = (12/18)/(6/40) = 4.444", abs(opro - (12 / 18) / (6 / 40)) < 1e-9)
        rb = run(mkargs(coded=[os.path.join(td, f"h2_{c}.jsonl") for c in CODERS],
                        stubs=None, meta=[m2], hypothesis="h2", include_b=True))
        check("B-inclusion adds the 5 B items to DEN-H2",
              rb["n_in_denominator"] == rh2["n_in_denominator"] + 5)
        check("no stub files -> m = 0 -> budget 0 -> survives = baseline rule",
              rh2["m_stub_congruent"] == 0 and rh2["flip_budget"] == 0
              and rh2["survives"] == rh2["baseline"]["rule"]["met"])
    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="§5.2 adversarial folklore-flip test (frozen).")
    ap.add_argument("--coded", nargs=3, metavar=("A", "B", "C"),
                    help="full-arm consolidated coder files (a b c)")
    ap.add_argument("--stubs", nargs=3, metavar=("A", "B", "C"),
                    help="B2 stub-arm consolidated coder files (a b c)")
    ap.add_argument("--meta", nargs="+", help="corpus JSONL(s) for the venue join")
    ap.add_argument("--tiers", help="JSON journal->tier overrides "
                    "(default: frozen tier table; use for the R2 F&P flip)")
    ap.add_argument("--hypothesis", choices=["h1", "h2"], required=False)
    ap.add_argument("--h2-scope", choices=["full", "orpro"], default="full",
                    help="§12 item 16 re-scope switch")
    ap.add_argument("--include-b", action="store_true",
                    help="DEN-H2 B-inclusion sensitivity (§3.2)")
    ap.add_argument("--full-set", action="store_true",
                    help="§5.2 full-set flip (sensitivity-note variant)")
    ap.add_argument("--export-flips", metavar="PATH",
                    help="export ALL 2-1 candidates (from/to cells) for "
                         "tipping_point.py flips")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not (args.coded and args.meta and args.hypothesis):
        die("required: --coded A B C, --meta ..., --hypothesis h1|h2", 2)
    out = run(args)
    blob = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"[adversarial-flip] {out['hypothesis']} survives={out['survives']} "
              f"(m={out['m_stub_congruent']}, budget={out['flip_budget']}) -> {args.out}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
