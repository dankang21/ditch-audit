# ditch-audit — Analysis Plan v1.1 (P3 preregistration draft, repaired)

2026-07-16 (v1.0 draft) · 2026-07-17 (v1.1 repair pass) · Owner: dk · Status: **DRAFT for dk
review — freeze candidate for the P3 OSF registration**
Companions: `codebook-v1.md` (v1.4c body, v1.4a gate protocol; §12-item-14 refresh pending),
`validation-battery-v1.md` (**v1.3 — co-amended with this revision**), `analysis/g1_report.md`
(v1.4a re-gate + post-declaration addendum), `docs/adjudication-log.md` (Final round F),
`outline-v0.4.md` §4–6, CONTEXT.md §3–4 (G2 rulings 4.9b/4.9c).

> **FIREWALL WARNING.** This document states the study's hypotheses, their predicted cells, and
> the analysis-critical cell list. It must NEVER be read by, quoted to, or summarized for the
> coder-runner agent or any coder-facing context. **v1.1: the ban applies from the moment this
> file exists, not from adoption** — the file already names both hypotheses and the critical
> cells. CLAUDE.md absolute rule 1's enumerated ban list and the coder-runner agent definition
> must name `docs/analysis-plan-v1.md` before any further coder run (orchestrator/dk action,
> outside this document's own authority; tracked in §14).

Conventions. "PROPOSED" marks a numeric value or rule this draft puts forward for dk's freeze
decision; "FROZEN-AT-P3" marks the slot the frozen value occupies in the OSF registration. Every
decision requiring dk's signature is cross-referenced to the decision register (§12) and carries a
`[dk: pending]` placeholder. All statistics in this plan are computable by stdlib-only Python
scripts (project rule); scripts and seeds are themselves freeze-manifest items (§11).

---

## 1. Instrument and corpus of record

### 1.1 Instrument (as gated at G1, 2026-07-16)

| Component | Value of record |
|---|---|
| Codebook | `docs/codebook-v1.md` v1.4c (D3 = 2-level {DEF, POS} + NA; kill-criterion collapse of CS1–5, codebook §12) |
| Coder prompt | build artifact of `scripts/build_coder_prompt.py`, SHA256 manifest verified per run |
| Coder A | Anthropic `claude-opus-4-8` (pin revision of record, 2026-07-15, pre-freeze, logged) |
| Coder B | Google `gemini-3.5-flash` |
| Coder C | OpenAI `gpt-5.5-2026-04-23` (provisional adjudicator; final seat by B6 rule — §12 item 4) |
| Coder D | open-weights archival, **mandatory**; family confirmed at P3 (battery §B0) |
| Generator/launderer E | GLM-class open-weights via Perplexity Agent API, `web_search` structurally omitted |
| Coder output rule | per-dimension majority of 3 independent identical runs; 3-way run split → run-1 value + `run_unstable` flag (codebook §9 v1.4a) |
| Adjudication | majority-of-three (A, B, C); 3-way coder splits → `unresolved` (§3.4) |
| G1 status | PASS on preregistered point statistic (min pairwise α: D1 .736 / D2 .727 / D3 .808 / D4 .705, n=89) — **conditional on the P4 confirmatory checkpoint (§6)**; gold-exclusion sensitivity drops three cells marginally under .70 (basis of the tightened checkpoint trigger) |

**Pin-record repair (v1.1).** The A/B strings above are family/version identifiers, not the
**dated snapshot identifiers** battery §B1 requires; manifest item 7 now requires full dated
snapshot ids for A and B before signing. The recorded sampling-parameter smoke test (battery
§B1) was run against the sonnet-era A pin and predates the `claude-opus-4-8` pin change; it is
**re-run and logged against `claude-opus-4-8` as a registered pre-freeze action** (manifest
item 7; battery §B1 v1.3 amended in tandem).

### 1.2 Corpus of record (G2 PASS, dk declaration 2026-07-17; CONTEXT §4.9b/4.9c)

| Stratum | Items | Abstract coverage |
|---|---|---|
| T2∪T3 post-2008 (**effective G2 gate; primary estimand population — §4.0**) | 2,690 | 2,496 = **92.8%** (≥ 90% gate) |
| T2∪T3 pre-2008 (**preregistered missingness stratum**, §4) | 672 | missing 210 = 31.2% (462 abstract-covered) |
| T2∪T3 overall (T2 2,818 + T3 544; denominator after 627 source-confirmed (reconciled at lock generation) review exclusions) | 3,362 | 2,958 = 88.0% |
| T1 topic-filtered candidates | 296 | 94.3% |
| APQ backfill (T1) | 151 | (per P2 records) |

15 abstract-bearing review essays are reversibly excluded (dk may revisit — §12 item 6).
Planning figure used in §7: **≈ 2,900 abstract-bearing T1∪T2 items** (T2 covered ≈ 2,958 −
covered-T3 [T3 total 544, abstract-bearing 445]; + T1 ≈ 279 + APQ). Exact counts are recomputed
from the locked P2 files at freeze (§7 mandatory action).

### 1.3 Pilot calibration rates (G1 report §9 + addendum B; n=69 real-corpus pilot items)

| Quantity | Point | 95% CI (Wilson) |
|---|---|---|
| P(D1 ∈ S1..S8) ("S-coded") | 20/69 = 29.0% | [19.6%, 40.6%] |
| P(D3 = POS \| S-coded) | 3/20 = 15.0% | [5.2%, 36.0%] |
| Chain-relevance (D1 ≠ X) | 39/69 = 56.5% | — |
| Item-level D1 unresolved rate | 5/69 = 7.2% | — |
| Cell-level unresolved rate | 6/356 = 1.7% | — |

---

## 2. Hypotheses and confirmatory specifications

### 2.1 Vocabulary (codebook v1.4 terms)

- **POS** = positive evidential claim (legacy CS4–CS5); **DEF** = defensive claim (legacy CS1–CS3).
  All legacy "CS4+" language in outline/battery maps to POS; "≤ CS3" maps to DEF.
- **alpha (α)** = a priori/conceptual; **beta (β)** = empirical contact; **gamma (γ)** =
  historical-documentary (D4). H1 contrasts α vs β∪γ.
- **S-coded** = adjudicated D1 ∈ {S1..S8}. B, P, I, M, X are not chain steps.
- **Mainstream** = T1∪T2; **confessional** = T3 (venue-tier table frozen at P3; F&P's T2 seat is
  the R2 sensitivity axis).
- D3 is a 2-level scale: ordinal ≡ nominal; all D3 statistics are computed nominal (notation
  cleanup of record, G1 addendum F; the matching codebook-§9 line refresh is §12 item 14).
- **Estimand of record (v1.1; §4.0):** the primary confirmatory population for both hypotheses is
  the **post-2008 stratum**; whole-window (2004–2024) estimates are a preregistered extension.

### 2.2 H1 — type–direction law (article level; rewritten in v1.4 terms)

**Statement.** Among mainstream-venue (T1∪T2) chain-step items whose claim strength is POS, the
load-bearing epistemic type differs by direction: pro-direction POS items are predominantly α;
contra-direction POS items are predominantly β∪γ.

**Population.** DEN-H1 (§3.1), restricted per §4.0 for the primary estimand. **Statistic.** 2×2
table, rows = D2 ∈ {pro, contra}, columns = D4 ∈ {α} vs {β∪γ}. Odds ratio

`OR_H1 = [n(pro,α) · n(contra,β∪γ)] / [n(pro,β∪γ) · n(contra,α)]`

with Woolf (logit) 95% CI; Haldane–Anscombe +0.5 on all cells if any cell = 0 (both raw and
corrected estimates reported; confirmatory-use restriction in §2.5); two-sided Fisher exact test
reported alongside.

**Registered prediction.** OR_H1 ≥ 3.

**Decision semantics (frozen at P3):**

| Outcome | Verdict |
|---|---|
| 95% CI lower bound > 1 **and** point OR ≥ 3 | H1 supported at registered magnitude |
| 95% CI lower bound > 1 and 1 < point OR < 3 | H1 directionally supported, registered magnitude not met (reported as such; no re-framing) |
| 95% CI includes 1, or point OR ≤ 1 | **H1 null** (kill-criterion input) |

A confirmatory H1 claim additionally requires the full confirmatory gate chain (§2.4). All
verdict wording is instrument-relative (§2.6).

### 2.3 H2 — venue topography (rewritten in v1.4 terms)

**Statement.** Among pro-direction chain-step items, the probability of a POS (vs DEF) claim is
higher in T3 than in T1∪T2. Among contra-direction items (control), the corresponding contrast is
predicted null or reversed.

**Population.** DEN-H2 (§3.2), restricted per §4.0 for the primary estimand. **Statistic.**
2×2×2 table: tier (T3 vs T1∪T2) × strength (POS vs DEF) × direction (pro vs contra). Fit the
saturated log-linear model (stdlib IPF implementation; equivalently a logit model of POS on
tier × direction). Report:

- `OR_pro  = odds(POS | T3, pro)  / odds(POS | T1∪T2, pro)`
- `OR_contra = odds(POS | T3, contra) / odds(POS | T1∪T2, contra)`
- interaction contrast `ROR = OR_pro / OR_contra` with 95% CI (Woolf on the three-way term).

**Registered predictions.** (i) OR_pro > 1; (ii) OR_contra ≈ 1 or < 1; (iii) ROR > 1.

**Decision semantics (frozen at P3):**

| Outcome | Verdict |
|---|---|
| LCL(OR_pro) > 1 **and** LCL(ROR) > 1 | H2 supported |
| LCL(OR_pro) > 1 but ROR CI includes 1 | H2 partially supported (pro-shift real, asymmetry not established) — does not count as "supported" for kill-criterion purposes |
| otherwise | **H2 null** |
| contra-control, **evaluable** (both contra tier-cells at adjudicated n ≥ 15): OR_contra CI includes 1 or entirely < 1 | contra-control prediction met (scored separately; OR_contra is exempt from the §5.1 stability BLOCK — v1.1) |
| contra-control **not evaluable** (either contra tier-cell n < 15) | reported as "not evaluable" — never as "met" (v1.1; at foreseeable contra-cell sizes an includes-1 CI is near-certain and uninformative) |

**v1.1 cell-integrity riders.** An H2 confirmatory verdict additionally requires every H2
analysis-critical cell at adjudicated n ≥ 15 at analysis time (§5.3 — under-floor cells block the
hypothesis; they never pass by being "not failed"), and no confirmatory ROR may rest on a
Haldane-corrected analysis-critical cell (§2.5). H2's confirmatory element is itself conditional
on the registered H2 power computation (§7; §12 item 16).

**Kill criterion (unchanged in substance, restated).** H1 null ∧ H2 null → no journal submission;
downgrade to descriptive-map preprint + essay. No salami-slicing; no post-hoc hypothesis swaps.
If item 16's re-scope fires, "H2 null" is read against the re-scoped confirmatory element
(LCL(OR_pro) ≤ 1), and the registration says so before any P4 data exist.

### 2.4 Confirmatory gate chain — the unique authority for BLOCK conditions (v1.1 restructure)

This chain is the **exhaustive registry of confirmatory blocks**. Every §9 row whose consequence
class is BLOCK maps to exactly one item below, and no BLOCK-class condition exists outside this
list (single-authority rule; v1.0 left B3-dis′ and the missingness consequence as orphan blockers
outside the chain).

A result may be reported as *confirmatory* only if ALL of the following hold; otherwise the run
degrades to a descriptive map (battery §B10 semantics):

1. **P4 reliability checkpoint** passed (§6; §9 row B9a) — G1 PASS is conditional on it by
   declaration. Failure halts P4 entirely.
2. **B2 text-driven stratum** retention, under the mechanized predicate and per-hypothesis gated
   effects of §9 row B2.
3. **B3 vaulted-half accuracy** ≥ frozen floors at P4 (§9 row B3-acc).
4. **B3-dis′ coding-contamination check** passed (§9 row B3-dis′). Failure strips B3-acc of
   confirmatory weight, so item 3 cannot be satisfied through a failed B3-dis′.
5. **B6 estimator stability** on the **directional headline effects only** (OR_H1, OR_pro, ROR):
   sign stability + CI overlap per §5.1. OR_contra is exempt — it is predicted ≈ 1 (§2.3
   prediction ii), so sign chatter around 1 across estimators is the design succeeding, not an
   instability; it is scored solely by its §2.3 decision row. (Battery §B6 v1.3 amended in tandem.)
6. **B8 analysis-critical cell floors** met for every cell entering the claimed hypothesis
   (§5.3), **including the n ≥ 15 floor evaluated at analysis time** — blocks the specific
   hypothesis whose cell failed.
7. **B5-strat sign persistence** on the recognition-unrecognized stratum, where evaluable
   (§9 row B5-strat; promoted NOTE → BLOCK, §12 item 15) — blocks the affected hypothesis.
8. **§5.2 adversarial folklore-flip survival** at the frozen 25% fraction (§12 item 15) —
   blocks the affected hypothesis.
9. **Whole-window extension claims only:** the §4.2 missingness criteria (M3 survival +
   tipping-point margins; §12 item 11). The post-2008 primary claim does not depend on this item.
10. The claimed effect meets its §2.2/§2.3 decision rule.

Failure of 1 halts P4; failure of 2, 3, 4, or 5 blocks all confirmatory claims (B10 block list);
failure of 6, 7, or 8 blocks the hypothesis affected; failure of 9 blocks only the extension
claim; sensitivity-note components (§9) never block but must be published.

### 2.5 Inference policy

- Two confirmatory hypotheses, one preregistered test each; no further multiplicity correction.
  Everything in §8 (robustness) and §10 (descriptive) is explicitly non-confirmatory.
- 95% CIs throughout; two-sided tests; α = .05 where a test is invoked.
- Zero-cell handling: Haldane–Anscombe 0.5; exact (conditional) estimates reported alongside.
  **v1.1 rule: no confirmatory verdict may rest on a CI whose computation required the Haldane
  correction on an analysis-critical cell.** Such estimates are reported as descriptive, with the
  exact conditional analysis alongside. (In practice the §5.3 n-floor will already have blocked
  the hypothesis; this rule closes the residual route by which a continuity correction on an
  empty cell could have manufactured an "H2 supported".)
- Bootstrap convention (used in §6): nonparametric percentile, B = 1,000, item-level resampling,
  single global RNG, seed = OSF registration date (YYYYMMDD), FROZEN-AT-P3. Loop order
  pair-outer/dim-inner **for the per-pair α computations inside each replicate; the checkpoint
  statistic then takes the per-dimension minimum over the three pairs within each replicate**
  (§6 — four interval quantities, not twelve). (The G1 report §3 documents
  convention-sensitivity of extreme bounds; freezing the convention removes that degree of
  freedom.)
- All analysis scripts: Python 3.10+ stdlib-only, hashes in the freeze manifest, re-runs must be
  byte-identical (the adjudication scripts already meet this standard).

### 2.6 Verdict vocabulary (frozen wording; v1.1)

All confirmatory verdicts are **instrument-relative**: the registered sentence form is
"H1 [H2] supported, **as measured by the frozen, preregistered multi-family LLM instrument**."
Real-corpus construct accuracy is formally unidentified (battery preamble concession of record);
the promoted real-corpus probes (§2.4 items 7–8) bound direction-correlated bias, they do not
identify accuracy. Unqualified "H1 is true / the law holds" phrasing is barred from the abstract
and conclusions. This wording freezes regardless of the §12 item 15 outcome; if dk declines the
item-15 promotions, this section is the **only** remaining mitigation and the limitation section
must say so explicitly.

---

## 3. Denominators and unit-level inclusion rules

The G1 review left the H1/H2 denominators as the open item (addendum F). The following operative
drafts are proposed for freeze. **[dk approval: pending — §12 item 0]**

### 3.1 DEN-H1 (primary H1 denominator)

An article *i* enters DEN-H1 iff all of:

| # | Condition | Source of the value |
|---|---|---|
| 1 | Venue tier(i) ∈ {T1, T2} | metadata join (D5 never coded) |
| 2 | Adjudicated D1(i) ∈ {S1..S8} | majority-of-3-coders over consolidated (majority-of-3-runs) codes |
| 3 | Adjudicated D2(i) ∈ {pro, contra} | same |
| 4 | Adjudicated D3(i) = POS, **after** the stage-2 full-text pass (§3.6) | same |
| 5 | Adjudicated D4(i) ∈ {α, β, γ} | same |
| 6 | No `unresolved` on any of D1, D2, D3, D4 | §3.4 |

Cell assignment: D2 × (α vs β∪γ). Note the NA-cascade rules make conditions 3–5 near-redundant
given 2 and D3=POS; they are stated independently so that exclusion accounting is mechanical.

### 3.2 DEN-H2 (isomorphic to DEN-H1)

Identical to DEN-H1 except: condition 1 becomes tier ∈ {T1, T2, T3}; condition 4 becomes
D3(i) ∈ {DEF, POS}; condition 5 (D4) is **not required**; and **condition 6 becomes: no
`unresolved` on D1, D2, D3** (v1.1 — H2 does not use D4, so D4-`unresolved` does not exclude
from DEN-H2; previously stated only by example in §3.4). Cell assignment:
tier(T3 vs T1∪T2) × D3 × D2.

**Preregistered DEN-H2 sensitivity: B-inclusion.** Bundled-target items (D1 = B) carry codeable
D2/D3 and are pro-side cumulative-case material; H2 is re-estimated with D1 ∈ {S1..S8, B}.
Primary remains S-coded-only (isomorphy with H1). [dk approval: pending — §12 item 0]

### 3.3 Adjudication rule of record

Per dimension, per item, over the three coders' consolidated codes: unanimous → adopted; 2-1 →
majority value adopted, minority coder and transition logged (published 2-1 matrix, §5.4); 3-way →
`unresolved`. Zero-human rule 5 applies: no human touches any item verdict.

### 3.4 `unresolved` handling

- **Primary analysis:** excluded (per battery §B6). Per-cell unresolved rates published.
- **Preregistered sensitivity (bounds):** each headline OR recomputed under every candidate
  resolution of the unresolved set — (a) all-to-A's value, (b) all-to-B's, (c) all-to-C's, and
  (d) the two adversarial assignments that respectively minimize and maximize the OR. The
  min/max envelope is published next to the primary estimate. Expected volume is small (pilot:
  1.7% of cells, 7.2% of items on D1).
- An item unresolved on a dimension outside the relevant denominator conditions is NOT excluded
  (e.g., D4-unresolved does not exclude from DEN-H2 — now stated in §3.2's definition).
- **Membership re-evaluation (v1.1):** every candidate resolution above, and every §5.2 flip,
  re-applies **all** denominator conditions — a resolved or flipped value can remove an item
  from the denominator entirely (e.g., a minority D1 = X), not merely move its cell.

### 3.5 `run_unstable` handling

`run_unstable` (3-way run split inside one coder; pilot: 1/267 coder-items = 0.37% — one item,
coder C, splitting on D1/D2/D4 simultaneously; per-coder-per-dimension unit: C 1/89 = 1.1% on
each of D1, D2, D4, A = B = 0) items are **included** in the primary analysis with their
consolidated (run-1) value, flagged in the public data; preregistered sensitivity: recompute
headline effects excluding all run_unstable items. If the P4 run_unstable rate exceeds the B1b
threshold (§9), the affected coder's k is raised (§9 consequence) — an instrument event, not an
analysis event.

### 3.6 Stage-2 full-text rule (POS candidates; T-2 mitigation)

- **Trigger (frozen, v1.1):** an item enters stage 2 iff ≥ 1 of coders A/B/C returns a
  **consolidated (majority-of-3-runs) coder-level** D3 = POS on the abstract. A single POS run
  inside an otherwise-DEF coder consolidation does **not** trigger (run-level noise is B1's
  jurisdiction, not a retrieval trigger).
- All three coders recode on the expanded sanitized text; the stage-2 adjudicated code is final
  and **replaces the stage-1 code for ALL analyses** — both denominators and every cell
  assignment (a stage-2 POS→DEF flip moves the item's DEN-H2 cell; v1.0 named only §3.1
  condition 4). Both stages logged and published; abstract-only (stage-1) codes retained as a
  preregistered sensitivity (headline effects recomputed on stage-1 codes).
- **False-negative audit (v1.1; one-way-ratchet mitigation):** the POS trigger applies the more
  accurate instrument differentially across exactly the cells the hypotheses compare (if T3
  abstracts trigger more often, T3 gets more full-text looks). Therefore a **seeded random
  sample of n = 100 stage-1 S-coded items with no POS trigger** (stratified by tier × direction;
  seed in manifest item 11) receives the same full-text recoding. Report the stage-1
  false-negative POS rate per stratum and an FN-adjusted headline estimate as a frozen
  sensitivity.
- Budget: outline §4.1 line (USD 300–800), explicitly extended by the audit's ≈ 100 retrievals;
  rolled into the manifest item 17 budget re-estimate.

### 3.7 Majority vs unanimity sensitivity

Preregistered: all headline effects recomputed on the **unanimous-only** denominator (items where
A=B=C on every denominator-relevant dimension before adjudication). Direction of expected bias is
unknown a priori; divergence between majority and unanimous estimates beyond the §5 stability
bands is reported as an adjudication-sensitivity finding (links to the B6 folklore-congruence
audit).

### 3.8 Unit rules

Article = unit; primary thesis only. Dual-claim coding on a 10% random subsample (seeded, seed in
manifest) as sensitivity (outline §4.2). Discussion notes coded normally, flagged `CHAIN`,
analyzed separately (descriptive). The **89 pilot-phase items (69 real-corpus + 20 gold
anchors — one set, not 109)** are **excluded from all confirmatory denominators** (pilot data
excluded per outline §4.7; anchors are curated and memorization-suspect); the machine-readable
exclusion-id list is a freeze-manifest artifact (joins manifest item 12). Checkpoint-tranche
handling: §12 item 5. Calibration-sample handling: §12 item 5′.

---

## 4. Missing-abstract stratum plan (G2 stratified interpretation, CONTEXT §4.9b)

### 4.0 Estimand of record (v1.1 restructure)

The pre-2008 no-abstract stratum (672 items; 210 missing abstracts, concentrated in PC 2004–07
and IJPR/Sophia early years) is **structural missingness** (publishing-practice era boundary),
not random: any rate borrowed from post-2008 items rests on an untestable MAR assumption. v1.0
treated whole-window estimates as primary with M1–M3 presented as "bounds"; the v1.1 review found
the scenarios are not bounds on all free margins (the imputed POS **volume** was fixed at
point-estimate rates while the plan's own Wilson CIs permit ≈ 3× the mass; the DEF margin and the
tier×strength allocation were never varied, so the ROR-adversarial corner was structurally
unreachable). Repair: align the estimand with what the corpus gate actually certified.

- **Primary confirmatory estimand: the post-2008 population** (T2∪T3 post-2008 = 2,690 items at
  92.8% coverage — the effective G2 gate; plus T1 at 94.3%). The era-restricted column of §4.3
  becomes the estimate of record for the §2.2/§2.3 verdicts.
- **Whole-window (2004–2024) estimates are a preregistered extension**, reported with the full
  §4.2 machinery. Extension claims carry §2.4 item 9.
- Register: §12 item 11 (updated defaults).

### 4.1 Era×venue bias table (published deliverable)

Rows = venue (F&P, RS, IJPR, Sophia, PC; + T1 venues); columns = era (2004–2007, 2008–2024).
Cells: item count, abstract coverage %, and observable-covariate profiles computable **without
abstracts**: article type (research/note), title-keyword topic profile (mechanical stdlib keyword
tally against a frozen keyword list — no LLM role, preserving the B0 role matrix; **the keyword
list is freeze-manifest item 18**), page count where available. Covered-vs-missing profile
differences reported per venue.

### 4.2 Missingness sensitivity machinery (v1.1: tipping point + anchored scenarios)

Missing pre-2008 items cannot be coded; this section bounds what they could have done to the
whole-window estimates.

**(a) Raw adversarial bound (reported once, expected uninformative):** all 210 missing items
assumed in-chain POS with the adversarial direction×type assignment. This bound will typically
nullify any effect and is reported to demonstrate the necessity of (b).

**(b) Tipping-point statistic (the operative sensitivity; replaces "rate-adjusted bounds"):**
for each hypothesis, the **minimum number of missing items that overturns the decision rule**
(moves the 95% CI to include 1, or the point OR below the registered magnitude) when allocated
adversarially over **all free margins** — direction, D4 type, strength (POS **and** DEF), and
tier for H2 (subject only to each missing item's known venue fixing its venue row). The search is
mechanical (greedy adversarial cell allocation; stdlib script, hash in manifest item 11). Two
statistics are reported per hypothesis:

- `TP_pos` — adversarial allocation restricted to imputed in-chain **POS** items, read against
  the 95% joint-UCL expected missing in-chain POS count (210 × UCL[P(S)] × UCL[P(POS|S)]);
- `TP_free` — all margins free (POS and DEF), read against the 95% UCL expected missing
  **in-chain** count (210 × UCL[P(S)]).

For H1, imputation is restricted to the missing stratum's **T1∪T2 portion** (DEN-H1 excludes T3;
the PC portion enters only the H2/DEN-H2 computation).

**(c) Anchored scenarios M1–M3 (published envelope; anchor frozen, fork removed):** M1/M2/M3
retained as descriptive scenario columns:

| Scenario | Direction | D4 (for H1) | Tier (for H2) |
|---|---|---|---|
| M1 all-pro | all pro | adversarial vs H1 (all β∪γ) | per stratum composition (PC portion → T3) |
| M2 all-contra | all contra | adversarial vs H1 (all α) | same |
| M3 anchored-proportional | anchor direction distribution | anchor type distribution | same |

**Frozen anchor (v1.1 — removes the pilot/tranche choose-your-anchor fork):** all rates
(P(S), P(POS|S)) and the M3 direction/type distributions = **checkpoint-tranche adjudicated
values at P4**; fallback where a tranche cell has n < 5: pilot values; where the pilot cell is
also empty: uniform allocation over the admissible values — every fallback use logged.
Allocation arithmetic: **fractional expected counts** (no integer rounding); Haldane handling
per §2.5 where a scenario cell is zero.

**Claim consequence (updated; §12 item 11):** the post-2008 primary claim is independent of this
section. A **whole-window extension claim** requires all of: (i) the decision rule met on the
whole-window estimate; (ii) survival under M3; (iii) tipping-point margins — `TP_pos` and
`TP_free` each exceed their UCL comparators in (b). M1/M2 and the level-(a) bound are envelope
notes, never blockers.

### 4.3 Reporting frame

The paper reports the **post-2008 estimates as primary** (estimand of record), the whole-window
estimates as the preregistered extension carrying the §4.2 machinery, the era×venue bias table,
and the M-scenario envelope. The 2008 era boundary doubles as one of robustness R4's split
reports.

---

## 5. Estimator-stability battery, tipping point, per-cell floors

### 5.1 Estimator battery (battery §B6, extended)

Headline effects (OR_H1, OR_pro, OR_contra, ROR) are computed under five estimators:

| ID | Estimator |
|---|---|
| E0 | unanimous-consensus-only (drop all items with any coder disagreement on denominator dimensions) |
| E1 | coder A only |
| E2 | coder B only |
| E3 | coder C only *(extension beyond battery §B6's four — [dk: approved 2026-07-17, §12 item 12])* |
| E4 | majority-of-three (**primary**) |

**Denominator semantics (v1.1):** single-coder estimators E1–E3 evaluate denominator membership
and cell assignment from **that coder's consolidated codes alone**; E0 applies §3.7's unanimity
condition on every denominator-relevant dimension.

**Stability requirement (confirmatory; FROZEN-AT-P3) — applies to the directional headline
effects only: OR_H1, OR_pro, ROR.** Across all estimators: (i) sign stability (every point
estimate on the same side of 1); (ii) **CI overlap, defined as interval intersection:
CI(Ei) ∩ CI(E4) ≠ ∅** (not point-in-interval — v1.1 disambiguation); (iii) per-family OR ratio
OR(Ei)/OR(E4) ∈ [0.5, 2] (battery PROVISIONAL, proposed frozen as-is).

**Consequences (§9 row B6-est):** sign instability on any directional headline effect **blocks
all confirmatory claims** (B10 block list); CI-overlap failure **blocks** (it is §2.4 item 5's
substance — v1.0 left it consequence-less); ratio breach: NOTE.

**OR_contra exemption (v1.1).** OR_contra is exempt from all three stability criteria: it is
predicted ≈ 1 (§2.3 prediction ii), so its point estimate will sit near 1 and flip sides across
E0–E4 by sampling noise precisely when the design succeeds — a stability BLOCK keyed to it would
fire spuriously on success. OR_contra is published under all five estimators descriptively; its
only scored reading is the §2.3 contra-control row. (Battery §B6 v1.3 amended in tandem.)

### 5.2 Tipping-point analysis and folklore-flip test

- **Tipping point (published diagnostic):** for each headline effect, the minimum number (and
  identity pattern) of 2-1 adjudicated items in analysis-critical cells whose flip moves the 95%
  CI to include 1, reported as a count and as a fraction of all 2-1 resolutions in those cells.
- **Stub-congruence (definition, v1.1 — "stub mode" was undefined in v1.0):** a 2-1 resolution is
  *stub-congruent* iff the adopted majority value equals the **majority of the three families'
  B2 stub-arm codes** on that dimension (stub majority = 2-1 or 3-0; a 3-way stub split means no
  stub majority → not stub-congruent).
- **Adversarial folklore-flip test (promoted to BLOCK; §12 item 15):** let m = the number of
  stub-congruent 2-1 resolutions in the hypothesis's analysis-critical cells. Flip the
  adversarially-selected **⌈0.25·m⌉** of them (the subset whose joint flip moves the headline
  effect furthest toward 1 — deterministic greedy search; script hashed, manifest item 11), with
  denominator membership re-evaluated per §3.4. The hypothesis's decision rule must still be
  met; failure blocks the confirmatory claim for that hypothesis (§2.4 item 8).
- **Full-set flip (sensitivity-note, as in v1.0):** every stub-congruent 2-1 resolution flipped
  to its minority value; survival reported. P1 basis: adjudication-log §F6 (pilot toward-share
  0.55).

### 5.3 Analysis-critical cells and per-cell floors (battery §B8, frozen list)

**H1 cells (4):** {pro, contra} × {α, β∪γ} within DEN-H1.
**H2 cells (8):** {T3, T1∪T2} × {POS, DEF} × {pro, contra} within DEN-H2.

Each analysis-critical cell carries (values per §9 rows B8):

- **Agreement floor (mechanized, v1.1):** cell membership is determined by **adjudicated**
  codes; for the cell's items, compute per-dimension raw agreement between each coder pair over
  the coders' consolidated codes, on the hypothesis's denominator-relevant dimensions; the floor
  **≥ 0.60 applies to the minimum over the three pairs**, defined at cell n ≥ 15. (v1.0's
  per-coder cell membership was uncomputable under disagreement; battery §B8 v1.3 amended in
  tandem.)
- Synthetic-criterion accuracy ≥ 70% on the cell's B3 items (n ≥ 10) — applies to the four
  synthetic-covered construct cells (B3: pro×POS×α, contra×POS×β∪γ, anti-folklore pro×POS×β,
  anti-folklore contra×POS×α); venue-tier cells are exempt by design (D5 is metadata-joined) and
  carry the agreement floor only (battery §B8 v1.3 now states the same).
- Published cell-wise confusion matrices.

**Consequence:** an analysis-critical cell failing its floor blocks the confirmatory claim for
the hypothesis it enters (the other hypothesis is unaffected); the effect is additionally
re-estimated excluding the failing cell's items as a labeled sensitivity.

**n-floor (v1.1, frozen — closes the "never-failed" loophole):** an analysis-critical cell with
adjudicated **n < 15 at analysis time renders the hypothesis it enters non-confirmatory**. The
§7 expansion rule may cure a projected shortfall **before** analysis, but the floor itself cannot
be waived, satisfied vacuously, or re-read as "not failed"; if expansion cannot populate the
cell, the terminal state is a non-confirmatory (descriptive) H-verdict. Expected counts for the
foreseeably thin cells (both T3-contra cells) are registered at freeze (§7 H2 recalculation) so
an under-floor outcome is predicted, not discovered.

### 5.4 Published adjudication artifacts

The full 2-1 resolution matrix (minority coder × dimension × transition), cross-tabulated against
the analysis-critical cells; the B6 folklore-congruence audit against the B2 stub baseline; the
conditional-agreement diagnostic (§6.3). All are P4 deliverables with P1 formats already
established (adjudication-log §F2/§F6).

---

## 6. P4 confirmatory reliability checkpoint (battery §B9a, operationalized)

The G1 PASS is conditional on this checkpoint (declaration banner of record). It exists because
the pilot gate estimate is a selected estimate (five sequential revisions, optional-stopping
structure) and the gold-exclusion sensitivity dropped three cells marginally under .70.

| Parameter | PROPOSED (FROZEN-AT-P3) |
|---|---|
| Sample | **n = 150 fresh P4 items** (zero pilot overlap; held-out venue-years — pilot used RS 2015 + IJPR 2015), drawn by a **seeded stratified random draw** from the locked P2 corpus (pilot/gold ids excluded): venue×year strata, proportional allocation with minimum-cell constraints guaranteeing span ≥ 4 venues and ≥ 6 distinct years; **the tranche-construction rule is a frozen script + seed (manifest items 11/15)** — "first 150 items" is undefined without it, and the tranche is not silently orderable |
| Statistic 1 (point) | min pairwise Krippendorff α over {(A,B),(A,C),(B,C)} ≥ **.70** on every dimension (D1/D2/D4 nominal; D3 nominal ≡ ordinal at 2 levels) |
| Statistic 2 (interval) | **for each dimension, bootstrap the min-pairwise α (the per-dimension minimum over the three pairs recomputed inside every replicate); its percentile 95% lower bound must be ≥ .667** (Krippendorff's tentative-conclusion floor). **Four interval quantities — one per dimension — NOT twelve per-pair bounds** (the per-pair reading is explicitly rejected here to prevent re-litigation; §9 row B9a). Bootstrap per §2.5 convention |
| Pass rule | **both** statistics, **every** dimension |
| Determinism sub-audit | n = 50 seeded subsample, scored per §9 rows **B1a/B1b/B1c** (v1.0 omitted B1c, the binding row). Run accounting: **B1a** = 2 extra single invocations per item per coder (run-level exact match); **B1b** = run-split rate over the tranche's consolidated runs; **B1c** = the full majority-of-3 pipeline re-run **twice** on the 50 items (= 6 extra runs per item per coder), consolidated exact-match between the two re-runs, per dimension per coder |
| Both-arm coding (v1.1) | the tranche is coded in **both arms** (raw + laundered): supplies the B3-dis′ real-item comparison arm and the laundered-arm eligibility measurement below |
| Laundered-arm eligibility (v1.1 — closes the B9 loop) | the laundered arm may become mandatory-primary for the tier analysis (B9 trigger) **only if its tranche coding independently meets the dual statistic above**. If B9 fires and the laundered arm is not eligible, **H2 is downgraded to non-confirmatory** (descriptive + both-arm sensitivity). An arm that passed no gate under the instrument of record can never become the confirmatory instrument (v1.0 allowed exactly that via the B9 auto-switch; laundered reliability evidence is otherwise sonnet-era only — §12 item 1 caveat) |
| Also reported | conditional-agreement diagnostic (§6.3); per-cell floor status on cells populated so far (§5.3); run_unstable rate; **realized tranche marginal S/POS counts (feeds the §7 stage-2 trigger through the firewalled yield script)** |
| On PASS | continue P4; checkpoint results published with the gate report |
| On FAIL | **halt P4 coding immediately; no confirmatory claims from any already-coded material**; dk decides between descriptive downgrade and instrument redesign — the G1 revision budget is exhausted, so redesign restarts the gate cycle, it does not patch it |

**Rationale for n = 150.** At n = 89 the bootstrap intervals had half-widths ≈ ±.10–.15; at
n = 150 the expected shrinkage (∝ √(89/150) ≈ 0.77) brings a true α ≈ .78–.80 instrument
comfortably past the .667 lower-bound criterion, while a true-α ≈ .70 instrument will fail
statistic 2 — which is the intended behavior (the checkpoint is load-bearing, not decorative).

**Reporting frame for the paper (frozen wording):** "tentative-band reliability,
checkpoint-confirmed." **Reliability–claim mismatch mitigation (v1.1):** because α ≈ .70 admits
substantial misclassification and only **nondifferential** error attenuates ORs (direction-
correlated error does not), a quantitative misclassification sensitivity is preregistered: using
the checkpoint's D4 and D2 pairwise disagreement matrices, recompute OR_H1 under (i) a
nondifferential-error scenario and (ii) direction-differential scenarios spanning the observed
disagreement rates (frozen scenario grid in the checkpoint spec, manifest item 15); publish the
corrected range next to the primary. If the H1 decision rule is not met across the plausible-
differential scenarios, the verdict carries a frozen **"reliability-sensitive"** qualifier.

### 6.3 Conditional-agreement alarm (family-correlation watch)

P(B=C | A≠B) per dimension on the checkpoint sample (P1 baseline: D1 .45 / D2 .71 / D3 .73 /
D4 .75 — no lockstep bloc). PROPOSED alarm (FROZEN-AT-P3):

- **Trigger:** P(B=C | A≠B) ≥ **0.90** on a dimension with conditioning n(A≠B) ≥ 20, evaluated
  at the checkpoint and at the P4 midpoint. **"Sustained" = two consecutive evaluations meeting
  the trigger** (v1.0 left "sustained" undefined on a single batch); a single triggering
  evaluation = logged watch flag.
- **Frozen response (v1.1 — "re-examined by dk" is not a preregisterable consequence):** on a
  sustained alarm, P4 pauses; the adjudicator seat switches to the frozen alternative seating
  (A — §12 item 4's option (b) alternative); all P4 adjudications to date are recomputed under
  the new seat (mechanical re-run); the event is logged as a preregistered deviation in the OSF
  transparent-changes section. No other instrument parameter may change in response (seating C
  would double-count the B-family prior — the original rationale, unchanged).

---

## 7. Statistical power and yield (mandatory freeze recalculation; G1 addendum B)

### 7.0 Calibration update (2026-07-17 — supersedes pilot-rate estimates below)

Stratified corpus calibration sample: n = 150 abstract-bearing T2∪T3 items (seed 20260717,
manifest `data/raw/calib_sample_manifest.json`; strata fp 25 / rs 35 / ijpr 28 / sophia 36 /
pc 26), sanitized, coded by coder B, single run (calibration-only; confirmatory treatment of
these 150 items = **§12 item 5′** — the v1.0 pointer dangled, the register item now exists).
Results (Wilson 95% CIs):

- P(S-coded) = 59/150 = **39.3%** [31.9, 47.3] — higher than the pilot's 29.0%
  (specialist-journal corpus is more chain-relevant than the pilot venue mix).
- P(POS | S) = 10/59 = **16.9%** [9.5, 28.5].
- Effective rate = **6.67%** → expected POS in the 2,958-abstract T2∪T3 corpus: **~197 point**
  [conservative 89, optimistic 398], before T1 additions and before the full-text pass on POS
  candidates (which can only add).
- **Population correction (v1.1):** the 197 figure is a **T2∪T3** count and may not be read
  against §7's H1 power table — DEN-H1 admits **T1∪T2 only** (§3.1); the T3/PC share belongs to
  DEN-H2. On the calibration sample's T2-only stratum the rate is **8/124 = 6.45%** → ≈ **162
  expected DEN-H1 POS** on the ~2,513 covered-T2 abstracts, ≈ 180–190 with T1/APQ additions —
  still above the 110 trigger, so the adequacy conclusion stands on the corrected population.
  The 197 T2∪T3 figure is retained for DEN-H2 planning only. PC stratum: 12/26 = **46% S-coded**
  (feeds the §7 H2 recalculation).
- Caveats: single-coder (B), single-run estimate; D1 distribution of note — S6 items exist in
  the corpus (3/150), so the A21 promotion path (codebook §8) is live.
- Expansion-trigger operationalization: the frozen two-stage rule of §12 item 10 (v1.0's
  "recommendation" to key on realized tranche yield is superseded by the deterministic,
  firewalled version there).

The outline's power sketch (300–450 CS4+ from 1,500 abstracts) is off by ~5× against pilot rates.
Recalculation on the corpus of record:

**Expected-yield formula (direction fixed, v1.1):**
`E[DEN-H1] = N_abstracts(T1∪T2) × P(S) × P(POS|S) × P(non-excluded)`, where
**P(non-excluded) = 1 − the expected unresolved-or-ineligible fraction** (pilot item-level D1
unresolved 7.2%, §1.3; recomputed from tranche data at the checkpoint). v1.0 printed the inverse
form `target_POS / [P(S)·P(POS|S)·P(non-excluded)]` as if it were an expected yield — that form
computes **required corpus size** for a target and is retained only for that purpose.

At pilot rates: ≈ 2,900 × .290 × .150 ≈ **126 POS items** (central; before the non-exclusion
factor). Propagating the pilot CIs: ≈ **[44, 300]** at the P(POS|S) interval alone; the dominant
uncertainty is P(POS|S) (n = 20 pilot S-items). D3=POS at stage-2 (full text) may raise this
rate relative to abstract-only coding (abstract understatement, codebook §11) — direction known,
magnitude unknown; the §3.6 FN audit measures it.

**Power sketch for H1** (Woolf normal approximation; OR = 3; contra α-share assumed .35;
α = .05 two-sided):

| n(DEN-H1) | pro:contra split | Power for OR = 3 |
|---|---|---|
| 80 | 60:40 | .64 |
| 126 | 60:40 | .83 |
| 126 | 70:30 | .77 |
| 200 | 60:40 | .96 |

**Mandatory freeze action (registered):** recompute N_abstracts and the expected yield (formula
above) on the locked P2 counts before the freeze is signed. **Trigger (frozen; §12 item 10):**
expected DEN-H1 yield < **110** → the harvest is expanded **before any P4 spend** (same Woolf
approximation as the table: power ≈ **.77 at the 110 boundary** at a 60:40 split, crossing .75
at n ≈ 104–105 — the trigger sits one step conservative of the .75 floor; v1.0's "< ~.75 at 110"
slightly overstated the loss). Expansion executes the **frozen preference order** — (i) complete
T1 venue-years not yet harvested, (ii) window extension (2000–2003 / 2025), (iii) EJPR
re-admission (reverses locked D-1) — **until projected yield ≥ 110, with no discretionary choice
among options** (§12 item 10; the two-stage re-check at the checkpoint and its firewall are
specified there). This resolves jointly with the 3× majority-of-3 and ~2.5–3× battery cost
multipliers (B12; G1 §7c): the P4 budget estimate is a freeze-manifest item.

**H2 cell feasibility and registered H2 power (v1.1 — H2 was never powered in v1.0).** The
binding cells are T3: PC 544 items, **445 abstract-bearing (81.8%, locked P2 count — v1.0's
"≈ 490" was a mis-quote)**; expected T3 chain items ≈ 445 × .29 ≈ **129** at pilot rates,
≈ 445 × .46 ≈ **205** at the §7.0 calibration PC-stratum rate. Direction and strength splits
within T3 were unknown at pilot (T2-only). **Mandatory freeze recalculation extended to H2:**
registered expected counts for **all 8 H2 analysis-critical cells** (including both T3-contra
cells — the §4.2/§5.3 failure mode is predicted here, not discovered at P4), using calibration
margins where estimable, and **registered power for LCL(ROR) > 1** at plausible splits (a
three-way interaction needs roughly 4× the sample of a main effect). Contingency: **§12
item 16** — if registered ROR power < .5, H2's confirmatory element re-scopes to OR_pro before
freeze and the kill criterion reads against the re-scoped element. The §5.3 n ≥ 15 cell floors
are checked at the checkpoint and P4 midpoint, with the same expansion rule if a critical H2
cell projects under floor.

---

## 8. Robustness battery (outline §5, restated operationally) and mirror audit

All items in this section are **non-confirmatory** (sensitivity/robustness), published in full.

- **R1 — alternative partitions.** Variants: 7-step (merge S7+S8 → deterministic relabel of coded
  D1), 10-step (split S3 into unicity/aseity vs sovereignty; split S4 via the Mill finite-god
  cut), liberal-target (drop S7: S7 items excluded, S8 retained with its γ-dependence noted).
  Merges and drops are deterministic relabels of frozen codes. **Splits cannot be recovered from
  coded data**: they require a scoped supplementary coding pass (S3- and S4-coded items only,
  same frozen coders, a frozen two-way split rule appended as a build-variant prompt — never a
  modification of the primary prompt; **the variant prompt is a freeze-manifest artifact,
  item 23, conditional on item 9**). PROPOSED: run the split pass post-P4 as preregistered
  sensitivity [dk: approved 2026-07-17 — §12 item 9]. H1/H2 must persist (decision rules re-met) across all
  admissible grains for the invariance claim; divergences reported per grain.
- **R2 — F&P tier flip.** H2 recomputed with F&P assigned T3. Both assignments published;
  the primary is the frozen tier table.
- **R3 — dominant-author exclusion.** Drop items authored by Swinburne, Plantinga, Draper, Oppy
  (metadata join, post-coding — blinding untouched); recompute H1/H2.
- **R4 — time split.** 2004–2013 vs 2014–2024; report tier × strength topography per window
  (the 2008 era boundary additionally reported per §4.3).
- **R5 — citation-weighted rerun.** Weights = log(1 + citations) from a single frozen snapshot
  (**the downloaded snapshot file itself is hashed — freeze-manifest item 22**; source and date
  recorded there); robustness-only by outline fiat.
- **B7a — reversed-default deletion test.** D4 re-derived under the reversed tie-break polarity
  ("delete the a-priori premise; if the argument still runs, code β") on all DEN-H1 items;
  report the fraction of D4 codes that are tie-break-decided; H1 must survive both polarities
  (sign + CI); PROPOSED sensitivity-note threshold: tie-break-decided fraction > 30% of DEN-H1
  items → prominent limitation flag (§9 row B7a).
- **B7b — strata monitors + metadata-only baseline.** Confidence- and text-length-stratified
  headline estimates; metadata-only null baseline (non-coder context; quantifies the
  prior-driven ceiling). Reporting-only (§9 row B7b — v1.1 splits the id: v1.0 used "B7" for two
  distinct components, leaving this one without a consequence class).
- **O4 — mirror audit (naturalism's burdens).** Exploratory appendix, preregistered here for the
  honesty rule: a 3-step naturalism mini-chain (N1 cosmogenesis / brute-fact viability; N2
  naturalistic fine-tuning response; N3 naturalistic account of consciousness), corpus = same
  T1∪T2 window keyword-filtered, capped at ~200 items (cost), same coder families and blinding,
  instrument = a mirror build variant of the frozen codebook (step table swapped; produced by the
  same build script with its own manifest; the primary prompt is untouched). **Published whatever
  it shows, including a naturalist α-zone if present** (CONTEXT §7). No confirmatory status.

---

## 9. Battery threshold table — numeric freeze proposal (battery §B10)

Every PROVISIONAL threshold with a proposed frozen value, its P1 evidentiary basis, and its
frozen consequence class: **BLOCK** = confirmatory-claim block · **NOTE** = sensitivity-note ·
**REVISE** = instrument-revision trigger. Rows marked ◆ are dk judgment calls (see §12).
**Single-authority rule (v1.1): every BLOCK in this table maps to exactly one §2.4 chain item;
this table introduces no block the chain does not enumerate.**

| ID | Component | PROVISIONAL (battery v1.2) | PROPOSED frozen value | P1 evidence | Consequence |
|---|---|---|---|---|---|
| B1a | Per-run decoding determinism (exact-match, 2 identical invocations, per dim per coder) | ≥ 95% | **report descriptively; sanity floor ≥ 70% per dimension per coder** — the binding metric moves to B1c ◆ | measured per-dim: A′ 95–100, B 85–95, **C 80–85** (v1.1 correction: v1.0's "C 70–85" quoted C's all-4-dims **joint** composite, 14/20 = 70, as the per-dim lower end; per-dim worst is 16/20 = 80 — det report s20260714); 95% unreachable at B/C endpoints (temperature not settable); majority-of-3 adopted as mitigation | < 70% per-dim: REVISE (coder k raised 3→5 for that coder; checkpoint sample recoded) |
| B1b | Consolidated run-split rate (`run_unstable` per coder) | — (new, v1.4a) | **≤ 2%** per coder per dimension; alarm at 5% | in the threshold's own unit: **C 1/89 = 1.1%** on each of D1/D2/D4 (one item, 3-way split on three dims); A = B = 0 (v1.0's "0.37% (C, 1/267)" pooled over coders×items, a different unit) | > 2%: NOTE + k raised 3→5; > 5%: REVISE (halt, dk review). Any k-raise triggers the B1c re-consolidation rule |
| B1c | Consolidated-output determinism (majority-of-3 pipeline re-run twice, n = 50 checkpoint subsample) | — (new) | **≥ 95%** exact-match per dimension per coder | **not measured at P1 — inferred** (v1.1 correction: v1.0's "1/267 → ≥ 95% comfortably implied" conflated 3-way run splits with consolidated re-run stability). Measured P1 **2-1 run-split** rates: C 12/89 (D1, 13.5%) / 8/89 (D2) / 8/89 (D3) / 7/89 (D4); B ≤ 9/89; A ≤ 5/89. Under the p = 2/3 reading of a 2-1 split, per-item consolidated re-run match ≈ .62 → **C's projected consolidated determinism ≈ 94–95% on D1 — at/below the floor**, marginal elsewhere. **Registered expectation: this REVISE may be live for C at P4.** Pre-freeze measurement option: §12 item 2 | < 95%: REVISE — k raised 3→5 for that coder **with mandatory re-consolidation of ALL that coder's prior P4 items at k = 5 before analysis** (never mixed within one coder column; mirrors the B1 substitution rule); determinism re-audited before continuing; cost carried in manifest item 17 |
| B2 | Text-driven-stratum requirement | stratum OR ≥ 2, CI excl. 1 | **mechanized predicate (v1.1):** stratum = items whose **adjudicated** stub-arm code differs from the **adjudicated** full-text code on **≥ 1 denominator-relevant dimension** for the hypothesis (H1: D1/D2/D3/D4; H2: D1/D2/D3). Gated effects per hypothesis: **H1 → stratum OR_H1 ≥ 2 with CI excl. 1; H2 → stratum OR_pro ≥ 2 with CI excl. 1** (stratum ROR published as NOTE — requiring OR_contra-dependent ROR would contradict the ≈1 prediction). Stub-degradation + stratum-builder scripts hashed (manifest item 20) | stub-recovery D2 .35–.51 (direction is text-driven, not topic-recoverable) → a substantial text-driven stratum exists; D1 stub-recovery high (.60–.76) = step ≈ topic, benign | fail: **BLOCK** (§2.4 item 2) |
| B3-acc | Synthetic accuracy floors (per coder; dev at P1, **vault at P4 is binding**) | D1 ≥ 85, D2 ≥ 85, D3 ≥ 70, D4 ≥ 75 | **D1 ≥ 85, D2 ≥ 85, D3 ≥ 85 (raised ◆), D4 ≥ 75** | dev-half measured 97–100 all coders all dims; D3 floor of 70 was set for the 5-level scale — at 2 levels chance = 50% and measured is 97–100, so 70 is vacuous | vault-half below floor at P4: **BLOCK** (§2.4 item 3) |
| B3-dis | Real-vs-synthetic discriminator | AUC ≤ 0.60 (precondition for trusting B3-acc) | **FAILED both rounds; re-launder cap reached.** PROPOSED (default): accept-with-mitigation ◆ — AUC reported descriptively; frozen contamination check B3-dis′ carries the teeth | R1 AUC .867–.991; R2 .709–.909; cause = family-E style fingerprint (24% laundered-real misread SYNTH vs 0% scrub-only); exam-mode natural experiment: C's codes *more* stable on flagged items (0.50 vs 0.81 dims changed) — distinguishability ≠ coding contamination | AUC itself: NOTE. See B3-dis′ |
| B3-dis′ | Coding-contamination check (replaces the AUC gate's teeth) | — | items a coder flags as synthetic must NOT show **higher** code-instability than unflagged. **Frozen test (v1.1):** per coder, one-sided **Mann–Whitney U** on per-item dims-changed (raw-vs-laundered arms), flagged vs unflagged, α = .05, minimum n ≥ 20 per group; P4 sample = the discriminator run over the **vaulted half + the §6 checkpoint tranche's real items** (both-arm coding guaranteed by §6); under-n → not evaluable → B3-acc carries a prominence-flagged caveat instead of a BLOCK | r1 measurement: flagged 0.50 vs unflagged 0.81 (more stable) — passes | fail at P4: B3-acc loses confirmatory weight → **BLOCK** (§2.4 item 4) |
| B4-flip | Contrast-set flip-tracking | ≥ 80% per dim | **freeze 80%** | not measured at P1 (P4 arm); B3 near-ceiling accuracy is weak indirect support | below: NOTE + per-cell reliance flagged on affected dimension |
| B4-para | Paraphrase stability (code-flip rate) | ≤ 10% | **≤ 10% light-rewording; ≤ 20% deep-restructure (reported)** ◆ — light vs deep classified **mechanically by the laundering-pipeline stage that produced the variant** (scrub-only / light-rewording / deep-restructure are distinct build artifacts; no post-hoc output judgment — v1.1) | raw-vs-laundered divergence 5–22% per coder (A 9–18, B 5–13, C 13–22) — includes genuine register effects, upper-bounds paraphrase instability | above: NOTE; interpret jointly with B2 only (folklore coders are maximally stable — necessary-not-sufficient caveat of record) |
| B4-cue | Cue-fidelity band for paraphrased items | preregistered band | **hedge/modal/directive term counts within ±20% of source** ◆ — **the term lexicon is a frozen artifact (manifest item 19)**; the band is unenforceable without it | not P1-measured; 3-round re-launder cap carried from B3 | violation: item re-laundered (cap 3) else scrub-only version used |
| B5 | Recognition-probe validation (planted-famous detection) | ≥ 90% | **freeze 90%, pooled "identified by ≥ 1 family"** | measured pooled 19/20 = 95% (per-family A 65 / B 85 / C 90) | below: stratification unusable → memorization bound weakens; NOTE + limitation |
| B5-strat | Fame-stratified re-estimation | — | headline effects re-estimated on the unrecognized stratum; **sign persistence required. Evaluability guard: BLOCK applies when the unrecognized stratum holds n ≥ 30 items of the hypothesis's denominator; below 30 → not evaluable → prominent limitation (NOTE)** ◆ (promoted NOTE → BLOCK, §12 item 15) | pilot unrecognized stratum n = 1 (A14) — statistically empty; expected to be large on the obscure corpus | sign flip on an evaluable stratum: **BLOCK for the affected hypothesis** (§2.4 item 7); not evaluable: NOTE (Duan et al. caveat stands: memorization bounded, not eliminated) |
| B6-est | Estimator stability | per-family OR ratio ∈ [0.5, 2] | **freeze [0.5, 2]** + sign stability + CI overlap (**CI(Ei) ∩ CI(E4) ≠ ∅**, interval intersection) — **directional effects only (OR_H1, OR_pro, ROR); OR_contra exempt** (§5.1; predicted ≈ 1, sign chatter on success is expected) | not estimable at pilot (3 POS items); pilot minority structure shows no global outlier coder | sign instability (directional effects): **BLOCK** (§2.4 item 5); **CI-overlap failure: BLOCK** (§2.4 item 5 — v1.0 left it unclassed); ratio breach: NOTE |
| B6-adj | Conditional-agreement alarm | alarm at ≈ 1 | **P(B=C \| A≠B) ≥ 0.90 with n(A≠B) ≥ 20, two consecutive evaluations (checkpoint, midpoint) = "sustained"** (§6.3) | P1 baseline .45–.75, no lockstep bloc | alarm: REVISE — **frozen response §6.3** (pause → seat switch to A → mechanical re-adjudication → logged deviation); no open-ended dk re-examination |
| B7a | Reversed deletion test | both polarities | **freeze**; tie-break-decided fraction reported; NOTE flag if > 30% of DEN-H1 | D4 weakest gate dimension (.705 min); polarity was consequential enough to codify — the **v1.4b multi-fatal-premise dominance rule** exists precisely to fix deletion-test polarity (codebook §12 v1.4b). Surviving coder-level non-NA type-substitution in final-round D4 2-1 resolutions: **2/17, both coder C (β→α ×1, γ→α ×1)**; the dominant D4 pattern is the NA/α cascade (15×), which this test does not probe. (v1.0's citation of the A04/A05/A07 "unison miss" family is superseded: gold re-adjudication ruled those designer memorization errors — the coders were right) | headline fails reversed polarity: NOTE (prominent limitation; confirmatory language downgraded to polarity-conditional) ◆ |
| B7b | Strata monitors + metadata-only baseline (v1.1 id split from B7) | — | report-only: confidence/text-length strata estimates; metadata-only prior-ceiling baseline | pilot formats established (adjudication-log §F2/§F6) | NOTE (published; never blocks) |
| B8-agr | Per-cell agreement floor | ≥ 0.60 pairwise raw, n ≥ 15 | **freeze 0.60 on the minimum pairwise per-dimension raw agreement; cell membership by adjudicated codes** (§5.3 mechanization — v1.0's per-coder membership was uncomputable under disagreement) | pilot cells too sparse to test; gate-level agreement passed | analysis-critical cell fails floor: **BLOCK for that hypothesis** (§2.4 item 6); **cell n < 15 at analysis time: hypothesis non-confirmatory** (§5.3 — never "not failed") |
| B8-syn | Per-cell synthetic accuracy | ≥ 70%, n ≥ 10 | **freeze as-is** (four construct cells; venue-tier cells exempt — battery §B8 v1.3 aligned) | dev-half construct cells at ceiling | same as B8-agr (§2.4 item 6) |
| B9 | Venue-register control | AUC > 0.65 → laundered arm mandatory-primary for tier analysis | **freeze: trigger = MAX over the three families' AUCs > 0.65 on T3-vs-rest** (most conservative aggregation — v1.0 left any/all/pooled open on a primary-arm flip); covariate arm named: **stdlib logistic regression (Newton–Raphson) of POS on tier×direction + predicted-tier** (the saturated IPF cannot take a covariate); arm switch subject to the **§6 laundered-arm eligibility rule** | not estimable at P1 (T3 absent from pilot — pilot spans two venues but a single tier) | trigger fires: laundered arm becomes primary for H2 **iff §6-eligible; else H2 non-confirmatory (descriptive + both-arm sensitivity)**; + register-matched strata + predicted-tier covariate re-estimate (reported) |
| B9a | Confirmatory checkpoint | size/statistics frozen at P3 | **n = 150; dual statistic — point min-pairwise α ≥ .70 on every dimension ∧ per-dimension min-pairwise bootstrap 95% LB ≥ .667 (four interval quantities, §6)**; tranche by frozen seeded stratified draw (manifest items 11/15) | n = 89 per-pair CIs: 8/12 pair×dim cells LB < .70 (descriptive motivation for the dual gate; **the frozen statistic is the per-dimension min over pairs, not the twelve per-pair bounds**); gold-exclusion drop (3 cells .676–.696); five-round selection structure | fail: **halt P4; BLOCK everything** (§2.4 item 1); dk chooses downgrade vs redesign |

---

## 10. Descriptive outputs (non-confirmatory)

- **Computed step status** (outline §4.4, POS ≡ CS4+): per step over T1∪T2 within window,
  evaluated as an ordered decision list (v1.1 — the v1.0 trichotomy was neither exhaustive nor
  fully defined):
  1. *contested* := both directions have ≥ k POS items;
  2. *headwind* := exactly one direction has ≥ k POS items AND the opposing direction has **zero
     POS items** (an opposing side with no items at all counts as DEF-only by frozen convention);
  3. *frozen* := no POS on either side in the trailing 10 years;
  4. *mixed/sparse* (residual) := everything else (e.g., sub-k POS on both sides).
  Reported at k ∈ {2, 3, 5}. The Table-1 status column is thereby recomputed, not asserted.
- Per-step direction × strength × type maps; venue-tier topography maps; B-prevalence (input to
  outline §7); S6 scarcity check (first clear S6 item promoted to anchor A21 with logged
  promotion, codebook §8); flag-class tallies (H, RE, CHAIN, MULTI).
- Full battery results including failures (B10 publication rule); cost log.

---

## 11. P3 freeze manifest (prereg-guardian machine-verification targets)

SHA256 per file; manifest signed at OSF registration; any post-freeze edit voids the run
(absolute rule 2). **v1.1: rows 18–25 added — prereg-guardian cannot machine-verify artifacts
the manifest does not enumerate.**

| # | Item |
|---|---|
| 1 | `docs/codebook-v1.md` — frozen version of record (v1.4c, or v1.4d if dk exercises the §F7 R3/R6 discretion before freeze — §12 item 8, incl. its v1.1 G1-voiding rider) **+ the §12 item 14 non-coder-facing refresh applied before hashing** |
| 2 | `pipeline/03_code/coder_prompt.txt` + build manifest (rebuilt iff item 1's coder-facing content changes; item 14's refresh touches non-coder-facing sections only) |
| 3 | `docs/validation-battery-v1.md` **v1.3 — the full document is the frozen artifact** (body sections co-amended with this plan; v1.0's "§B10 numeric table finalized" wording would have frozen contradictory body text as-is) |
| 4 | `docs/analysis-plan-v1.md` (this document, post-§12 resolutions) |
| 5 | `docs/gold-anchors-v1.json` (gold v1.3) |
| 6 | `docs/synthetic-specs-v1.json` + **vaulted-half SHA256** (hash registered; vault opened once at P4) |
| 7 | Model snapshot pins: A and B as **full dated snapshot identifiers** (the undated strings `claude-opus-4-8` / `gemini-3.5-flash` do not satisfy §B1's dated-snapshot requirement and are not machine-verifiable) · C `gpt-5.5-2026-04-23` · D (family + weights hash, confirmed at P3) · E (exact GLM model string + call dates); per-pin published retirement dates verified to cover P4 + reproduction window (B1); **pre-freeze action: re-run + log the sampling-parameter smoke test on `claude-opus-4-8`** (§1.1) |
| 8 | Role-exclusivity matrix (battery §B0) |
| 9 | Venue-tier assignment table (incl. F&P = T2 primary, R2 flip preregistered) |
| 10 | Step-status k thresholds {2, 3, 5} + the §10 decision-list predicates |
| 11 | Analysis code skeleton hashes (`scripts/alpha.py`, `scripts/adjudicate.py`, `scripts/consolidate_runs.py`, + the H1/H2 analysis and bootstrap scripts to be added pre-freeze; stdlib-only) **+ fixed seeds: §2.5 bootstrap seed · §3.8 subsample seed · §6 tranche seed · §3.6 FN-audit seed** **+ the §4.2 tipping-point search and §5.2 adversarial-flip search scripts** |
| 12 | Corpus lock: P2 harvest JSONL hashes, review-exclusion list (627 — reconciled count of record in data/raw/locks/review_exclusions.json; the earlier '620' was the pre-lock nominal figure), review-essay list (15), missingness-stratum item list (672 items; 210 missing), T1 candidate list, **machine-readable confirmatory-exclusion id list (89 pilot-phase = 69 real + 20 gold; §3.8)** |
| 13 | Denominator definitions DEN-H1 / DEN-H2 (§3) as dk-approved |
| 14 | Adjudicator-seat rule + frozen seat outcome + its computation inputs + **the both-seat co-analysis divergence rule** (§12 item 4) |
| 15 | Checkpoint spec (§6) incl. **the tranche-construction script (frozen artifact + hash + seed — authored pre-freeze; v1.0 froze a pointer to a nonexistent rule)**, the exact interval-statistic definition (four per-dimension min-pairwise quantities), the determinism sub-audit run accounting, the laundered-arm eligibility rule, and the misclassification-sensitivity scenario grid |
| 16 | dk decision register (§12) with recorded resolutions |
| 17 | P4 budget re-estimate (3× majority-of-3 × ~2.5–3× battery multiplier; B12 / G1 §7c; + §3.6 FN-audit line + §6 both-arm tranche coding + potential B1c k-raise re-consolidation) |
| 18 | §4.1 frozen title-keyword list (era×venue bias table input) |
| 19 | B4-cue lexicon: the frozen hedge/modal/directive term list behind the ±20% band |
| 20 | B2 stub-degradation script + text-driven-stratum builder script |
| 21 | Probe prompt templates: B5 recognition probe · B9 venue-inference probe · B7b metadata-only baseline (coder-facing instruments; hash prevents silent drift) |
| 22 | R5 citation snapshot: **script frozen now** (`pipeline/05_analysis/fetch_citation_snapshot.py`, hashed); **snapshot data pulled at P5** (citation counts are analysis-time covariates, not instrument) — at pull time the downloaded snapshot file itself is hashed + source and date recorded (the script's `*_manifest.json`) |
| 23 | R1 split-rule build-variant prompt (conditional on §12 item 9 = (a)) |
| 24 | Sanitizer + laundering pipeline versions (script hashes) underpinning the raw-vs-laundered arms |
| 25 | Calibration-exposure disclosure: the 150 calib item ids + coder-B calibration outputs (§12 item 5′ artifact) |

---

### 11.1 Frozen operationalization choices (2026-07-17, recorded before manifest generation)

Six interpretation points surfaced during freeze-script authoring; the shipped script defaults
are hereby FROZEN as the choices of record (each script's `interpretation_notes` cross-references
this section):

1. **Tranche eligibility** (build_checkpoint_tranche.py): abstract-bearing items only — items
   without abstracts are uncodable; `--allow-missing-abstract` exists but is NOT the frozen path.
2. **Text-driven-stratum unresolved handling** (build_text_driven_stratum.py): STRICT — an item
   counts as divergent only when both the stub-arm and full-text adjudicated codes exist and
   differ; `--unresolved stub-differs` is a preregistered sensitivity, not the primary.
3. **Tipping-point comparator population** (tipping_point.py missing): tier-restricted — the H1
   comparator uses the T1∪T2 missing-stratum pool, not the flat all-tier missing pool (210); the full-pool figure is
   reported descriptively.
4. **H2 adversarial-flip objective** (adversarial_flip.py): minimize the minimum decision-rule
   margin min(LCL−1) across OR_pro and ROR (H1 uses the spec's single-effect wording directly).
5. **P(non-excluded) numerator** (firewalled_yield.py): item-level D1-unresolved basis
   (pilot-consistent); `--excl-dims all` is a preregistered sensitivity.
6. **Flip-candidate scope** (tipping_point.py flips): all 2-1 majority verdicts are candidates
   (not stub-congruent only); congruence flags are exported so the congruent-only variant is a
   computable sensitivity.

## 12. dk decision register (open items blocking or shaping the freeze)

Each item: evidence pointer → options → proposed default → `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`.

**0. Denominator wording (DEN-H1/DEN-H2, §3.1–3.2, incl. B-inclusion sensitivity).**
G1-review carry-over (addendum F: "H2 denominator definition frozen in the analysis plan").
Default: adopt §3 as written (incl. the v1.1 condition-6 exception and membership
re-evaluation rules). `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**1. Primary arm — raw vs laundered coding for P4 (battery §B4; G1 §8 item 3).**
Evidence: r1 both-arm gate comparison — raw min-α D1 .734 / D2 .673 / D3 .608 / D4 .569 vs
laundered .671 / .717 / .681 / .609; D4 failed under both (text-intrinsic); D2 raw-fail/
laundered-pass (register cue); D1 raw-pass/laundered-fail (paraphrase perturbs scope cues);
per-coder divergence A 9–18% / B 5–13% / C 13–22%. **Caveat: the v1.4a re-gate ran the raw arm
only; the laundered arm was never re-measured under opus-A + majority-of-3** — choosing
laundered-primary would rest on sonnet-era evidence. Options: (a) raw primary + laundered
sensitivity, with the B9 conditional override; (b) laundered primary. **v1.1 rider (closes the
ungated-arm loop):** whichever arm is primary, the §6 checkpoint tranche is coded in both arms,
and the B9 switch is subject to the §6 laundered-arm eligibility rule — if B9 fires and the
laundered arm has not independently passed the dual checkpoint statistic, H2 degrades to
non-confirmatory instead of switching onto an ungated instrument. Default: **(a) + rider**.
`[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**2. B1 determinism floors (§9 rows B1a–B1c).**
The 95% per-run floor is unreachable at B/C endpoints; proposal shifts the binding floor to the
consolidated level (B1c ≥ 95%) with a 70% per-run sanity floor and a 2% run-split ceiling.
**v1.1 correction of record: B1c was never measured at P1** — the v1.0 "comfortably implied"
evidence conflated 3-way run splits with consolidated re-run stability; measured 2-1 run-split
rates project coder C at ≈ 94–95% on D1 (at/below the floor), so the B1c REVISE (k-raise 3→5 +
full re-consolidation) is registered as **expected possibly-live at P4**. Options: (a) as
proposed in §9; (b) preregister self-consistency-of-k with k = 5 from the start (cost +67%);
(c) **measure B1c pre-freeze** on a small slice (e.g., 20 items × 2 pipeline re-runs = 6 extra
runs/item/coder) to replace the projection with a datum before committing to the floor.
Default: **(a)**, with (c) recommended if budget allows. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**3. Hypothesis-blind hired-human audit (~50 real-corpus items) coupled to the checkpoint
(G1 addendum D; dk's stated preference on record = (b)).**
Evidence: dev-half 97–100% vs real-corpus α .70–.74 — synthetic items are easier than real ones;
the criterion-validity gap is otherwise stated as an unquantified limitation. Options:
(a) limitation-only, gap quantified; (b) hired-human audit — **requires a dk amendment to
absolute rule 5 (zero-human)**, plus: abstract wording changes ("zero human item-coding" →
"no designer or investigator coding; an independent, hypothesis-blind, hired human audit of 50
items is reported as external calibration"), CLAUDE.md rule 5 edit, agent-contract edits, and a
preregistered audit protocol (sampling frame, blinding, no adjudication authority — audit is
*measured against*, never *overrides*, the instrument). If (b), the protocol must be frozen at P3
with the rest. Interaction (v1.1): if (b) is adopted, it supplements but does not replace the
§12 item 15 probes — the audit measures accuracy, item 15 guards direction-bias. Default: none —
this is an absolute-rule amendment and is dk's alone. `[dk: **REJECTED 2026-07-17** — zero-human rule stands unamended. dk's stated rationale: any human audit channel the designer commissions is a designer-opinion contamination path ("인간 감사는 내 의견이 들어갈 수 있으므로 거절. 모두 기계로만"); the PI is the system's only hypothesis-aware human, so a hired auditor selected/briefed by the PI does not restore independence. Option (a) adopted: the criterion-validity gap is stated as the principal limitation with the dev-half (97–100%) vs real-corpus pairwise-α (.70–.84) figures quoted, and no human criterion exists anywhere in the pipeline — by design, not by omission.]`

**4. Adjudicator seat (C) — final assignment by the preregistered B6 rule.**
Rule of record: "highest dev-half synthetic accuracy AND lowest asymmetric error-correlation with
the other two, computed on pilot real-corpus disagreement items." **v1.1 mechanization: the
accuracy term = unweighted mean over the four dimensions' dev-half accuracies; ties broken by
the asymmetry term** (v1.0 left the aggregation open; outcome-robust here — C is 100 on all
four — but the rule, not the outcome, freezes). Computed inputs (gold excluded; 56 real-corpus
2-1 resolutions, adjudication-log Final round §F2/Appendix F):

| Family | Dev-half accuracy (D1/D2/D3/D4) | Tie-break asymmetry when the other two disagree |
|---|---|---|
| A | 97/100/100/97 | sides B 18 vs C 14 → **.563** toward B (n=32) — most symmetric |
| B | 97/100/97/100 | sides C 24 vs A 18 → .571 toward C (n=42) |
| C | **100/100/100/100** | sides B 24 vs A 14 → **.632** toward B (n=38) — least symmetric |

Companion diagnostic (n=89): P(B=C | A≠B) = D1 .45 / D2 .71 / D3 .73 / D4 .75 — no lockstep bloc.
**The rule's two terms point to different families (accuracy → C; symmetry → A), so the
combination procedure itself must be frozen.** Options: (a) lexicographic accuracy-first with an
asymmetry veto at ≥ .75 → **C retained** (passes veto at .632); (b) symmetry-first → A (then the
reliability pair becomes B×C — note D3 B×C = 1.000 is the pair the min-pairwise design flags as a
correlated-prior watch item); (c) composite score (requires a frozen weighting).
**v1.1 mandatory addition (neutralizes the post-data selection of the combination procedure —
the pilot votes are already seen, which no procedure choice can un-see):** all headline effects
are re-estimated under the alternative seating (A as adjudicator) and published alongside the
primary, with a **frozen divergence rule: if the two seatings yield different §2.2/§2.3 verdicts
on any hypothesis, confirmatory language for that hypothesis is withdrawn** (reported as
adjudication-dependent). Default: **(a) + the co-analysis**, with the §6.3 alarm as the
in-flight guard. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**5. Checkpoint-tranche (first 150 P4 items) in the confirmatory denominators.**
Options: (a) exclude (clean pilot-analogy; costs ≈ 5% of corpus ≈ 6–7 expected POS items —
material at the §7 power margin); (b) include, with a checkpoint-stratum sensitivity column.
**v1.1 correction: v1.0's "inclusion carries no optional-stopping hazard" argument was wrong.**
Halting on failure removes multiplicity across analyses, but not conditioning: given that the
run continues, the tranche's realized codes are selected for above-threshold inter-family
agreement, while the remaining ~2,750 items' codes are unconditioned — and agreement plausibly
correlates with folklore-congruent coding (the premise of B2/B6-adj). The bias is second-order
at 150/2,900 but not zero. Default **(b)** is therefore adopted only with two frozen riders:
(1) **conditional-verdict rule — if any headline decision rule is met with the tranche included
but not with it excluded, the excluded verdict governs** and the discrepancy is reported (the
sensitivity column is claim-relevant, not publish-only); (2) the tranche is a **seeded random
draw** within the venue/year constraints (§6; seed in manifest item 11), so no ordering
discretion exists. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**5′. Calibration-sample disposition (the 150 coder-B single-run pre-freeze items; §7.0).**
v1.0 referenced this register item without creating it — 150 real-corpus items touched by one
coder family outside the frozen protocol had no registered disposition. Options: (a) **include
in confirmatory denominators**: the 150 items re-enter P4 as ordinary items — fresh tri-coder
coding under the frozen instrument; coder B's calibration outputs are **never merged** into
confirmatory codes; a `calib_exposed` flag ships in the public data (coder-B prior single-run
exposure disclosed; per-call statelessness noted, disclosure registered anyway); preregistered
sensitivity: headline effects recomputed excluding the 150. (b) exclude from confirmatory
denominators entirely (cost: ≈ 10 expected POS items at calibration rates — material at the §7
power margin). Disclosure artifact either way: manifest item 25. Default: **(a)**.
`[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**6. Review-essay 15 (reversibly excluded at G2).**
Options: (a) sustain exclusion (consistent with the article-only inclusion rule; count reported);
(b) include as a flagged separate class (descriptive only, never in DEN-H1/H2). Default: **(a)**.
`[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**7. CL-1..CL-5 hypothesis-wording audit (G1 addendum F).**
dk audits the five v1.3 clarifications for hypothesis-neutrality before freeze; sign-off recorded
in the manifest. Pure review task; no default needed. `[dk: pending]`

**8. Residual boundary one-liners R3/R6 (adjudication-log §F7).**
The revision-loop budget is exhausted; §F7 recommends carrying R1/R2/R4/R5 as boundary noise and
flags only R3 (NA-vs-pro on successful defenses) and R6 (neutral-vs-NA labeling seam) as having
plausible one-line hypothesis-neutral fixes — an out-of-loop, dk-only, pre-freeze discretionary
edit weighed against over-fitting. If exercised → codebook v1.4d + prompt rebuild + manifest.
**v1.1 consequence rider: exercising the discretion (i) voids G1 as reliability evidence for the
frozen instrument (G1 measured v1.4c, and the registration may not present gate evidence that
does not pertain to the registered instrument) and (ii) designates the §6 checkpoint as the SOLE
reliability gate for v1.4d — halt semantics unchanged, checkpoint parameters unmodifiable in
response.** If that trade is unattractive, the default (decline both) is the only clean option.
Default: **decline both** (the residue is a measured property; §5/§6 monitor it). `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**9. R1 split-variant supplementary coding pass (§8).**
The 10-step grain requires recoding S3/S4 items under a frozen split rule (build-variant prompt;
manifest item 23). Options: (a) approve as post-P4 sensitivity pass; (b) drop split grains, run
merge/drop grains only (weakens the R1 answer to the grain objection). Default: **(a)**.
`[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**10. Power shortfall response rule (§7) — single frozen two-stage trigger (v1.1 rewrite; v1.0
left two operationalizations simultaneously live).**
Frozen rule: **Stage 1 (pre-P4):** expected DEN-H1 yield computed by the §7 formula from the
locked P2 counts × the §7.0 calibration T2-stratum rates; if < 110, expand the harvest before
any P4 spend. **Stage 2 (checkpoint):** projected DEN-H1 yield recomputed by the same frozen
formula from the tranche's realized marginal counts; if < 110, expand before further spend.
**Expansion is deterministic:** the frozen preference order — (i) T1-completion, (ii) window
extension 2000–2003/2025, (iii) EJPR re-admission (reverses locked D-1) — executes until
projected yield ≥ 110; no choice among options remains open. **Firewall (v1.1): the stage-2
interim look is performed by a firewalled script whose only surfaced outputs are the trigger
boolean and marginal S/POS counts — no D2×D4, strength, or tier cross-tabs are exposed to dk (or
any agent context) before the expansion decision is logged** (an interim look at the outcome
margin that changes the population definition is defensible only if provably blind to the
association under test and deterministic in response). Budget interaction noted in manifest
item 17. Default: adopt as written. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**11. Estimand of record + missingness machinery (§4; v1.1 restructure).**
Default: (a) primary confirmatory claim = **post-2008 population** (matches the effective G2
gate; the pre-2008 stratum is structural MNAR and any rate-borrowing is untestable);
(b) whole-window claims = preregistered extension gated by §2.4 item 9 (M3 survival +
tipping-point margins, §4.2); (c) M3 anchor frozen = checkpoint-tranche adjudicated
distributions with the §4.2 fallback ladder (pilot → uniform, logged). Alternative: v1.0's
whole-window-primary with M3-as-blocker (rejected by the v1.1 review: the M-scenarios are not
bounds on the volume/DEF/tier margins, and the anchor was double-defined). `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**12. Estimator battery extension E3 = C-only (§5.1).**
Battery §B6 names four estimators; symmetry argues for five. Default: **approve**. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**13. B3 discriminator disposition (G1 §8 item 2; §9 rows B3-dis/B3-dis′).**
Options: (a) accept-with-mitigation (AUC descriptive + frozen B3-dis′ contamination check with
BLOCK teeth, now with the §9 frozen test procedure); (b) diversify the generator beyond family
E — constrained by the no-new-keys rule and the B0 lineage-disjointness requirements.
Default: **(a)**. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**14. Codebook non-coder-facing refresh (pre-freeze; requires dk approval as a codebook
revision — absolute rule 2 changelog entry).**
Three lines in codebook sections that contradict the frozen plan/battery and would otherwise be
hashed as-is into manifest item 1: (i) §9 "ordinal for D3 (CS1–CS5 is ordered)" → D3 nominal at
2 levels {DEF, POS} + NA (plan §2.1 notation of record); (ii) §9 "optionally D = open-weights
archival coder" → D **mandatory** (plan §1.1; battery §B0); (iii) §11 cost-line pointer "outline
§4.5" → outline §4.1 (where the USD 300–800 line lives). All three sections are non-coder-facing
(no prompt rebuild; the build manifest verifies). Logged in codebook §12. Default: **apply
before hashing manifest item 1**. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**15. Real-corpus direction-bias probes with BLOCK teeth (§2.4 items 7–8; §5.2; §9 B5-strat).**
v1.0's blocking gates all measured agreement or synthetic accuracy — functions of the same three
families whose shared training folklore is the threat model's named risk; the one real-corpus
accuracy gate (B3) lost its precondition when the discriminator failed both rounds, and its
replacement (B3-dis′) tests stability, not accuracy. Without a real-corpus direction-bias
blocker, an instrument in which all three families resolve ambiguous D4 calls toward the
folklore prior (pro→α, contra→β∪γ — exactly H1's prediction) passes every gate. Adopted
defaults: (i) **§5.2 adversarial folklore-flip test at the frozen 25% fraction → BLOCK** for the
affected hypothesis; (ii) **B5-strat sign persistence, evaluability-guarded (n ≥ 30) → BLOCK**
for the affected hypothesis. Independently of this item, §2.6's instrument-relative verdict
vocabulary freezes. If dk declines both promotions, §2.6 is the only remaining mitigation and
the limitation section must say so (the battery preamble already concedes real-corpus accuracy
is formally unidentified). Options: adopt both (default) / adopt one / decline both.
`[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

**16. H2 power contingency (§7; v1.1 — H2's confirmatory element was never powered).**
The §7 freeze recalculation now covers H2: registered expected counts for all 8 analysis-critical
cells and registered power for LCL(ROR) > 1 at plausible splits. Frozen contingency: if the
registered ROR power < **.5**, H2's confirmatory element re-scopes to **OR_pro** (LCL(OR_pro) > 1;
ROR remains registered *estimation*, reported with CI but carrying no supported/null verdict),
and the kill criterion reads "H2 null" against the re-scoped element. Alternative: extend the T3
frame pre-freeze (more PC venue-years / additional T3 venue — interacts with locked D-1 and
budget). Default: compute at freeze; adopt the re-scope iff power < .5. `[dk: **approved 2026-07-17 — default adopted** (register batch ruling: group A wholesale + group B per defaults)]`

---

## 13. Deviation policy

Post-freeze, no threshold, denominator, decision rule, seed, or consequence in this document may
change. Any forced deviation (e.g., a mid-run model retirement, handled per the preregistered B1
substitution protocol; a §6.3 sustained-alarm seat switch) is logged in the OSF registration's
transparent-changes section with date, cause, and scope; any deviation outside a preregistered
protocol voids the confirmatory run (absolute rule 2). The audit package publishes all component
results, including failures (B10).

## 14. Repair history (v1.1)

v1.1 (2026-07-17) is a pre-freeze repair pass against an adversarial review of v1.0:
**51 findings — 10 blocker, 27 should-fix, 14 nit; all 10 blockers and all 27 should-fixes
applied; 13 of 14 nits applied.**

- Blockers repaired: OR_contra removed from the sign-stability BLOCK (§2.3/§2.4/§5.1; battery
  §B6); B2 stratum predicate mechanized + scripts manifested (§9 B2, item 20); register item 5′
  created for the calibration 150 (§12); checkpoint interval statistic fixed to four
  per-dimension min-pairwise quantities (§2.5/§6/§9 B9a); tranche-construction rule authored as
  a frozen seeded stratified draw (§6, manifest 11/15); B1c P1 evidence corrected to
  "not measured — inferred" with measured 2-1 run-split rates and a registered expected-live
  REVISE (§9 B1c, item 2); real-corpus direction-bias probes given BLOCK teeth + §2.6
  instrument-relative verdict vocabulary (item 15); B9 laundered-arm switch closed with a
  checkpoint eligibility rule (§6, §9 B9, item 1); the n-floor "never-failed" and Haldane
  loopholes closed (§2.3/§2.5/§5.3); the missingness estimand restructured — post-2008 primary,
  tipping-point statistics, frozen M3 anchor (§4, item 11).
- Should-fixes: gate chain made the unique BLOCK authority (§2.4); CI-overlap defined + classed;
  stage-2 trigger frozen at consolidated coder level with global code replacement + FN audit
  (§3.6); M-scenario computability (anchor, fractional allocation, T1∪T2 restriction);
  battery co-amended to v1.3 and manifest item 3 widened to the full document; pin/smoke-test
  actions registered (§1.1, item 7); per-cell agreement floor mechanized (§5.3); B3-dis′ test
  procedure frozen; expansion trigger unified + firewalled (item 10); manifest rows 18–25 added;
  §6 determinism sub-audit cites B1a/B1b/B1c with run accounting; "sustained" defined + frozen
  §6.3 response; B9 aggregation = max-family AUC + named covariate estimator; codebook refresh
  routed through item 14; B7 evidence re-grounded post-gold-re-adjudication; B1a evidence
  corrected (C 80–85 per-dim); §7 H2 feasibility corrected (445 abstract-bearing) + H2 power
  registered (item 16); §7.0 population correction (T2-only 6.45% → ≈162); checkpoint-tranche
  conditioning honestly stated + conditional-verdict rule (item 5); mid-run REVISE responses
  frozen (§6.3, §9 B1c); seat-rule aggregation frozen + both-seat co-analysis (item 4); item 8
  G1-voiding rider; misclassification sensitivity preregistered (§6).
- Nits: 13 applied (§3.8 wording; §3.2 condition-6; §3.4 membership re-evaluation; §5.2
  stub-congruence definition; B7a/B7b id split; §10 decision list; item 4 aggregation; §9 B1b
  unit; B9 single-tier wording; §7 power annotation; §2.3 contra-control evaluability; B4-para
  mechanical classification; battery header bump to its real version). **1 nit escalated, not
  applied here: the CLAUDE.md rule-1 ban-list + coder-runner agent-definition update** — those
  files are outside this document's authority (orchestrator/dk action; the firewall banner now
  states the ban is effective immediately).
- Cross-document consistency: `validation-battery-v1.md` co-amended to **v1.3** (B0 unchanged;
  B1, B2, B3, B5, B6, B8, B9, B9a, B10 bodies aligned with §9; header version corrected);
  codebook edits NOT made directly — routed through §12 item 14 (dk approval hook).

## Changelog

- v1.1 (2026-07-17): repair pass per §14. No hypothesis, prediction, or registered magnitude
  changed; changes are estimand scoping (§4.0), gate mechanization, consequence-class closure,
  and evidence-citation corrections.
- v1.0 (2026-07-16): initial draft for dk review. Synthesized from outline v0.4 §4.4–4.7/§5/§6;
  validation-battery v1.2 (full); CONTEXT §3–4 (incl. G2 rulings 4.9b/4.9c); G1 report (v1.4a
  re-gate + post-declaration addendum A–F); adjudication-log §7 and Final round §F; codebook
  §9–10/§12. H1/H2 restated in codebook-v1.4 vocabulary (D3 = {DEF, POS}); B6 seat-rule inputs
  computed from the Final-round register; B10 numeric proposals annotated with P1 evidence.
