#!/usr/bin/env python3
# Krippendorff's alpha + gold-accuracy harness for ditch-audit (gate G1).
# Prereqs: Python 3.10+, stdlib only. Metrics per codebook-v1 §9:
#   nominal for d1_step / d2_direction / d4_type; ordinal for d3_strength.
# NA handling: nominal dims -> "NA" is a real category (agreement on NA counts);
#   ordinal d3 -> "NA" treated as missing (pairwise exclusion).
#
# Usage:
#   Reliability:  python3 alpha.py rel coded_a.jsonl coded_b.jsonl [coded_c.jsonl ...]
#   Gold check:   python3 alpha.py gold coded_a.jsonl [coded_b.jsonl ...] --gold docs/gold-anchors-v1.json
#   Self-test:    python3 alpha.py selftest
#
# Exit code: 0 if (rel mode) all dimensions pass GATE, else 1. Other modes: 0 on success.

import json
import sys
from collections import Counter, defaultdict

DIMS = {
    "d1_step": "nominal",
    "d2_direction": "nominal",
    "d3_strength": "ordinal",
    "d4_type": "nominal",
}
CS_ORDER = ["CS1", "CS2", "CS3", "CS4", "CS5"]
GATE = 0.70


def krippendorff(units, metric="nominal", order=None):
    """units: iterable of per-item value lists (one value per coder; None = missing).
    Returns alpha (float) or None if not computable. De==0 (single category) -> 1.0."""
    units = [[v for v in u if v is not None] for u in units]
    units = [u for u in units if len(u) >= 2]
    if not units:
        return None
    o = defaultdict(float)  # coincidence matrix
    for u in units:
        m = len(u)
        w = 1.0 / (m - 1)
        for i in range(m):
            for j in range(m):
                if i != j:
                    o[(u[i], u[j])] += w
    n_c = Counter()
    for (c, _k), v in o.items():
        n_c[c] += v
    n = sum(n_c.values())
    if n <= 1:
        return None
    if order is not None:
        unknown = [c for c in n_c if c not in order]
        if unknown:
            raise ValueError(f"values outside declared order: {unknown}")
        cats = [c for c in order if c in n_c]
    else:
        cats = sorted(n_c)

    if metric == "nominal":
        def d2(c, k):
            return 0.0 if c == k else 1.0
    elif metric == "ordinal":
        idx = {c: i for i, c in enumerate(cats)}
        def d2(c, k):
            if c == k:
                return 0.0
            a, b = sorted((idx[c], idx[k]))
            s = sum(n_c[cats[g]] for g in range(a, b + 1)) - (n_c[c] + n_c[k]) / 2.0
            return s * s
    else:
        raise ValueError(f"unknown metric: {metric}")

    Do = sum(v * d2(c, k) for (c, k), v in o.items()) / n
    De = sum(n_c[c] * n_c[k] * d2(c, k) for c in cats for k in cats) / (n * (n - 1))
    if De == 0:
        return 1.0
    return 1.0 - Do / De


def load_jsonl(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out[rec["item_id"]] = rec
    return out


def dim_units(files, dim):
    """files: list of {item_id: record}. Returns per-item value lists for one dimension."""
    ids = set()
    for f in files:
        ids |= set(f)
    ordinal = DIMS[dim] == "ordinal"
    units = []
    for i in sorted(ids):
        vals = []
        for f in files:
            v = f.get(i, {}).get(dim)
            if ordinal and v == "NA":
                v = None  # pairwise exclusion on the ordinal scale
            vals.append(v)
        units.append(vals)
    return units


def cmd_rel(paths):
    files = [load_jsonl(p) for p in paths]
    print(f"reliability: {len(paths)} coders, items(union) = {len(set().union(*[set(f) for f in files]))}")
    print(f"{'dimension':<14}{'metric':<9}{'alpha':>8}  gate>={GATE}")
    ok = True
    for dim, metric in DIMS.items():
        units = dim_units(files, dim)
        order = CS_ORDER if dim == "d3_strength" else None
        a = krippendorff(units, metric, order)
        verdict = "-" if a is None else ("PASS" if a >= GATE else "FAIL")
        ok &= (a is not None and a >= GATE)
        n_used = sum(1 for u in units if sum(v is not None for v in u) >= 2)
        s = "n/a" if a is None else f"{a:8.4f}"
        print(f"{dim:<14}{metric:<9}{s:>8}  {verdict}  (units used: {n_used})")
    print("G1:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def cmd_gold(coder_paths, gold_path):
    gold = json.load(open(gold_path, encoding="utf-8"))["anchors"]
    for cp in coder_paths:
        coded = load_jsonl(cp)
        print(f"\ngold accuracy — {cp} (matching on anchor_id == item_id)")
        for dim in DIMS:
            hit = tot = 0
            misses = []
            for a in gold:
                rec = coded.get(a["anchor_id"])
                if rec is None:
                    continue
                tot += 1
                if rec.get(dim) == a["gold"][dim]:
                    hit += 1
                else:
                    misses.append(f"{a['anchor_id']}:{rec.get(dim)}!={a['gold'][dim]}")
            pct = "n/a" if tot == 0 else f"{hit}/{tot} = {hit/tot:.0%}"
            print(f"  {dim:<14}{pct}   {'; '.join(misses) if misses else ''}")
        missing = [a["anchor_id"] for a in gold if a["anchor_id"] not in coded]
        if missing:
            print(f"  not coded: {missing}")
    print("\ncaveat: famous anchors — accuracy here upper-bounds corpus accuracy (codebook §8).")
    return 0


def selftest():
    # T1: perfect agreement -> 1.0
    assert krippendorff([["a", "a"]] * 10, "nominal") == 1.0
    assert krippendorff([["CS2", "CS2"]] * 10, "ordinal", CS_ORDER) == 1.0
    # T2: hand-computed nominal case: 8 agree (4 aa, 4 bb), 2 cross-disagree -> alpha = 0.62 exactly
    units = [["a", "a"]] * 4 + [["b", "b"]] * 4 + [["a", "b"], ["b", "a"]]
    a = krippendorff(units, "nominal")
    assert abs(a - 0.62) < 1e-12, a
    # T3: ordinal penalizes distant disagreement more than adjacent; nominal identical (equal marginal spread)
    agree = [[c, c] for c in CS_ORDER for _ in range(2)]
    adj = agree + [["CS2", "CS3"], ["CS3", "CS2"]]
    far = agree + [["CS1", "CS5"], ["CS5", "CS1"]]
    a_adj_o = krippendorff(adj, "ordinal", CS_ORDER)
    a_far_o = krippendorff(far, "ordinal", CS_ORDER)
    a_adj_n = krippendorff(adj, "nominal")
    a_far_n = krippendorff(far, "nominal")
    assert a_adj_o > a_far_o, (a_adj_o, a_far_o)
    assert abs(a_adj_n - a_far_n) < 1e-12
    # T4: missing-value handling (pairwise exclusion leaves computable pairs)
    units = [["a", "a", None]] * 5 + [["a", None, "b"]] * 2
    assert krippendorff(units, "nominal") is not None
    print("selftest PASS")
    print(f"  T2 nominal hand-case: alpha = {a:.4f} (expected 0.6200)")
    print(f"  T3 ordinal adjacent vs distant: {a_adj_o:.4f} > {a_far_o:.4f}; nominal equal at {a_adj_n:.4f}")
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__ or "see header comments")
        return 2
    mode = argv[1]
    if mode == "selftest":
        return selftest()
    if mode == "rel":
        return cmd_rel(argv[2:])
    if mode == "gold":
        if "--gold" in argv:
            i = argv.index("--gold")
            gold_path = argv[i + 1]
            coder_paths = argv[2:i]
        else:
            *coder_paths, gold_path = argv[2:]
        return cmd_gold(coder_paths, gold_path)
    print(f"unknown mode: {mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
