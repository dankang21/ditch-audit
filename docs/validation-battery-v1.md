# ditch-audit — Zero-Human Validation Battery v1.3

2026-07-14 (v1.0/v1.2) · 2026-07-17 (v1.3) · Owner: dk · Status: draft thresholds (PROVISIONAL →
numeric values frozen at P3; frozen values proposed in analysis-plan §9)
Companion to `codebook-v1.md` (v1.1+) and `analysis-plan-v1.md` (v1.1 — **the full battery
document, not only the B10 table, is the frozen manifest artifact**; body sections below are
kept consistent with the plan's §9 by co-amendment).
(v1.3 title-line note: the header read "v1.0" through two revisions while the changelog and all
citing documents said v1.2 — corrected.)

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
| Coder A | Anthropic (pinned dated snapshot, direct API) | G1 = min pairwise α over all three coder pairs (v1.2) |
| Coder B | Google (pinned dated snapshot, direct API) | G1 as above |
| Coder C | OpenAI (pinned dated snapshot, direct API) | G1 as above + majority adjudicator. Seat-assignment rule preregistered (B6) |
| Coder D (archival, **mandatory**) | open-weights, lineage disjoint from Z.AI and Moonshot (DeepSeek/Qwen/Llama-class all admissible), weights archived; family confirmed at P3 | re-executability after endpoint retirement; results reported, not gating |
| Generator/launderer E | **GLM-class open-weights (Z.AI lineage) served via the Perplexity Agent API** (dk decision 2026-07-14; no new keys) — **`web_search` tool omitted on every call = structurally no search**; each response's `tool_calls_details` and absent `search_results` logged as proof; exact model string + call date archived with the artifact hashes | synthetic generation (B3), laundering/paraphrase/contrast sets (B4). **Sonar-class models are barred from every blinded role**: their retrieval grounding cannot be verified off (`disable_search` proves non-surfacing, not non-grounding) and their base lineage is undocumented/mutable. E-output drift is tolerable — artifacts are one-shot, frozen, hashed |
| Conformity checkers | **Kimi-class (Moonshot lineage) via the same Agent API, search tool omitted** + mechanical checks; dk spec sign-off is the FINAL gate, logged before any coding results are seen | B3 — E may not certify its own generations; checker lineage disjoint from all coders and E |
| Harvest aid (unblinded) | Perplexity Sonar (search ON) | P2 abstract-coverage backfill only — the one role where retrieval grounding is an asset; never touches sanitized/blinded material |

API call logs published with the audit package to make the no-contact claims verifiable.

## B1. Instrument fixation

- Dated model snapshots pinned in the OSF manifest; provider version headers logged per call.
- Each pinned snapshot's **published retirement date** verified to cover the full P4-plus-reproduction window and recorded in the manifest; full request/response logs archived so retired-endpoint results remain auditable.
- Mid-run model-deprecation policy preregistered (halt → substitute snapshot → full recode of the affected coder's assignments; never mixed within one coder column).
- **Determinism audit (v1.3 — three-level structure, replaces the single ≥95% per-run floor,
  which is unreachable at B/C endpoints):**
  - **B1a** per-run determinism: 2 identical extra invocations per item per coder, exact-match
    per dimension; descriptive, sanity floor ≥ 70% per dimension per coder (< 70% → REVISE).
  - **B1b** consolidated run-split rate (`run_unstable` per coder per dimension): ≤ 2%,
    alarm at 5%.
  - **B1c** consolidated-output determinism (binding): the majority-of-3 pipeline re-run twice
    on the n = 50 checkpoint subsample (6 extra runs/item/coder); ≥ 95% exact-match per
    dimension per coder. **Not measured at P1** (P1 measured B1a and run splits only; plan §9
    row B1c records the projection and the registered possibly-live REVISE for coder C).
  - REVISE consequence for any level: coder k raised 3→5 **with mandatory re-consolidation of
    all that coder's prior P4 items at the new k before analysis** (never mixed within one
    coder column — same principle as the model-substitution rule above).
- **Sampling-parameter honesty:** the 2026-07-14 smoke test (A rejected explicit temperature;
  only B accepts temperature 0) was run against the **sonnet-era A pin and predates the
  `claude-opus-4-8` pin change** — it is re-run and logged against the current A pin as a
  registered pre-freeze action (plan §1.1, manifest item 7). Effective parameters are
  machine-logged per call (`_meta`); run-level determinism rests on the determinism audit above,
  not on a temperature claim — stated as such in the prereg.
- Prompt = build artifact with SHA256 manifest (existing rule); coder-runner verifies hash before every run.

## B2. Cue-ablation folklore baseline (primary anti-folklore instrument)

- For every item, a fresh context of each coder family codes a **degraded stub** (topic keywords /
  first clause only; scripted degradation, no argumentative content).
- The stub-coding IS the folklore predictor: it quantifies how much of the full-text code is
  recoverable from topic identity alone.
- Report: (i) stub-vs-full agreement per dimension; (ii) headline effects re-estimated on the
  **text-driven stratum — mechanized predicate (v1.3): items whose ADJUDICATED stub-arm code
  differs from the ADJUDICATED full-text code on ≥ 1 denominator-relevant dimension for the
  hypothesis at hand (H1: D1/D2/D3/D4; H2: D1/D2/D3)**; (iii) survival requirement for a
  confirmatory claim, per hypothesis: **H1 → stratum OR_H1 ≥ 2 with CI excluding 1; H2 →
  stratum OR_pro ≥ 2 with CI excluding 1** (stratum ROR published as a sensitivity-note; an
  OR_contra-dependent requirement would contradict the registered ≈1 prediction).
  The stub-degradation and stratum-builder scripts are freeze-manifest artifacts (plan §11
  item 20).
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
  **Iteration cap: 3 regeneration rounds per item**, every regeneration logged with its trigger —
  an uncapped patch loop would let the discriminator gate become an expectancy channel.
- PROVISIONAL accuracy floors (per coder, dev half at P1): D1 ≥ 85%, D2 ≥ 85%, D3 ≥ 70% (±1 level ≥ 90%), D4 ≥ 75%.
  **v1.3: proposed frozen floors move D3 to ≥ 85%** (the 70% floor was set for the 5-level CS
  scale; at the 2-level {DEF, POS} scale chance = 50% and measured dev-half is 97–100 — plan §9
  row B3-acc). The ±1-level criterion is void at 2 levels.
- **Discriminator disposition of record (v1.3):** the AUC ≤ 0.60 pass was FAILED in both rounds
  (R1 .867–.991, R2 .709–.909; re-launder cap reached). AUC is reported descriptively (NOTE);
  the gate's teeth move to the **B3-dis′ coding-contamination check** — per coder, one-sided
  Mann–Whitney U (α = .05, n ≥ 20 per group) that flagged items do NOT show higher
  code-instability (per-item dims-changed, raw-vs-laundered arms) than unflagged; failure strips
  B3-acc of confirmatory weight (BLOCK; plan §2.4 item 4, §9 rows B3-dis/B3-dis′).

## B4. Perturbation arms

- **Contrast sets (code-flipping minimal pairs):** family E produces minimal edits that flip a
  code (negate the conclusion; add/remove a strength hedge to move CS2↔CS4; swap the load-bearing
  premise empirical↔conceptual to flip beta↔alpha), verified against spec like B3 items.
  Coders must track the flip. PROVISIONAL: flip-tracking ≥ 80% per dimension.
- **Paraphrase stability:** semantics-preserving paraphrase (family E, cue statistics constrained:
  hedge rate and register vocabulary preserved; two intensities — light rewording / deep
  restructure, **classified mechanically by the pipeline stage that produced the variant
  (distinct build artifacts), never by post-hoc output judgment (v1.3)**). NOTE (red-team
  finding): stability is necessary, not sufficient — a folklore coder is maximally
  paraphrase-stable; interpret only jointly with B2. PROVISIONAL: code-flip ≤ 10% light /
  ≤ 20% deep (plan §9 B4-para). The cue-fidelity hedge/modal/directive lexicon behind the ±20%
  band is a frozen manifest artifact (plan §11 item 19).
- **Entity-swap:** named interlocutors replaced by role tags on a subsample; code divergence flags
  memorization-adjacent coding.
- **Laundering method hierarchy (v1.2):** prefer **mechanical identity-scrubbing** (the existing
  sanitizer, with scrub logs) wherever the item passes the recognition probe; full paraphrase only
  where scrubbing fails the probe. Every paraphrased item carries a **cue-fidelity check**:
  hedging/modal/directive term counts preserved within a preregistered band; violations
  re-laundered (same 3-round cap as B3). Rationale: paraphrase perturbs exactly the dimensions
  being measured (claim-strength register), so it is a last resort, not a default.
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
- Analyses stratified by recognizability; headline effects re-estimated on the unrecognized
  stratum. **v1.3 (plan §12 item 15): sign persistence on the unrecognized stratum is promoted
  from sensitivity-note to a confirmatory BLOCK for the affected hypothesis, with an
  evaluability guard — the BLOCK applies when the unrecognized stratum holds n ≥ 30 items of
  the hypothesis's denominator; below that, "not evaluable" → prominent limitation (NOTE).**
- Gold-anchor accuracy is reported ONLY within this stratification (diagnostic; codebook §8).

## B6. Adjudication integrity

- **Adjudicator-seat rule (v1.2; error-correlation term amended post-G1, dk review item 4):** the
  C seat (majority adjudicator) is provisionally OpenAI; final assignment at P3 by a fixed rule —
  the family with the highest dev-half synthetic accuracy (B3) and the lowest asymmetric
  error-correlation with the other two, computed on **pilot real-corpus disagreement items**
  (the synthetic dev-half is at ceiling, 97–100%, leaving error correlation unidentifiable there;
  anchors remain excluded as memorization-suspect). The rule, not the outcome, is what freezes.
- **Conditional-agreement diagnostic (post-G1 addition; v1.3 frozen definition):** the P4
  confirmatory checkpoint and the P4 midpoint report P(B=C | A≠B) per dimension (P1 baseline:
  45–75%, no lockstep bloc). **Alarm trigger: ≥ 0.90 on a dimension with conditioning
  n(A≠B) ≥ 20; "sustained" = two consecutive evaluations.** Frozen response (plan §6.3): P4
  pauses, the adjudicator seat switches to the frozen alternative (A), all P4 adjudications are
  mechanically recomputed, the event is logged as a preregistered deviation — no open-ended
  re-examination (seating C would double-count the B-family prior; rationale unchanged).
- Majority-of-three (A, B, C). 3-way splits → `unresolved`: excluded from primary analysis;
  sensitivity bounds computed under each candidate resolution; per-cell unresolved rates reported.
- **2-1 resolution matrix** published, cross-tabulated against analysis-predicted cells;
  folklore-congruence of resolutions audited against the B2 baseline (does the tie-breaker
  systematically break TOWARD the stub-predictable code?). **Stub-congruent (v1.3 definition):
  the adopted majority value equals the majority of the three families' stub-arm codes on that
  dimension (no stub majority → not stub-congruent).** The plan's §5.2 adversarial folklore-flip
  test (25% fraction, BLOCK — plan §12 item 15) consumes this definition.
- **Estimator stability (v1.3: five estimators — E3 = C-only added, plan §12 item 12):**
  headline effects under (E0) drop-all-disagreements, (E1) A-only, (E2) B-only, (E3) C-only,
  (E4) majority (primary). **Confirmatory claims require sign stability and CI overlap
  (defined: CI(Ei) ∩ CI(E4) ≠ ∅, interval intersection) across all estimators — on the
  DIRECTIONAL headline effects only (OR_H1, OR_pro, ROR). OR_contra is exempt** (registered
  prediction ≈ 1: near-1 sign chatter across estimators is the design succeeding; OR_contra is
  scored solely by the plan's §2.3 contra-control row, with its evaluability floor).
  PROVISIONAL: per-family OR ratio within [0.5, 2] (breach = NOTE); sign instability and
  CI-overlap failure = BLOCK (plan §2.4 item 5).
- Tipping-point analysis: fraction (and cell pattern) of 2-1 resolutions that must be wrong to
  nullify each headline effect.

## B7. Analysis-side robustness (folklore-facing; v1.3 id split B7a/B7b)

- **B7a — reversed-default deletion test:** D4 recoded under the opposite tie-break polarity
  ("delete the a-priori premise; if the argument still runs, code beta"); report the fraction of
  D4 decided by the tie-break; headline claims must survive both polarities (NOTE-class:
  prominent limitation + polarity-conditional confirmatory language on failure — plan §9 B7a).
- **B7b — strata monitors + metadata-only baseline (report-only, NOTE):** confidence- and
  text-length-stratified effect estimates (low-information stratum monitored); metadata-only
  null baseline — a non-coder context codes from bibliographic metadata alone (no abstract);
  quantifies the prior-driven coding ceiling. Probe template is a manifest artifact (plan §11
  item 21).

## B8. Analysis-critical cells (per-cell floors)

The cells that decide the headline analyses (frozen precisely at P3): direction × CS4+ × epistemic
type cells entering the primary 2×2 (both diagonal and anti-diagonal), and CS4+ × venue-tier cells
entering the interaction contrast.

- **Agreement floor (all analysis-critical cells; mechanized v1.3):** cell membership by
  **adjudicated** codes; per-dimension raw agreement computed between each coder pair over the
  coders' consolidated codes on the cell's items (denominator-relevant dimensions); PROVISIONAL
  ≥ 0.60 applied to the **minimum over the three pairs**; defined at cell n ≥ 15.
- **Synthetic-criterion accuracy floor (the four B3-covered construct cells ONLY; PROVISIONAL
  ≥ 70% on the cell's B3 items, n ≥ 10).** **Venue-tier cells are exempt from the synthetic
  floor** (consistent with B3's coverage rule: D5 is metadata-joined, never coded from text);
  their only per-cell control is the agreement floor. (v1.3 fixes the internal contradiction
  with B3's exemption; plan §5.3 states the same.)
- Cell-wise confusion matrices in the published package.
- **n-floor consequence (v1.3):** an analysis-critical cell with adjudicated n < 15 at analysis
  time renders the hypothesis it enters **non-confirmatory** (plan §5.3 — the floor cannot be
  waived or read as "not failed"; no confirmatory verdict may rest on a Haldane-corrected
  analysis-critical cell, plan §2.5).

## B9. Venue-register control (tier-analysis specific)

- Venue-inference probe: each family classifies venue tier from sanitized text alone; report AUC
  per family. Probe template is a manifest artifact (plan §11 item 21).
- **Run phase:** P4 (the P1 pilot corpus is single-tier — T3 absent — so T3-vs-rest AUC is not
  estimable before the P3 arm decision). The trigger below is preregistered as a **conditional
  rule** that overrides the P3 primary-arm choice for the tier analysis only.
- PROVISIONAL → v1.3 frozen form: **trigger = MAX over the three families' AUCs > 0.65 on
  T3-vs-rest** (most conservative aggregation; frozen to prevent an any/all/pooled choice at a
  primary-arm flip). Trigger consequences: the laundered arm (B4) becomes mandatory-primary for
  the tier analysis **only if it has independently passed the B9a dual statistic on the
  checkpoint tranche (plan §6 laundered-arm eligibility rule); if the trigger fires and the
  laundered arm is not eligible, H2 degrades to non-confirmatory (descriptive + both-arm
  sensitivity)** — an ungated arm never becomes the confirmatory instrument. Additionally
  re-estimate within register-matched strata and with predicted-tier as covariate — **covariate
  estimator named (v1.3): stdlib logistic regression (Newton–Raphson) of POS on
  tier×direction + predicted-tier** (the saturated IPF cannot take a covariate); reported, not
  primary.

## B9a. P4 confirmatory reliability checkpoint (post-G1 declaration condition — load-bearing)

The G1 PASS declaration (2026-07-16) is **conditional** on this checkpoint; it exists because the
pilot gate estimate is a selected estimate (five sequential revisions, optional-stopping
structure) and the gold-exclusion sensitivity dropped three cells marginally under .70.
- Sample: fresh items only (no pilot overlap), drawn from held-out venue-years; **n = 150,
  drawn by the frozen seeded stratified venue×year random draw (tranche-construction script +
  seed = manifest artifacts; plan §6, §11 items 11/15)**. The tranche is coded in **both arms**
  (raw + laundered) — feeds B3-dis′ and the B9 eligibility rule.
- Dual statistic, both required, on every dimension: point min-pairwise α ≥ .70 AND **the
  per-dimension min-pairwise α's bootstrap 95% lower bound ≥ .667** (Krippendorff's
  tentative-conclusion floor) — **four interval quantities, one per dimension (the min over
  pairs is recomputed inside each replicate); NOT twelve per-pair bounds** (plan §2.5/§6).
- Reporting frame for the paper: tentative-band reliability, checkpoint-confirmed (+ the plan's
  §6 misclassification sensitivity for the reliability–claim gap).
- Failure consequence (frozen at P3): halt P4 coding; no confirmatory claims; dk decides between
  descriptive downgrade and instrument redesign (outside the exhausted G1 revision budget).
- Also reported at checkpoint: conditional-agreement diagnostic (B6), per-cell floors (B8),
  determinism sub-audit (B1a/B1b/B1c), run_unstable rate, and the firewalled yield-trigger
  outputs (plan §12 item 10).

## B10. Battery pass/fail semantics (frozen at P3)

- Every PROVISIONAL threshold above receives a frozen numeric value and a frozen consequence
  (confirmatory-claim block vs sensitivity-note vs instrument-revision trigger) in the OSF
  registration. No post-hoc threshold selection; no narrative rescue of failed components.
- **Single-authority rule (v1.3): the plan's §2.4 gate chain is the exhaustive registry of
  BLOCK conditions; every BLOCK below maps to exactly one chain item.** Component failures that
  BLOCK confirmatory claims: B2 text-driven-stratum failure (chain 2) · B3 vaulted-half accuracy
  below floor at P4 (chain 3) · B3-dis′ contamination-check failure (chain 4) · B6 estimator
  sign-instability or CI-overlap failure on a directional headline effect (chain 5) · B8
  analysis-critical cell floor/n-floor failure (chain 6, per-hypothesis) · B5-strat sign flip on
  an evaluable unrecognized stratum (chain 7, per-hypothesis) · the plan-§5.2 adversarial
  folklore-flip failure (chain 8, per-hypothesis) · B9a checkpoint failure (chain 1: halt).
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

- v1.3 (2026-07-17, co-amendment with analysis-plan v1.1; pre-freeze): header version corrected
  (was mislabeled v1.0). B1 determinism restructured to B1a/B1b/B1c (binding floor at the
  consolidated level; B1c flagged not-measured-at-P1); sonnet-era smoke test marked superseded
  (re-run on the opus A-pin = registered pre-freeze action). B2 text-driven-stratum predicate
  mechanized (adjudicated stub vs full-text, ≥ 1 denominator-relevant dimension) with
  per-hypothesis gated effects. B3: proposed D3 floor 85 at 2 levels; discriminator disposition
  of record (AUC failed → B3-dis′ carries BLOCK teeth, frozen Mann–Whitney procedure). B5-strat
  promoted NOTE → evaluability-guarded BLOCK. B6: five estimators; stability criteria restricted
  to directional effects with OR_contra exempt; CI overlap defined; conditional-agreement alarm
  given a frozen trigger/sustained definition and a frozen response. B7 split into B7a/B7b. B8:
  agreement floor mechanized (adjudicated membership, min-pairwise); venue-tier cells exempted
  from the synthetic floor (internal contradiction with B3 removed); n-floor consequence stated.
  B9: max-family AUC aggregation; laundered-arm eligibility rule (no ungated primary);
  covariate estimator named. B9a: n = 150; four per-dimension interval quantities; seeded
  tranche construction; both-arm coding. B10 block list aligned to the plan's §2.4
  single-authority chain. All numeric freeze proposals live in analysis-plan §9.
- v1.2 (2026-07-14, allocation review, dk-approved): G1 redefined to min pairwise α (codebook v1.2).
  E reassigned Sonar → GLM-class open-weights via Perplexity Agent API with `web_search` omitted
  (structural no-search; Sonar's `disable_search` proves non-surfacing only, and its lineage is
  undocumented — web-verified 2026-07-14); Sonar barred from blinded roles, retained as P2 harvest
  aid. Conformity checker staffed (Kimi-class, same route). Coder D mandatory; Llama re-admitted to
  D's candidate pool (E no longer Llama-derived). Laundering hierarchy (mechanical scrub first,
  cue-fidelity band), discriminator iteration cap, adjudicator-seat rule, snapshot-retirement
  manifest requirement added. No new API keys (dk constraint).
- v1.0 (2026-07-14): initial battery, drafted from the red-team synthesis (3 adversarial reviews,
  6-agent research sweep); dk approvals of record: zero-human rule (absolute), coder C = OpenAI
  (v1.2: provisional, rule-based final assignment), dk synthetic-spec sign-off, document package.
  Thresholds PROVISIONAL until P3.
