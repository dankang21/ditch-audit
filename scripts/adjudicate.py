#!/usr/bin/env python3
"""Mechanical majority-vote adjudication for coder disagreements.

Zero human item-judgment (CLAUDE.md absolute rule 5). Every decision here is a
deterministic function of the three coders' output files. No item code is chosen
by a human; the script only tallies A/B/C and applies majority-of-three.

Two datasets (identical mechanical rule; different plumbing only):

  (default, no args)  Round-1 raw arm, 55 items
      data/coded/{pilot_rs2015,gold_anchors}_{a,b,c}.jsonl   (coded)
      data/coded/stubs_{...}_{a,b,c}.jsonl                    (cue-ablation, B2)
      docs/gold-anchors-v1.json                               (gold codes, diagnostic)
    Output is byte-identical to the pre-refactor script (regression-pinned).

  (--dataset all89)   v1.4a majority-of-3 consolidated union, 89 items
      data/coded/all89_{a,b,c}.jsonl                          (coded; RS35+gold20+IJPR34)
      stubs cover only the 55 RS+gold items; the 34 IJPR items have no stub
      (B6 congruence audit is computed over stub-covered 2-1 resolutions only).
      Gold D3 codes are legacy-mapped CS1-3->DEF, CS4-5->POS (codebook v1.4 §12).

Outputs : JSON blob on stdout with every derived table.
"""
import json, sys, os
from collections import Counter, defaultdict

ROOT = "/home/dk/mobile/dk/ditch-audit"
DIMS = ["d1_step", "d2_direction", "d3_strength", "d4_type"]
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


# ---- dataset specs ----------------------------------------------------------
# A spec resolves the input files into a flat model:
#   coded_flat : {coder: {iid: rec}}
#   stub_flat  : {coder: {iid: rec}}          (may omit iids -> no stub coverage)
#   gold       : {iid: {dim: val}}            (diagnostic gold codes)
#   group_of   : {iid: group_label}
#   items      : [iid, ...]                   (deterministic order)
#   size_keys  : [(out_key, count), ...]      (emitted right after n_items)

def spec_default():
    """Round-1 raw arm; 2 groups loaded as whole files. Byte-identical plumbing."""
    groups = ["pilot_rs2015", "gold_anchors"]
    coded_flat = {c: {} for c in CODERS}
    stub_flat = {c: {} for c in CODERS}
    group_of, items = {}, []
    counts = {}
    for g in groups:
        per = {c: load_jsonl(os.path.join(ROOT, "data/coded", f"{g}_{c}.jsonl")) for c in CODERS}
        st = {c: load_jsonl(os.path.join(ROOT, "data/coded", f"stubs_{g}_{c}.jsonl")) for c in CODERS}
        counts[g] = len(per["a"])
        for c in CODERS:
            coded_flat[c].update(per[c])
            stub_flat[c].update(st[c])
        for iid in per["a"].keys():
            group_of[iid] = g
            items.append(iid)
    gold_raw = json.load(open(os.path.join(ROOT, "docs/gold-anchors-v1.json")))
    gold = {a["anchor_id"]: a["gold"] for a in gold_raw["anchors"]}
    return {
        "coded_flat": coded_flat, "stub_flat": stub_flat, "gold": gold,
        "group_of": group_of, "items": items,
        "size_keys": [("n_pilot", counts["pilot_rs2015"]), ("n_gold", counts["gold_anchors"])],
    }


def spec_all89():
    """v1.4a consolidated union (89). Single coded file; group by membership;
    stubs cover RS+gold only; IJPR (34) have no stub."""
    coded_flat = {c: load_jsonl(os.path.join(ROOT, "data/coded", f"all89_{c}.jsonl")) for c in CODERS}
    # stub coverage = RS + gold stub files, merged; IJPR items are absent.
    stub_flat = {c: {} for c in CODERS}
    for sg in ["stubs_pilot_rs2015", "stubs_gold_anchors"]:
        for c in CODERS:
            stub_flat[c].update(load_jsonl(os.path.join(ROOT, "data/coded", f"{sg}_{c}.jsonl")))
    gold_raw = json.load(open(os.path.join(ROOT, "docs/gold-anchors-v1.json")))
    gold = {a["anchor_id"]: dict(a["gold"]) for a in gold_raw["anchors"]}
    # codebook v1.4 §12: legacy CS gold D3 codes map CS1-3->DEF, CS4-5->POS *at
    # scoring* (D3 was collapsed to {DEF,POS,NA}). Normalize gold D3 so conflict
    # flags compare like-with-like; the coded values are already v1.4 codes.
    cs_map = {"CS1": "DEF", "CS2": "DEF", "CS3": "DEF", "CS4": "POS", "CS5": "POS"}
    for a in gold.values():
        a["d3_strength"] = cs_map.get(a["d3_strength"], a["d3_strength"])
    # group membership from the source group files (id lists only)
    rs_ids = set(load_jsonl(os.path.join(ROOT, "data/coded", "pilot_rs2015_a.jsonl")))
    ijpr_ids = set(load_jsonl(os.path.join(ROOT, "data/coded", "pilot_ijpr2015_a.jsonl")))
    group_of = {}
    for iid in coded_flat["a"]:
        if iid in gold:
            group_of[iid] = "gold_anchors"
        elif iid in rs_ids:
            group_of[iid] = "pilot_rs2015"
        elif iid in ijpr_ids:
            group_of[iid] = "pilot_ijpr2015"
        else:
            group_of[iid] = "unknown"
    items = list(coded_flat["a"].keys())
    counts = Counter(group_of.values())
    return {
        "coded_flat": coded_flat, "stub_flat": stub_flat, "gold": gold,
        "group_of": group_of, "items": items,
        "size_keys": [("n_rs2015", counts["pilot_rs2015"]),
                      ("n_gold", counts["gold_anchors"]),
                      ("n_ijpr2015", counts["pilot_ijpr2015"])],
    }


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


def stub_prediction(stub_flat, iid, dim):
    """Cue-ablation (B2) folklore predictor for one (item, dim).
    Returns (mode_or_'AMBIGUOUS', stub_votes_counter), or (None, None) if the
    item has no stub coverage for all three coders (e.g. IJPR)."""
    if not all(iid in stub_flat[c] for c in CODERS):
        return None, None
    svals = [stub_flat[c][iid][dim] for c in CODERS]
    ct = Counter(svals)
    top = ct.most_common()
    if len(top) >= 2 and top[0][1] == top[1][1]:
        mode = "AMBIGUOUS"  # no unique stub mode (incl. 3-way stub split)
    else:
        mode = top[0][0]
    return mode, ct


def run(spec):
    coded_flat = spec["coded_flat"]
    stub_flat = spec["stub_flat"]
    gold = spec["gold"]
    group_of = spec["group_of"]
    items = spec["items"]

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
    b6_no_coverage = Counter()  # dim -> count of 2-1 resolutions with no stub coverage

    for iid in items:
        g = group_of[iid]
        for dim in DIMS:
            vals = [coded_flat[c][iid][dim] for c in CODERS]
            verdict, resolved, minority_coder = majority(vals)
            if verdict == "agree":
                continue
            rec = {
                "group": g, "item_id": iid, "dim": dim,
                "a": vals[0], "b": vals[1], "c": vals[2],
                "a_rat": coded_flat["a"][iid].get("rationale", ""),
                "b_rat": coded_flat["b"][iid].get("rationale", ""),
                "c_rat": coded_flat["c"][iid].get("rationale", ""),
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
            smode, sct = stub_prediction(stub_flat, iid, dim)
            if smode is None:
                b6_no_coverage[dim] += 1
                continue
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

    # ---- aggregate counts ---------------------------------------------------
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
    congruence_rate = (b6_overall["toward_stub"] /
                       (b6_overall["toward_stub"] + b6_overall["away_stub"])
                       if (b6_overall["toward_stub"] + b6_overall["away_stub"]) else None)

    out = {"n_items": len(items)}
    for k, v in spec["size_keys"]:
        out[k] = v
    out["n_cells"] = len(items) * len(DIMS)
    out["n_disagree"] = n_disagree
    out["n_majority"] = n_majority
    out["n_unresolved"] = n_unresolved
    out["per_dim"] = per_dim
    out["minority_dist"] = dict(minority_dist)
    out["matrix"] = {f"{k[0]}|{k[1]}": v for k, v in matrix.items()}
    out["cell_detail"] = {f"{k[0]}|{k[1]}": v for k, v in cell_detail.items()}
    out["unresolved"] = unresolved
    out["recur_undirected"] = {f"{k[0]}|{'/'.join(sorted(k[1]))}": v
                               for k, v in sorted(recur_undirected.items(), key=lambda x: -x[1])}
    out["recur_directed"] = {f"{k[0]}|{k[1]}->{k[2]}": v
                             for k, v in sorted(recur_directed.items(), key=lambda x: -x[1])}
    out["gold_conflicts"] = gold_conflicts
    out["gold_unresolved"] = gold_unresolved
    out["b6_by_dim"] = {d: dict(b6[d]) for d in DIMS}
    out["b6_votes"] = b6_votes
    out["b6_overall"] = dict(b6_overall)
    out["b6_congruence_rate_toward"] = congruence_rate
    if sum(b6_no_coverage.values()):
        out["b6_no_stub_coverage"] = dict(b6_no_coverage)
    out["b6_detail"] = b6_detail
    out["disagreements"] = disagreements
    return out


def main():
    argv = sys.argv[1:]
    if "--dataset" in argv:
        i = argv.index("--dataset")
        ds = argv[i + 1] if i + 1 < len(argv) else ""
    else:
        ds = "default"
    if ds == "default":
        spec = spec_default()
    elif ds == "all89":
        spec = spec_all89()
    else:
        sys.exit(f"unknown --dataset {ds!r} (use: all89)")
    out = run(spec)
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
