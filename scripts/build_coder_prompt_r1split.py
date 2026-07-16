#!/usr/bin/env python3
# Builds pipeline/03_code/coder_prompt_r1split.txt — the R1 10-step
# split-grain BUILD-VARIANT prompt (analysis-plan v1.1 §8 R1; §12 item 9
# resolution (a); freeze-manifest item 23: "R1 split-rule build-variant
# prompt").
#
# Scope (plan §8): the 10-step grain splits S3 into unicity/aseity vs
# sovereignty and S4 via the Mill finite-god cut. Splits cannot be recovered
# from coded data; they require a scoped supplementary coding pass (S3- and
# S4-coded items only, same frozen coders) under "a frozen two-way split
# rule appended as a build-variant prompt — never a modification of the
# primary prompt". Accordingly:
#   * docs/codebook-v1.md is NOT modified; the split-rule fragment lives in
#     THIS script as a constant (the variant codebook fragment of record);
#   * pipeline/03_code/coder_prompt.txt is NOT touched; the variant is a
#     separate build artifact (coder_prompt_r1split.txt);
#   * the variant prompt does NOT reveal the item's prior D1 code (coder
#     independence preserved): the sub-step key is conditional on the
#     coder's OWN D1 assignment; the S3/S4 item selection happens
#     driver-side, post hoc;
#   * the FIREWALL check is IDENTICAL to the primary build: the FORBIDDEN
#     token list is imported from scripts/build_coder_prompt.py (in sync by
#     construction), as are the section extractor, preamble and tail;
#   * the manifest line appended to pipeline/03_code/PROMPT_MANIFEST.txt
#     carries codebook=<hash> prompt=<primary on-disk hash>
#     r1split_prompt=<variant hash>, so run_coders.py's last-line
#     `prompt=` verification of the PRIMARY prompt keeps passing (asserted
#     before writing).
# Prereqs: Python 3.10+, stdlib only. Run from repo root.

import argparse
import hashlib
import importlib.util
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_BUILDER = ROOT / "scripts" / "build_coder_prompt.py"
CODEBOOK = ROOT / "docs" / "codebook-v1.md"
PRIMARY_PROMPT = ROOT / "pipeline" / "03_code" / "coder_prompt.txt"
OUT = ROOT / "pipeline" / "03_code" / "coder_prompt_r1split.txt"
MANIFEST = ROOT / "pipeline" / "03_code" / "PROMPT_MANIFEST.txt"

# run_coders.py's exact primary-prompt manifest regex (asserted against the
# appended line so the primary verification can never break).
RUN_CODERS_PROMPT_RE = re.compile(r"\bprompt=([0-9a-f]{64})\b")
R1SPLIT_RE = re.compile(r"\br1split_prompt=([0-9a-f]{64})\b")

# ---------------------------------------------------------------------------
# VARIANT CODEBOOK FRAGMENT OF RECORD (manifest item 23). The two-way split
# rules below are the frozen R1 10-step definitions; the primary codebook is
# untouched. Written to pass the identical firewall scan.
# ---------------------------------------------------------------------------
R1_FRAGMENT = """
## R1. Sub-step refinement (build-variant; supplementary pass)

This variant adds ONE key to the output schema: `d1_substep`. First code all
dimensions exactly as specified above; then refine your own D1 assignment as
follows. Never let the sub-step change D1–D4.

**If your D1 = S3**, assign `d1_substep` by the component the primary
conclusion most directly supports or opposes:

| Code | Sub-thesis |
|---|---|
| S3a | Unicity/aseity: the agent is unique, a se, uncreated — it depends on nothing and has no rivals or peers |
| S3b | Sovereignty: everything other than the agent ontologically depends on it (creation, grounding, conservation of all else) |

Decision rule: the argument's differentiating premise decides — a premise
about the agent's own independence, necessity, or uniqueness → S3a; a
premise about the dependence of everything else on the agent → S3b. If the
item treats both components as one inseparable package with no differential
bearing, code S3a.

**If your D1 = S4**, assign `d1_substep` by the Mill finite-god cut:

| Code | Sub-thesis |
|---|---|
| S4a | Moral character: the ultimate is perfectly good (vs indifferent, evil, or morally imperfect) |
| S4b | Unlimitedness: the good ultimate is unlimited in power and scope (vs a Mill-style finite or limited deity) |

Decision rule: a verdict about the ultimate's moral character (goodness,
indifference, malevolence) → S4a; a verdict about whether goodness is
combined with unlimited power — finite-god proposals, or solutions that
limit the ultimate's power and offer the limitation as its actual
description → S4b. If both components are equally load-bearing, code S4a.

**Any other D1 value** → `d1_substep` = NA.

Output: return the same JSON schema as above with one additional key,
placed after "d1_step":
"d1_substep": "S3a|S3b|S4a|S4b|NA"
"""


def load_primary_builder():
    """Import scripts/build_coder_prompt.py (main() is __main__-guarded; the
    import runs no I/O). Supplies FORBIDDEN, PREAMBLE, TAIL and
    extract_sections — firewall and extraction identical by construction."""
    spec = importlib.util.spec_from_file_location("build_coder_prompt",
                                                  PRIMARY_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def firewall_scan(prompt: str, forbidden) -> list:
    """Identical scan semantics to the primary build (case-insensitive
    substring). Returns the sorted list of hits (empty = clean)."""
    low = prompt.lower()
    return sorted({t for t in forbidden if t in low})


def build_variant_prompt(md: str, bp) -> str:
    """Compose the variant prompt from the codebook text. Pure function;
    deterministic."""
    body = bp.extract_sections(md, ["3.", "4.", "5.", "6."])
    marker = "You will assign four codes."
    if marker not in bp.PREAMBLE:
        raise SystemExit(
            "primary PREAMBLE changed: expected sentence not found — "
            "re-align the variant preamble derivation before building")
    preamble = bp.PREAMBLE.replace(
        marker,
        "You will assign four codes and one sub-step refinement "
        "(final section).")
    return preamble + "\n" + body + "\n" + R1_FRAGMENT.strip() + "\n" + bp.TAIL


def manifest_line(stamp: str, h_cb: str, h_primary: str, h_variant: str) -> str:
    return (f"{stamp} codebook={h_cb} prompt={h_primary} "
            f"r1split_prompt={h_variant}")


def verify_manifest_compat(line: str, h_primary: str, h_variant: str):
    """The appended line must (a) yield the PRIMARY hash to run_coders.py's
    regex (its verification reads the LAST manifest line) and (b) carry the
    variant hash under its own token."""
    m = RUN_CODERS_PROMPT_RE.search(line)
    if not m or m.group(1) != h_primary:
        raise SystemExit(
            "manifest line would break run_coders.py's primary verification: "
            f"{line!r}")
    m2 = R1SPLIT_RE.search(line)
    if not m2 or m2.group(1) != h_variant:
        raise SystemExit(f"manifest line lost the variant hash: {line!r}")


def last_manifest_entry(manifest_text: str) -> str:
    last = ""
    for ln in manifest_text.splitlines():
        if ln.strip():
            last = ln.strip()
    return last


def build(write: bool = True) -> dict:
    bp = load_primary_builder()
    md = CODEBOOK.read_text(encoding="utf-8")
    prompt = build_variant_prompt(md, bp)

    hits = firewall_scan(prompt, bp.FORBIDDEN)
    if hits:
        low = prompt.lower()
        for t in hits:
            i = low.find(t)
            print(f"FIREWALL VIOLATION: token '{t}' at offset {i}: "
                  f"...{prompt[max(0, i - 40):i + 40]!r}...", file=sys.stderr)
        raise SystemExit(1)
    for ph in ("{{text}}", "{{text_extra}}"):
        if ph not in prompt:
            raise SystemExit(f"missing placeholder {ph}")
    for needle in ("S3a", "S3b", "S4a", "S4b", "d1_substep"):
        if needle not in prompt:
            raise SystemExit(f"variant fragment lost required element {needle}")

    h_cb = hashlib.sha256(md.encode()).hexdigest()
    h_variant = hashlib.sha256(prompt.encode()).hexdigest()

    # primary-prompt integrity: the on-disk primary must match the last
    # manifest entry (both its prompt hash and the codebook hash), else the
    # primary is stale relative to the codebook and must be rebuilt first.
    if not PRIMARY_PROMPT.exists() or not MANIFEST.exists():
        raise SystemExit("primary prompt/manifest missing — run "
                         "scripts/build_coder_prompt.py first")
    h_primary = hashlib.sha256(PRIMARY_PROMPT.read_bytes()).hexdigest()
    last = last_manifest_entry(MANIFEST.read_text(encoding="utf-8"))
    m = RUN_CODERS_PROMPT_RE.search(last)
    if not m or m.group(1) != h_primary:
        raise SystemExit(
            "on-disk coder_prompt.txt does not match the last manifest entry "
            "— refusing to append a variant line over a broken primary state")
    mcb = re.search(r"\bcodebook=([0-9a-f]{64})\b", last)
    if not mcb or mcb.group(1) != h_cb:
        raise SystemExit(
            "codebook changed since the last primary build — rebuild the "
            "primary prompt (scripts/build_coder_prompt.py) before the "
            "variant, so both derive from the same codebook version")

    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = manifest_line(stamp, h_cb, h_primary, h_variant)
    verify_manifest_compat(line, h_primary, h_variant)

    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(prompt, encoding="utf-8")
        with MANIFEST.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"built {OUT.relative_to(ROOT)} ({len(prompt)} chars)")
        print(f"firewall clean; manifest appended: codebook={h_cb[:12]}... "
              f"prompt={h_primary[:12]}... r1split_prompt={h_variant[:12]}...")
    return {"prompt": prompt, "h_cb": h_cb, "h_primary": h_primary,
            "h_variant": h_variant, "line": line}


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    bp = load_primary_builder()

    # firewall list identity BY CONSTRUCTION (imported, not copied)
    check("FORBIDDEN list is the primary builder's own object",
          firewall_scan("uses the h" + "ypothesis word", bp.FORBIDDEN)
          == ["hypothes"])
    check("firewall scan clean on a neutral string",
          firewall_scan("assign the sub-step by the differentiating premise",
                        bp.FORBIDDEN) == [])

    # variant composition from the real codebook (in-memory, no writes)
    md = CODEBOOK.read_text(encoding="utf-8")
    prompt = build_variant_prompt(md, bp)
    check("variant passes the identical firewall scan",
          firewall_scan(prompt, bp.FORBIDDEN) == [])
    check("variant keeps the primary coding sections",
          "## 3." in prompt and "## 4." in prompt and "## 5." in prompt
          and "## 6." in prompt)
    check("variant carries the split fragment (S3a/S3b/S4a/S4b, Mill cut)",
          all(s in prompt for s in ("S3a", "S3b", "S4a", "S4b",
                                    "Mill finite-god cut", "d1_substep")))
    check("variant preamble announces the extra key",
          "one sub-step refinement" in prompt)
    check("placeholders intact",
          "{{text}}" in prompt and "{{text_extra}}" in prompt)
    check("substep never overrides the primary dimensions (wording present)",
          "Never let the sub-step change D1–D4." in prompt)
    check("variant does not reveal any prior code to the coder",
          "previously coded" not in prompt.lower()
          and "was coded" not in prompt.lower())
    check("build is deterministic", build_variant_prompt(md, bp) == prompt)

    # the variant fragment must not touch the primary artifacts
    check("output path is the variant file, not the primary",
          OUT.name == "coder_prompt_r1split.txt"
          and PRIMARY_PROMPT.name == "coder_prompt.txt" and OUT != PRIMARY_PROMPT)

    # manifest-line compatibility with run_coders.py's verification
    h_cb = "c" * 64
    h_p = "a" * 64
    h_v = "b" * 64
    line = manifest_line("2026-01-01T00:00:00Z", h_cb, h_p, h_v)
    m = RUN_CODERS_PROMPT_RE.search(line)
    check("run_coders regex extracts the PRIMARY hash from the variant line",
          m is not None and m.group(1) == h_p)
    check("r1split token does not shadow the primary token (word boundary)",
          RUN_CODERS_PROMPT_RE.search(
              "2026 codebook=" + h_cb + " r1split_prompt=" + h_v) is None)
    check("variant hash recoverable under its own token",
          R1SPLIT_RE.search(line).group(1) == h_v)
    try:
        verify_manifest_compat("2026 codebook=x r1split_prompt=" + h_v, h_p, h_v)
        broke = False
    except SystemExit:
        broke = True
    check("compat verifier rejects a line without the primary hash", broke)

    # dry-run against the real repo state: hashes align, nothing written
    before_prompt = PRIMARY_PROMPT.read_bytes()
    before_manifest = MANIFEST.read_bytes()
    r = build(write=False)
    check("dry-run leaves primary prompt and manifest untouched",
          PRIMARY_PROMPT.read_bytes() == before_prompt
          and MANIFEST.read_bytes() == before_manifest)
    check("dry-run primary hash matches the last manifest entry",
          RUN_CODERS_PROMPT_RE.search(
              last_manifest_entry(MANIFEST.read_text())).group(1)
          == r["h_primary"])
    check("dry-run variant prompt equals the in-memory composition",
          r["prompt"] == prompt)
    if OUT.exists():
        check("on-disk variant artifact matches this build",
              hashlib.sha256(OUT.read_bytes()).hexdigest() == r["h_variant"])

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Build the R1 split-grain variant prompt (manifest item 23).")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    build(write=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
