#!/usr/bin/env python3
"""Mechanical majority-vote adjudication for P1 raw-arm coder disagreements.

Zero human item-judgment (CLAUDE.md absolute rule 5). Every decision here is a
deterministic function of the three coders' output files. No item code is chosen
by a human; the script only tallies A/B/C and applies majority-of-three.

Inputs : data/coded/{pilot_rs2015,gold_anchors}_{a,b,c}.jsonl   (raw arm, 55 items)
         data/coded/stubs_{...}_{a,b,c}.jsonl                    (cue-ablation, B2)
         docs/gold-anchors-v1.json                               (gold codes, diagnostic)
Outputs : JSON blob on stdout with every derived table.
"""
import json, sys, os
from collections import Counter, defaultdict

ROOT = "/home/dk/mobile/dk/ditch-audit"
DIMS = ["d1_step", "d2_direction", "d3_strength", "d4_type"]
GROUPS = ["pilot_rs2015", "gold_anchors"]
CODERS = ["a", "b", "c"]


def load_jsonl(path):
    out = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["item_id"]] = r
    return out


def load_group(prefix):
    return {c: load_jsonl(os.path.join(ROOT, "data/coded", f"{prefix}_{c}.jsonl")) for c in CODERS}


# ---- load coded (raw arm) + stubs -------------------------------------------
coded = {g: load_group(g) for g in GROUPS}
stubs = {g: load_group("stubs_" + g) for g in GROUPS}

# gold codes
gold_raw = json.load(open(os.path.join(ROOT, "docs/gold-anchors-v1.json")))
gold = {a["anchor_id"]: a["gold"] for a in gold_raw["anchors"]}

# ordered item list (pilot then gold), preserving file order
items = []  # (group, item_id)
for g in GROUPS:
    for iid in coded[g]["a"].keys():
        items.append((g, iid))


def majority(vals):
    """vals = [a,b,c]. Returns (verdict, resolved_value_or_None, minority_coder_or_None)."""
    ct = Counter(vals)
    if len(ct) == 1:
        return ("agree", vals[0], None)
    if len(ct) == 3:
        return ("unresolved", None, None)
    # len==2 -> one value x2, one value x1  => 2-1
    maj_val = ct.most_common(1)[0][0]
    min_val = [v for v in ct if v != maj_val][0]
    minority_coder = CODERS[[i for i, v in enumerate(vals) if v == min_val][0]]
    return ("majority", maj_val, minority_coder)


def stub_prediction(g, iid, dim):
    """Cue-ablation (B2) folklore predictor for one (item, dim).
    Returns (mode_value_or_ambiguous, stub_votes_counter)."""
    svals = [stubs[g][c][iid][dim] for c in CODERS]
    ct = Counter(svals)
    top = ct.most_common()
    if len(top) >= 2 and top[0][1] == top[1][1]:
        mode = "AMBIGUOUS"  # no unique stub mode (incl. 3-way stub split)
    else:
        mode = top[0][0]
    return mode, ct


# ---- main pass --------------------------------------------------------------
disagreements = []          # every non-agreeing (item,dim)
matrix = defaultdict(int)   # (minority_coder, dim) -> count  [2-1 only]
cell_detail = defaultdict(list)  # (minority_coder, dim) -> [ (min_val -> maj_val), ...]
unresolved = []
recur_undirected = Counter()  # (dim, frozenset{competing values}) for 2-1 splits
recur_directed = Counter()    # (dim, min_val, maj_val) for 2-1 splits
gold_conflicts = []
gold_unresolved = []

# B6 stub-congruence
b6 = {d: Counter() for d in DIMS}   # dim -> {toward_stub, away_stub, uninformative}
b6_votes = {d: {"maj_gt_min": 0, "min_gt_maj": 0, "tie": 0} for d in DIMS}
b6_detail = []

for (g, iid) in items:
    for dim in DIMS:
        vals = [coded[g][c][iid][dim] for c in CODERS]
        verdict, resolved, minority_coder = majority(vals)
        if verdict == "agree":
            continue
        rec = {
            "group": g, "item_id": iid, "dim": dim,
            "a": vals[0], "b": vals[1], "c": vals[2],
            "a_rat": coded[g]["a"][iid].get("rationale", ""),
            "b_rat": coded[g]["b"][iid].get("rationale", ""),
            "c_rat": coded[g]["c"][iid].get("rationale", ""),
            "verdict": verdict, "resolved": resolved, "minority_coder": minority_coder,
        }
        disagreements.append(rec)

        if verdict == "unresolved":
            unresolved.append(rec)
            if iid in gold:
                gold_unresolved.append({"item_id": iid, "dim": dim, "gold": gold[iid][dim],
                                        "a": vals[0], "b": vals[1], "c": vals[2]})
            continue

        # ---- 2-1 majority ----
        min_val = vals[CODERS.index(minority_coder)]
        matrix[(minority_coder, dim)] += 1
        cell_detail[(minority_coder, dim)].append(f"{min_val}->{resolved}")
        recur_undirected[(dim, frozenset([min_val, resolved]))] += 1
        recur_directed[(dim, min_val, resolved)] += 1

        # gold conflict (diagnostic; gold revision is dk-only, instrument-design)
        if iid in gold:
            gv = gold[iid][dim]
            if resolved != gv:
                gold_conflicts.append({"item_id": iid, "dim": dim, "resolved": resolved,
                                       "gold": gv, "minority_coder": minority_coder,
                                       "min_val": min_val,
                                       "min_matches_gold": (min_val == gv)})

        # ---- B6 stub-congruence ----
        smode, sct = stub_prediction(g, iid, dim)
        maj_stubvotes = sct.get(resolved, 0)
        min_stubvotes = sct.get(min_val, 0)
        if maj_stubvotes > min_stubvotes:
            b6_votes[dim]["maj_gt_min"] += 1
        elif min_stubvotes > maj_stubvotes:
            b6_votes[dim]["min_gt_maj"] += 1
        else:
            b6_votes[dim]["tie"] += 1
        if smode == "AMBIGUOUS" or (smode != resolved and smode != min_val):
            klass = "uninformative"
        elif smode == resolved:
            klass = "toward_stub"
        else:  # smode == min_val
            klass = "away_stub"
        b6[dim][klass] += 1
        b6_detail.append({"item_id": iid, "dim": dim, "resolved": resolved,
                          "min_val": min_val, "stub_mode": smode,
                          "stub_votes": dict(sct), "class": klass})

# ---- aggregate counts -------------------------------------------------------
n_disagree = len(disagreements)
n_majority = sum(1 for d in disagreements if d["verdict"] == "majority")
n_unresolved = len(unresolved)

per_dim = {d: {"disagree": 0, "majority": 0, "unresolved": 0} for d in DIMS}
for d in disagreements:
    per_dim[d["dim"]]["disagree"] += 1
    per_dim[d["dim"]][d["verdict"]] += 1

minority_dist = Counter(d["minority_coder"] for d in disagreements if d["verdict"] == "majority")

# B6 overall
b6_overall = Counter()
for d in DIMS:
    for k, v in b6[d].items():
        b6_overall[k] += v
total_21 = n_majority
congruence_rate = (b6_overall["toward_stub"] /
                   (b6_overall["toward_stub"] + b6_overall["away_stub"])
                   if (b6_overall["toward_stub"] + b6_overall["away_stub"]) else None)

out = {
    "n_items": len(items),
    "n_pilot": len(coded["pilot_rs2015"]["a"]),
    "n_gold": len(coded["gold_anchors"]["a"]),
    "n_cells": len(items) * len(DIMS),
    "n_disagree": n_disagree,
    "n_majority": n_majority,
    "n_unresolved": n_unresolved,
    "per_dim": per_dim,
    "minority_dist": dict(minority_dist),
    "matrix": {f"{k[0]}|{k[1]}": v for k, v in matrix.items()},
    "cell_detail": {f"{k[0]}|{k[1]}": v for k, v in cell_detail.items()},
    "unresolved": unresolved,
    "recur_undirected": {f"{k[0]}|{'/'.join(sorted(k[1]))}": v
                         for k, v in sorted(recur_undirected.items(), key=lambda x: -x[1])},
    "recur_directed": {f"{k[0]}|{k[1]}->{k[2]}": v
                       for k, v in sorted(recur_directed.items(), key=lambda x: -x[1])},
    "gold_conflicts": gold_conflicts,
    "gold_unresolved": gold_unresolved,
    "b6_by_dim": {d: dict(b6[d]) for d in DIMS},
    "b6_votes": b6_votes,
    "b6_overall": dict(b6_overall),
    "b6_congruence_rate_toward": congruence_rate,
    "b6_detail": b6_detail,
    "disagreements": disagreements,
}
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
