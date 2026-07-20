# ditch-audit

**A preregistered zero-human LLM measurement design — and the confirmatory checkpoint that
rejected its instrument.**

This repository is the public audit trail of a study that set out to measure twenty years
(2004–2024) of the peer-reviewed philosophy-of-religion literature — coding ~3,500 articles
for which step of natural theology's inferential chain each addresses, in which direction, at
what claim strength, on what kind of evidence — using a fixed, preregistered, multi-family LLM
instrument with **zero human item-coding**.

**The study halted at its own gate.** At the start of the confirmatory run, the preregistered
fresh-data reliability checkpoint (150 seed-drawn items, dual statistic frozen in advance)
failed on all four coding dimensions. Under the frozen decision tree this stopped all coding;
no hypothesis was ever tested. Per the preregistered kill criterion, the project downgraded to
a methods-forward preprint plus a companion essay — no journal submission.

- **Preprint** (v0.3, 43 pp.): `docs/draft/draft-v0.md` · LaTeX package + compiled PDF:
  `docs/draft/preprint-v0.3.zip` · *(archive DOI: to be added at upload)*
- **Companion essay**: `docs/draft/essay-checkpoint.md` — "The Checkpoint That Killed Our
  Study — and Why We're Glad It Did"
- **Checkpoint result of record**: `analysis/checkpoint_report.md` + `checkpoint_dual_raw.json`

## Why the commit history is part of the paper

The paper's outcome-blindness claim is mechanically checkable here:

| Tag | Commit | What it proves |
|---|---|---|
| `g1-conditional-pass` | `e043fad` | Pilot gate passed — declared conditional on the checkpoint |
| `draft-v0.1-outcome-blind` | `1493e46` | Full paper drafted, Results as empty preregistered shells, **before** any confirmatory run |
| `prereg-content` | `83d0b49` | The artifact set the freeze manifest seals (64 items, SHA256) |
| `p3-freeze` | `bafc712` | Preregistration freeze established (guardian-verified) |
| `p4-checkpoint-fail` | `c894932` | The checkpoint FAIL of record — dual statistic unmet on all dimensions |
| `draft-v0.2-resolution` | `0b359fe` | Shells resolved to the realized (rejection) branch; diff-verifiable change inventory |
| `draft-v0.3` | `4763093` | Preprint repositioning + verified bibliography |

The diff from `draft-v0.1-outcome-blind` to `draft-v0.2-resolution` is the proof object: the
result shells, decision rules, and outcome scenarios predate the result and were not altered
by it — only resolved.

## Repository map

| Path | Contents |
|---|---|
| `docs/` | Frozen instruments of record: codebook (v1.4e), validation battery (v1.3), analysis plan (v1.1), gold anchors, synthetic-item specs, prior-art sweep, outline |
| `docs/draft/` | The preprint (markdown source of truth + generated LaTeX + zip) and essay |
| `PREREG_MANIFEST.txt` | SHA256 freeze manifest (64 artifacts + aggregate hashes) |
| `analysis/` | Guardian verification ledger, G1 pilot gate report, checkpoint report |
| `pipeline/` | Harvest → sanitize → code → battery → analysis scripts (stdlib-only Python) |
| `scripts/` | Reliability harness (`alpha.py`), adjudication, prompt builder (the hypothesis firewall) |
| `CONTEXT.md` | Intellectual lineage and every binding design adjudication, dated |
| `CLAUDE.md` | The operating rules the orchestration ran under (absolute rules incl. the zero-human rule) |

**Not in this repository** (by absolute rule, enforced by `.gitignore` throughout history):
the copyrighted abstract corpora (`data/raw|sanitized|coded`), coder outputs, and the sealed
synthetic vault. Their SHA256 hashes are in the freeze manifest; aggregates and codes ship
with the OSF audit package. API keys were never committed.

## Reproduction

The frozen instrument is re-executable: coder D is a pinned open-weights model
(`qwen3.5:4b`, digest in the manifest) served locally via Ollama, and every analysis script
is stdlib-only Python 3.10+ with fixed seeds (registration date 20260717). See
`pipeline/05_analysis/checkpoint_stats.py selftest` and `scripts/alpha.py selftest` for the
statistic implementations, and the preprint's §4 for the design.

## Authorship & AI disclosure

Jaehoon Kang (design, gate approvals, synthetic-spec sign-off). All item coding was performed
by LLMs under the zero-human rule; prose drafting and orchestration were assisted by an LLM
(Claude). Full disclosure in the preprint's back matter.
