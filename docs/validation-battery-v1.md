# ditch-audit — Zero-Human Validation Battery v1.0

2026-07-14 · Owner: dk · Status: draft thresholds (PROVISIONAL → numeric values frozen at P3)
Companion to `codebook-v1.md` (v1.1+). Canonical spec for all validity evidence replacing human coding.

> **FIREWALL WARNING.** This file names the hypotheses' critical cells. It must NEVER be
> read by, quoted to, or summarized for coder-facing contexts (coder-runner ban list).

## Preamble — rationale and claim discipline

Binding dk decision (2026-07-14): **no human codes any item** — no human coder, no human
item-adjudication, no human validation sample (the P4 150-item human sample is removed).
The designer's human labor is confined to instrument design: codebook authorship, synthetic-item
specs and sign-off (B3), and gate approvals.

Consequences accepted:
- The paper claims **measurement by a fixed, preregistered, multi-family LLM instrument**, not
  human-equivalent annotation. The abstract must disclose zero-human coding in its own voice.
- Instrument accuracy on the real corpus distribution is formally unidentified (every criterion
  item is either famous-real or synthetic). Stated as the design's principal limitation.
- Venue strategy tilts methods-forward (Metaphilosophy / Synthese class; computational-humanities
  venues as fallback), consistent with the existing kill-criteria downgrade path.

The battery's job: bound every identifiable artifact — memorization, shared training-folklore,
style/register leakage, version drift, majority-vote error-laundering — with preregistered,
automatable tests whose pass/fail semantics are frozen at P3.

**Threat model note (red-team finding of record):** the headline pattern under study coincides
with field folklore plausibly present in every coder family's training corpus. Inter-family
agreement therefore CANNOT by itself evidence text-driven coding; B2, B4, and B7 exist
specifically against this.

## B0. Model-family role-exclusivity matrix

No family appears in more than one row-group. Assignments frozen at P3 with dated snapshots.

| Role | Family | Notes |
|---|---|---|
| Coder A (reliability pair) | Anthropic (pinned snapshot) | G1 primary |
| Coder B (reliability pair) | Google (pinned snapshot) | G1 primary |
| Coder C (adjudicator) | OpenAI (pinned snapshot) | majority vote only; excluded from G1 α |
| Coder D (archival, optional) | open-weights (e.g. Llama/DeepSeek-class, weights archived) | re-executability after endpoint retirement; results reported, not gating |
| Generator/launderer E | a family used by NO coder (e.g. Mistral-class) | synthetic generation (B3), style laundering (B4), paraphrase/contrast sets (B4) |
| Conformity checkers | non-coder families **other than family E** + mechanical checks + dk spec sign-off | B3 — E may not certify its own generations |

API call logs published with the audit package to make the no-contact claims verifiable.

## B1. Instrument fixation

- Dated model snapshots pinned in the OSF manifest; provider version headers logged per call.
- Mid-run model-deprecation policy preregistered (halt → substitute snapshot → full recode of the affected coder's assignments; never mixed within one coder column).
- **Determinism audit:** re-code an n=20 (P1) / n=50 (P4) subsample twice per family; report exact-match rate. PROVISIONAL floor: ≥ 95% exact match per dimension.
- Prompt = build artifact with SHA256 manifest (existing rule); coder-runner verifies hash before every run.

## B2. Cue-ablation folklore baseline (primary anti-folklore instrument)

- For every item, a fresh context of each coder family codes a **degraded stub** (topic keywords /
  first clause only; scripted degradation, no argumentative content).
- The stub-coding IS the folklore predictor: it quantifies how much of the full-text code is
  recoverable from topic identity alone.
- Report: (i) stub-vs-full agreement per dimension; (ii) headline effects re-estimated on the
  stratum where full-text codes DIVERGE from stub codes (the text-driven stratum);
  (iii) H1/H2 must survive in the text-driven stratum for a confirmatory claim. PROVISIONAL:
  confirmatory claim requires the text-driven-stratum OR to remain ≥ 2 with CI excluding 1.
- Run at P1 on all 55 pilot items (feasibility + variance estimate), at P4 on the full corpus.

## B3. Synthetic criterion set (headline construct-validity evidence)

- **N = 60**: development half (30, usable during G1 revision loops) / **vaulted half** (30,
  generated and SHA256-hashed before P1 coder runs, opened once at P4) — prevents
  revision-loop overfitting from consuming the criterion.
- **Specs authored and signed by dk** (instrument-design labor, within the zero-human rule; the
  WE1–WE9 precedent). Spec fields: target codes (all four dimensions), content constraints,
  anti-folklore flag, hedging quota, length band. Generation to spec by family E; conformity
  checked by non-coder families + mechanical checks (e.g. CS5 requires an explicit numeral;
  neutral requires no verdict verb) + dk sign-off per item against spec. Publish spec → item →
  walkthrough for every synthetic item (reader-falsifiable).
- **Cell coverage (exact accounting):** the ≥ 10 floor applies to the **full 60** (union of
  halves; each half carries ≥ 5 per covered cell) over exactly four covered cells:
  (i) pro×CS4+×alpha, (ii) contra×CS4+×beta/gamma, (iii) anti-folklore pro×CS4+×beta
  (A07/WE7 pattern), (iv) anti-folklore contra×CS4+×alpha (WE8 pattern) = 40 items;
  the remaining 20 = hedged underdetermined-→-neutral items (WE9 pattern; tests prior-filling,
  ≥ 10) + mainstream-hedged-register CS4 items (tests understatement handling, ≥ 10).
  **Venue-tier cells are exempt** from synthetic coverage — D5 is joined from metadata,
  never coded from text; their only per-cell control is the B8 agreement floor.
- **Style laundering + discriminator test:** all synthetic items pass through family-E laundering
  toward corpus surface statistics (length, hedge rate, readability); each coder family then
  classifies real-vs-synthetic on sanitized text in fresh contexts. PROVISIONAL pass: discriminator
  AUC ≤ 0.60 (CI including 0.5 preferred); fail → re-launder before any accuracy scoring.
- PROVISIONAL accuracy floors (per coder, dev half at P1): D1 ≥ 85%, D2 ≥ 85%, D3 ≥ 70% (±1 level ≥ 90%), D4 ≥ 75%.

## B4. Perturbation arms

- **Contrast sets (code-flipping minimal pairs):** family E produces minimal edits that flip a
  code (negate the conclusion; add/remove a strength hedge to move CS2↔CS4; swap the load-bearing
  premise empirical↔conceptual to flip beta↔alpha), verified against spec like B3 items.
  Coders must track the flip. PROVISIONAL: flip-tracking ≥ 80% per dimension.
- **Paraphrase stability:** semantics-preserving paraphrase (family E, cue statistics constrained:
  hedge rate and register vocabulary preserved; two intensities — light rewording / deep
  restructure). NOTE (red-team finding): stability is necessary, not sufficient — a folklore coder
  is maximally paraphrase-stable; interpret only jointly with B2. PROVISIONAL: code-flip ≤ 10%.
- **Entity-swap:** named interlocutors replaced by role tags on a subsample; code divergence flags
  memorization-adjacent coding.
- **Raw-vs-laundered arm:** at P1, the 55 pilot items are coded both raw and style-laundered;
  divergence measured. At P3, dk decides which arm is primary for P4 (laundered coding also
  neutralizes venue-register leakage → feeds B9); the other becomes a preregistered sensitivity.

## B5. Recognition probe (memorization bound)

- Every real item: each coder family, fresh context, asked to name author/title/venue from the
  sanitized text; scored by script against metadata.
- **Probe validation:** the 20 gold anchors + a planted set of known-famous texts must be detected.
  PROVISIONAL: ≥ 90% planted-famous detection, else the stratification is not used.
- Claim discipline: a negative probe excludes **verbatim/item-level recall only** — topic-level
  priors are B2's job (Duan et al. COLM 2024 caveat).
- Analyses stratified by recognizability; headline effects re-estimated on the unrecognized stratum.
- Gold-anchor accuracy is reported ONLY within this stratification (diagnostic; codebook §8).

## B6. Adjudication integrity

- Majority-of-three (A, B, C). 3-way splits → `unresolved`: excluded from primary analysis;
  sensitivity bounds computed under each candidate resolution; per-cell unresolved rates reported.
- **2-1 resolution matrix** published, cross-tabulated against analysis-predicted cells;
  folklore-congruence of resolutions audited against the B2 baseline (does the tie-breaker
  systematically break TOWARD the stub-predictable code?).
- **Four-estimator stability:** headline effects under (i) drop-all-disagreements, (ii) A-only,
  (iii) B-only, (iv) majority — confirmatory claims require sign stability and CI overlap across
  all four. PROVISIONAL: per-family OR ratio within [0.5, 2].
- Tipping-point analysis: fraction (and cell pattern) of 2-1 resolutions that must be wrong to
  nullify each headline effect.

## B7. Analysis-side robustness (folklore-facing)

- Reversed-default deletion test: D4 recoded under the opposite tie-break polarity ("delete the
  a-priori premise; if the argument still runs, code beta"); report the fraction of D4 decided by
  the tie-break; headline claims must survive both polarities.
- Confidence- and text-length-stratified effect estimates (low-information stratum monitored).
- Metadata-only null baseline: a non-coder context codes from bibliographic metadata alone
  (no abstract); quantifies prior-driven coding ceiling.

## B8. Analysis-critical cells (per-cell floors)

The cells that decide the headline analyses (frozen precisely at P3): direction × CS4+ × epistemic
type cells entering the primary 2×2 (both diagonal and anti-diagonal), and CS4+ × venue-tier cells
entering the interaction contrast. Each carries: per-cell coder agreement floor (PROVISIONAL ≥ 0.60
pairwise raw agreement, n-floor 15), per-cell synthetic-criterion accuracy floor (PROVISIONAL ≥ 70%
on the cell's B3 items, n ≥ 10), and cell-wise confusion matrices in the published package.

## B9. Venue-register control (tier-analysis specific)

- Venue-inference probe: each family classifies venue tier from sanitized text alone; report AUC.
- **Run phase:** P4 (the P1 pilot corpus is single-venue, so T3-vs-rest AUC is not estimable
  before the P3 arm decision). The trigger below is preregistered as a **conditional rule** that
  overrides the P3 primary-arm choice for the tier analysis only.
- PROVISIONAL: AUC > 0.65 on T3-vs-rest → the laundered arm (B4) becomes mandatory-primary for the
  tier analysis; additionally re-estimate within register-matched strata and with predicted-tier
  as covariate.

## B10. Battery pass/fail semantics (frozen at P3)

- Every PROVISIONAL threshold above receives a frozen numeric value and a frozen consequence
  (confirmatory-claim block vs sensitivity-note vs instrument-revision trigger) in the OSF
  registration. No post-hoc threshold selection; no narrative rescue of failed components.
- Component failures that BLOCK any confirmatory claim (result becomes descriptive-map preprint,
  per existing kill criteria): B2 text-driven-stratum failure · B3 vaulted-half accuracy below
  floor at P4 · B6 four-estimator sign instability.
- The audit package publishes all component results, including failures.

## B11. Reproducibility

- One open-weights family (coder D) + archived weights/prompts/harness in the OSF package →
  re-execution (not just re-inspection) survives API endpoint retirement. Data availability
  section states the distinction honestly.

## B12. Cost note

Battery multiplies API volume ≈ 2.5–3× over plain tri-coder runs (probes + stubs + perturbation
arms + laundered arm). Abstract-length calls; pilot-scale cost remains small; P4 budget estimated
at low hundreds of USD — logged in `data/coded/cost_log.md`.

## Changelog

- v1.0 (2026-07-14): initial battery, drafted from the red-team synthesis (3 adversarial reviews,
  6-agent research sweep); dk approvals of record: zero-human rule (absolute), coder C = OpenAI,
  dk synthetic-spec sign-off, document package. Thresholds PROVISIONAL until P3.
