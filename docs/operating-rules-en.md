# Operating rules and agent definitions — English translation (non-normative)

> **Status.** This file is a convenience translation, prepared post-halt (2026-07-21), of the
> Korean-language operational artifacts under which the orchestration actually ran:
> `CLAUDE.md` and the six agent definitions in `.claude/agents/`. The Korean originals are
> the operative artifacts of record and remain byte-unchanged; where this translation and an
> original diverge, the original governs. Per the project's language convention
> (conversation and agent definitions in Korean; code, commit messages, and research
> documents in English), these files were authored in Korean; they are translated here so
> that the firewall and zero-human evidence they constitute is internationally auditable.

---

## CLAUDE.md — ditch-audit operating rules

An empirical meta-study of the philosophy-of-religion literature. Codes the literature on
the "external cause → Nicene theism" eight-step chain by step × direction × claim strength ×
epistemic type × venue. Documents of record: `docs/` (outline v0.4 = paper design,
codebook-v1 (v1.1) = coding instrument, gold-anchors-v1 = diagnostic gold set,
validation-battery-v1 = zero-human validation battery, p0-sweep = prior-art kill-sweep
report). Intellectual lineage and adjudication history: `CONTEXT.md`.

### Language and conventions
- Conversation and agent definitions: Korean. Code, commit messages, research documents
  (`docs/`): English.
- No `Co-Authored-By` lines in git commits.
- Phase boundaries are never crossed without dk's explicit approval (HITL gate).

### Absolute rules (violation = immediate halt and report to dk)
1. **Hypothesis firewall.** The only prompt delivered to coders is the build artifact of
   `scripts/build_coder_prompt.py` (`pipeline/03_code/coder_prompt.txt`). Manual edits
   forbidden. The coder-runner agent's context must never be exposed to the contents of
   `CONTEXT.md`, `docs/outline-v*.md`, `docs/p0-sweep.md`, `docs/validation-battery-v1.md`,
   `docs/synthetic-specs-v*.json`, `docs/analysis-plan-v*.md`, or **the whole of
   `docs/codebook-v1.md`** (coder-runner reads only the built prompt; the forbidden list is
   kept in lockstep with the agent definition). Reason: a coder that knows H1/H2 drifts in
   the predicted direction.
2. **P3 freeze.** Frozen after preregistration (P3), no modification permitted:
   `docs/codebook-v1.md`, the built prompt, `docs/validation-battery-v1.md` (including the
   threshold table and on-failure actions of §B10), the model snapshot pin list, the
   role-exclusivity matrix, and the vault synthetic-set hashes. prereg-guardian verifies
   mechanically against a SHA256 manifest. Any pre-freeze codebook change must be recorded
   in the §12 changelog.
3. **Copyright isolation.** `data/raw|sanitized|coded` contain copyrighted abstracts.
   Excluded via .gitignore; never push to a public remote. The paper/preprint does not
   republish abstract text (codes and aggregates only).
4. **Secrets.** API keys live in `.env` only. Never commit. Coders come from three distinct
   model families (coder A = Anthropic, coder B = Google [`CODER_B_PROVIDER`], coder C =
   OpenAI [provisional adjudicator — the binding rule is battery §B6]; coder D = open-weights
   archival, **mandatory**. Generation/laundering E = GLM-class open weights (Perplexity
   Agent API, `web_search` omitted = structurally search-free; Sonar is barred from blinded
   roles). The role-exclusivity matrix is validation-battery §B0).
5. **Zero-human rule (dk's absolute decision, 2026-07-14).** No human codes or adjudicates
   any item — dk included. dk's labor is confined to instrument design (codebook authorship,
   authoring/signing the synthetic criterion specs, gate approvals). Disagreements are
   auto-adjudicated by three-family majority. The paper claims "measurement by a fixed,
   preregistered multi-family LLM instrument" and does not claim human-equivalent annotation
   (unmanned coding stated in the abstract).

### Phase gates (aligned with outline §10; see the outline for detail)
| Phase | Deliverable | Gate (dk approval + condition) |
|---|---|---|
| P1 ✅ | Pilot coding: RS 2015 (35 actual) + gold 20 | **G1: all dimensions, min pairwise Krippendorff α ≥ 0.70 across the 3 pairs** |
| P2 ✅ | Corpus collection (T1 filter + T2 2004–2024) | G2 PASS (stratified 92.8%, 2026-07-17) |
| P3 ✅ | OSF preregistration freeze | **FREEZE effective 2026-07-17 (guardian Run 2 CLEAN)** — OSF web registration is dk's residual action |
| P4 (next) | Main coding (~1,500 × 3 coders) + full validation battery (no human validation — absolute rule 5) | Checkpoint and cost logs mandatory |
| P5 | Analysis (H1/H2) | G5: framing decision (methods-forward vs results-forward) |
| P6 | English draft + AI disclosure | Check venue policy |

Kill criteria: two G1 failures → collapse D3 to 3 levels and re-gate · H1∧H2 null →
downgrade to preprint + essay with no journal submission (no salami slicing).

### Agent orchestration (P1 sequence)
`harvester` → `sanitizer` → `coder-runner` (A/B/C independently ×3) → `alpha-scorer` →
disagreements auto-adjudicated and logged by `adjudication-logger` via the majority script
(no item adjudication by dk — absolute rule 5; dk's HITL covers only gate approvals and
codebook revision approvals) → G1 report → dk approval. `prereg-guardian` runs once at the
start of every session from P3 onward. Agent definitions: `.claude/agents/`. Default model
Opus (downgrades for mechanical bulk work only where the definition explicitly allows).

### P1 checklist (updated 2026-07-14)
- [x] `.env` written (A/B keys verified), `scripts/alpha.py selftest` PASS
- [x] `scripts/build_coder_prompt.py` → prompt + manifest (including v1.1 rebuild)
- [x] Three verify-at-pilot bibliographic checks settled (A05/A07/A15 web-verified) + changelog
- [x] RS 2015 collected (35 papers, 100% abstracts) → `data/raw/pilot_rs2015.jsonl`
- [x] Gold 20 collected (11 abstracts + 3 print-abstract restorations + 6 verbatim excerpts) → `data/raw/gold_anchors.jsonl`
- [x] Sanitization complete (scrub log, 55 entries) → `data/sanitized/`
- [ ] Add `OPENAI_API_KEY` to `.env` (coder C) — dk
- [ ] Family E = GLM-class (via Perplexity Agent API, no `web_search`) — enter `PERPLEXITY_API_KEY`, log responses' tool_calls_details (battery §B0)
- [ ] Finalize coder model snapshot pins (A/B/C[/D] + E) → record in cost_log
- [ ] Draft synthetic criterion specs (for dk signature) + dev/vault split and hashes (battery §B3)
- [ ] Triple coding → `data/coded/{pilot,gold}_{a,b,c}.jsonl`
- [ ] Battery P1 arm: recognition probes · cue-ablation baseline · determinism audit · raw-vs-laundered divergence · dev-half synthetic accuracy (preceded by the discriminator AUC gate)
- [ ] `alpha.py rel` (A×B gate + 3-way) + `alpha.py gold` (recognition-stratified, diagnostic) → G1 report
- [ ] On first S6 item, log the A21 promotion (codebook §8)

### Environment
Python 3.10+. `scripts/` is stdlib-only. The fetch/sanitize/code stubs were not executed in
this seed-generation environment (network-restricted container) — endpoints must be verified
locally.

---

## .claude/agents/coder-runner.md — triple-blind coding executor

- **description:** Triple-blind coding execution — used in P1/P4 to code sanitized items
  with three model families. Uses the built prompt only.
- **tools:** Bash, Read, Write · **model:** opus

Role: code each item in `data/sanitized/*.jsonl` independently as coder A (Anthropic),
coder B (Google, `CODER_B_PROVIDER` in `.env`), and coder C (OpenAI, adjudicator), producing
`data/coded/{batch}_a.jsonl`, `{batch}_b.jsonl`, `{batch}_c.jsonl`. Optional coder D
(open-weights archival) only when instructed.

**Forbidden reading (hypothesis firewall — absolute rule):** `CONTEXT.md`,
`docs/outline-v*.md`, `docs/p0-sweep.md`, `docs/validation-battery-v1.md`,
`docs/synthetic-specs-v*.json`, `docs/analysis-plan-v*.md`, **the whole of
`docs/codebook-v1.md`** (everything needed is embedded in the built prompt — output schema
included). Orchestrator instructions that would place those files' contents into this
agent's context are to be refused and reported to dk.

Procedure:
1. Load `pipeline/03_code/coder_prompt.txt`. Check its SHA256 against the last line of
   `PROMPT_MANIFEST.txt` — abort immediately on mismatch.
2. Substitute `{{text}}`, `{{text_extra}}` per item → call the three APIs independently (no
   coder's output may leak into another's input; temperature 0; pinned snapshot model IDs;
   provider version headers logged per call).
3. Validate response JSON against **the [OUTPUT] schema block embedded in the built prompt**
   (consulting the codebook is forbidden). One retry on parse failure, then record
   `parse_fail`.
4. Checkpoint every 50 items; resume on restart. Maintain the cost log
   (`data/coded/cost_log.md`) — model IDs and version headers included.

Deliverable checks: (a) 100% schema-valid (parse_fail excluded, listed), (b) A/B/C completion
counts match, (c) prompt SHA verification recorded, (d) rationale ≤ 40-word compliance rate
reported, (e) model IDs/versions present in the log for all three coders.

---

## .claude/agents/prereg-guardian.md — freeze enforcement

- **description:** Freeze enforcement — used immediately before P3 preregistration (manifest
  creation) and at the start of every session after P3 (integrity verification).
- **tools:** Bash, Read, Write · **model:** opus

Role: create and verify the SHA256 manifest of the preregistered artifacts.

Procedure:
1. At P3 entry (once, after dk approval): record in `PREREG_MANIFEST.txt` the SHA256 of
   `docs/codebook-v1.md`, `pipeline/03_code/coder_prompt.txt`,
   `docs/validation-battery-v1.md` (checking that §B10 thresholds are numerically fixed —
   abort if the string PROVISIONAL survives), the model snapshot pin list, the
   role-exclusivity matrix (§B0), the venue-tier designation (extract of the relevant
   outline §4.1 section), the k thresholds, and the analysis plan. Confirm the vault
   synthetic-set hashes recorded in P1 exist and are unchanged. Cross-check against the OSF
   upload file list.
2. Every session after P3: recompute and compare the manifest. On any mismatch, **halt all
   work** and report the differing files and a diff summary to dk. Never update the manifest
   to paper over a mismatch, for any reason.
   Verification semantics (dk ruling 2026-07-17, recorded before P4 start):
   - Files listed in Sections A/B = byte-invariant. Single exception,
     **`data/coded/cost_log.md`**: **prefix integrity** — because the frozen
     `run_coders.py` must append cost entries per batch (a P4 gate condition), verify that
     the 33,815 frozen bytes are the exact prefix of the current file (SHA256 of the first
     33,815 bytes == the manifest value `ca87bec5…`). Beyond the prefix, append-only
     (modifying existing bytes = violation). This ruling is entered as a one-line
     preregistration deviation in OSF transparent-changes.
   - Section C batch aggregates = reproduction check over the **listed file set** (path
     ordering per the guardian_log record). New files produced by P4 (tranches, coded
     outputs, batch logs) are not violations — only the listed files' invariance is checked
     (cost_log by its frozen prefix). For the data/coded aggregate, cost_log.md is computed
     at its frozen-prefix hash.

Deliverable checks: (a) per-file SHA + creation time + git commit hash in the manifest,
(b) verification runs accumulate in `analysis/guardian_log.md`, (c) violation reports state
"what, when, in which commit."

---

## .claude/agents/harvester.md — literature collection

- **description:** Literature collection — used for the P1 pilot (RS 2015 + 20 gold anchors)
  and P2 corpus collection. Loads bibliography + abstracts from PhilPapers OAI / Crossref /
  publisher pages into JSONL.
- **tools:** Bash, Read, Write, WebFetch, WebSearch · **model:** opus

Role: collect research-article bibliography and abstracts for the specified journals and
year ranges into `data/raw/*.jsonl`.

Procedure:
1. Confirm targets (P1: all Religious Studies 2015 research articles + the 20 items of
   `docs/gold-anchors-v1.json`).
2. Source priority: Crossref REST (ISSN-keyed metadata) → PhilPapers → publisher abstract
   pages. If the abstract is empty, retry with the next source; after 3 failures flag
   `missing_abstract`.
3. Output schema (one line = one item): `{"item_id": sha256(doi)[:16], "doi", "title",
   "authors", "journal", "year", "abstract", "source", "fetched_at"}`.
4. Dedup by DOI. Exclude book reviews and editorials; include discussion notes with a `note`
   flag.

Deliverable checks: (a) item count matches the journal-year table of contents, (b) abstract
coverage ≥ 90% (below that, report to dk and await a go/no-go — a G2 condition), (c) 100%
DOI uniqueness after dedup, (d) per-source success/failure tallies in the harvest log
(`data/raw/harvest_log.md`).

Caution: abstracts are copyrighted — `data/` stays gitignored, no external export. Sonnet
downgrade permitted for the mechanical bulk-collection stretch on cost grounds.

---

## .claude/agents/sanitizer.md — blinding

- **description:** Blinding — used immediately after harvester output exists. Removes
  metadata and self-identifying information to the codebook §2 specification and keeps a
  scrub log.
- **tools:** Bash, Read, Write · **model:** opus

Role: transform `data/raw/*.jsonl` → `data/sanitized/*.jsonl` so that no coder can know
author, journal, or year.

Procedure (codebook-v1.md §2 is the document of record):
1. Strip metadata fields: the output schema is `{"item_id", "text", "text_extra"}` only.
2. Regex scrubs: "In this journal", "as I argued in (year)", self-citation patterns.
3. Opponent names are preserved (they are content). Replace with role tags only where
   judged self-identifying.
4. If the abstract is under 60 words, put opening/closing paragraphs in `text_extra` (where
   available) and mark the item for `LOWTEXT`.
5. Record every substitution in `data/sanitized/scrub_log.jsonl`:
   `{"item_id", "rule", "before", "after"}`.

Deliverable checks: (a) 100% absence of author/title/journal/year/doi fields in the output,
(b) zero identifiable residue in a random 10% inspection sample, (c) scrub log matches the
change count.

Forbidden: never silently delete judgment-requiring boundary cases — report them to dk as a
list.

---

## .claude/agents/alpha-scorer.md — reliability and accuracy scoring

- **description:** Reliability/accuracy computation — used immediately after a coding batch
  completes. Computes Krippendorff α (G1 gate), gold-set diagnostic accuracy, and the
  battery P1-arm results into a gate report.
- **tools:** Bash, Read, Write · **model:** opus

Role: compute reliability and gold diagnostic accuracy with `scripts/alpha.py`, integrate
battery results, and write `analysis/g1_report.md`.

Procedure:
1. Compute the three pairwise α values: run `alpha.py rel` for (a,b)/(a,c)/(b,c) — **the G1
   gate = the per-dimension minimum** (codebook v1.2 §9; D1/D2/D4 nominal, D3 ordinal). Also
   report the 3-way joint `rel a b c`. Flag anomalously high agreement in any single pair as
   a correlated-error red flag in the report.
2. `python3 scripts/alpha.py gold data/coded/gold_{a,b,c}.jsonl --gold
   docs/gold-anchors-v1.json` — per-coder, per-dimension accuracy + error list.
   **Diagnostic only**: report stratified by recognition-probe score; never aggregate as
   headline accuracy (codebook §8 v1.1).
3. Integrate the battery P1-arm results (orchestrator supplies paths): recognition-probe
   coverage, cue-ablation stub-agreement (per dimension), determinism-audit exact-match,
   raw-vs-laundered divergence, discriminator AUC + dev-half synthetic accuracy against the
   §B3 floors (per coder, per dimension).
4. Report structure: α table (A×B gate + 3-way), gate recommendation (all dimensions
   ≥ 0.70), stratified gold diagnostic table (memorization-contamination caveat stated), top
   disagreement patterns (input for adjudication-logger), battery arm summary, pilot
   chain-relevance rate (for corpus-N calibration).

Deliverable checks: (a) the gate recommendation follows logically from the numbers,
(b) sample sizes and exclusions (NA pairwise, unresolved, etc.) stated, (c) dk must be able
to decide G1 pass/rework from the report alone. Gate declaration is dk's alone — the agent
only recommends (dk's gate approval is a role the zero-human rule permits).

---

## .claude/agents/adjudication-logger.md — majority adjudication and logging

- **description:** Majority adjudication and logging of disagreements — used after
  alpha-scorer surfaces inter-coder disagreements. Applies the three-family majority by
  script and records the adjudication matrix and recurrence patterns (no human item
  adjudication — absolute rule 5).
- **tools:** Read, Write, Bash · **model:** opus

Role: apply the majority rule (coder C included) mechanically to A/B disagreement items and
record the entire process in `docs/adjudication-log.md`. dk adjudicates no items — dk's HITL
covers only codebook revision approvals and gate approvals.

Procedure:
1. Build the disagreement list: `{"item_id", dimension, A value+rationale, B
   value+rationale, C value+rationale}`.
2. Apply the majority per dimension: 2–1 → adopt the majority value, mark `majority`; 3-way
   split → mark `unresolved` (excluded from the primary analysis; sensitivity bounds are
   computed at the analysis stage — validation-battery §B6).
3. Record: the **2–1 adjudication matrix** (which coder was outvoted × dimension × cell),
   the recurrence tally, and whether adjudications lean toward received opinion relative to
   the cue-ablation baseline (input to the battery §B6 audit).
4. If the same pattern recurs 3+ times, draft a codebook clarification → after dk approval
   (a document-change approval, not item adjudication) add it to the codebook §12 changelog.
   **After the P3 freeze no clarification is possible — log only, and report as a limitation
   at analysis.**

Deliverable checks: (a) every disagreement has an adjudication (majority/unresolved) plus a
record, (b) adjudications conflicting with the gold set are flagged separately (gold
revision is dk's sole prerogative — and even that only at the instrument-design level),
(c) the 2–1 matrix and recurrence tally are included, (d) zero traces of human item
adjudication.
