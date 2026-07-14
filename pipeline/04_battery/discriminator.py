#!/usr/bin/env python3
"""discriminator.py — real-vs-synthetic discrimination test (validation
battery arm).

Mixes REAL sanitized abstracts with SYNTHETIC ones (path argument; the file
may not exist yet elsewhere — schema assumed {"item_id","text",...}), shuffles
them with a fixed seed, and asks each coder family (pins/endpoints reused from
pipeline/03_code/run_coders.py) for a bare REAL/SYNTHETIC verdict. No
rationale is requested (verdict-only prompt). This is a probe, NOT a coding
run: coder_prompt.txt is never used. Every call is fresh and independent.

Only the `text` field is sent for BOTH arms — `text_extra` is withheld because
its mere presence (gold last paragraphs) would leak the REAL label.

Output: data/battery/discriminator_<tag>.jsonl, one line per item x family:
  {"item_id", "family", "label_true": "REAL"|"SYNTHETIC",
   "label_pred": "REAL"|"SYNTHETIC"|null, "response"}
plus a per-family stdout summary: accuracy, TPR/FPR/TNR (positive class =
REAL), and balanced accuracy = (TPR+TNR)/2 as the AUC approximation for a
hard binary verdict (per spec: no Mann-Whitney). Unparseable verdicts count
in denominators and as errors in accuracy.

Existing (item_id, family) pairs are skipped on restart; failed calls are not
written (retried on rerun).

Usage:
  python3 pipeline/04_battery/discriminator.py \
      --real data/sanitized/pilot_rs2015.jsonl --synthetic data/battery/synthetic.jsonl \
      --seed 7 [--tag mytag] [--families a,b,c] [--limit N]
  python3 pipeline/04_battery/discriminator.py --smoke [--seed 7]
      (built-in dummy items with dummy labels; real API calls, no research
       item text; writes only data/battery/smoke_discriminator.jsonl)
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import battery_common as bc

DISC_PROMPT = (
    "Is the following abstract from a REAL published journal article or "
    "SYNTHETIC (machine-written for a study)? Reply exactly REAL or SYNTHETIC."
)

MAX_CONSECUTIVE_ERRORS = 3
_VERDICT_RE = re.compile(r"\b(REAL|SYNTHETIC)\b")

# Built-in SYNTHETIC dummies for --smoke. The REAL/SYNTHETIC labels below are
# dummy fixtures (every text is machine-written for this script).
SMOKE_REAL = [
    {"item_id": "SMOKE-DISC-R1",
     "text": ("This synthetic validation abstract reports an invented survey of "
              "forty coastal lighthouse stations and their entirely fictional "
              "maintenance ledgers, written only to exercise a pipeline.")},
    {"item_id": "SMOKE-DISC-R2",
     "text": ("A dummy abstract claiming, for testing purposes alone, that "
              "imaginary garden mazes can be ranked by hedge topology.")},
]
SMOKE_SYNTH = [
    {"item_id": "SMOKE-DISC-S1",
     "text": ("Another machine-written placeholder abstract: it asserts nothing "
              "about any real literature and exists to test a REAL/SYNTHETIC "
              "verdict parser.")},
    {"item_id": "SMOKE-DISC-S2",
     "text": ("Fabricated stub abstract number four, describing a nonexistent "
              "replication of a nonexistent study of nonexistent tide tables.")},
]


def parse_verdict(response: str):
    m = _VERDICT_RE.search((response or "").upper())
    return m.group(1) if m else None


def build_probe(item: dict) -> str:
    return DISC_PROMPT + "\n\n[ABSTRACT]\n" + (item.get("text") or "")


def load_done_pairs(path: str) -> set:
    done = set()
    if os.path.exists(path):
        for rec in bc.read_jsonl(path):
            if rec.get("item_id") and rec.get("family"):
                done.add((rec["item_id"], rec["family"]))
    return done


def summarize(out_path: str, families: list, providers: dict):
    recs = {}
    if os.path.exists(out_path):
        for rec in bc.read_jsonl(out_path):
            recs[(rec.get("item_id"), rec.get("family"))] = rec  # last wins
    print(f"\n[summary] {os.path.basename(out_path)} (positive class = REAL; "
          "balanced accuracy approximates AUC for a hard verdict)")
    for fam in families:
        rows = [r for (_, f), r in recs.items() if f == fam]
        n_real = sum(1 for r in rows if r["label_true"] == "REAL")
        n_syn = sum(1 for r in rows if r["label_true"] == "SYNTHETIC")
        tp = sum(1 for r in rows if r["label_true"] == "REAL" and r["label_pred"] == "REAL")
        tn = sum(1 for r in rows if r["label_true"] == "SYNTHETIC" and r["label_pred"] == "SYNTHETIC")
        fp = sum(1 for r in rows if r["label_true"] == "SYNTHETIC" and r["label_pred"] == "REAL")
        invalid = sum(1 for r in rows if r["label_pred"] is None)
        tpr = tp / n_real if n_real else float("nan")
        tnr = tn / n_syn if n_syn else float("nan")
        fpr = fp / n_syn if n_syn else float("nan")
        bal = (tpr + tnr) / 2 if n_real and n_syn else float("nan")
        acc = (tp + tn) / len(rows) if rows else float("nan")
        model = providers[fam].model if fam in providers else "?"
        print(f"  family {fam} ({model}): n={len(rows)} (real={n_real} synth={n_syn}) "
              f"acc={acc:.3f} TPR={tpr:.3f} FPR={fpr:.3f} TNR={tnr:.3f} "
              f"balanced_acc(~AUC)={bal:.3f} invalid={invalid}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Real-vs-synthetic discriminator probe.")
    ap.add_argument("--real", help="REAL sanitized JSONL")
    ap.add_argument("--synthetic", help="SYNTHETIC JSONL ({'item_id','text',...})")
    ap.add_argument("--seed", type=int, default=7, help="shuffle seed (default 7)")
    ap.add_argument("--tag", help="output tag (default <real>_vs_<synth>_s<seed>)")
    ap.add_argument("--families", default="a,b,c")
    ap.add_argument("--limit", type=int, default=None, help="cap on shuffled item count")
    ap.add_argument("--smoke", action="store_true",
                    help="built-in dummy items; writes smoke_discriminator.jsonl")
    args = ap.parse_args(argv)

    families = bc.parse_families(args.families)
    bc.ensure_battery_dir()
    m = bc.rc()

    if args.smoke:
        real_items, syn_items = SMOKE_REAL, SMOKE_SYNTH
        out_path = os.path.join(bc.BATTERY_DIR, "smoke_discriminator.jsonl")
        if os.path.exists(out_path):
            os.remove(out_path)  # smoke runs are idempotent
    else:
        if not args.real or not args.synthetic:
            bc.die("--real and --synthetic are both required unless --smoke", 2)
        real_path, syn_path = m.resolve_path(args.real), m.resolve_path(args.synthetic)
        for p in (real_path, syn_path):
            if not os.path.exists(p):
                bc.die(f"file not found: {p}", 2)
        real_items, syn_items = bc.read_jsonl(real_path), bc.read_jsonl(syn_path)
        tag = args.tag or f"{bc.batch_tag(real_path)}_vs_{bc.batch_tag(syn_path)}_s{args.seed}"
        out_path = os.path.join(bc.BATTERY_DIR, f"discriminator_{tag}.jsonl")

    pool = [dict(it, _label="REAL") for it in real_items] + \
           [dict(it, _label="SYNTHETIC") for it in syn_items]
    ids = [it.get("item_id") for it in pool]
    if len(ids) != len(set(ids)) or not all(ids):
        bc.die("item_id collision or missing item_id across real/synthetic inputs", 4)
    random.Random(args.seed).shuffle(pool)
    if args.limit is not None:
        pool = pool[: args.limit]

    providers = bc.make_providers(families)  # fail fast on missing keys
    done = load_done_pairs(out_path)
    print(f"[disc] {len(pool)} shuffled item(s) (seed={args.seed}) x families "
          f"{','.join(families)} -> {out_path} (resume: {len(done)} pair(s) done)")
    print("[disc] coding prompt NOT loaded — verdict-only probe prompt")

    errors = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for fam in families:
            provider = providers[fam]
            consecutive = 0
            for item in pool:
                iid = item["item_id"]
                if (iid, fam) in done:
                    continue
                try:
                    text, _meta = bc.call_provider(provider, build_probe(item))
                except m.HTTPCallError as e:
                    errors += 1
                    consecutive += 1
                    print(f"  [error] {iid} family={fam}: HTTP {e.status}: {e.body[:200]}",
                          file=sys.stderr)
                    if consecutive >= MAX_CONSECUTIVE_ERRORS:
                        print(f"  [abort] family {fam}: {consecutive} consecutive errors",
                              file=sys.stderr)
                        break
                    continue
                consecutive = 0
                rec = {"item_id": iid, "family": fam, "label_true": item["_label"],
                       "label_pred": parse_verdict(text), "response": text}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                done.add((iid, fam))
                if args.smoke:
                    print(f"[smoke:{fam}] {iid}: true={rec['label_true']} "
                          f"pred={rec['label_pred']}")

    summarize(out_path, families, providers)
    if errors:
        print(f"[disc] {errors} call error(s) — rerun to retry missing pairs", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
