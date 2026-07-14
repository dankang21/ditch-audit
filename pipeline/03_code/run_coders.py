#!/usr/bin/env python3
# STUB — dual blind coder runner. Prereqs: Python 3.10+, requests (or anthropic/openai SDKs).
# Env (.env): ANTHROPIC_API_KEY, CODER_B_PROVIDER (openai|google), matching key.
#
# HARD RULES (coder-runner agent, CLAUDE.md rule 1):
#   - Prompt = pipeline/03_code/coder_prompt.txt ONLY.
#   - Before any call: recompute sha256(coder_prompt.txt) and match the LAST line
#     of PROMPT_MANIFEST.txt; mismatch -> abort.
#   - Substitute {{text}} / {{text_extra}}; call coder A and coder B independently.
#   - Validate output against codebook §5 schema; 1 retry on parse failure, then
#     record {"item_id": ..., "parse_fail": true}.
#   - Checkpoint every 50 items (resume on restart); append per-call cost to
#     data/coded/cost_log.md.
# Out: data/coded/{batch}_a.jsonl, data/coded/{batch}_b.jsonl
raise SystemExit("stub: implement per coder-runner agent spec (see .claude/agents/coder-runner.md)")
