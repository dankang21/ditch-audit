# ditch-audit — Analysis Plan v1.0 (P3 preregistration draft)

2026-07-16 · Owner: dk · Status: **DRAFT for dk review — freeze candidate for the P3 OSF registration**
Companions: `codebook-v1.md` (v1.4c body, v1.4a gate protocol), `validation-battery-v1.md` (v1.2),
`analysis/g1_report.md` (v1.4a re-gate + post-declaration addendum), `docs/adjudication-log.md`
(Final round F), `outline-v0.4.md` §4–6, CONTEXT.md §3–4 (G2 rulings 4.9b/4.9c).

> **FIREWALL WARNING.** This document states the study's hypotheses, their predicted cells, and
> the analysis-critical cell list. It must NEVER be read by, quoted to, or summarized for the
> coder-runner agent or any coder-facing context. It joins the coder-runner ban list at adoption
> (CLAUDE.md absolute rule 1; the orchestrator updates the ban list and the agent definition in
> tandem).

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

### 1.2 Corpus of record (G2 PASS, dk declaration 2026-07-17; CONTEXT §4.9b/4.9c)

| Stratum | Items | Abstract coverage |
|---|---|---|
| T2∪T3 post-2008 (**effective G2 gate**) | 2,690 | 2,496 = **92.8%** (≥ 90% gate) |
| T2∪T3 pre-2008 (**preregistered missingness stratum**, §4) | 672 | 210 = 31.2% (462 missing) |
| T2∪T3 overall (T2 2,818 + T3 544; denominator after 620 source-confirmed review exclusions) | 3,362 | 2,958 = 88.0% |
| T1 topic-filtered candidates | 296 | 94.3% |
| APQ backfill (T1) | 151 | (per P2 records) |

15 abstract-bearing review essays are reversibly excluded (dk may revisit — §12 item 6).
Planning figure used in §7: **≈ 2,900 abstract-bearing T1∪T2 items** (T2 covered ≈ 2,958 −
covered-T3; T3 total 544; + T1 ≈ 279 + APQ). Exact counts are recomputed from the locked P2
files at freeze (§7 mandatory action).

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
  cleanup of record, G1 addendum F).

### 2.2 H1 — type–direction law (article level; rewritten in v1.4 terms)

**Statement.** Among mainstream-venue (T1∪T2) chain-step items whose claim strength is POS, the
load-bearing epistemic type differs by direction: pro-direction POS items are predominantly α;
contra-direction POS items are predominantly β∪γ.

**Population.** DEN-H1 (§3.1). **Statistic.** 2×2 table, rows = D2 ∈ {pro, contra}, columns =
D4 ∈ {α} vs {β∪γ}. Odds ratio

`OR_H1 = [n(pro,α) · n(contra,β∪γ)] / [n(pro,β∪γ) · n(contra,α)]`

with Woolf (logit) 95% CI; Haldane–Anscombe +0.5 on all cells if any cell = 0 (both raw and
corrected estimates reported); two-sided Fisher exact test reported alongside.

**Registered prediction.** OR_H1 ≥ 3.

**Decision semantics (frozen at P3):**

| Outcome | Verdict |
|---|---|
| 95% CI lower bound > 1 **and** point OR ≥ 3 | H1 supported at registered magnitude |
| 95% CI lower bound > 1 and 1 < point OR < 3 | H1 directionally supported, registered magnitude not met (reported as such; no re-framing) |
| 95% CI includes 1, or point OR ≤ 1 | **H1 null** (kill-criterion input) |

A confirmatory H1 claim additionally requires the full confirmatory gate chain (§2.4).

### 2.3 H2 — venue topography (rewritten in v1.4 terms)

**Statement.** Among pro-direction chain-step items, the probability of a POS (vs DEF) claim is
higher in T3 than in T1∪T2. Among contra-direction items (control), the corresponding contrast is
predicted null or reversed.

**Population.** DEN-H2 (§3.2). **Statistic.** 2×2×2 table: tier (T3 vs T1∪T2) × strength
(POS vs DEF) × direction (pro vs contra). Fit the saturated log-linear model (stdlib IPF
implementation; equivalently a logit model of POS on tier × direction). Report:

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
| OR_contra CI: includes 1 or entirely < 1 | contra-control prediction met (scored separately) |

**Kill criterion (unchanged, restated).** H1 null ∧ H2 null → no journal submission; downgrade to
descriptive-map preprint + essay. No salami-slicing; no post-hoc hypothesis swaps.

### 2.4 Confirmatory gate chain

A result may be reported as *confirmatory* only if ALL of the following hold; otherwise the run
degrades to a descriptive map (battery §B10 semantics):

1. **P4 reliability checkpoint** passed (§6) — G1 PASS is conditional on it by declaration.
2. **B2 text-driven stratum**: the headline effect re-estimated on the stratum where full-text
   codes diverge from stub codes retains OR ≥ 2 with 95% CI excluding 1 (§9 row B2).
3. **B3 vaulted-half accuracy** ≥ frozen floors at P4 (§9 row B3-acc).
4. **B6 estimator stability**: sign stability + CI overlap across the estimator battery (§5).
5. **B8 analysis-critical cell floors** met for every cell entering the claimed hypothesis (§5.3).
6. The claimed effect meets its §2.2/§2.3 decision rule.

Failure of 1 halts P4 entirely; failure of 2, 3, or 4 blocks confirmatory claims (B10 block list);
failure of 5 blocks the specific hypothesis whose cell failed; sensitivity-note components (§9)
never block but must be published.

### 2.5 Inference policy

- Two confirmatory hypotheses, one preregistered test each; no further multiplicity correction.
  Everything in §8 (robustness) and §10 (descriptive) is explicitly non-confirmatory.
- 95% CIs throughout; two-sided tests; α = .05 where a test is invoked.
- Zero-cell handling: Haldane–Anscombe 0.5; exact (conditional) estimates reported alongside.
- Bootstrap convention (used in §6): nonparametric percentile, B = 1,000, item-level resampling,
  single global RNG, loop order pair-outer/dim-inner, seed = OSF registration date (YYYYMMDD),
  FROZEN-AT-P3. (The G1 report §3 documents convention-sensitivity of extreme bounds; freezing
  the convention removes that degree of freedom.)
- All analysis scripts: Python 3.10+ stdlib-only, hashes in the freeze manifest, re-runs must be
  byte-identical (the adjudication scripts already meet this standard).

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
D3(i) ∈ {DEF, POS}; condition 5 (D4) is **not required** (H2 does not use D4; D4-`unresolved`
does not exclude from DEN-H2). Cell assignment: tier(T3 vs T1∪T2) × D3 × D2.

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
  (e.g., D4-unresolved does not exclude from DEN-H2).

### 3.5 `run_unstable` handling

`run_unstable` (3-way run split inside one coder; pilot rate 1/267 coder-items = 0.37%) items are
**included** in the primary analysis with their consolidated (run-1) value, flagged in the public
data; preregistered sensitivity: recompute headline effects excluding all run_unstable items. If
the P4 run_unstable rate exceeds the B1b threshold (§9), the affected coder's k is raised (§9
consequence) — an instrument event, not an analysis event.

### 3.6 Stage-2 full-text rule (POS candidates; T-2 mitigation)

Any item where ≥ 1 coder returns D3 = POS on the abstract is queued for full-text/front-matter
retrieval; all three coders recode on the expanded sanitized text; the stage-2 code is final and
is what enters §3.1 condition 4. Both stages logged and published; abstract-only codes retained
as a preregistered sensitivity (headline recomputed on stage-1 codes). Budget line per outline
§4.1 (USD 300–800).

### 3.7 Majority vs unanimity sensitivity

Preregistered: all headline effects recomputed on the **unanimous-only** denominator (items where
A=B=C on every denominator-relevant dimension before adjudication). Direction of expected bias is
unknown a priori; divergence between majority and unanimous estimates beyond the §5 stability
bands is reported as an adjudication-sensitivity finding (links to the B6 folklore-congruence
audit).

### 3.8 Unit rules

Article = unit; primary thesis only. Dual-claim coding on a 10% random subsample (seeded, seed in
manifest) as sensitivity (outline §4.2). Discussion notes coded normally, flagged `CHAIN`,
analyzed separately (descriptive). The pilot's 89 items and the 20 gold anchors are **excluded
from all confirmatory denominators** (pilot data excluded per outline §4.7; anchors are curated
and memorization-suspect). Checkpoint-tranche handling: §12 item 5.

---

## 4. Missing-abstract stratum plan (G2 stratified interpretation, CONTEXT §4.9b)

The pre-2008 no-abstract stratum (672 items; 462 missing abstracts, concentrated in PC 2004–07
and IJPR/Sophia early years) is structural missingness (publishing-practice era boundary), not
random. It is modeled, not hidden:

### 4.1 Era×venue bias table (published deliverable)

Rows = venue (F&P, RS, IJPR, Sophia, PC; + T1 venues); columns = era (2004–2007, 2008–2024).
Cells: item count, abstract coverage %, and observable-covariate profiles computable **without
abstracts**: article type (research/note), title-keyword topic profile (mechanical stdlib keyword
tally against a frozen keyword list — no LLM role, preserving the B0 role matrix), page count
where available. Covered-vs-missing profile differences reported per venue.

### 4.2 Sensitivity scenarios (preregistered; carried by both H1 and H2)

Missing pre-2008 items cannot be coded; scenarios impute their **aggregate** cell contributions.
Two levels × three scenarios:

**Level (a) — raw adversarial bound (reported once, expected uninformative):** all 462 missing
items assumed in-chain POS with the adversarial direction×type assignment. This bound will
typically nullify any effect and is reported to demonstrate the necessity of level (b).

**Level (b) — rate-adjusted bounds (the operative sensitivity):** missing items are assumed
in-chain and POS at the pilot rates (P(S) = .290, P(POS|S) = .150 → expected ≈ 20 POS items among
462; recomputed with checkpoint-tranche rates at P4), allocated:

| Scenario | Direction | D4 (for H1) | Tier (for H2) |
|---|---|---|---|
| M1 all-pro | all pro | adversarial vs H1 (all β∪γ) | per stratum composition (PC portion → T3) |
| M2 all-contra | all contra | adversarial vs H1 (all α) | same |
| M3 pilot-proportional | pilot direction distribution | pilot type distribution | same |

Report each headline OR under M1/M2/M3 alongside the primary estimate.

**Claim consequence (PROPOSED; [dk: pending — §12 item 11]):** a confirmatory claim requires
survival (decision rule still met) under **M3**; M1/M2 rate-adjusted bounds are sensitivity-notes
(published envelope), not blockers. Rationale: M1/M2 are deliberately adversarial on every free
margin simultaneously; M3 is the empirically anchored scenario.

### 4.3 Reporting frame

The paper reports H1/H2 on the coded corpus with the missingness stratum explicitly bounded, and
the era-restricted (2008–2024) estimates as a companion column — this doubles as robustness R4's
late window.

---

## 5. Estimator-stability battery, tipping point, per-cell floors

### 5.1 Estimator battery (battery §B6, extended)

Headline effects (OR_H1, OR_pro, OR_contra, ROR) are computed under five estimators:

| ID | Estimator |
|---|---|
| E0 | unanimous-consensus-only (drop all items with any coder disagreement on denominator dimensions) |
| E1 | coder A only |
| E2 | coder B only |
| E3 | coder C only *(extension beyond battery §B6's four — [dk: pending, §12 item 12])* |
| E4 | majority-of-three (**primary**) |

**Stability requirement (confirmatory; FROZEN-AT-P3):** across all estimators, (i) sign stability
(every point OR on the same side of 1), (ii) 95% CI overlap with the primary estimate, (iii)
per-family OR ratio OR(Ei)/OR(E4) ∈ [0.5, 2] (battery PROVISIONAL, proposed frozen as-is).
Sign instability on any headline effect **blocks all confirmatory claims** (B10 block list).

### 5.2 Tipping-point analysis

For each headline effect: the minimum number (and identity pattern) of 2-1 adjudicated items in
analysis-critical cells whose flip moves the 95% CI to include 1, reported as a count and as a
fraction of all 2-1 resolutions in those cells. **Folklore stress test (preregistered
sensitivity-note):** recompute each headline effect with every *stub-congruent* 2-1 resolution
(B2 stub mode = adopted value; the folklore-suspect subset — pilot toward-share 0.55) flipped to
its minority value; report whether the decision rule survives. P1 basis: adjudication-log §F6.

### 5.3 Analysis-critical cells and per-cell floors (battery §B8, frozen list)

**H1 cells (4):** {pro, contra} × {α, β∪γ} within DEN-H1.
**H2 cells (8):** {T3, T1∪T2} × {POS, DEF} × {pro, contra} within DEN-H2.

Each analysis-critical cell carries (values per §9 rows B8):
- pairwise raw coder agreement ≥ 0.60 with cell n ≥ 15 (agreement floor);
- synthetic-criterion accuracy ≥ 70% on the cell's B3 items (n ≥ 10) — applies to the four
  synthetic-covered construct cells (B3: pro×POS×α, contra×POS×β∪γ, anti-folklore pro×POS×β,
  anti-folklore contra×POS×α); venue-tier cells are exempt by design (D5 is metadata-joined) and
  carry the agreement floor only;
- published cell-wise confusion matrices.

**Consequence:** an analysis-critical cell failing its floor blocks the confirmatory claim for
the hypothesis it enters (the other hypothesis is unaffected); the effect is additionally
re-estimated excluding the failing cell's items as a labeled sensitivity. A cell failing its
**n-floor** (n < 15) triggers the §7 yield rule, not a validity verdict.

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
| Sample | the **first 150 items of the P4 coding run** — fresh items only, zero pilot overlap, drawn from held-out venue-years (pilot used RS 2015 + IJPR 2015); tranche constrained to span ≥ 4 venues and ≥ 6 distinct years |
| Statistic 1 (point) | min pairwise Krippendorff α over {(A,B),(A,C),(B,C)} ≥ **.70** on every dimension (D1/D2/D4 nominal; D3 nominal ≡ ordinal at 2 levels) |
| Statistic 2 (interval) | bootstrap 95% lower bound ≥ **.667** (Krippendorff's tentative-conclusion floor) on every dimension; bootstrap per §2.5 convention |
| Pass rule | **both** statistics, **every** dimension |
| Determinism sub-audit | n = 50 subsample re-coded twice per family; scored per §9 rows B1a/B1b |
| Also reported | conditional-agreement diagnostic (§6.3); per-cell floor status on cells populated so far (§5.3); run_unstable rate |
| On PASS | continue P4; checkpoint results published with the gate report |
| On FAIL | **halt P4 coding immediately; no confirmatory claims from any already-coded material**; dk decides between descriptive downgrade and instrument redesign — the G1 revision budget is exhausted, so redesign restarts the gate cycle, it does not patch it |

**Rationale for n = 150.** At n = 89 the bootstrap intervals had half-widths ≈ ±.10–.15; at
n = 150 the expected shrinkage (∝ √(89/150) ≈ 0.77) brings a true α ≈ .78–.80 instrument
comfortably past the .667 lower-bound criterion, while a true-α ≈ .70 instrument will fail
statistic 2 — which is the intended behavior (the checkpoint is load-bearing, not decorative).

**Reporting frame for the paper (frozen wording):** "tentative-band reliability,
checkpoint-confirmed."

### 6.3 Conditional-agreement alarm (family-correlation watch)

P(B=C | A≠B) per dimension on the checkpoint sample (P1 baseline: D1 .45 / D2 .71 / D3 .73 /
D4 .75 — no lockstep bloc). PROPOSED alarm (FROZEN-AT-P3): any dimension sustained ≥ **0.90**
→ preregistered family-correlation alarm; the majority rule and adjudicator seating are
re-examined by dk before further P4 spend (seating C then double-counts the B-family prior).

---

## 7. Statistical power and yield (mandatory freeze recalculation; G1 addendum B)

### 7.0 Calibration update (2026-07-17 — supersedes pilot-rate estimates below)

Stratified corpus calibration sample: n = 150 abstract-bearing T2∪T3 items (seed 20260717,
manifest `data/raw/calib_sample_manifest.json`), sanitized, coded by coder B, single run
(calibration-only; confirmatory treatment of these 150 items = dk decision register item 5').
Results (Wilson 95% CIs):
- P(S-coded) = 59/150 = **39.3%** [31.9, 47.3] — higher than the pilot's 29.0% (specialist-journal corpus is more chain-relevant than the pilot venue mix).
- P(POS | S) = 10/59 = **16.9%** [9.5, 28.5].
- Effective H1 rate = **6.67%** → expected POS in the 2,958-abstract T2∪T3 corpus:
  **~197 point** [conservative 89, optimistic 398], before T1 additions and before the
  full-text pass on POS candidates (which can only add).
Reading against §7's power table: the point estimate lands in the adequate-power band; only
the conservative lower bound falls below the 110 trigger. Recommended operationalization of
decision item 10: key the expansion trigger on the **realized POS yield of the P4 checkpoint
tranche** (first 150 items), not on a pre-P4 commitment.
Caveats: single-coder (B), single-run estimate; D1 distribution of note — S6 items exist in
the corpus (3/150), so the A21 promotion path (codebook §8) is live.


The outline's power sketch (300–450 CS4+ from 1,500 abstracts) is off by ~5× against pilot rates.
Recalculation on the corpus of record:

**Expected DEN-H1 yield** = N_abstracts(T1∪T2) × P(S) × P(POS|S)
≈ 2,900 × .290 × .150 ≈ **126 POS items** (central).
Propagating the pilot CIs: ≈ **[44, 300]** at the P(POS|S) interval alone; the dominant
uncertainty is P(POS|S) (n = 20 pilot S-items). D3=POS at stage-2 (full text) may raise this
rate relative to abstract-only coding (abstract understatement, codebook §11) — direction known,
magnitude unknown.

**Power sketch for H1** (Woolf normal approximation; OR = 3; contra α-share assumed .35;
α = .05 two-sided):

| n(DEN-H1) | pro:contra split | Power for OR = 3 |
|---|---|---|
| 80 | 60:40 | .64 |
| 126 | 60:40 | .83 |
| 126 | 70:30 | .77 |
| 200 | 60:40 | .96 |

**Mandatory freeze action (registered):** recompute N_abstracts and the yield chain
`target_POS / [P(S) · P(POS|S) · P(non-excluded)]` on the locked P2 counts before the freeze is
signed. **PROPOSED trigger:** if the central expected DEN-H1 yield < **110** (power < ~.75 at a
60:40 split), the harvest is expanded **before any P4 spend** — candidate expansions in
preference order: (i) complete T1 venue-years not yet harvested, (ii) window extension
(2000–2003 / 2025), (iii) EJPR re-admission (reverses locked D-1) — each a dk decision (§12
item 10). This resolves jointly with the 3× majority-of-3 and ~2.5–3× battery cost multipliers
(B12; G1 §7c): the P4 budget estimate is a freeze-manifest item.

**H2 cell feasibility.** The binding cells are T3 (PC 544 items; ≈ 490 abstract-bearing;
× .29 ≈ 140 chain items). Direction and strength splits within T3 are unknown at pilot (pilot
was T2-only); the §5.3 n ≥ 15 cell floors are checked at the checkpoint and P4 midpoint, with
the same expansion rule if a critical H2 cell projects under floor.

---

## 8. Robustness battery (outline §5, restated operationally) and mirror audit

All items in this section are **non-confirmatory** (sensitivity/robustness), published in full.

- **R1 — alternative partitions.** Variants: 7-step (merge S7+S8 → deterministic relabel of coded
  D1), 10-step (split S3 into unicity/aseity vs sovereignty; split S4 via the Mill finite-god
  cut), liberal-target (drop S7: S7 items excluded, S8 retained with its γ-dependence noted).
  Merges and drops are deterministic relabels of frozen codes. **Splits cannot be recovered from
  coded data**: they require a scoped supplementary coding pass (S3- and S4-coded items only,
  same frozen coders, a frozen two-way split rule appended as a build-variant prompt — never a
  modification of the primary prompt). PROPOSED: run the split pass post-P4 as preregistered
  sensitivity [dk: pending — §12 item 9]. H1/H2 must persist (decision rules re-met) across all
  admissible grains for the invariance claim; divergences reported per grain.
- **R2 — F&P tier flip.** H2 recomputed with F&P assigned T3. Both assignments published;
  the primary is the frozen tier table.
- **R3 — dominant-author exclusion.** Drop items authored by Swinburne, Plantinga, Draper, Oppy
  (metadata join, post-coding — blinding untouched); recompute H1/H2.
- **R4 — time split.** 2004–2013 vs 2014–2024; report tier × strength topography per window
  (the 2008 era boundary additionally reported per §4.3).
- **R5 — citation-weighted rerun.** Weights = log(1 + citations) from a single frozen snapshot
  (source and date in manifest); robustness-only by outline fiat.
- **B7 — reversed-default deletion test.** D4 re-derived under the reversed tie-break polarity
  ("delete the a-priori premise; if the argument still runs, code β") on all DEN-H1 items;
  report the fraction of D4 codes that are tie-break-decided; H1 must survive both polarities
  (sign + CI); PROPOSED sensitivity-note threshold: tie-break-decided fraction > 30% of DEN-H1
  items → prominent limitation flag (§9 row B7).
- **B7 — strata monitors.** Confidence- and text-length-stratified headline estimates;
  metadata-only null baseline (non-coder context; quantifies the prior-driven ceiling).
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

| ID | Component | PROVISIONAL (battery v1.2) | PROPOSED frozen value | P1 evidence | Consequence |
|---|---|---|---|---|---|
| B1a | Per-run decoding determinism (exact-match, 2 identical invocations, per dim per coder) | ≥ 95% | **report descriptively; sanity floor ≥ 70%** — the binding metric moves to B1c ◆ | measured: A′ 95–100, B 85–95, C 70–85; 95% unreachable at B/C endpoints (temperature not settable); majority-of-3 adopted as mitigation | < 70%: REVISE (coder k raised 3→5 for that coder; checkpoint sample recoded) |
| B1b | Consolidated run-split rate (`run_unstable` per coder) | — (new, v1.4a) | **≤ 2%** per coder per dimension; alarm at 5% | measured 0.37% worst (C, 1/267); A = B = 0 | > 2%: NOTE + k raised 3→5; > 5%: REVISE (halt, dk review) |
| B1c | Consolidated-output determinism (majority-of-3 pipeline re-run twice, n = 50 checkpoint subsample) | — (new) | **≥ 95%** exact-match per dimension per coder | 1/267 run splits → consolidated determinism ≥ 95% comfortably implied; restores the original floor's intent at the consolidated level | < 95%: REVISE (k raised; determinism re-audited before continuing) |
| B2 | Text-driven-stratum requirement | stratum OR ≥ 2, CI excl. 1 | **freeze as-is** | stub-recovery D2 .35–.51 (direction is text-driven, not topic-recoverable) → a substantial text-driven stratum exists; D1 stub-recovery high (.60–.76) = step ≈ topic, benign | fail: **BLOCK** (B10 list) |
| B3-acc | Synthetic accuracy floors (per coder; dev at P1, **vault at P4 is binding**) | D1 ≥ 85, D2 ≥ 85, D3 ≥ 70, D4 ≥ 75 | **D1 ≥ 85, D2 ≥ 85, D3 ≥ 85 (raised ◆), D4 ≥ 75** | dev-half measured 97–100 all coders all dims; D3 floor of 70 was set for the 5-level scale — at 2 levels chance = 50% and measured is 97–100, so 70 is vacuous | vault-half below floor at P4: **BLOCK** (B10 list) |
| B3-dis | Real-vs-synthetic discriminator | AUC ≤ 0.60 (precondition for trusting B3-acc) | **FAILED both rounds; re-launder cap reached.** PROPOSED (default): accept-with-mitigation ◆ — AUC reported descriptively; add frozen contamination check B3-dis′ | R1 AUC .867–.991; R2 .709–.909; cause = family-E style fingerprint (24% laundered-real misread SYNTH vs 0% scrub-only); exam-mode natural experiment: C's codes *more* stable on flagged items (0.50 vs 0.81 dims changed) — distinguishability ≠ coding contamination | AUC itself: NOTE. See B3-dis′ |
| B3-dis′ | Coding-contamination check (new, replaces the AUC gate's teeth) | — | items a coder flags as synthetic must NOT show **higher** code-instability than unflagged (one-sided; raw-vs-laundered dims-changed comparison, per coder) | r1 measurement: flagged 0.50 vs unflagged 0.81 (more stable) — passes | fail at P4: B3-acc loses confirmatory weight → **BLOCK** |
| B4-flip | Contrast-set flip-tracking | ≥ 80% per dim | **freeze 80%** | not measured at P1 (P4 arm); B3 near-ceiling accuracy is weak indirect support | below: NOTE + per-cell reliance flagged on affected dimension |
| B4-para | Paraphrase stability (code-flip rate) | ≤ 10% | **≤ 10% light-rewording; ≤ 20% deep-restructure (reported)** ◆ | raw-vs-laundered divergence 5–22% per coder (A 9–18, B 5–13, C 13–22) — includes genuine register effects, upper-bounds paraphrase instability | above: NOTE; interpret jointly with B2 only (folklore coders are maximally stable — necessary-not-sufficient caveat of record) |
| B4-cue | Cue-fidelity band for paraphrased items | preregistered band | **hedge/modal/directive term counts within ±20% of source** ◆ | not P1-measured; 3-round re-launder cap carried from B3 | violation: item re-laundered (cap 3) else scrub-only version used |
| B5 | Recognition-probe validation (planted-famous detection) | ≥ 90% | **freeze 90%, pooled "identified by ≥ 1 family"** | measured pooled 19/20 = 95% (per-family A 65 / B 85 / C 90) | below: stratification unusable → memorization bound weakens; NOTE + limitation |
| B5-strat | Fame-stratified re-estimation | — | headline effects re-estimated on the unrecognized stratum; sign must persist | pilot unrecognized stratum n = 1 (A14) — statistically empty; expected to be large on the obscure corpus | sign flip: NOTE (prominent); does not block (memorization is bounded, not eliminated — Duan et al. caveat) |
| B6-est | Estimator stability | per-family OR ratio ∈ [0.5, 2] | **freeze as-is** + sign stability + CI overlap (§5.1) | not estimable at pilot (3 POS items); pilot minority structure shows no global outlier coder | sign instability: **BLOCK** (B10); ratio breach: NOTE |
| B6-adj | Conditional-agreement alarm | alarm at ≈ 1 | **≥ 0.90 sustained on any dimension** (§6.3) | P1 baseline .45–.75, no lockstep bloc | alarm: REVISE (adjudication design re-examined by dk before further spend) |
| B7 | Reversed deletion test | both polarities | **freeze**; tie-break-decided fraction reported; NOTE flag if > 30% of DEN-H1 | D4 was the weakest gate dimension (.705 min; α↔β crux A04/A05/A07 family) — polarity dependence is a live risk | headline fails reversed polarity: NOTE (prominent limitation; confirmatory language downgraded to polarity-conditional) ◆ |
| B8-agr | Per-cell agreement floor | ≥ 0.60 pairwise raw, n ≥ 15 | **freeze as-is** | pilot cells too sparse to test; gate-level agreement passed | analysis-critical cell fails: **BLOCK for that hypothesis** (§5.3) |
| B8-syn | Per-cell synthetic accuracy | ≥ 70%, n ≥ 10 | **freeze as-is** (four construct cells; venue cells exempt) | dev-half construct cells at ceiling | same as B8-agr |
| B9 | Venue-register control | AUC > 0.65 → laundered arm mandatory-primary for tier analysis | **freeze as-is**; measurable only at P4 (pilot single-venue) | not estimable at P1 (T3 absent from pilot) | trigger fires: laundered arm becomes primary for H2 only + register-matched strata + predicted-tier covariate |
| B9a | Confirmatory checkpoint | size/statistics frozen at P3 | **n = 150; dual statistic (point ≥ .70 ∧ bootstrap LB ≥ .667, every dimension)** (§6) | n = 89 CIs: 8/12 cells LB < .70; gold-exclusion drop (3 cells .676–.696); five-round selection structure | fail: **halt P4; BLOCK everything**; dk chooses downgrade vs redesign |

---

## 10. Descriptive outputs (non-confirmatory)

- **Computed step status** (outline §4.4, POS ≡ CS4+): per step over T1∪T2 within window —
  *contested* := both directions ≥ k POS items; *headwind* := POS one-sided with opposing side
  DEF-only; *frozen* := no POS either side in the trailing 10 years. Reported at k ∈ {2, 3, 5}.
  The Table-1 status column is thereby recomputed, not asserted.
- Per-step direction × strength × type maps; venue-tier topography maps; B-prevalence (input to
  outline §7); S6 scarcity check (first clear S6 item promoted to anchor A21 with logged
  promotion, codebook §8); flag-class tallies (H, RE, CHAIN, MULTI).
- Full battery results including failures (B10 publication rule); cost log.

---

## 11. P3 freeze manifest (prereg-guardian machine-verification targets)

SHA256 per file; manifest signed at OSF registration; any post-freeze edit voids the run
(absolute rule 2).

| # | Item |
|---|---|
| 1 | `docs/codebook-v1.md` — frozen version of record (v1.4c, or v1.4d if dk exercises the §F7 R3/R6 discretion before freeze — §12 item 8) |
| 2 | `pipeline/03_code/coder_prompt.txt` + build manifest (rebuilt iff item 1 changes) |
| 3 | `docs/validation-battery-v1.md` with §B10 numeric table finalized from §9 above |
| 4 | `docs/analysis-plan-v1.md` (this document, post-§12 resolutions) |
| 5 | `docs/gold-anchors-v1.json` (gold v1.3) |
| 6 | `docs/synthetic-specs-v1.json` + **vaulted-half SHA256** (hash registered; vault opened once at P4) |
| 7 | Model snapshot pins: A `claude-opus-4-8` · B `gemini-3.5-flash` · C `gpt-5.5-2026-04-23` · D (family + weights hash, confirmed at P3) · E (exact GLM model string + call dates); per-pin published retirement dates verified to cover P4 + reproduction window (B1) |
| 8 | Role-exclusivity matrix (battery §B0) |
| 9 | Venue-tier assignment table (incl. F&P = T2 primary, R2 flip preregistered) |
| 10 | Step-status k thresholds {2, 3, 5} |
| 11 | Analysis code skeleton hashes (`scripts/alpha.py`, `scripts/adjudicate.py`, `scripts/consolidate_runs.py`, + the H1/H2 analysis and bootstrap scripts to be added pre-freeze; stdlib-only; fixed seeds incl. the §2.5 bootstrap seed and §3.8 subsample seed) |
| 12 | Corpus lock: P2 harvest JSONL hashes, review-exclusion list (620), review-essay list (15), missingness-stratum item list (672/462), T1 candidate list |
| 13 | Denominator definitions DEN-H1 / DEN-H2 (§3) as dk-approved |
| 14 | Adjudicator-seat rule + frozen seat outcome + its computation inputs (§12 item 4) |
| 15 | Checkpoint spec (§6) incl. tranche-construction rule |
| 16 | dk decision register (§12) with recorded resolutions |
| 17 | P4 budget re-estimate (3× majority-of-3 × ~2.5–3× battery multiplier; B12 / G1 §7c) |

---

## 12. dk decision register (open items blocking or shaping the freeze)

Each item: evidence pointer → options → proposed default → `[dk: pending]`.

**0. Denominator wording (DEN-H1/DEN-H2, §3.1–3.2, incl. B-inclusion sensitivity).**
G1-review carry-over (addendum F: "H2 denominator definition frozen in the analysis plan").
Default: adopt §3 as written. `[dk: pending]`

**1. Primary arm — raw vs laundered coding for P4 (battery §B4; G1 §8 item 3).**
Evidence: r1 both-arm gate comparison — raw min-α D1 .734 / D2 .673 / D3 .608 / D4 .569 vs
laundered .671 / .717 / .681 / .609; D4 failed under both (text-intrinsic); D2 raw-fail/
laundered-pass (register cue); D1 raw-pass/laundered-fail (paraphrase perturbs scope cues);
per-coder divergence A 9–18% / B 5–13% / C 13–22%. **Caveat: the v1.4a re-gate ran the raw arm
only; the laundered arm was never re-measured under opus-A + majority-of-3** — choosing
laundered-primary would rest on sonnet-era evidence. Options: (a) raw primary + laundered
sensitivity, with the B9 conditional override (laundered becomes mandatory-primary for the tier
analysis if venue-inference AUC > .65); (b) laundered primary. Default: **(a)**. `[dk: pending]`

**2. B1 determinism floors (§9 rows B1a–B1c).**
The 95% per-run floor is unreachable at B/C endpoints; proposal shifts the binding floor to the
consolidated level (B1c ≥ 95%) with a 70% per-run sanity floor and a 2% run-split ceiling.
Alternative: preregister self-consistency-of-k with k = 5 from the start (cost +67%).
Default: as proposed in §9. `[dk: pending]`

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
with the rest. Default: none — this is an absolute-rule amendment and is dk's alone. `[dk: pending]`

**4. Adjudicator seat (C) — final assignment by the preregistered B6 rule.**
Rule of record: "highest dev-half synthetic accuracy AND lowest asymmetric error-correlation with
the other two, computed on pilot real-corpus disagreement items." Computed inputs (gold excluded;
56 real-corpus 2-1 resolutions, adjudication-log Final round §F2/Appendix F):

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
correlated-prior watch item); (c) composite score (requires a frozen weighting). Default: **(a)**,
with the §6.3 alarm as the in-flight guard. `[dk: pending]`

**5. Checkpoint-tranche (first 150 P4 items) in the confirmatory denominators.**
Options: (a) exclude (clean pilot-analogy; costs ≈ 5% of corpus ≈ 6–7 expected POS items —
material at the §7 power margin); (b) include, with a checkpoint-stratum sensitivity column.
Note: inclusion carries no optional-stopping hazard — checkpoint failure halts everything, so no
selection among analyzable outcomes survives; the items are coded by the same frozen instrument.
Default: **(b)**. `[dk: pending]`

**6. Review-essay 15 (reversibly excluded at G2).**
Options: (a) sustain exclusion (consistent with the article-only inclusion rule; count reported);
(b) include as a flagged separate class (descriptive only, never in DEN-H1/H2). Default: **(a)**.
`[dk: pending]`

**7. CL-1..CL-5 hypothesis-wording audit (G1 addendum F).**
dk audits the five v1.3 clarifications for hypothesis-neutrality before freeze; sign-off recorded
in the manifest. Pure review task; no default needed. `[dk: pending]`

**8. Residual boundary one-liners R3/R6 (adjudication-log §F7).**
The revision-loop budget is exhausted; §F7 recommends carrying R1/R2/R4/R5 as boundary noise and
flags only R3 (NA-vs-pro on successful defenses) and R6 (neutral-vs-NA labeling seam) as having
plausible one-line hypothesis-neutral fixes — an out-of-loop, dk-only, pre-freeze discretionary
edit weighed against over-fitting. If exercised → codebook v1.4d + prompt rebuild + manifest.
Default: **decline both** (the residue is a measured property; §5/§6 monitor it). `[dk: pending]`

**9. R1 split-variant supplementary coding pass (§8).**
The 10-step grain requires recoding S3/S4 items under a frozen split rule (build-variant prompt).
Options: (a) approve as post-P4 sensitivity pass; (b) drop split grains, run merge/drop grains
only (weakens the R1 answer to the grain objection). Default: **(a)**. `[dk: pending]`

**10. Power shortfall response rule (§7).**
Default: freeze the trigger (central expected DEN-H1 yield < 110 → expand harvest before P4
spend, preference order T1-completion → window extension → EJPR re-admission). Expansion choices
touch locked decisions (D-1) and budget. `[dk: pending]`

**11. Missingness scenarios — claim-blocking status (§4.2).**
Default: M3 survival required for confirmatory language; M1/M2 rate-adjusted bounds published as
sensitivity envelope. `[dk: pending]`

**12. Estimator battery extension E3 = C-only (§5.1).**
Battery §B6 names four estimators; symmetry argues for five. Default: **approve**. `[dk: pending]`

**13. B3 discriminator disposition (G1 §8 item 2; §9 rows B3-dis/B3-dis′).**
Options: (a) accept-with-mitigation (AUC descriptive + frozen B3-dis′ contamination check with
BLOCK teeth); (b) diversify the generator beyond family E — constrained by the no-new-keys rule
and the B0 lineage-disjointness requirements. Default: **(a)**. `[dk: pending]`

---

## 13. Deviation policy

Post-freeze, no threshold, denominator, decision rule, seed, or consequence in this document may
change. Any forced deviation (e.g., a mid-run model retirement, handled per the preregistered B1
substitution protocol) is logged in the OSF registration's transparent-changes section with date,
cause, and scope; any deviation outside a preregistered protocol voids the confirmatory run
(absolute rule 2). The audit package publishes all component results, including failures (B10).

## Changelog

- v1.0 (2026-07-16): initial draft for dk review. Synthesized from outline v0.4 §4.4–4.7/§5/§6;
  validation-battery v1.2 (full); CONTEXT §3–4 (incl. G2 rulings 4.9b/4.9c); G1 report (v1.4a
  re-gate + post-declaration addendum A–F); adjudication-log §7 and Final round §F; codebook
  §9–10/§12. H1/H2 restated in codebook-v1.4 vocabulary (D3 = {DEF, POS}); B6 seat-rule inputs
  computed from the Final-round register; B10 numeric proposals annotated with P1 evidence.
