#!/usr/bin/env python3
# STUB — tri-family blind coder runner (zero-human design, codebook v1.1).
# Prereqs: Python 3.10+, stdlib urllib (or provider SDKs).
# Env (.env): ANTHROPIC_API_KEY (A), GOOGLE_API_KEY + CODER_B_PROVIDER=google (B),
#             OPENAI_API_KEY (C, adjudicator). Optional coder D = open-weights archival.
#
# HARD RULES (coder-runner agent, CLAUDE.md rules 1 & 5):
#   - Prompt = pipeline/03_code/coder_prompt.txt ONLY (docs/codebook-v1.md is BANNED;
#     the output schema is embedded in the prompt's [OUTPUT] block).
#   - Before any call: recompute sha256(coder_prompt.txt) and match the LAST line
#     of PROMPT_MANIFEST.txt; mismatch -> abort.
#   - Substitute {{text}} / {{text_extra}}; call coders A, B, C independently
#     (temperature 0; pinned dated snapshots; log provider version headers per call
#     — validation-battery B1).
#   - Validate output against the prompt-embedded schema; 1 retry on parse failure,
#     then record {"item_id": ..., "parse_fail": true}.
#   - Checkpoint every 50 items (resume on restart); append per-call cost + model IDs
#     to data/coded/cost_log.md.
# Out: data/coded/{batch}_a.jsonl, {batch}_b.jsonl, {batch}_c.jsonl
raise SystemExit("stub: implement per coder-runner agent spec (see .claude/agents/coder-runner.md)")
