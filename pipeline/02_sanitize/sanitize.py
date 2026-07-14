#!/usr/bin/env python3
# STUB — implements codebook-v1.md §2 (canonical). Prereqs: Python 3.10+, stdlib.
# In:  data/raw/*.jsonl (harvester schema)
# Out: data/sanitized/*.jsonl  -> {"item_id","text","text_extra"}
#      data/sanitized/scrub_log.jsonl -> {"item_id","rule","before","after"}
#
# Pass 1 (mechanical): drop metadata fields; regex scrubs, e.g.
#   r"\bIn this journal\b", r"\bas I (have )?argued in \(?\d{4}\)?",
#   self-citation patterns "(AUTHOR \d{4}[a-z]?)" ONLY when AUTHOR matches the
#   item's own author list (requires raw metadata at scrub time — never emitted).
# Pass 2 (LLM scrub, optional at pilot): flag residual self-identification for
#   human review; do NOT auto-delete borderline content (sanitizer agent rule).
# Keep opponent names (content). Abstracts < 60 words -> populate text_extra, flag LOWTEXT.
raise SystemExit("stub: implement per sanitizer agent spec (see .claude/agents/sanitizer.md)")
