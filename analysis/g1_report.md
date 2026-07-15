# G1 Reliability Report — P1 Pilot (ditch-audit), FINAL (v1.4a re-gate)

> **GATE DECLARATION (dk, 2026-07-16): G1 = PASS.** Declared on the preregistered statistic
> (min pairwise α ≥ 0.70, every dimension, n=89, coder output = majority-of-3) with the three
> honesty caveats below carried forward to methods. P1 closed; P2 (corpus build) authorized.


**Date:** 2026-07-16 · **Scope:** P1 pilot, **n=89** items = RS 2015 (35) + IJPR 2015 (34) + gold anchors (20), triple-coded (A=Anthropic `claude-opus-4-8`, B=Google `gemini-3.5-flash`, C=OpenAI `gpt-5.5-2026-04-23`). **Coder output = per-dimension majority of 3 independent identical runs** (codebook v1.4a §9); per-run originals in `data/coded/*.r{1,2,3}_*.jsonl`, preserved under each record's `_runs` field. **parse_fail = 0.**

**Gate spec (codebook v1.4a §9):** G1 = per-dimension **minimum pairwise Krippendorff α over {(A,B),(A,C),(B,C)} ≥ 0.70** on every dimension; 3-way joint α reported alongside; D1/D2/D4 nominal, D3 ordinal (NA = pairwise exclusion). D3 is the v1.4 collapsed 2-level scale {DEF, POS} (kill-criterion path); legacy CS gold/spec targets map CS1–3→DEF, CS4–5→POS at scoring.

**Reproduce.** Gate: `python3 scripts/alpha.py rel data/coded/all89_a.jsonl data/coded/all89_b.jsonl` (and `a c`, `b c`, and `a b c` for the 3-way). Gold: `python3 scripts/alpha.py gold data/coded/gold_anchors_{a,b,c}.jsonl --gold docs/gold-anchors-v1.json`. Consolidation: `python3 scripts/consolidate_runs.py <batch>`. Bootstrap CI method documented in §3. Battery inputs under `data/battery/`.

> **This report RECOMMENDS; it does not DECLARE.** Gate declaration is dk's (zero-human rule: dk's gate approval is instrument-design labor, not item judgment; the rule permits dk to approve the gate). The agent's recommendation and its honest caveats are in §7. The full document is designed so dk can decide PASS / re-work on the strength of this file alone.

---

## 1. Trajectory — five rounds to the re-gate

G1 round 1 failed 3 of 4 dimensions. The instrument passed on the fifth pass only after a preregistered revision loop (codebook clarification), a kill-criterion collapse (D3), a pilot-stage coder-A pin revision, and a noise-aware protocol change (majority-of-3 + corpus expansion). **Every one of these instrument choices is disclosed here; none is optional to publish** (see §7 caveat b).

**Per-round minimum pairwise α (the gate statistic), all four dimensions:**

| # | Codebook | Instrument change of record | n | D1 | D2 | D3 | D4 | Gate (min ≥ .70) |
|---|---|---|---|---|---|---|---|---|
| r1 | v1.1 | baseline; A = `claude-sonnet-5`, D3 5-level (CS1–5) | 55 | .734 | **.673** | **.608** | **.569** | **FAIL** (D2,D3,D4) |
| r2 | v1.3 | CL-1..CL-5 boundary clarifications (§7 adjud-log) | 55 | .733 | **.661** | **.609** | **.613** | **FAIL** (D2,D3,D4) |
| r3 | v1.3 + pin | **A → `claude-opus-4-8`** (D3 still 5-level) | 55 | .752 | .769 | **.479** | **.677** | **FAIL** (D3,D4) |
| r4 | v1.4 | **D3 collapsed to {DEF,POS}** (analytic collapse of r3 codes) | 55 | .752 | .769 | .718 | **.677** | **FAIL** (D4) |
| **final** | **v1.4a** | **majority-of-3 runs + IJPR-2015 expansion** | **89** | **.736** | **.727** | **.808** | **.705** | **PASS (all 4)** |

Reading the trajectory:
- **r1→r2:** codebook clarifications (CL-1..5) alone did **not** move the gate — the failing cells stayed exclusively coder-A pairs. This is the evidence of record that the residual disagreement was not document-ambiguity but a systematic A-isolate (sonnet-5).
- **r3:** the A pin revision (sonnet-5 → opus-4-8) lifted D1/D2/D4 A-pairs above .70, but exposed that the **5-level D3 was unreliable on its own** (min .479) — this is what triggered the preregistered D3 kill criterion.
- **r4:** collapsing D3 to {DEF,POS} fixed D3 (.718/.840/.873 across pairs) and left **D4 (.677) as the sole failing dimension**.
- **r4 → final:** the residual D4 gap was inside the bootstrap noise band. An independent v1.4 **single-run** fresh re-code at n=55 actually fell *further* (D1 .647 / D2 .640 / D3 .868 / D4 .690 — FAIL on D1/D2/D4), confirming that point estimates were **decoding-noise-dominated at n=55**. v1.4a's response — majority-of-3 runs (removes per-run decoding noise) plus a one-venue-year expansion to n=89 (tightens the estimate) — brought **all four minimums above .70**. (`data/coded/all55_{a,b,c}.jsonl` = the failed v1.4 single-run n=55 re-code, retained for audit.)

Archives: `data/coded/round1/` (r1), `data/coded/round2_sonnet5_a/` (r2 A) + `data/coded/round3_5level/{b,c}` (r2 B/C, carried into r3), `data/coded/round3_5level/` (r3, opus A + 5-level D3). Codebook §12 changelog and `docs/adjudication-log.md` §7 carry the CL-1..5 rationales.

---

## 2. Final gate table — v1.4a, n=89, majority-of-3 (parse_fail = 0)

| Dim | metric | A×B | A×C | B×C | **min = GATE** | verdict | 3-way joint |
|---|---|---|---|---|---|---|---|
| D1 step | nominal | 0.7357 | 0.7753 | 0.8153 | **0.7357** (ab) | **PASS** | 0.7752 |
| D2 direction | nominal | 0.7760 | 0.7274 | 0.8348 | **0.7274** (ac) | **PASS** | 0.7787 |
| D3 strength | ordinal | 0.8092 | 0.8079 | **1.0000** | **0.8079** (ac) | **PASS** | 0.8890 |
| D4 type | nominal | 0.8395 | 0.7051 | 0.7820 | **0.7051** (ac) | **PASS** | 0.7747 |

**Point-estimate gate = PASS on all four dimensions.** The 3-way joint α (.775 / .779 / .889 / .775) also clears .70 on every dimension — joint and min-pairwise agree, unlike r1 where joint masked the pairwise failures.

**Sample / exclusions.** D1/D2/D4 use all 89 units (NA is a real nominal category — no exclusion). D3 (ordinal) excludes items where either coder returned NA (neutral/X/I stop-rule cascade):

| D3 pair | units used | NA-excluded |
|---|---|---|
| A×B | 44 | 45 |
| A×C | 42 | 47 |
| B×C | 48 | 41 |
| 3-way | 50 | 39 |

The D3 gate rests on **42 paired judgments** (A×C, the binding pair), not 89. This small effective-n is what drives the wide D3 confidence interval in §3.

**Correlated-error red-flag check (§9).** The r1 pathology — every failing cell an A-pair — is gone; disagreement is now distributed, not A-isolated. One cell warrants transparency: **D3 B×C = 1.000** (perfect Google/OpenAI agreement on 48 units). Under the min-pairwise design this is exactly the "anomalously high single-pair agreement" the gate is built to surface. It does **not** inflate the gate (the gate is the min, D3 A×C .808), but two readings are live: (i) the collapsed 2-level {DEF,POS} is genuinely easy, or (ii) DEF/POS is a coarse, folklore-recoverable binary shared by two families' priors — cue-ablation D3 stub-recovery is a non-trivial .56–.62 (§5). This is a **P4 watch item** for the B2 folklore-congruence audit, not a gate blocker.

---

## 3. Bootstrap confidence intervals — the interval evidence (honest)

Nonparametric percentile bootstrap: **seed 20260716, B=1000**, resample the 89 item-units with replacement, recompute each pairwise α, take the 2.5/97.5 percentiles. (Deterministic given the seed; loop order pair-outer/dim-inner, single global RNG.)

| Dim | A×B point [95% CI] | A×C point [95% CI] | B×C point [95% CI] |
|---|---|---|---|
| D1 | 0.736 [0.632, 0.838] | 0.775 [0.672, 0.864] | 0.815 [**0.718**, 0.896] |
| D2 | 0.776 [0.661, 0.870] | 0.727 [0.595, 0.840] | 0.835 [**0.724**, 0.932] |
| D3 | 0.809 [0.429, 1.000] | 0.808 [0.457, 1.000] | 1.000 [**1.000**, 1.000] |
| D4 | 0.839 [**0.729**, 0.942] | 0.705 [0.551, 0.827] | 0.782 [0.639, 0.900] |

**8 of 12 cells have a bootstrap 95% lower bound below .70.** Only 4 cells (D1 bc, D2 bc, D3 bc, D4 ab — bolded) clear .70 at the lower bound. The **lowest bound is ≈ 0.43** (D3 A×B .429 / A×C .457) — the D3 small-effective-unit cells (42–44 paired judgments, and resamples can collapse to near-single-category), producing very wide intervals. D3 B×C is degenerate at [1.000,1.000] (whenever both non-NA they always agree).

**Interpretation.** The **point-estimate gate passes** (all four minimums ≥ .70, §2), which is the preregistered statistic. But the **interval evidence is not comfortably above the floor** at n=89: two-thirds of pairwise cells could sit below .70 under resampling, and D3's reliability is estimated on very few units. This is reported transparently, not to override the gate but because it directly motivates the P4 in-flight reliability checkpoint (§7 caveat a; §8 item 5). The exact lowest bound is sensitive to bootstrap loop-order and percentile convention (.428–.449 across conventions); the qualitative finding — 8/12 below .70, lowest ≈ .43 on a D3 small-unit cell — is stable.

---

## 4. Gold diagnostic — DIAGNOSTIC ONLY (codebook §8; headline-forbidden)

Per codebook §8 and battery §B5, gold accuracy carries **zero headline construct-validity weight** (famous, memorization-suspect, and coded against designer-adjudicated keys). Construct validity lives in the synthetic criterion set (§5, B3). Reported here only as diagnostic corroboration. Scored on the majority-of-3 codes; D3 gold CS keys auto-mapped CS→DEF/POS by `alpha.py gold`.

**Per-coder gold accuracy (n=20 anchors):**

| Coder | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| A | 16/20 = 80% | 17/20 = 85% | 13/20 = 65% | 15/20 = 75% |
| B | 15/20 = 75% | 19/20 = 95% | 16/20 = 80% | 16/20 = 80% |
| C | 15/20 = 75% | 20/20 = 100% | 17/20 = 85% | 16/20 = 80% |

**Recognition-probe stratification (`recognition_gold_anchors.jsonl`; probe not re-run since r1 — it is a text-recognition task independent of the coding pin).** Probe validated: pooled "identified by ≥1 family" = **19/20 = 95% ≥ 90%** planted-famous floor (per-family A 65 / B 85 / C 90). The unrecognized stratum is **n=1 (A14 only)** → statistically empty at pilot scale but reported per rule.

**Memorization-contamination caveat (binding).** The single unrecognized anchor (A14) is also the anchor the instrument handles worst (A: D1 miss, D2/D3/D4 NA; C: D1 miss). The one item that cannot be recognized is the one coded worst → recognized-stratum accuracy **upper-bounds** obscure-corpus accuracy, and n=1 cannot estimate the unrecognized rate. **Do not read gold accuracy as validity.**

**Shared gold misses that corroborate the reliability profile** (all/most coders miss the same way → a codebook-clarity residue, not a coder-quality problem):
- **D3 A04/A05/A07 (all three coders):** A05/A07 gold CS4→POS coded DEF; A04 gold CS2→DEF coded POS. The DEF/POS boundary still leaks on defeater-rebuttal-vs-positive-evidential items — the residue of the collapsed D3.
- **D4 A04/A05/A07 (all three coders):** the alpha/beta deletion-test crux persists (A05/A07 gold beta coded alpha; A04 gold alpha coded beta). Note the gold set itself splits structurally similar evil-arguments (A01 beta vs A04 alpha) — an instrument-design tension for dk, not a coder failure.
- **D1 A06/A11/A12/A13 adjacency** (S1↔S2↔S3), A14 (unrecognized outlier).

These are the same shared-miss families flagged in r1; they now sit *below* the passing reliability, i.e. they are localized clarity residues, not gate blockers. They remain candidate CL drafts for a pre-P3 codebook touch-up (dk approves the document change only).

---

## 5. Battery summary (P1 arms; PROVISIONAL thresholds per validation-battery-v1)

| Arm | Metric / floor | Result | Verdict vs PROVISIONAL | Re-run status |
|---|---|---|---|---|
| **B1 determinism** (`det_report_*_s20260716.json`, n=20 re-code twice) | exact-match ≥ 95% per dim | **A′ = `opus-4-8`: 95 / 95 / 100** (D1 19/20, D2 19/20, D3 19/20, D4 20/20) | **A′ ≈ floor** (95/95/95/100) | **re-run for v1.4a** (A′ only) |
| B1 (carried, s20260714) | as above | **B: 85 / 90 / 95 / 95** · **C: 80 / 85 / 85 / 80** | B/C below 95% floor | not re-run (endpoints unchanged) |
| **majority-of-3 stability** (v1.4a §9) | 3-way run split rate | **1 coder-item / 267** (0.37%): coder C, item `33c1d57ae85edfcf`, dims D1/D2/D4. A: 0, B: 0, C: 1 | see §6 | new (v1.4a) |
| **B2 cue-ablation** (`cue_ablation_summary.json`, n=55 pilot) | P1 = feasibility/variance (no pass/fail) | stub-recoverable: A D1 .73 / D2 **.51** / D3 .56 / D4 .56 · B .76 / **.49** / .62 / .65 · C .60 / **.35** / .38 / .36 | **anti-folklore signal holds:** D2 low (.35–.51) = direction is text-driven, not topic-recoverable; D1 high = step ≈ topic (benign) | not re-run since v1.4 |
| **B3 dev-half accuracy** (`dev_half_accuracy.json`, n=30; D3 re-scored CS→DEF/POS, confirmed) | D1≥85 D2≥85 D3≥70 D4≥75 | A 97/100/**100**/97 · B 97/100/**97**/100 · C 100/100/**100**/100 | **PASS all coders, all dims, near-ceiling** (D3 DEF/POS = 30/29/30 of 30) | not re-run since v1.4; **D3 mapping re-verified** (see below) |
| **B3 discriminator** (`discriminator_p1/p2.jsonl`) — precondition for trusting B3 accuracy | AUC ≤ 0.60 (real-vs-synth) | R1: A .882 / B .867 / C .991 · R2 (re-laundered): A .709 / B .789 / C .909 | **FAIL both rounds** | not re-run since v1.4 |
| **B5 recognition probe** (`recognition_*.jsonl`) | ≥ 90% planted-famous | pooled 19/20 = 95%; per-family A 65 / B 85 / C 90 | probe validated | not re-run |

**Dev-half D3 re-verification (task-required).** Re-scoring `data/coded/synthetic_dev_v2_{a,b,c}.jsonl` against `docs/synthetic-specs-v1.json` dev-half targets with the CS→DEF/POS map reproduces `dev_half_accuracy.json` exactly (A 29/30·30/30·30/30·29/30; B 29/30·30/30·29/30·30/30; C 30/30 all). All dev-half dimensions clear the B3 floors with wide margin; D3 near-ceiling under the collapsed scale. **Construct-validity evidence is unaffected by the D3 collapse.**

**Discriminator failure — carried mitigation (unchanged since r1, not contradicted by v1.4a).** Cause = family-E (GLM) **style fingerprint**, not memorization (24% of laundered real items misread as SYNTH, 0% of scrub-only; name-swap hypothesis rejected). The r1 **exam-mode natural experiment** showed this does **not** propagate into coding: C's codes were *more* stable on the 10 items it flagged as synthetic (mean 0.50 vs 0.81 dims changed), i.e. distinguishability ≠ coding contamination. dk decision deferred to P3 (§8 item 2). Battery arms carry **P3-freeze decisions, not G1 decisions.**

---

## 6. Why majority-of-3 (v1.4a rationale, on the record)

The pinned endpoints are not sampling-deterministic (B1: A′ 95–100%, B 85–95%, C 70–85% per-dimension exact-match between two identical invocations). At single-run n=55 this decoding noise dominated the gate (the failed v1.4 single-run re-code, §1). Majority-of-3 removes per-run noise from the reliability signal, and it does so cleanly: **across all 267 coder-items (89 × 3 coders), only 1 produced a genuine three-way run split** (coder C, `33c1d57ae85edfcf`, dims D1/D2/D4 — flagged `run_unstable`, run-1 value taken). Coders A and B: zero splits. So the majority is well-defined for 266/267 coder-items, and the one split is logged, not silently resolved. Cost consequence: this **triples P4 per-coder API volume** (§7 caveat c).

---

## 7. G1 recommendation (agent recommends; dk declares)

**RECOMMENDATION: G1 = PASS** on the preregistered statistic. All four dimensions clear the min-pairwise floor: **D1 .736, D2 .727, D3 .808, D4 .705** (each ≥ 0.70), and the 3-way joint clears on every dimension. The r1 A-isolate pathology is resolved; disagreement is distributed and the gate is not carried by any single anomalous pair. dk may declare G1 PASS and advance to P2 on this basis.

**The PASS is honest only if carried with three caveats — dk should weigh these before declaring:**

**(a) Interval evidence is not comfortably above the floor.** 8 of 12 pairwise bootstrap cells have a 95% lower bound below .70 (lowest ≈ .43, D3 small-unit; §3). The point estimates pass; the intervals say the instrument sits *near* .70, not *safely above* it, and D3 reliability rests on ~42 paired units. **Recommendation:** make a **P4 in-flight reliability checkpoint** a P3-freeze item (§8 item 5) — re-compute min-pairwise α on the first ~150 P4 items with a preregistered halt/revise trigger, so the gate is re-validated on real-corpus scale before the full spend.

**(b) Pilot-stage instrument selection must be disclosed in full.** The instrument that passes is not the instrument that started P1: coder A was swapped (`sonnet-5`→`opus-4-8`), majority-of-3 was introduced, and D3 was collapsed to {DEF,POS} — all chosen during the pilot **with the gate in view**. This is a real researcher-degrees-of-freedom exposure. It is defensible **only** because (i) the D3 collapse was preregistered as a kill-criterion path, (ii) the A pin revision and majority-of-3 were logged pre-freeze with stated mechanistic rationales (not gate-chasing on the target hypotheses — coders are H1/H2-blind by the firewall), and (iii) the **entire five-round trajectory (§1) is published as the methods narrative.** Concealing any round would be misconduct; transparency is the mitigation. The paper must present §1 in full.

**(c) P4 cost is ~3× baseline.** Majority-of-3 triples per-coder coding volume (§6); the battery adds a further ~2.5–3× (B12). P4 budget must be re-estimated before the freeze.

**What is solid enough to build on:** D1–D4 reliability now all clear (majority-of-3, n=89); dev-half construct-validity accuracy is near-ceiling for all three coders and unaffected by the D3 collapse; A′ determinism is at floor; the anti-folklore signal (D2 text-driven, B2) holds; the exam-mode null stands. The weaknesses are localized and named (interval width, D3 effective-n, the E-fingerprint discriminator) — the profile of an instrument that is ready to gate **with a preregistered P4 reliability checkpoint**, not one that has failed.

---

## 8. P3-freeze decision items (dk's, re-organized; not G1 blockers)

The re-gate resolves G1 but sharpens the freeze agenda. Items dk must settle at P3 (prereg-guardian will manifest-verify the freeze):

1. **B1 determinism floor.** 95% is unreachable at B/C non-settable-temperature endpoints (B 85–95, C 80–85). Majority-of-3 is the adopted mitigation; **freeze the floor value and the rule** (lower the floor, or preregister self-consistency-of-k with k and the split-resolution rule).
2. **Discriminator replacement / mitigation.** AUC persistently > .60 (E-fingerprint, both rounds; 3-round re-launder cap reached). Freeze one of: accept-with-mitigation (exam-mode null + dev-half ceiling, §5–6) **or** diversify the generator beyond family E.
3. **Primary arm (raw vs laundered) for P4** (B4). r1 measured raw-vs-laundered divergence; the primary arm and its sensitivity twin freeze here. (Note B9: T3-register AUC is only estimable at P4, and can override this choice for the tier analysis only.)
4. **P4 in-flight reliability checkpoint (NEW — the §7a recommendation).** Freeze the checkpoint size, the re-computed statistic (min-pairwise α), and the halt/revise trigger threshold.
5. **Adjudicator seat (C) final assignment** by the B6 preregistered rule (highest dev-half accuracy + lowest asymmetric error-correlation, computed on synthetic-dev only) — the rule freezes, not the outcome.
6. **Per-cell floors (B8)** and the frozen analysis-critical cells; **vault-half hash**, model-snapshot pins, role-exclusivity matrix, and the frozen codebook (v1.4a) per absolute-rule-2.

Frozen inputs already staged: codebook v1.4a, built coder prompt + manifest, validation-battery-v1 (§B10 thresholds → numeric at P3), vault synthetic-set hash.

---

## 9. Corpus-N calibration (pilot chain-relevance, updated for n=89 / opus-A / majority-of-3)

Chain-relevance = fraction of items with D1 ≠ X (in-chain, codeable), over the **69 pilot items** (RS 2015 n=35 + IJPR 2015 n=34; gold anchors excluded — curated in-chain). Basis = cross-coder majority of the majority-of-3 codes.

| | non-X (relevant) | X | note |
|---|---|---|---|
| Coder A | 45/69 = 65% | 24 | |
| Coder B | 46/69 = 67% | 23 | |
| Coder C | 45/69 = 65% | 24 | |
| **Majority-of-3 (cross-coder)** | **39/69 = 57%** | 25 | 5 items are D1 3-way coder splits → **unresolved** |

By venue: **RS 18/35 = 51%** · **IJPR 21/34 = 62%.** Majority D1 distribution (pilot 69): X 25 · S4 13 · M 7 · I 6 · B 5 · unresolved 5 · S5 3 · S8 2 · S2 2 · P 1.

**Calibration shift vs r1.** r1 reported ~74% (RS only, n=35, single-run sonnet-5 A). The final estimate is **~57%** — lower because (i) opus-A + majority-of-3 scope more items to X/M/I, and (ii) the IJPR mix differs from RS. At ~57% majority chain-relevance, a target of *N* in-chain-codeable items needs ≈ **N / 0.57** harvested abstracts; a **1,500-abstract coded corpus yields ≈ 855 in-chain** items (down from r1's ~1,110). **Caveats:** two venues, single year, n=69; the X-rate spans 51% (RS) to 62% (IJPR) and will shift with venue tier and topic mix. Treat as an order-of-magnitude prior; re-estimate after the P2 harvest (G2).

---

## Appendix A — file provenance
- **Gate:** `data/coded/all89_{a,b,c}.jsonl` (89×3, parse_fail 0, majority-of-3); per-run originals `data/coded/{pilot_rs2015,pilot_ijpr2015,gold_anchors}.r{1,2,3}_{a,b,c}.jsonl`; consolidation `scripts/consolidate_runs.py`.
- **Trajectory archives:** `data/coded/round1/` (r1 v1.1), `data/coded/round2_sonnet5_a/` + `data/coded/round3_5level/{b,c}` (r2), `data/coded/round3_5level/` (r3), `data/coded/all55_{a,b,c}.jsonl` (failed v1.4 single-run n=55 re-code).
- **Gold:** `data/coded/gold_anchors_{a,b,c}.jsonl` vs `docs/gold-anchors-v1.json`.
- **Battery:** `data/battery/{det_report_det_pilot_rs2015_s20260716.json (A′), det_report_det_pilot_rs2015_s20260714.json (B/C), cue_ablation_summary.json, dev_half_accuracy.json, discriminator_p1.jsonl, discriminator_p2.jsonl, recognition_gold_anchors.jsonl, recognition_pilot_rs2015.jsonl}`; dev-half coded `data/coded/synthetic_dev_v2_{a,b,c}.jsonl` vs `docs/synthetic-specs-v1.json`.
- **Metrics/thresholds:** codebook v1.4a §8–§9 (§12 changelog = full round trajectory), validation-battery-v1 §B0–B12; adjudication `docs/adjudication-log.md`. `scripts/alpha.py selftest` PASS (hand-computed nominal case 0.6200; ordinal adjacent-vs-distant 0.9373 > 0.4355).

---
---

# APPENDIX R1 — Round 1 (v1.1) G1 report (PRESERVED; superseded by the v1.4a re-gate above)

> Preserved verbatim-in-substance for the audit trail and the §7(b) transparency requirement. This report reflects the **n=55, single-run, `claude-sonnet-5`-A** instrument and gated at codebook **v1.2**. Its **RAW-arm FAIL** verdict (D2/D3/D4 below .70) is the r1 row of §1 above and initiated the revision loop. Its laundered-arm, exam-mode, and disagreement-pattern analyses remain the source of record for those findings. Conclusions here are **superseded** by §§1–9; do not cite the r1 gate verdict as current.

**Date:** 2026-07-15 · **Scope:** P1 pilot, 55 items (RS 2015 n=35 + gold anchors n=20), triple-coded (A=Anthropic sonnet-5, B=Google, C=OpenAI) · parse_fail = 0 / 165 records · Gate spec: codebook v1.2 §9.

## R1.1 — G1 gate table, RAW arm (`all55`, n=55, parse_fail=0)

| Dim | metric | A×B | A×C | B×C | **min = GATE** | verdict | 3-way joint |
|---|---|---|---|---|---|---|---|
| D1 step | nominal | 0.7756 | 0.7741 | 0.7344 | **0.7344** | PASS | 0.7609 |
| D2 direction | nominal | **0.6733** | 0.6746 | 0.7591 | **0.6733** | FAIL | 0.7013 |
| D3 strength | ordinal (CS1–5) | **0.6075** | 0.7804 | 0.7454 | **0.6075** | FAIL | 0.7431 |
| D4 type | nominal | 0.7319 | **0.5694** | 0.7035 | **0.5694** | FAIL | 0.6682 |

**R1 RAW GATE = FAIL** on D2, D3, D4 (only D1 clears). The 3-way joint failed only D4 — joint α masked the pairwise failures, which is why v1.2 gates on the minimum. D3 A-pairs rested on 29 paired units (A returns NA on D3 for 26/55; B 20; C 17). **Correlated-error check:** no anomalously high pair; the disagreement was **coder A as systematic isolate** — every failing cell an A-pair, B×C passing precisely because A is absent.

## R1.2 — Laundered arm + raw-vs-laundered divergence

| Dim | A×B | A×C | B×C | **min** | verdict | 3-way |
|---|---|---|---|---|---|---|
| D1 | 0.7971 | 0.6713 | 0.6933 | 0.6713 | FAIL | 0.7203 |
| D2 | 0.7210 | 0.7268 | 0.7166 | 0.7166 | PASS | 0.7211 |
| D3 | 0.7090 | 0.8517 | 0.6811 | 0.6811 | FAIL | 0.7551 |
| D4 | 0.6332 | 0.6085 | 0.6381 | 0.6085 | FAIL | 0.6258 |

Laundered GATE = FAIL (D1, D3, D4). **D4 failed under both arms** (raw .569, laundered .609) = text-intrinsic type ambiguity. D2 failed raw / passed laundered (register cue). D1 passed raw / failed laundered (paraphrase perturbs A's scope cues). Raw-vs-laundered per-coder code divergence (fraction of items changed): A 9/18/13/15% · B 13/7/7/5% · C 20/20/22/13% (C least paraphrase-stable, B most).

## R1.3 — Gold diagnostic (DIAGNOSTIC ONLY, r1 codes)

Per-coder gold accuracy (n=20): A 75/90/75/80 · B 75/95/75/75 · C 75/100/75/80 (D1/D2/D3/D4). Recognition probe validated (19/20 = 95% ≥ 90%); unrecognized stratum n=1 (A14 only). Binding memorization caveat: A14 is both the one unrecognized anchor and the worst-coded → recognized-stratum accuracy upper-bounds obscure-corpus accuracy. Shared misses: **D3 CS2↔CS4** (A04/A05/A07), **D4 alpha↔beta** (A01/A05/A07), D1 adjacency (A06/A11/A12/A13). These seeded the CL drafts and the D3-collapse decision.

## R1.4 — Battery (r1, PROVISIONAL)

| Arm | Result | Verdict |
|---|---|---|
| B1 determinism (s20260714) | A 100/100/100/100 · B 85/90/95/95 · C 80/85/85/80 | A PASS; B FAIL (D1,D2); C FAIL (all) → motivated majority-of-3 |
| B2 cue-ablation | A .73/.51/.56/.56 · B .76/.49/.62/.65 · C .60/.35/.38/.36 | D2 low = text-driven (anti-folklore signal) |
| B3 dev-half | A 97/100/100/97 · B 97/100/97/100 · C 100/100/100/100 | PASS all, near-ceiling |
| B3 discriminator | R1 A .882/B .867/C .991 · R2 A .709/B .789/C .909 | FAIL both (E-fingerprint; exam-mode null shows no coding contamination) |

## R1.5 — Disagreement patterns (r1; input to CL-1..5)

A-isolated (B=C≠A) vs 3-way splits, raw: D1 4/1 · D2 7/3 · D3 8/0 · D4 6/0 of 55. Nearly every disagreement was A-against-the-other-two. Five representative items drove CL-1..5: `cf6c7a966fb376fd` (I/M attribute-impossibility, NA cascade), `cabd8f6e0c2ae4a5`/`99fa3cbf1908eea8` (Eucharistic real-presence S5/S8/X), A05 (D2 net-sign on a hiddenness defense), A04/A01 (D4 alpha/beta crux), `ca506d1433c426ca` (D3 CS2/CS3 boundary). Full register in `docs/adjudication-log.md` Appendix A; clarifications CL-1..CL-5 in §7 of that log and codebook §12 (v1.3).

## R1.6 — Exam-mode natural experiment (r1)

C flagged 10 laundered-real items as SYNTHETIC (24%; 0% of scrub-only). C's codes were *more* stable on those 10 (mean 0.50 dims changed vs 0.81 on other laundered-real; A/B same direction). **The E-style fingerprint is a surface-statistics artifact that does not propagate into coding** — the key mitigation for the discriminator failure. Caveats: n=10, one 4-dim outlier.

## R1.7 — Corpus-N (r1)

Chain-relevance (RS 2015, n=35, single-run): A 26/35, B 25/35, C 26/35, majority 26/35 = 74% non-X (+1 unresolved). *Superseded by §9 above (n=69, majority-of-3): ~57%.*

## R1.8 — r1 recommendation (superseded)

r1 recommended entering the codebook revision loop (round 1 of 2), priority D4 > D3 > D2 > D1-scope, and explicitly **not** collapsing D3 yet (a second D3 failure trigger). That loop (v1.3 CL-1..5 → r2, A pin revision → r3, D3 collapse → r4, majority-of-3 → final) is the §1 trajectory; its terminus is the §7 PASS recommendation.
