# ditch-audit

Empirical meta-study of the peer-reviewed philosophy-of-religion literature:
step x direction x claim strength x epistemic type x venue, over the 8-step
inferential chain from "external cause" to Nicene theism.

Canonical documents: `docs/` (outline v0.3, P0 sweep report, codebook v1, gold anchors).
Operating rules for Claude Code: `CLAUDE.md`. Intellectual lineage: `CONTEXT.md`.

Quickstart:
  git init && git add -A && git commit -m "seed: ditch-audit v1"
  cp .env.example .env   # add API keys (never committed)
  python3 scripts/build_coder_prompt.py        # builds the firewalled coder prompt
  python3 scripts/alpha.py selftest            # verify the reliability harness
Then follow the P1 checklist in CLAUDE.md.
