#!/usr/bin/env python3
# Self-consistency consolidation (codebook v1.4a §9): a coder's code for an item is
# the per-dimension MAJORITY of three independent identical runs. A three-way split
# takes the run-1 value and flags the item "run_unstable". Deterministic; stdlib-only.
#
# Usage: consolidate_runs.py <batch_name> [<batch_name> ...]
#   reads  data/coded/<batch>.r{1,2,3}_<coder>.jsonl   (coders a,b,c)
#   writes data/coded/<batch>_<coder>.jsonl            (consolidated)
# Non-dimension fields (flags, confidence, rationale, _meta) are taken from run 1;
# per-run values are preserved under "_runs" for the audit package.

import json
import os
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CODED = os.path.join(ROOT, "data", "coded")
DIMS = ("d1_step", "d2_direction", "d3_strength", "d4_type")


def load(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                out[rec["item_id"]] = rec
    return out


def consolidate(batch, coder):
    runs = []
    for r in ("r1", "r2", "r3"):
        p = os.path.join(CODED, f"{batch}.{r}_{coder}.jsonl")
        if not os.path.exists(p):
            raise SystemExit(f"missing run file: {p}")
        runs.append(load(p))
    ids = sorted(runs[0])
    if any(sorted(rn) != ids for rn in runs[1:]):
        raise SystemExit(f"{batch}/{coder}: run item sets differ")
    out_path = os.path.join(CODED, f"{batch}_{coder}.jsonl")
    n_unstable = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for iid in ids:
            base = dict(runs[0][iid])  # run-1 record carries non-dimension fields
            unstable = []
            for d in DIMS:
                vals = [rn[iid].get(d) for rn in runs]
                top, k = Counter(vals).most_common(1)[0]
                if k >= 2:
                    base[d] = top
                else:  # three-way split: run-1 value, flagged
                    base[d] = vals[0]
                    unstable.append(d)
            if unstable:
                n_unstable += 1
                base.setdefault("flags", [])
                if "run_unstable" not in base["flags"]:
                    base["flags"] = list(base["flags"]) + ["run_unstable"]
                base["run_unstable_dims"] = unstable
            base["_runs"] = {d: [rn[iid].get(d) for rn in runs] for d in DIMS}
            f.write(json.dumps(base, ensure_ascii=False) + "\n")
    print(f"[consolidate] {batch}/{coder}: {len(ids)} items -> {out_path}"
          f" (3-way splits: {n_unstable})")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: consolidate_runs.py <batch_name> ...")
    for batch in sys.argv[1:]:
        for coder in "abc":
            consolidate(batch, coder)


if __name__ == "__main__":
    main()
