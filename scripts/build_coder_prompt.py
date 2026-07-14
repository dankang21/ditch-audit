#!/usr/bin/env python3
# Builds pipeline/03_code/coder_prompt.txt from docs/codebook-v1.md.
# THE ONLY SANCTIONED WAY to produce the coder prompt (CLAUDE.md absolute rule 1).
# - extracts codebook sections 3 (procedure), 4 (dimensions + edge anchors),
#   5 (output schema), 6 (synthetic worked examples)
# - wraps with the fixed preamble of codebook §7
# - FIREWALL CHECK: refuses to emit if hypothesis-leaking tokens appear
# - appends SHA256 of codebook + prompt to pipeline/03_code/PROMPT_MANIFEST.txt
# Prereqs: Python 3.10+, stdlib only. Run from repo root.

import hashlib
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODEBOOK = ROOT / "docs" / "codebook-v1.md"
OUT = ROOT / "pipeline" / "03_code" / "coder_prompt.txt"
MANIFEST = ROOT / "pipeline" / "03_code" / "PROMPT_MANIFEST.txt"

# Tokens that would leak study expectations into the coder's context.
FORBIDDEN = [
    "h1", "h2", "hypothes", "predict", "topography", "headwind",
    "contested", "frozen", "prereg", "lessing",
    # v1.1a firewall-audit additions (hypothesis-adjacent design vocabulary)
    "stereotyp", "folklore", "battery", "expected", "criterion",
    "gold", "vault", "launder",
]

PREAMBLE = """You are coding one sanitized journal-article abstract for a study of
argumentative structure in philosophy of religion. You will assign four codes.
Do not guess the author or venue; if you recognize the text, ignore that
recognition and code only what the text asserts.

Procedure: relevance -> special classes -> step -> direction (net effect on the
STEP thesis, tracing reply-chains) -> strength -> type (deletion test) ->
confidence, flags, one-sentence rationale (<= 40 words). Return JSON only,
matching the output schema exactly.
"""

TAIL = """
TEXT TO CODE:
{{text}}
{{text_extra}}
"""


def extract_sections(md: str, wanted_prefixes):
    """Split on '## ' headings; return concatenated bodies of wanted sections."""
    parts = re.split(r"(?m)^## ", md)
    keep = []
    for p in parts[1:]:
        header, _, body = p.partition("\n")
        if any(header.strip().startswith(w) for w in wanted_prefixes):
            keep.append(f"## {header}\n{body.strip()}\n")
    if len(keep) != len(wanted_prefixes):
        raise SystemExit(
            f"section extraction mismatch: wanted {wanted_prefixes}, got {len(keep)}"
        )
    return "\n".join(keep)


def main():
    md = CODEBOOK.read_text(encoding="utf-8")
    body = extract_sections(md, ["3.", "4.", "5.", "6."])
    prompt = PREAMBLE + "\n" + body + TAIL

    low = prompt.lower()
    hits = sorted({t for t in FORBIDDEN if t in low})
    if hits:
        for t in hits:
            i = low.find(t)
            print(f"FIREWALL VIOLATION: token '{t}' at offset {i}: "
                  f"...{prompt[max(0, i-40):i+40]!r}...", file=sys.stderr)
        raise SystemExit(1)
    for ph in ("{{text}}", "{{text_extra}}"):
        if ph not in prompt:
            raise SystemExit(f"missing placeholder {ph}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(prompt, encoding="utf-8")
    h_cb = hashlib.sha256(md.encode()).hexdigest()
    h_pr = hashlib.sha256(prompt.encode()).hexdigest()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(f"{stamp} codebook={h_cb} prompt={h_pr}\n")
    print(f"built {OUT.relative_to(ROOT)} ({len(prompt)} chars)")
    print(f"firewall clean; manifest appended: codebook={h_cb[:12]}... prompt={h_pr[:12]}...")


if __name__ == "__main__":
    main()
