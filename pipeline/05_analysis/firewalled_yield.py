#!/usr/bin/env python3
"""firewalled_yield.py — firewalled DEN-H1 yield trigger (analysis-plan v1.1
§7 / §12 item 10; checkpoint reporting line in §6 "Also reported").

================================ FIREWALL ====================================
WHY THIS SCRIPT IS FIREWALLED (plan §12 item 10, verbatim rationale): "an
interim look at the outcome margin that changes the population definition is
defensible only if provably blind to the association under test and
deterministic in response." The stage-2 interim look happens BEFORE the
expansion decision is logged, while P4 coding is live. If the person (or agent
context) making that look could see direction×type, strength or tier
CROSS-TABS, the expansion decision — which changes the estimand population —
could be steered toward a desired H1/H2 outcome.

THEREFORE the ONLY surfaced outputs of this script are:
  * the trigger boolean (projected DEN-H1 yield < threshold),
  * the projected-yield scalar and its marginal inputs: item count, S count
    (adjudicated D1 ∈ S1..S8), POS count (S-coded ∧ adjudicated D3 = POS),
    and the unresolved count entering P(non-excluded),
  * the frozen deterministic expansion preference order, iff triggered.
NO per-item rows, NO D2×D4 tables, NO strength-by-direction or tier cross-tabs
are computed into the output object; direction (D2) and type (D4) values are
never read except (optionally, --excl-dims all) to COUNT unresolved
adjudications, never to tabulate values. Do not extend this script's output
without a preregistered amendment — any additional field is a firewall breach
(absolute rule 1 adjacency; plan §12 item 10).
==============================================================================

Frozen two-stage trigger (§12 item 10):
  Stage 1 (pre-P4, --stage1): expected DEN-H1 yield from the LOCKED P2 counts ×
    the §7.0 calibration T2-stratum rates, all passed as explicit counts.
  Stage 2 (checkpoint): projected DEN-H1 yield recomputed by the SAME frozen
    formula from the checkpoint tranche's realized marginal counts
    (adjudicated majority-of-three over the three coder files).
  Formula (§7, direction fixed in v1.1):
    E[DEN-H1] = N_abstracts(T1∪T2) × P(S) × P(POS|S) × P(non-excluded),
    P(non-excluded) = 1 − expected unresolved-or-ineligible fraction.
  Trigger: yield < 110 (frozen) -> expansion BEFORE further spend, in the
  frozen preference order, until projected yield >= 110, no discretionary
  choice: (i) complete unharvested T1 venue-years; (ii) window extension
  2000–2003 / 2025; (iii) EJPR re-admission (reverses locked D-1).

Rate conventions (§1.3 / §7.0 basis, recorded as interpretation notes):
  * P(S) = S / n over ALL tranche T1∪T2 items (pilot: 20/69);
  * P(POS|S) = POS / S;
  * the unresolved-or-ineligible fraction defaults to the ITEM-LEVEL D1
    unresolved rate (the §1.3 pilot basis, 7.2%); --excl-dims all counts items
    unresolved on ANY of D1–D4 instead (closer to the literal DEN-H1
    condition 6) — a counting variant only, values never surfaced.
  * the tranche is restricted to T1∪T2 items via the venue join (DEN-H1
    admits T1∪T2 only — §3.1/§7.0 population correction); the join is
    INTERNAL; no tier cross-tab is emitted.

stdlib-only, deterministic, zero API calls.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

DIMS = ["d1_step", "d2_direction", "d3_strength", "d4_type"]
CODERS = ["a", "b", "c"]
S_STEPS = {f"S{i}" for i in range(1, 9)}
UNRESOLVED = "__unresolved__"
THRESHOLD = 110  # frozen (§7 / §12 item 10)

# frozen deterministic expansion preference order (§12 item 10)
EXPANSION_ORDER = [
    "(i) complete T1 venue-years not yet harvested",
    "(ii) window extension (2000-2003 / 2025)",
    "(iii) EJPR re-admission (reverses locked D-1)",
]

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


def adjudicate_value(vals: list) -> str:
    top, n = Counter(vals).most_common(1)[0]
    return top if n >= 2 else UNRESOLVED


def projected_yield(n_abstracts: float, p_s: float, p_pos_given_s: float,
                    p_nonexcluded: float) -> float:
    """The frozen §7 formula, literally."""
    return n_abstracts * p_s * p_pos_given_s * p_nonexcluded


def stage2_marginals(coded_paths: list, meta_paths: list, tiers_json: str,
                     excl_dims: str) -> dict:
    """Adjudicate the tranche and return ONLY marginal counts (firewall).
    Direction/type/tier values are never tabulated; D2/D4 codes are read only
    when --excl-dims all needs their unresolved COUNT."""
    coded = {c: read_jsonl(p) for c, p in zip(CODERS, coded_paths)}
    tiers_tab = dict(DEFAULT_TIERS)
    if tiers_json:
        for k, v in json.load(open(tiers_json, encoding="utf-8")).items():
            tiers_tab[" ".join(k.split()).casefold()] = v
    tier_of = {}
    for p in meta_paths:
        for iid, r in read_jsonl(p).items():
            j = " ".join((r.get("journal") or "").split()).casefold()
            tier_of.setdefault(iid, tiers_tab.get(j, ""))
    common = sorted(set(coded["a"]) & set(coded["b"]) & set(coded["c"]))
    n = s = pos = unres = 0
    for iid in common:
        if tier_of.get(iid) not in ("T1", "T2"):
            continue  # DEN-H1 admits T1∪T2 only; join is internal (firewall)
        n += 1
        d1 = adjudicate_value([coded[c][iid]["d1_step"] for c in CODERS])
        excl_set = ["d1_step"] if excl_dims == "d1" else DIMS
        item_unres = any(
            adjudicate_value([coded[c][iid][d] for c in CODERS]) == UNRESOLVED
            for d in excl_set)
        if item_unres:
            unres += 1
        if d1 in S_STEPS:
            s += 1
            d3 = adjudicate_value([coded[c][iid]["d3_strength"] for c in CODERS])
            if d3 == "POS":
                pos += 1
    return {"n_t12_tranche_items": n, "s_count": s, "pos_count": pos,
            "unresolved_count": unres}


def evaluate(n_abstracts: float, marg: dict, threshold: float) -> dict:
    n, s, pos, u = (marg["n_t12_tranche_items"], marg["s_count"],
                    marg["pos_count"], marg["unresolved_count"])
    if n <= 0:
        die("no T1∪T2 tranche items found")
    p_s = s / n
    p_pos = (pos / s) if s else 0.0
    p_ne = 1.0 - u / n
    y = projected_yield(n_abstracts, p_s, p_pos, p_ne)
    trig = y < threshold
    out = {
        "spec": "plan v1.1 §7 / §12 item 10 firewalled yield trigger (stage 2)",
        "trigger_expand_before_further_spend": trig,
        "projected_den_h1_yield": y,
        "threshold": threshold,
        "n_abstracts_t12_locked": n_abstracts,
        "marginals": marg,
        "rates": {"p_s": p_s, "p_pos_given_s": p_pos, "p_nonexcluded": p_ne},
        "firewall": "outputs restricted to boolean + marginal S/POS counts "
                    "(no D2×D4 / strength / tier cross-tabs) — plan §12 item 10",
    }
    if trig:
        out["frozen_expansion_preference_order"] = EXPANSION_ORDER
        out["expansion_rule"] = ("execute the preference order until projected "
                                 "yield >= threshold; no discretionary choice "
                                 "among options (§12 item 10)")
    return out


def stage1(args) -> dict:
    p_s = args.ps[0] / args.ps[1]
    p_pos = args.ppos[0] / args.ppos[1]
    p_ne = 1.0 - args.unres[0] / args.unres[1]
    y = projected_yield(args.n_abstracts, p_s, p_pos, p_ne)
    trig = y < args.threshold
    out = {
        "spec": "plan v1.1 §7 / §12 item 10 yield trigger (stage 1, pre-P4)",
        "trigger_expand_before_p4_spend": trig,
        "projected_den_h1_yield": y,
        "threshold": args.threshold,
        "n_abstracts_t12_locked": args.n_abstracts,
        "rates": {"p_s": p_s, "p_pos_given_s": p_pos, "p_nonexcluded": p_ne},
        "rate_counts": {"ps": args.ps, "ppos": args.ppos, "unres": args.unres},
    }
    if trig:
        out["frozen_expansion_preference_order"] = EXPANSION_ORDER
    return out


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    import os, tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    # formula known-answer (pilot rates, §1.3): 2900 × .29 × .15 × (1-.072)
    y = projected_yield(2900, 20 / 69, 3 / 20, 1 - 5 / 69)
    check("frozen formula reproduces the §7 pilot-rate arithmetic",
          abs(y - 2900 * (20 / 69) * (3 / 20) * (64 / 69)) < 1e-9)
    check("§7 central figure ≈ 126 before non-exclusion (formula shape)",
          abs(2900 * (20 / 69) * (3 / 20) - 126.086) < 0.01)

    def rec(iid, d1, d2, d3, d4):
        return {"item_id": iid, "d1_step": d1, "d2_direction": d2,
                "d3_strength": d3, "d4_type": d4}

    # synthetic tranche: 20 T1∪T2 items — 8 S-coded (3 POS), 1 D1-unresolved,
    # 11 X/M items; + 5 T3 items that must NOT enter the marginals.
    full = {c: {} for c in CODERS}
    meta = []
    k = 0

    def add(d1, d3, journal, n, twist=None):
        nonlocal k
        for _ in range(n):
            iid = f"y{k:03d}"
            k += 1
            for c in CODERS:
                full[c][iid] = rec(iid, d1, "pro", d3, "alpha")
            if twist == "d1_3way":
                full["a"][iid] = rec(iid, "S1", "pro", d3, "alpha")
                full["b"][iid] = rec(iid, "S2", "pro", d3, "alpha")
                full["c"][iid] = rec(iid, "X", "pro", d3, "alpha")
            if twist == "d2_3way":
                full["a"][iid] = rec(iid, d1, "pro", d3, "alpha")
                full["b"][iid] = rec(iid, d1, "contra", d3, "alpha")
                full["c"][iid] = rec(iid, d1, "neutral", d3, "alpha")
            meta.append({"item_id": iid, "journal": journal, "year": 2019})

    add("S4", "POS", "Religious Studies", 3)
    add("S4", "DEF", "Religious Studies", 4)
    add("S2", "DEF", "Mind", 1)
    add("X", "NA", "Sophia", 10)
    add("S9INVALID", "NA", "Sophia", 0)
    add("M", "NA", "Sophia", 1, twist="d1_3way")   # D1 unresolved
    add("S4", "DEF", "Sophia", 1, twist="d2_3way")  # D2 unresolved (D1 fine, S-coded)
    add("S4", "POS", "Philosophia Christi", 5)      # T3: excluded from marginals

    with tempfile.TemporaryDirectory(prefix="fyield_selftest_") as td:
        cp = []
        for c in CODERS:
            p = os.path.join(td, f"tr_{c}.jsonl")
            cp.append(p)
            with open(p, "w") as f:
                for r in full[c].values():
                    f.write(json.dumps(r) + "\n")
        mp = os.path.join(td, "meta.jsonl")
        with open(mp, "w") as f:
            for r in meta:
                f.write(json.dumps(r) + "\n")

        marg = stage2_marginals(cp, [mp], None, "d1")
        # T1∪T2 items: 3+4+1+10+1+1 = 20; S: 3+4+1+1(d2_3way item, D1=S4) = 9;
        # POS: 3; D1-unresolved: 1
        check("T3 items excluded from marginals", marg["n_t12_tranche_items"] == 20)
        check("S count = 9", marg["s_count"] == 9)
        check("POS count = 3", marg["pos_count"] == 3)
        check("D1-unresolved count = 1", marg["unresolved_count"] == 1)
        marg_all = stage2_marginals(cp, [mp], None, "all")
        check("--excl-dims all also counts the D2-unresolved item",
              marg_all["unresolved_count"] == 2)

        out = evaluate(2500.0, marg, THRESHOLD)
        expect = 2500 * (9 / 20) * (3 / 9) * (1 - 1 / 20)
        check("stage-2 yield matches frozen formula",
              abs(out["projected_den_h1_yield"] - expect) < 1e-9)
        check("no trigger above threshold", out["trigger_expand_before_further_spend"] is False
              and "frozen_expansion_preference_order" not in out)
        out2 = evaluate(2500.0, marg, 400.0)
        check("trigger fires below threshold with frozen expansion order",
              out2["trigger_expand_before_further_spend"] is True
              and out2["frozen_expansion_preference_order"] == EXPANSION_ORDER)

        # ---- FIREWALL assertions: surfaced output must contain no
        # direction/type/tier values or cross-tab structures
        blob = json.dumps(out2).casefold()
        for banned in ('"pro"', '"contra"', '"neutral"', '"alpha"', '"beta"',
                       '"gamma"', "d2_direction", "d4_type", "t3_pro", "t3_contra",
                       "t12_pro", "t12_contra", "item_id", '"def"'):
            check(f"firewall: output free of {banned!r}", banned not in blob)
        allowed_keys = {"spec", "trigger_expand_before_further_spend",
                        "projected_den_h1_yield", "threshold",
                        "n_abstracts_t12_locked", "marginals", "rates",
                        "firewall", "frozen_expansion_preference_order",
                        "expansion_rule"}
        check("firewall: no unregistered top-level fields",
              set(out2.keys()) <= allowed_keys)
        check("firewall: marginals are scalars only",
              all(isinstance(v, (int, float)) for v in out2["marginals"].values()))

        # stage-1 arithmetic (§7.0 calibration T2 stratum: 8/124, 10/59 shape)
        ns = argparse.Namespace(n_abstracts=2513.0, ps=[8, 124], ppos=[10, 59],
                                unres=[5, 69], threshold=THRESHOLD)
        s1 = stage1(ns)
        e1 = 2513 * (8 / 124) * (10 / 59) * (1 - 5 / 69)
        check("stage-1 yield matches frozen formula",
              abs(s1["projected_den_h1_yield"] - e1) < 1e-9)
        # determinism
        check("stage-2 deterministic", stage2_marginals(cp, [mp], None, "d1") == marg)
    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Firewalled DEN-H1 yield trigger (plan §7 / §12 item 10). "
                    "Surfaced outputs: trigger boolean + marginal S/POS counts ONLY.")
    ap.add_argument("--stage1", action="store_true",
                    help="stage-1 (pre-P4) mode: explicit counts, no coded input")
    ap.add_argument("--n-abstracts", type=float,
                    help="locked P2 abstract-bearing T1∪T2 count (freeze recomputation, §7)")
    ap.add_argument("--threshold", type=float, default=THRESHOLD,
                    help="frozen trigger threshold (110)")
    ap.add_argument("--coded", nargs=3, metavar=("A", "B", "C"),
                    help="stage 2: tranche consolidated coder files (a b c)")
    ap.add_argument("--meta", nargs="+", help="stage 2: corpus JSONL(s), venue join (internal)")
    ap.add_argument("--tiers", help="JSON journal->tier overrides")
    ap.add_argument("--excl-dims", choices=["d1", "all"], default="d1",
                    help="unresolved-or-ineligible counting basis (default d1 = §1.3 pilot basis)")
    ap.add_argument("--ps", type=int, nargs=2, metavar=("K", "N"),
                    help="stage 1: P(S) counts")
    ap.add_argument("--ppos", type=int, nargs=2, metavar=("K", "N"),
                    help="stage 1: P(POS|S) counts")
    ap.add_argument("--unres", type=int, nargs=2, metavar=("K", "N"),
                    help="stage 1: unresolved-or-ineligible counts")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.n_abstracts is None:
        die("--n-abstracts is required (locked P2 T1∪T2 abstract-bearing count)", 2)
    if args.stage1:
        if not (args.ps and args.ppos and args.unres):
            die("stage 1 requires --ps --ppos --unres", 2)
        out = stage1(args)
    else:
        if not (args.coded and args.meta):
            die("stage 2 requires --coded A B C and --meta ...", 2)
        marg = stage2_marginals(args.coded, args.meta, args.tiers, args.excl_dims)
        out = evaluate(args.n_abstracts, marg, args.threshold)
    blob = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"[firewalled-yield] trigger="
              f"{out.get('trigger_expand_before_further_spend', out.get('trigger_expand_before_p4_spend'))} "
              f"yield={out['projected_den_h1_yield']:.1f} -> {args.out}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
