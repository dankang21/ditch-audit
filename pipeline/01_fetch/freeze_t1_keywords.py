#!/usr/bin/env python3
"""freeze_t1_keywords.py — freeze + verify the §4.1 title-keyword list
(analysis-plan v1.1 §11 freeze-manifest item 18: "§4.1 frozen title-keyword
list (era×venue bias table input)").

The list of record is the KEYWORDS constant of
pipeline/01_fetch/fetch_t1_candidates.py (the P2 T1 pre-filter list, kept
verbatim from the P2 T1 spec). Plan §4.1 reuses it as the frozen keyword
list for the era×venue bias table's title-keyword topic profile (mechanical
stdlib tally — no LLM role, preserving the B0 role matrix).

Freeze mechanics (deliberate, per the freeze instruction):
  * the frozen artifact is a COPY: pipeline/01_fetch/t1_keywords_frozen.json;
  * fetch_t1_candidates.py is NOT refactored to read that file (the P2
    harvest provenance script stays byte-identical to what ran);
  * this script is the consistency selfcheck binding the two: `--check`
    (default) verifies the frozen JSON equals the in-script list exactly
    (order-sensitive) and that the recorded source-script SHA256 still
    matches; any drift is a freeze violation (exit 5).

`--write` (re)generates the frozen JSON deterministically (no timestamp;
sorted keys; byte-identical re-runs). --selftest exercises the check logic
on fixtures and then runs the real check.

stdlib-only, Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_SCRIPT = os.path.join(PKG_DIR, "fetch_t1_candidates.py")
FROZEN_JSON = os.path.join(PKG_DIR, "t1_keywords_frozen.json")
SOURCE_REL = "pipeline/01_fetch/fetch_t1_candidates.py"


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_source_keywords(path: str = SOURCE_SCRIPT) -> list:
    """Execute fetch_t1_candidates.py's source in a fresh namespace (module
    level runs no I/O — it only defines constants/functions and imports
    fetch_pilot, same property) and return its KEYWORDS constant. The source
    text is exec'd directly (never via importlib bytecode caches) so the
    check always reads the bytes on disk."""
    with open(path, encoding="utf-8") as f:
        src_text = f.read()
    ns = {"__file__": path, "__name__": "_t1_keywords_freeze_check"}
    sys.path.insert(0, os.path.dirname(path))
    try:
        exec(compile(src_text, path, "exec"), ns)
    finally:
        sys.path.pop(0)
    kws = ns.get("KEYWORDS")
    if not isinstance(kws, list) or not all(isinstance(k, str) for k in kws):
        die(f"{path}: KEYWORDS constant missing or malformed")
    return list(kws)


def frozen_blob(keywords: list, source_sha: str) -> dict:
    return {
        "lock": "t1_keywords_frozen",
        "spec": "plan v1.1 §11 item 18 — §4.1 frozen title-keyword list "
                "(era×venue bias table input)",
        "generation_rule": (
            "verbatim, order-preserving copy of the KEYWORDS constant in "
            + SOURCE_REL + " (the P2 T1 recall-first pre-filter list). The "
            "source script is NOT refactored to read this file; "
            "freeze_t1_keywords.py --check verifies copy/script identity."),
        "match_rule": (
            "case-insensitive substring match (inflections via partial "
            "substrings), as in the source script; §4.1 applies it as a "
            "mechanical stdlib tally over TITLES for the era×venue bias "
            "table (the T1 pre-filter matched title ∪ abstract)."),
        "source_script": SOURCE_REL,
        "source_script_sha256": source_sha,
        "count": len(keywords),
        "keywords": keywords,
    }


def write_frozen(json_path: str = FROZEN_JSON, source_path: str = SOURCE_SCRIPT) -> dict:
    kws = load_source_keywords(source_path)
    blob = frozen_blob(kws, sha256_file(source_path))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(blob, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"[freeze] {len(kws)} keyword(s) -> {json_path}")
    print(f"[freeze] sha256={sha256_file(json_path)}")
    return blob


def check(json_path: str = FROZEN_JSON, source_path: str = SOURCE_SCRIPT) -> list:
    """Return a list of drift findings (empty = consistent)."""
    problems = []
    if not os.path.exists(json_path):
        return [f"frozen file missing: {json_path}"]
    blob = json.load(open(json_path, encoding="utf-8"))
    kws_script = load_source_keywords(source_path)
    kws_frozen = blob.get("keywords")
    if kws_frozen != kws_script:
        set_f, set_s = set(kws_frozen or []), set(kws_script)
        problems.append(
            "keyword lists differ (order-sensitive): "
            f"only-frozen={sorted(set_f - set_s)} "
            f"only-script={sorted(set_s - set_f)} "
            f"order_or_dup_drift={set_f == set_s}")
    if blob.get("count") != len(kws_script):
        problems.append(f"count field {blob.get('count')} != {len(kws_script)}")
    actual_sha = sha256_file(source_path)
    if blob.get("source_script_sha256") != actual_sha:
        problems.append(
            "source script changed since freeze: recorded "
            f"{blob.get('source_script_sha256')} != actual {actual_sha}")
    return problems


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    import tempfile
    ok = True

    def rep(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    with tempfile.TemporaryDirectory(prefix="t1kw_selftest_") as td:
        src = os.path.join(td, "fetch_t1_candidates.py")
        with open(src, "w") as f:
            f.write('KEYWORDS = ["alpha term", "beta", "gamma-cut"]\n')
        jp = os.path.join(td, "t1_keywords_frozen.json")

        blob = write_frozen(jp, src)
        rep("write copies the in-script list verbatim",
            blob["keywords"] == ["alpha term", "beta", "gamma-cut"])
        rep("fresh copy passes the check", check(jp, src) == [])

        b1 = open(jp, "rb").read()
        write_frozen(jp, src)
        rep("re-write byte-identical (no timestamps)",
            open(jp, "rb").read() == b1)

        # keyword drift in the frozen copy is detected
        blob2 = json.load(open(jp))
        blob2["keywords"] = ["alpha term", "beta"]
        json.dump(blob2, open(jp, "w"), indent=1, sort_keys=True)
        rep("frozen-copy drift detected",
            any("keyword lists differ" in p for p in check(jp, src)))

        # script drift is detected (source hash + list comparison)
        write_frozen(jp, src)
        with open(src, "a") as f:
            f.write("KEYWORDS = KEYWORDS + ['smuggled']\n")
        probs = check(jp, src)
        rep("in-script drift detected (list + source hash)",
            any("differ" in p for p in probs)
            and any("source script changed" in p for p in probs))

        # order change alone is a violation (order-sensitive freeze)
        with open(src, "w") as f:
            f.write('KEYWORDS = ["beta", "alpha term", "gamma-cut"]\n')
        write_frozen(jp, src)
        with open(src, "w") as f:
            f.write('KEYWORDS = ["alpha term", "beta", "gamma-cut"]\n')
        rep("order drift detected",
            any("order_or_dup_drift=True" in p for p in check(jp, src)))

    # the real artifact must verify (freeze condition)
    real = check()
    for p in real:
        print(f"  [real-check] {p}")
    rep("REAL frozen list consistent with fetch_t1_candidates.py", real == [])

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Freeze/verify the §4.1 title-keyword list (manifest item 18).")
    ap.add_argument("--write", action="store_true",
                    help="(re)generate t1_keywords_frozen.json from the source script")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.write:
        write_frozen()
        return 0
    problems = check()
    if problems:
        for p in problems:
            print(f"DRIFT: {p}", file=sys.stderr)
        die("t1_keywords_frozen.json inconsistent with fetch_t1_candidates.py "
            "(freeze violation)", 5)
    print("[check] t1_keywords_frozen.json matches the in-script KEYWORDS "
          "list and source hash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
