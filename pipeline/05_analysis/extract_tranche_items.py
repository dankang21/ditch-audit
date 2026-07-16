#!/usr/bin/env python3
"""Materialize a tranche's raw items from the locked P2 corpus, by manifest ids.

``build_checkpoint_tranche.py`` (frozen, manifest item 15) emits an id-only
manifest (OSF-publishable — no abstract text). Coding needs the actual records,
so this script joins the manifest's ``item_ids_sorted`` back against the same
locked corpus files and writes a raw batch JSONL for the sanitizer.

Guarantees:
  * corpus-drift guard — every input file's SHA256 is recomputed and compared
    against the hash recorded IN the tranche manifest; any mismatch aborts
    (the draw is only valid against the exact bytes it was drawn from);
  * verbatim pass-through — matched records are copied as their ORIGINAL JSONL
    lines (no re-serialization), preserving byte-identity with the locked corpus;
    enforced, not assumed: a matched line that is not strip-invariant
    (line != stripped + "\n") aborts instead of silently normalizing;
  * completeness — every manifest id must be found exactly once; duplicate ids
    across files take the first occurrence in manifest input order (mirrors the
    builder's dedup rule, which recorded dup_dropped for the draw);
  * output order = ``item_ids_sorted`` (deterministic; re-runs byte-identical).

Post-freeze operational tooling: reads frozen artifacts, writes only new files.

Usage: extract_tranche_items.py --manifest <tranche_manifest.json> --out data/raw/<name>.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="tranche manifest JSON (id list + input hashes)")
    ap.add_argument("--out", required=True, help="output raw batch JSONL (must not already exist)")
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        man = json.load(f)
    ids = man["item_ids_sorted"]
    want = set(ids)
    if len(want) != len(ids):
        print("ABORT: manifest id list contains duplicates", file=sys.stderr)
        return 2

    out_path = args.out if os.path.isabs(args.out) else os.path.join(REPO_ROOT, args.out)
    if os.path.exists(out_path) or os.path.islink(out_path):
        print(f"ABORT: output already exists (refusing to overwrite): {out_path}", file=sys.stderr)
        return 2

    # manifest input paths are data-only: refuse reads outside <repo>/data
    data_root = os.path.join(os.path.realpath(REPO_ROOT), "data") + os.sep
    for inp in man["inputs"]:
        path = inp["path"] if os.path.isabs(inp["path"]) else os.path.join(REPO_ROOT, inp["path"])
        if not os.path.realpath(path).startswith(data_root):
            print(f"ABORT: manifest input escapes data/: {path}", file=sys.stderr)
            return 2

    # corpus-drift guard: recompute every recorded input hash before reading a line
    for inp in man["inputs"]:
        path = inp["path"] if os.path.isabs(inp["path"]) else os.path.join(REPO_ROOT, inp["path"])
        actual = sha256_file(path)
        if actual != inp["sha256"]:
            print(f"ABORT: corpus drift — {path}\n  manifest {inp['sha256']}\n  actual   {actual}",
                  file=sys.stderr)
            return 3

    lines: dict[str, str] = {}
    for inp in man["inputs"]:
        path = inp["path"] if os.path.isabs(inp["path"]) else os.path.join(REPO_ROOT, inp["path"])
        with open(path, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                iid = json.loads(stripped)["item_id"]
                if iid in want and iid not in lines:
                    if line != stripped + "\n":
                        print(f"ABORT: matched line for {iid} is not strip-invariant "
                              f"(would be normalized, breaking verbatim guarantee): {path}",
                              file=sys.stderr)
                        return 5
                    lines[iid] = stripped

    missing = [i for i in ids if i not in lines]
    if missing:
        print(f"ABORT: {len(missing)} manifest ids not found in corpus: {missing[:5]}...",
              file=sys.stderr)
        return 4

    with open(out_path, "w", encoding="utf-8") as f:
        for iid in ids:
            f.write(lines[iid] + "\n")

    print(f"[extract] {len(ids)} items -> {out_path}")
    print(f"[extract] sha256(out) = {sha256_file(out_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
