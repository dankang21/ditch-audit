#!/usr/bin/env python3
"""P4 batch wrapper around the FROZEN sanitizer (pipeline/02_sanitize/sanitize.py).

Why this exists: the frozen ``sanitize.py`` ``main()`` rewrites
``data/sanitized/{scrub_log,exclusions}.jsonl`` in place ("w" mode, whole-run
log). Both files are listed per-SHA256 in ``PREREG_MANIFEST.txt`` Section C
(BATCH data/sanitized, files=6), so running the frozen entrypoint on a P4 batch
would mutate freeze-snapshot files and void the guardian verification.

This wrapper imports the frozen module UNMODIFIED and reuses ``process()``
verbatim — identical record-level sanitization logic, identical RAW -> OUT
paths for the batch file itself — and redirects only the run logs to
batch-suffixed paths (``scrub_log_<name>.jsonl`` / ``exclusions_<name>.jsonl``).
Freeze-listed files are never opened for writing; batch names that would
collide with one are refused. Post-freeze operational tooling: no method
change, no new sanitization behavior.

Usage: sanitize_batch.py <raw-basename> [...]   (e.g. tranche_ckpt)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sanitize as S  # noqa: E402  FROZEN module (manifest item24) — imported, never edited

# data/sanitized files listed per-SHA256 in PREREG_MANIFEST.txt Section C.
FROZEN_LISTED = {
    "calib_sample.jsonl",
    "exclusions.jsonl",
    "gold_anchors.jsonl",
    "pilot_ijpr2015.jsonl",
    "pilot_rs2015.jsonl",
    "scrub_log.jsonl",
}


def main(argv: list[str]) -> int:
    names = argv[1:]
    if not names:
        print("usage: sanitize_batch.py <raw-basename> [...]", file=sys.stderr)
        return 2
    for name in names:
        for out_name in (f"{name}.jsonl", f"scrub_log_{name}.jsonl", f"exclusions_{name}.jsonl"):
            if out_name in FROZEN_LISTED:
                print(f"REFUSED: output {out_name} is freeze-listed (PREREG_MANIFEST Section C)",
                      file=sys.stderr)
                return 3
        if not (S.RAW / f"{name}.jsonl").exists():
            print(f"REFUSED: input not found: data/raw/{name}.jsonl", file=sys.stderr)
            return 2

    S.OUT.mkdir(parents=True, exist_ok=True)
    for name in names:
        log: list = []
        excluded: list = []
        lowtext: list = []
        written = S.process(name, log, excluded, lowtext)
        with (S.OUT / f"scrub_log_{name}.jsonl").open("w", encoding="utf-8") as f:
            for e in log:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        with (S.OUT / f"exclusions_{name}.jsonl").open("w", encoding="utf-8") as f:
            for e in excluded:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"=== sanitize_batch {name} ===")
        print(f"  written: {written}")
        print(f"  scrub_log entries: {len(log)} -> data/sanitized/scrub_log_{name}.jsonl")
        print(f"  excluded: {len(excluded)} -> {[e['item_id'] for e in excluded]}")
        print(f"  LOWTEXT items: {len(lowtext)} -> {lowtext}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
