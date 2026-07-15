# G1 Reliability Report — P1 Pilot (ditch-audit)

**Date:** 2026-07-15 · **Scope:** P1 pilot, 55 items (RS 2015 n=35 + gold anchors n=20), triple-coded (A=Anthropic, B=Google, C=OpenAI) · **parse_fail = 0 / 165 records** · **Gate spec:** codebook v1.2 §9 — G1 = per-dimension **minimum pairwise Krippendorff α over {(A,B),(A,C),(B,C)} ≥ 0.70** on every dimension; 3-way joint α reported alongside; D1/D2/D4 nominal, D3 ordinal (NA = pairwise exclusion).

**Reproduce:** `python3 scripts/alpha.py rel data/coded/all55_{a,b,c}.jsonl` (and the three pairs); `python3 scripts/alpha.py gold data/coded/gold_anchors_{a,b,c}.jsonl --gold docs/gold-anchors-v1.json`. Battery inputs under `data/battery/`.

> **This report recommends; it does not declare.** Gate declaration is dk's (zero-human rule: dk's gate approval is instrument-design labor, not item judgment). The agent's recommendation is in §8.

---

## 1. G1 gate table — RAW arm (`all55`, n=55, union=55, parse_fail=0)

| Dim | metric | A×B | A×C | B×C | **min = GATE** | verdict | 3-way joint |
|---|---|---|---|---|---|---|---|
| D1 step | nominal | 0.7756 | 0.7741 | 0.7344 | **0.7344** | **PASS** | 0.7609 |
| D2 direction | nominal | **0.6733** | 0.6746 | 0.7591 | **0.6733** | **FAIL** | 0.7013 |
| D3 strength | ordinal | **0.6075** | 0.7804 | 0.7454 | **0.6075** | **FAIL** | 0.7431 |
| D4 type | nominal | 0.7319 | **0.5694** | 0.7035 | **0.5694** | **FAIL** | 0.6682 |

**RAW GATE = FAIL** on D2, D3, D4 (3 of 4 dimensions below 0.70). Only D1 clears. The 3-way joint fails on D4 only (0.668) and is *above* the min-pairwise gate on the other three — i.e. joint α masks the pairwise failures, which is exactly why v1.2 gates on the minimum.

**Sample / exclusions.** D1/D2/D4 use all 55 units (no missing, no NA-exclusion — NA is a real nominal category). D3 excludes items where either coder returned NA (neutral/X/I cascade):

| D3 pair | units used | excluded (NA-pairwise) |
|---|---|---|
| A×B | 29 | 26 |
| A×C | 29 | 26 |
| B×C | 34 | 21 |
| 3-way | 34 | 21 |

D3's A-pair gate rests on **29 paired judgments**, not 55. Coder A returns NA on D3 for **26/55** items (B: 20, C: 17) — A scopes more items to X/I/neutral (see §5), which both shrinks the D3 denominator and is itself a D1-scope signal.

**Correlated-error check (§9 red-flag).** No pair shows *anomalously* high agreement: B×C (0.703–0.759) is the highest-agreeing pair and the only one passing all four, but the magnitude is moderate, not extreme, so it does not read as shared-prior collusion between Google and OpenAI. The disagreement is not symmetric noise — it is **coder A as systematic isolate** (§5): every failing cell is an A-pair, and B×C passes precisely because A is absent from it. Because C is the majority adjudicator, A-vs-{B,C} splits will resolve toward the B/C reading; whether C's tie-breaks systematically track the stub-predictable code is the B6/B2 folklore-congruence audit to run once codes are frozen.

---

## 2. Laundered arm + raw-vs-laundered divergence

Same 3-pair/3-way computation on the style-laundered coding (`laundered_*`; 42 items family-E paraphrased, 13 scrub-only per `data/battery/laundered_*.jsonl:laundered`).

| Dim | A×B | A×C | B×C | **min = GATE** | verdict | 3-way |
|---|---|---|---|---|---|---|
| D1 | 0.7971 | **0.6713** | 0.6933 | **0.6713** | **FAIL** | 0.7203 |
| D2 | 0.7210 | 0.7268 | 0.7166 | **0.7166** | **PASS** | 0.7211 |
| D3 | 0.7090 | 0.8517 | **0.6811** | **0.6811** | **FAIL** | 0.7551 |
| D4 | 0.6332 | **0.6085** | 0.6381 | **0.6085** | **FAIL** | 0.6258 |

**Laundered GATE = FAIL** (D1, D3, D4). Arm-dependence of the outcome is itself a finding:

- **D4 fails under both arms** (raw min 0.569, laundered min 0.609). The type ambiguity is text-intrinsic, not a laundering artifact → highest-priority clarification.
- **D2 fails raw but passes laundered** (0.673 → 0.717). Part of the raw D2 gap is surface-register cue that paraphrase neutralizes — consistent with A reading directional cues from register that wash out under rewording.
- **D1 passes raw but fails laundered** (paraphrase perturbs the scope cues A relies on).

Per B4, laundered-arm coding also neutralizes venue-register leakage; dk picks the primary arm at P3. Neither arm passes G1 as-is.

**Raw-vs-laundered code divergence (per coder, per dim; fraction of items whose code changed):**

| Coder | D1 | D2 | D3 | D4 | (paraphrased-42 subset) |
|---|---|---|---|---|---|
| A | 9% | 18% | 13% | 15% | 10/17/12/14% |
| B | 13% | 7% | 7% | 5% | 14/7/7/5% |
| C | 20% | 20% | 22% | 13% | 21/19/21/12% |

C is the least paraphrase-stable, A intermediate, B most stable. The 13 scrub-only items (identical text raw vs laundered) still show small nonzero divergence (A 1–3, B 1, C 2–3 per dim) = residual endpoint non-determinism (ties to §4 B1), not a paraphrase effect. Divergence over the 42 truly-paraphrased items nearly equals the all-55 figure, so the paraphrase effect dominates for A/C.

---

## 3. Gold diagnostic — DIAGNOSTIC ONLY (codebook §8; headline-forbidden)

Per codebook §8 v1.1 and battery §B5, gold accuracy carries **zero headline construct-validity weight** and is reported **only** stratified by the recognition probe. Construct validity lives in the synthetic criterion set (§4, B3).

**Per-coder gold accuracy (n=20 anchors):**

| Coder | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| A | 75% | 90% | 75% | 80% |
| B | 75% | 95% | 75% | 75% |
| C | 75% | 100% | 75% | 80% |

**Recognition-probe stratification (`recognition_gold_anchors.jsonl`).** The probe is validated (pooled "identified by ≥1 family" = **19/20 = 95% ≥ 90%** planted-famous floor, B5). But that is exactly the problem: **19 of 20 anchors are recognized by at least one family** (per-family identify rate A 65% / B 85% / C 90%). The unrecognized stratum is **n=1 (A14 only)** → 3 coder-observations. Stratification is technically usable but statistically empty at pilot scale.

| Dim | RECOGNIZED (19 anchors, 57 obs) | UNRECOGNIZED (A14 only, 3 obs) |
|---|---|---|
| D1 | 45/57 = 79% | 0/3 = 0% |
| D2 | 56/57 = 98% | 1/3 = 33% |
| D3 | 44/57 = 77% | 1/3 = 33% |
| D4 | 46/57 = 81% | 1/3 = 33% |

**Memorization-contamination caveat (binding).** The single unrecognized anchor (A14) is *also* the one all three coders miscode on D1 (gold S3; A→I, B→I, C→B) and mostly miss on D2/D3/D4. So the one item that cannot be recognized is the one the instrument handles worst — a vivid illustration that recognized-stratum accuracy (77–98%) **upper-bounds** obscure-corpus accuracy, but n=1 is far too small to estimate the unrecognized rate. **Do not read gold accuracy as validity.** Its legitimate use is diagnostic corroboration of the reliability failures below.

**Shared gold misses that corroborate the reliability failures (all/most coders miss the same way → codebook-clarity problem, not coder-quality):**
- **D3 CS2↔CS4:** A04, A05, A07 — all three coders code CS2, gold says CS4 (defeater-rebuttal vs positive-evidential). Mirrors the D3 reliability failure.
- **D4 alpha↔beta:** A01/A05/A07 gold=beta but coders (esp. A) code alpha; A04 gold=alpha. Mirrors the D4 reliability failure. Note the gold set itself splits structurally similar evil-arguments (A01 beta vs A04 alpha) — an instrument-design tension for dk.
- **D1 adjacency:** A06/A11/A12/A13 (S1↔S2↔S3 confusions), A14 (unrecognized outlier).

---

## 4. Battery integration (P1 arms, PROVISIONAL thresholds per validation-battery-v1)

| Arm | Metric / floor | Result | Verdict vs PROVISIONAL | P3-freeze action |
|---|---|---|---|---|
| **B1 determinism** (`det_report_*`, n=20, re-code twice) | exact-match ≥ 95% per dim | A 100/100/100/100 · **B 85/90/95/95** · **C 80/85/85/80** (D1/D2/D3/D4) | A PASS; **B FAIL (D1,D2); C FAIL (all)** | B/C endpoints reject settable temperature (only B accepts temp=0; A/C sampling not pinnable, B1 note). 95% is structurally unreachable at these endpoints → dk must **lower the floor or adopt majority-of-k self-consistency**, stated in prereg. |
| **B2 cue-ablation** (`cue_ablation_summary`, stub-vs-full agreement) | P1 = feasibility/variance (no pass/fail) | Stub-recoverable rates — A: D1 73% D2 51% D3 56% D4 56% · B: 76/49/62/65 · C: 60/35/38/36 | **Positive signal:** D2 low (35–51%) = direction is **text-driven**, not topic-recoverable (anti-folklore). D1 high (60–76%) = step ≈ topic classification (benign). | Confirmatory H1/H2-in-text-driven-stratum gate runs at P4, not P1. |
| **B3 dev-half accuracy** (`dev_half_accuracy`, n=30) | D1≥85 D2≥85 D3≥70 D4≥75 | A 97/100/100/97 · B 97/100/97/100 · C 100/100/100/100 | **PASS (all coders, all dims), near-ceiling** | Headline construct-validity evidence holds. Vaulted half stays sealed to P4. |
| **B3 discriminator** (`discriminator_p1/p2`) — **precondition for trusting B3 accuracy** | AUC ≤ 0.60 (real-vs-synth) | R1: A .882 / B .867 / C .991 · R2 (re-laundered): A .709 / B .789 / C .909 | **FAIL both rounds** (AUC = balanced-accuracy from hard labels; independently reproduced) | Cause identified = **family-E (GLM) style fingerprint**, not memorization: 24% of laundered real items misread as SYNTH, **0%** of scrub-only real items; name-swap hypothesis rejected (80% vs 82%). Re-laundering judged **unproductive** (C floor persists; 3-round cap). See §6 for why this does **not** contaminate coding. dk decision at P3: accept-with-mitigation (exam-mode null + dev-half ceiling) **or** diversify the generator beyond E. |

Only G1 (§1) is the pilot gate. The battery arms are reported alongside; B1 and the discriminator carry **P3-freeze threshold decisions**, not G1 decisions.

---

## 5. Disagreement patterns (input for adjudication-logger + codebook revision drafts)

**A is the systematic isolate.** Counting items where A differs from **both** B and C (B=C≠A) vs 3-way splits, raw arm:

| Dim | 3 agree | A-isolated (B=C≠A) | 3-way split |
|---|---|---|---|
| D1 | 38/55 | 4 | 1 |
| D2 | 39/55 | 7 | 3 |
| D3 | 39/55 | 8 | 0 |
| D4 | 40/55 | 6 | 0 |

Nearly every disagreement is A-against-the-other-two; true 3-way splits are rare (4 total). This is why B×C passes all four dimensions and every failing gate cell is an A-pair. Pairwise raw %-agreement (context for α): D1 ab80/ac80/bc76 · D2 ab76/ac76/bc84 · D3 ab86/ac83/bc91 · D4 ab85/ac76/bc84.

**Five representative items (3-coder codes = D1/D2/D3/D4, with rationales):**

1. **`cf6c7a966fb376fd`** (A-isolated on all four dims — one item flips the whole row via NA-cascade)
   - A: `I / NA / NA / NA` — "omniscience-impossibility argument… intra-theistic attribute puzzle excluded; codes stop after class assignment."
   - B/C: `M / pro / CS2 / alpha` — "methodological critique of an atheological strategy… conceptual defeater-rebuttal supporting theistic case-making."
   - **Clarify (D1):** rebutting an attribute-impossibility argument that generalizes to *how atheological arguments must proceed* → **M, not I**. The I→NA cascade means D1 scope errors silently drive D2/D3/D4.

2. **`cabd8f6e0c2ae4a5`** (and parallel `99fa3cbf1908eea8`) — sacramental Real-Presence coherence
   - A: `S8 / neutral / NA / NA` (LOWTEXT) / or `X` on the parallel item — "internal coherence exposition… not bearing on a chain step."
   - B: `S8 / pro / CS1 / alpha` — "coherence of a Christological Eucharist theory… S8 incarnation coherence."
   - C: `S5 / pro / CS1 / alpha` — "special divine presence/action… S5."
   - **Clarify (D1):** where do Eucharistic/sacramental real-presence coherence items go — **S5 vs S8 vs X**? Add a binding edge anchor. High leverage: cascades to D2/D3/D4.

3. **`A05`** (gold: S5/**contra**/CS4/beta) — net-effect sign error on a hiddenness defense
   - A: `S5 / **pro** / CS2 / alpha` — "defends the hiddenness argument… net effect supports the hiddenness case."
   - B/C: `S5 / **contra** / CS2 / alpha` — "defends the atheistic hiddenness argument… net contra-S5."
   - **Clarify (D2):** A described a contra effect but coded pro. Defending an argument whose conclusion is *anti-step* = **contra**. Add a hiddenness/evil worked example to the CHAIN net-sign rule. (Laundered D2 passes → part of this gap is register-cue, partly self-resolving under a laundered primary arm.)

4. **`A04`** (gold: S4/contra/**CS2**/**alpha**) + **`A01`** (gold: S4/contra/CS4/**beta**) — the D4 alpha/beta crux
   - A04 — A: `…/CS4/**alpha**` (gold alpha ✓); B/C: `…/CS4/**beta**` (deletion test → empirical suffering load-bearing).
   - A01 — A: `…/**alpha**` (gold **beta** ✗); B/C: `…/**beta**` (gold ✓).
   - **Clarify (D4):** A defaults *alpha* (existence-of-evil treated as common ground); B/C default *beta* (observed suffering load-bearing). Even the gold set splits A01(beta) vs A04(alpha). Sharpen the deletion test's "common-ground" clause for existence-of-evil / existence-of-minds premises; add worked examples distinguishing evidential-from-observation (beta) vs parity/symmetry-conceptual (alpha). Also note: all three miss A04 D3 (coded CS4, gold CS2).

5. **`ca506d1433c426ca`** (and parallel `8de10cee13eacd75`) — the D3 CS2/CS3 boundary
   - A: `B / pro / **CS3** / alpha` — "sustains permissibility-without-evidence."
   - B/C: `B / pro / **CS2** / alpha` — "rebuts objections to Plantinga's model → defeater-rebuttal."
   - **Clarify (D3):** reformed-epistemology items both *rebut a defeater* (CS2) and *assert permissibility* (CS3). A reads the target claim (CS3); B/C read the dialectical move (CS2). Add a priority rule (e.g., code CS3 only when defeater-rebuttal is not the primary move). A17 shows the parallel CS1↔CS2 (coherence vs defeater) split.

---

## 6. Exam-mode natural experiment (does the discriminator's E-fingerprint leak into coding?)

The discriminator flags C mislabeling **10 laundered real items as SYNTHETIC** (24% of the 42; 0% of scrub-only). Test: do C's codes diverge (raw vs laundered) *more* on those 10 than on other laundered real items — i.e. does "recognizing test-ness" destabilize coding?

| Group (laundered real) | n | mean dims changed (of 4), C | distribution |
|---|---|---|---|
| C-flagged as SYNTHETIC | 10 | **0.50** | 8×0, 1×1, 1×4 |
| Other laundered real | 32 | **0.81** | 20×0, 5×1, 2×2, 3×3, 2×4 |
| (control A) flagged vs other | | 0.10 vs 0.66 | |
| (control B) flagged vs other | | 0.00 vs 0.44 | |

**Result: the opposite of destabilization.** C's codes are *more* stable on the very items it (separately) flagged as synthetic (median 0 dims changed; 8/10 unchanged), and A/B show the same direction. The E-style fingerprint the discriminator detects is a **surface-statistics artifact that does not propagate into the coding task**. This is the key mitigation for the §4 discriminator failure: distinguishability ≠ coding contamination. Caveats: n=10, one 4-dim outlier inflates the flagged mean; suggestive, not confirmatory.

---

## 7. Corpus-N calibration (pilot chain-relevance)

Chain-relevance = fraction of items with D1 ≠ X (in-chain, codeable), pilot RS 2015 (n=35):

| | non-X (relevant) | X | note |
|---|---|---|---|
| Coder A | 26/35 = 74% | 9 | |
| Coder B | 25/35 = 71% | 10 | |
| Coder C | 26/35 = 74% | 9 | |
| **Majority-of-3** | **26/35 = 74%** | 8 | + 1 item (`99fa3cbf1908eea8`) is a D1 3-way split (X/S8/S5) → unresolved |

Majority D1 distribution (pilot): X 8 · M 7 · B 5 · I 4 · S4 4 · S5 2 · S8 2 · S2 1 · P 1 · unresolved 1. (Gold anchors, by contrast: only 1/20 X — the anchor set is curated in-chain.)

**Calibration for P2/P4 corpus N.** At ~74% chain-relevance: a target of *N* in-chain-codeable items needs ≈ **N / 0.74** harvested abstracts; a 1,500-abstract coded corpus yields ≈ **1,110 in-chain** items. **Caveats:** single venue, single year, n=35; the X-rate will shift with venue tier and topic mix (RS is comparatively theology-heavy → possibly higher X than a philosophy-of-religion-focused corpus). Treat as an order-of-magnitude prior, to be re-estimated after the P2 harvest.

---

## 8. G1 recommendation (agent recommends; dk declares)

**RAW arm G1 = FAIL.** Min-pairwise α below the 0.70 floor on **D2 (0.673)**, **D3 (0.608)**, **D4 (0.569)**; only **D1 (0.734)** clears. The 3-way joint fails only D4, confirming that joint α masks the pairwise failures. **Laundered arm also FAILS** (D1 0.671, D3 0.681, D4 0.609); **D4 fails under both arms.** No pair passes all four except B×C (raw) — the failure is coder-A-idiosyncratic and rule-specific, not diffuse noise.

**Recommendation: enter the codebook revision loop, round 1 of 2 (§9; kill-criteria: 2 failures → collapse D3).** This is a *document-clarification* pass — dk approves the codebook change, never item codes (absolute rule 5). **Do not collapse D3 yet** (that is triggered only by a *second* D3 failure). Priority-ordered clarifications, each mapped to a failing cell and a representative item:

1. **D4 (highest priority — fails both arms, both gold and reliability):** deletion-test "common-ground" clause for existence-of-evil / existence-of-minds premises; alpha (parity/conceptual) vs beta (evidential-from-observation) worked examples. Items A04/A01, `924861649ecbf24e`.
2. **D3:** CS2 (defeater-rebuttal) vs CS3 (permissibility) priority rule for reformed-epistemology items; CS1 vs CS2 for coherence-vs-defeater. Items `ca506d1433c426ca`, A17. Gold corroborates a CS2↔CS4 gap (A04/A05/A07).
3. **D2:** CHAIN net-sign rule — defending an anti-step argument = contra; hiddenness/evil worked example. Item A05. (Partly register-driven; laundered D2 already passes.)
4. **D1 scope (leverage — cascades via NA):** I-vs-M for attribute-impossibility rebuttals (`cf6c7a966fb376fd`); Eucharistic/sacramental real-presence → S5/S8/X edge anchor (`cabd8f6e0c2ae4a5`, `99fa3cbf1908eea8`).

After revision: re-code the 55, re-run §1. **Parallel P3-freeze decisions dk must settle (not G1 blockers):** (i) B1 determinism floor — B/C cannot reach 95% at non-settable-temperature endpoints; adopt self-consistency-of-k or lower the floor in prereg; (ii) discriminator AUC — persistent E-fingerprint; accept-with-mitigation (§6 exam-mode null + dev-half ceiling) or diversify the generator; (iii) primary arm (raw vs laundered) for P4.

**What is solid enough to build on:** D1 reliability (raw), dev-half construct-validity accuracy (near-ceiling, all coders), A-determinism, the anti-folklore signal that D2 is text-driven (B2), and the exam-mode null. The instrument's weaknesses are localized and diagnosable (D4 deletion test, D3 CS-calibration, D1 scope edges) — the profile of a codebook that needs sharpening, not one that has failed.

---

### Appendix — file provenance
- Reliability inputs: `data/coded/all55_{a,b,c}.jsonl` (55×3, parse_fail 0); laundered `data/coded/laundered_{pilot_rs2015,gold_anchors}_{a,b,c}.jsonl`; laundered-meta `data/battery/laundered_{pilot_rs2015,gold_anchors}.jsonl`.
- Gold: `data/coded/gold_anchors_{a,b,c}.jsonl` vs `docs/gold-anchors-v1.json`.
- Battery: `data/battery/{det_report_det_pilot_rs2015_s20260714.json, cue_ablation_summary.json, dev_half_accuracy.json, discriminator_p1.jsonl, discriminator_p2.jsonl, recognition_gold_anchors.jsonl, recognition_pilot_rs2015.jsonl}`.
- Metrics/thresholds: codebook v1 §8–§9 (v1.2 gate), validation-battery-v1 §B1–B6. `scripts/alpha.py selftest` PASS (hand-computed nominal case 0.6200).
