# ditch-audit

**A preregistered zero-human LLM measurement design — and the confirmatory checkpoint that
rejected its instrument.**

This repository is the public audit trail of a study that set out to measure twenty-one issue-years
(2004–2024) of the peer-reviewed philosophy-of-religion literature — coding ~3,500 articles
for which step of natural theology's inferential chain each addresses, in which direction, at
what claim strength, on what kind of evidence — using a fixed, preregistered, multi-family LLM
instrument with **zero human item-coding**.

**The study halted at its own gate.** At the start of the confirmatory run, the preregistered
fresh-data reliability checkpoint (150 seed-drawn items, dual statistic frozen in advance)
failed on all four coding dimensions. Under the frozen decision tree this stopped all coding;
no hypothesis was ever tested. Per the preregistered kill criterion, the project downgraded to
a methods-forward preprint plus a companion essay — no journal submission.

- **Repository**: <https://github.com/dankang21/ditch-audit>
- **Preprint** (v0.8, 58 pp.): `docs/draft/draft-v0.md` · LaTeX package + compiled PDF:
  `docs/draft/preprint-v0.8.zip` · *(archive DOI: to be added at upload)*
- **Companion essay**: `docs/draft/essay-checkpoint.md` — "The Checkpoint That Killed Our
  Study — and Why We're Glad It Did"
- **Checkpoint result of record**: `analysis/checkpoint_report.md` + `checkpoint_dual_raw.json`

## Outcome-blindness evidence

This repository publishes the **full, dated development history** (85+ commits,
phase-tagged). The commits of record for the paper's central evidentiary claim — that the
result shells, decision rules, and outcome scenarios predate the result — are directly
inspectable:

| tag | commit | what it seals |
|---|---|---|
| `prereg-content` | `83d0b49` | preregistration content of record |
| `p3-freeze` | `bafc712` | freeze manifest sealed (guardian CLEAN) |
| `draft-v0.1-outcome-blind` | `1493e46` | full draft with neutral result shells, before any confirmatory run |
| `p4-checkpoint-fail` | `c894932` | checkpoint FAIL of record |
| `draft-v0.2-resolution` | `0b359fe` | shells resolved to *not run*; no shell rewritten |

`analysis/audit-exports/draft-v0.1-to-v0.2.diff` remains as a convenient extract of the
v0.1 → v0.2 comparison. Two verification anchors are independent of git metadata (commit
timestamps alone are not tamper-proof): the freeze manifest (`PREREG_MANIFEST.txt`) pins the
frozen artifact set by SHA256, so any copy can be checked against the seal, and the OSF
registration's own timestamp externally anchors the ordering of freeze and checkpoint.

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
| `CLAUDE.md` | The operating rules the orchestration ran under (absolute rules incl. the zero-human rule). In Korean, per the project's language convention; English translation: `docs/operating-rules-en.md` |
| `.claude/agents/` | Orchestration agent definitions — published as firewall evidence: `coder-runner.md` names the documents coder-facing contexts were forbidden to receive, and `prereg-guardian.md` specifies the freeze verification run each session. In Korean; translated in `docs/operating-rules-en.md` |
| `docs/operating-rules-en.md` | Non-normative English translation of `CLAUDE.md` and all six agent definitions (the Korean originals are the operative artifacts and are unchanged) |

**Not in this repository** (excluded by design, absolute rule 3): the copyrighted abstract
corpora (`data/raw|sanitized|coded`), coder outputs, and the sealed synthetic vault. Their
SHA256 hashes are in the freeze manifest; aggregates and codes ship with the OSF audit
package. API keys live only in an untracked `.env` and appear nowhere in this release.

## Reproduction

The frozen instrument is re-executable: coder D is a pinned open-weights model
(`qwen3.5:4b`, digest in the manifest) served locally via Ollama, and every analysis script
is stdlib-only Python 3.10+ with fixed seeds (registration date 20260717). See
`pipeline/05_analysis/checkpoint_stats.py selftest` and `scripts/alpha.py selftest` for the
statistic implementations, and the preprint's §4 for the design.

## License

Code (`scripts/`, `pipeline/`, `.claude/`): **MIT** — see `LICENSE`.
Documents (`docs/` including the preprint and essay, `analysis/`, `CLAUDE.md`, `CONTEXT.md`,
this README): **CC BY 4.0** — see `LICENSE-docs`.

## Authorship & AI disclosure

Jaehoon Kang (ORCID [0009-0008-1020-9533](https://orcid.org/0009-0008-1020-9533); design, gate approvals, synthetic-spec sign-off). Repository commits are
authored as `dk` and `Daniel Kang` under a single email (see `.mailmap`, which normalizes
the display name); all three names refer to the same person. The history is published
as-is — rewriting it to normalize names would change every commit hash and void the
hash-anchored evidence above. All item coding was performed
by LLMs under the zero-human rule; prose drafting and orchestration were assisted by an LLM
(Claude). Full disclosure in the preprint's back matter.
