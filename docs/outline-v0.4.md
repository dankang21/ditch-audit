# ditch-audit — Paper Outline & Coding Protocol

**v0.4** · 2026-07-14 · Owner: dk · Status: D-1..D-6 confirmed · G0 PASS · **P1 instrument shipped** (codebook v1.1 + gold-anchors v1 + validation-battery v1) · v0.4 amendment: **zero-human coding** (binding dk decision) — dk pilot hand-coding and the P4 human-coded sample removed; tri-family coders + preregistered validation battery replace them (§4.6, T-5/T-6) · Next: pilot run (RS 2015 + 20 anchors), gate G1 α ≥ 0.70
Codename: `ditch-audit` · AI-use disclosure: drafted with Claude; **all corpus coding performed by LLMs with zero human item-coding — disclosed in the abstract's own voice and detailed in methods**; final disclosure text per target-venue policy at submission.

---

## 0. Thesis and abstract

**One-line thesis.** The inferential chain from "physical reality has an external cause" to Nicene Christian theism, individuated by a witness-based criterion, has eight logically independent steps; a systematic audit of 20 years of peer-reviewed philosophy of religion shows (i) dispute status tracks epistemic type — contested ⟺ a priori, empirically exposed ⟺ one-sidedly against — and (ii) strong positive claims migrate to confessionally affiliated venues. Lessing's ditch as a measurable property of the literature, not an aphorism.

**Abstract draft (~150 words).**
> The inferential chain from a bare first cause to the God of Nicene Christianity has been discussed piecewise — as the "gap problem," as "ramified natural theology," as the "dwindling probabilities" debate — but never measured as a whole. We introduce a witness-based criterion for individuating the chain's logically independent steps, yielding an eight-step canonical partition whose burden count is invariant under definitional bundling. We then audit twenty years of the peer-reviewed philosophy-of-religion literature (N ≈ [pilot-calibrated]), coding each article's step, direction, claim strength, and the epistemic type of its load-bearing evidence. All coding was performed by a fixed, preregistered, multi-family LLM instrument with zero human item-coding, validated by a preregistered contamination-control battery. Two regularities are predicted and tested: (1) positive evidential claims *for* chain steps are overwhelmingly a priori, while positive claims *against* are empirical or historical; (2) strong pro-side claims migrate from mainstream to confessionally affiliated venues — a pattern not attributable to hostile gatekeeping, given the subfield's majority-theist composition. Implications for cumulative-case natural theology are discussed.

---

## 1. Claims and non-claims

| ID | Claim | Kind |
|----|-------|------|
| C1 | A witness-based individuation criterion yields a canonical 8-step partition of the chain (external cause → Nicene theism) | framework |
| C2 = H1 | In mainstream venues, positive evidential claims **pro** are predominantly a priori (α); positive claims **contra** are predominantly empirical/historical (β·γ) | empirical, falsifiable |
| C3 = H2 | Pro-side claim strength distribution shifts toward strong positive (CS4–CS5) in confessional venues relative to mainstream venues; no symmetric shift contra | empirical, falsifiable |
| C4 | The count of independent evidential burdens is invariant under logical/definitional repackaging (anti-bundling) | formal + dialectical |

**Explicit non-claims (scope fences, stated in §1 and §9 of the paper):**
- NOT first-order atheology; the paper takes no position on any step's truth.
- NOT a claim that theism is irrational (CS3-type warrant claims are orthogonal to the audit).
- NOT a suppression/censorship claim: we measure the published record, not submission flows.
- NOT citation-weighted "importance" (fashion metric; robustness-only, see R5).

---

## 2. Paper outline (section map with content notes)

- **§1 Introduction.** Three disconnected literatures that this paper connects at the meta level: (a) the *gap problem* — first cause → divine attributes (Pruss 2009 naming; Rasmussen, IJPR 2009; Ocampo, IJPR 2024 systematizes "Stage II" strategies for one segment only); (b) *ramified natural theology* — bare theism → Christian doctrine, pro-side program (Swinburne's coinage; Holder, Routledge 2021; Gauch, Phil. Christi 2013); (c) *dwindling probabilities* — the multiplicative-structure exchange (Plantinga, WCB/OUP 2000; Swinburne, F&P 2004; T. McGrew, Phil. Christi 2004). Contribution type: **measurement of the dialectic, not participation in it.** Differentiation from the existing empirical program (P0 finding): De Cruz (Episteme 2017; Res Philosophica 2018) and De Cruz & De Smedt (2016) measure *persons* — surveys and experiments on philosophers; Draper & Nichols (Monist 2013) diagnose field-level cognitive bias; the PhilPapers surveys measure composition. No prior work measures the *literature's* argumentative structure (step × direction × claim strength × epistemic type × venue).
- **§2 The individuation criterion.** A step S_i is admitted iff: (i) logically necessary for the target (Nicene-minimal definition); (ii) not derivable from S_1..S_{i−1}, certified by a **witness** — an extant scholarly position accepting all prior steps and rejecting S_i; (iii) a dedicated peer-reviewed literature disputes S_i specifically. Grain-dependence acknowledged upfront; robustness deferred to §6, canonicity defended in §7.
- **§3 The canonical partition.** Table 1 (below): thesis, witnesses, anchor literatures, audited status, epistemic type.
- **§4 Methods.** Corpus + codebook summary (full protocol = online appendix / OSF).
- **§5 Results.** H1, H2, per-step descriptive maps, computed step-status table.
- **§6 Robustness.** R1–R5 battery (below).
- **§7 Formal section.** Burden-invariance proposition; canonical-partition definition; repositions the dwindling-probabilities exchange as a dispute over partition choice that the witness criterion adjudicates. This is the paper's claim to a contribution *within* an existing debate, not merely alongside it.
- **§8 Objections and replies.** Five, pre-answered (map in §8 below).
- **§9 What the map licenses.** And what it does not (non-claims).

---

## 3. Table 1 — the canonical eight-step partition (as audited, 2026-07)

Types: **α** = a priori/metaphysical (no in-principle empirical exposure) · **β** = empirical contact · **γ** = historical-singular.

| # | Thesis (exact statement to be disputed) | Witness (accepts 1..i−1, rejects i) | Anchor literature (audited set) | Status | Type |
|---|---|---|---|---|---|
| S1 | Physical reality as a whole has an external cause or ground (not a brute fact) | Russell (brute fact); Oppy | pro: Pruss–Rasmussen (OUP 2018); fine-tuning physics Barnes (PASA 2012); White (Noûs 2000) — functional pro: rebuts the multiverse rejoinder (correction v0.3; caught during gold-coding, see codebook §8) · contra: Oppy (CUP 2006), Malpass–Morriston (PQ 2020), McGrew–McGrew–Vestrup (Mind 2001), Adams (Phys. Rep. 2019) | contested — pure metaphysics after BGV-inference withdrawal | α (+β sub-dispute on fine-tuning degree) |
| S2 | That ground is an agent with intentions and will | Leslie axiarchism; Tegmark (Found. Phys. 2008) | pro: Swinburne (OUP 2004) · contra: Morriston (F&P 2000) | contested; **only observational channel routes through S5** | α |
| S3 | The agent is unique, a se, uncreated; all else ontologically depends on it (*pantokrator*) | Bostrom simulator (PQ 2003); Hartshorne (SUNY 1984); Mormon finitism | gap-problem lit: Pruss 2009; Rasmussen (IJPR 2009); Ocampo (IJPR 2024); bundling fence: Geach (Philosophy 1973), Hasker (Cornell 1989) | contested / frozen — evidence up to S2 shared with contingent-creator hypotheses | α |
| S4 | The ultimate is perfectly good | Draper indifference; Law evil-god; Mill finite god (1874) | contra: Rowe (APQ 1979), Draper (Noûs 1989), Law (RS 2010), Cahn (Analysis 1977) · pro = defenses only: Plantinga (OUP 1974), Wykstra (IJPR 1984) | headwind | α+β (Draper's likelihood argument has data contact) |
| S5 | The good ultimate acts specially in the world post-creation (miracles, answered prayer) | Wiles; deism | contra: Cochrane CD000368 (2009), STEP (AHJ 2006), Wildman (T&S 2004), Hume · pro: coherence defenses only | **strong headwind; the chain's only fully live empirical channel** | β |
| S6 | The authentic bearer of that God's special revelation is the Hebrew prophetic tradition | Islam; Judaism; Hick pluralism (Yale 1989) | contra: Alston parity (Cornell 1991) · pro: Plantinga (OUP 2000) — permissibility only | headwind / near-frozen; evidence defers to S7 | β·γ |
| S7 | Jesus of Nazareth was bodily raised (~AD 30) | Lüdemann (1994); Allison non liquet (T&T Clark 2021) | pro: Wright (Fortress 2003), Swinburne (OUP 2003, + dwindling-probabilities caveat) · base rate ~10¹¹:0 (analysis, not citation) | strong headwind; **evidence-frozen** (fixed corpus) | γ |
| S8 | The resurrection shows Jesus is God incarnate; God is triune | **Lapide** (accepts S1–S7, rejects S8); Tuggy (RS 2003) | pro-coherence: Morris (Cornell 1986), Brower–Rea (F&P 2005) | defensive; truth-evidence fully S7-dependent | α (γ-dependent) |

Structural findings carried from the audit (to be re-derived from corpus, not assumed): contested ⟺ α; headwind ⟺ β·γ, no exceptions; S2's hidden dependency on S5; test coverage ≈ 2/8 with covered segments failing.

---

## 4. Coding protocol

### 4.1 Corpus definition

**Venue tiers (preregistered assignments):**
- **T1 general:** Mind, Noûs, Philosophical Quarterly, APQ, Analysis, Philosophical Studies — topic-filtered to chain-relevant items only (keyword pre-filter + LLM relevance pass).
- **T2 specialist mainstream:** Faith & Philosophy, Religious Studies, IJPR, Sophia [+ EJPR pending D-1]. Window: 2004–2024.
- **T3 confessionally affiliated:** Philosophia Christi [+ Journal of Analytic Theology, TheoLogica pending D-2].

Note on F&P: published by the Society of Christian Philosophers but editorially open (Draper, Morriston publish contra-side there). Its T2 assignment is a **preregistered sensitivity axis** (R2), not a hidden judgment call.

**Inclusion:** research articles. **Exclusion:** book reviews. Discussion notes coded but flagged as a separate class.
**Harvest:** PhilPapers OAI-PMH + Crossref by ISSN; dedupe on DOI; metadata QA pass.
**N estimate:** T2 ≈ 170 items/yr × 20 yr ≈ 3,400 raw → chain-relevant est. 40–60% (pilot calibrates). Exact per-journal counts = P2 deliverable; current figures are estimates, not data.
**Access risk:** abstracts open (publisher pages / PhilPapers); full text paywalled (PDC, CUP, Springer). Mitigation: primary coding on abstract + accessible front matter; full-text retrieval **only** for CS4+ candidates and adjudication cases. Budget line: USD 300–800 worst case (pay-per-view).

### 4.2 Unit of analysis
Article; **primary thesis only** for H1/H2. Multi-claim articles: primary claim coded; dual-claim coding on a 10% random subsample as sensitivity.

### 4.3 Coding dimensions

**D1 — Step assignment.** Values: S1..S8, plus:
- **B** = bundled target (argument concludes to a conjunctive God directly: ontological arguments; generic religious-experience arguments → subtag B-RE). Prevalence of B is itself data for §7.
- **P** = pragmatic (Pascal-type; excluded from H1 — non-evidential).
- **I** = intra-theistic attribute puzzles (omnipotence paradox, foreknowledge-freedom): excluded from the chain per the Geach/Hasker fence (internal disputes, not path tolls).
- **M** = meta/methodology. **X** = out of scope.

Decision rule: the step whose thesis the article's primary conclusion most directly supports or negates.
Edge anchors (codebook examples): hiddenness → S5 (flag H); evil, logical and evidential → S4; fine-tuning-to-design → S1, unless the conclusion is agency → S2; miracles-general → S5; resurrection → S7; incarnation/trinity coherence → S8; religious experience → B-RE.

**D2 — Direction.** pro / contra / neutral-mapping.

**D3 — Claim strength** (symmetric scale; the H2 backbone):
- **CS1** coherence/possibility ("X is not incoherent / not shown false")
- **CS2** defeater rebuttal ("argument A against X fails") — incl. undercutting defeaters
- **CS3** epistemic permissibility ("belief in X can be warranted without propositional evidence")
- **CS4** positive evidential, qualitative ("E confirms X"; "X more probable than not")
- **CS5** positive evidential, quantitative (explicit probabilities / Bayes factors)

Anchor set: skeptical theism → pro-CS2 · Plantinga reformed epistemology → pro-CS3 · Swinburne EoG → pro-CS4/CS5 · Rowe 1979 → contra-CS4 · Draper 1989 → contra-CS4 · Law evil-god → contra-CS2 (undercutting).

**D4 — Load-bearing evidence type.** α / β / γ; mixed resolved by the **deletion test**: delete the empirical (or historical) premise — if the argument still runs, code α.

**D5 — Venue tier.** T1 / T2 / T3 per §4.1.

### 4.4 Computed step status (derived, never coded per article)
Within window, over T1∪T2:
- **contested** := both directions have ≥ k items at CS4+ (default k = 3)
- **headwind** := CS4+ one-sided; opposing side ≤ CS3 only
- **frozen** := no CS4+ either side in trailing 10 years

Report at k ∈ {2, 3, 5}. This makes the conversation's verdicts (Table 1 "Status" column) **computable rather than asserted** — the audit either reproduces them or corrects them.

### 4.5 Hypotheses and analysis plan

**H1 (type–status law, article level).** Among T1∪T2 items at CS4–CS5: evidence-type distribution differs by direction — pro predominantly α; contra predominantly β·γ.
Statistic: 2×2 (direction × α vs β·γ), odds ratio + 95% CI; per-step descriptive maps as secondary output. Registered prediction: OR ≥ 3.
Rationale for article-level testing: n = 8 at step level is statistically vacuous; the law must show at the item level (expected 300–450 CS4+ items given ~1,500 relevant articles at 20–30% CS4+ prevalence).

**H2 (venue topography).** Among **pro** items: P(CS4+ | T3) > P(CS4+ | T1∪T2). Among **contra** items (control): predicted null or reversed.
Statistic: tier × strength × direction log-linear model; report the two ORs and the interaction contrast.

**Null handling (kill criterion).** H1 ∧ H2 both null → no journal submission; downgrade to descriptive-map preprint + essay. No salami-slicing, no post-hoc hypothesis swaps.

### 4.6 LLM coding pipeline (v0.4 — zero-human)
- **Zero-human rule (binding, 2026-07-14):** no human codes any item — no human coder, no human item-adjudication, no human validation sample. The designer's labor = instrument design (codebook, synthetic-item specs/sign-off, gate approvals). The paper claims **measurement by a fixed, preregistered, multi-family LLM instrument**, not human-equivalent annotation; the abstract discloses this in its own voice.
- **Blind coding:** strip author, title, journal, and year before the model sees the text. Rationale: contamination control — models recognize famous papers and may code by reputation instead of content (input-level masking is the validated countermeasure; prompt-level instructions are not).
- **Tri-family coders:** A (Anthropic) ∥ B (Google) — the reliability pair gating G1 — ∥ C (OpenAI, adjudicator). Disagreements → majority-of-three; 3-way splits → unresolved protocol with sensitivity bounds. Optional D = open-weights archival coder (re-executability). Dated snapshots pinned at preregistration.
- **Validity evidence** (replacing the former human-coded sample): the preregistered battery in `validation-battery-v1.md` — cue-ablation folklore baseline; dk-spec'd synthetic criterion set (dev/vaulted halves) with style-laundering and a discriminator test; contrast sets and paraphrase arms; recognition probes with fame-stratified analyses; four-estimator stability; per-cell agreement floors; reversed-default deletion-test sensitivity. Numeric thresholds and failure consequences frozen at P3.
- **Reliability:** Krippendorff's α per dimension on independent first-pass codes; **gate: α(A,B) ≥ 0.70** each dimension. Fail → codebook revision loop (max 2; then simplify D3 to a 3-level scale).
- **Codebook = versioned prompt** (git). Frozen at preregistration; any post-freeze edit voids the run.
- **Known limitation (stated, not hidden):** with no human criterion, instrument accuracy on the real corpus distribution is formally unidentified; the battery bounds the identifiable artifact classes and the claim is disciplined accordingly.

### 4.7 Preregistration
OSF. Freeze after pilot (P1), before full run (P4): hypotheses, codebook version, tier assignments, k thresholds, analysis code skeleton, **model snapshots (dated), the full validation-battery threshold table and failure consequences (validation-battery §B10), the role-exclusivity matrix, and the vaulted synthetic-half hash**. Pilot data explicitly excluded from confirmatory analysis.

---

## 5. Robustness battery
- **R1 — alternative partitions:** 7-step (merge S7+S8), 10-step (split S3 into unicity/aseity vs sovereignty; split S4 via the Mill finite-god cut), liberal-target variant (drop S7 — Bultmann-style demythologized target). H1/H2 must persist across all admissible grains. **This is the pre-built answer to the referee's first attack.**
- **R2 — F&P tier flip** (T2 ↔ T3): recompute H2.
- **R3 — dominant-author exclusion:** drop Swinburne, Plantinga, Draper, Oppy; check for author-driven artifacts.
- **R4 — time split:** 2004–2013 vs 2014–2024; topography stability.
- **R5 — citation-weighted rerun:** optional, robustness-only (citation counts measure fashion, not truth — never primary).

---

## 6. Threats to validity
- **T-1 post-hoc scheme** (the 8-step partition was built from qualitative reading). Mitigation: preregistration + R1.
- **T-2 abstract-only coding** may miss claim-strength nuance. Mitigation: full text mandatory for all CS4/CS5 candidates.
- **T-3 survivorship:** the published record only; no inference to submission or suppression flows. Fence stated in §1 and §9.
- **T-4 gatekeeping objection — and its reversal.** Objection: "mainstream venues are biased against theism, so H2 measures bias, not epistemics." Reply: the specialist subfield is majority-theist — PhilPapers survey (Bourget & Chalmers, Phil. Studies 2014): ≈72% of philosophy-of-religion specialists accept or lean toward theism — and T2 editors/referees are drawn from that pool. A "defenses pass, strong positive claims migrate" pattern **cannot** be explained by hostile gatekeeping in a majority-theist subfield; field composition biases against H2, so a positive H2 result is conservative. Secondary anchors: Draper & Nichols, "Diagnosing cognitive biases in philosophy of religion" (Monist 96(3), 2013); De Cruz's empirical program — Episteme 14(1) (2017): argument-strength ratings track prior belief, with her PoR sample ≈58% Christian theist vs ≈16% atheist; Res Philosophica (2018): most philosophers of religion were theists *before* entering the field. The selection-bias data sharpens the reversal: composition is prior to and independent of gatekeeping.
- **T-5 LLM contamination (item-level memorization).** Mitigation: input-level blinding + recognition probes with fame-stratified re-estimation + paraphrase/entity-swap perturbation (validation-battery §B4–B5).
- **T-6 shared training-prior ("folklore") artifact — the design's principal threat (v0.4).** All coder families read the field's secondary discourse in pretraining; the headline pattern coincides with field folklore, so inter-family agreement alone cannot evidence text-driven coding, and majority adjudication can resolve toward the shared prior. Mitigations: cue-ablation folklore baseline with a text-driven-stratum requirement for any confirmatory claim (§B2); counter-stereotypical worked examples in the frozen prompt (codebook WE7–WE9); anti-folklore synthetic criterion cells and code-flipping contrast sets (§B3–B4); four-estimator stability and 2-1 resolution audits (§B6); reversed-default deletion test (§B7). Residual risk stated as a limitation: a folklore component below the battery's detection floor cannot be excluded.

---

## 7. Formal appendix sketch — burden invariance and canonical partitions

Target: T ≡ S1 ∧ … ∧ S8. Chain rule: P(T|E) = Π_i P(S_i | S_1..i−1, E), for every ordering and every coarsening into blocks; coarsening merely relocates factors into intra-block conditionals — i.e., into the bundle's prior structure.

**Proposition (burden invariance).** The multiset of conditional burdens is invariant under representation. Corollary: definitional bundling ("maximally great being") cannot reduce the number of burdens; it relocates them into the bundled proposition's prior. Mathematically elementary (chain-rule identity); the contribution is dialectical:

**Definition (canonical partition).** The maximal partition of T each of whose cell boundaries is **witness-certified** — occupied by an extant scholarly position accepting all prior cells and rejecting that cell, with dedicated literature.

**Claim.** Canonical partitions are the admissible accounting units for cumulative-case arguments. Both Plantinga's dwindling-probabilities argument and Swinburne's F&P 2004 reply presuppose partition choices; the witness criterion adjudicates which choices are admissible. This positions the paper as a contribution **inside** that exchange. The grain objection lives here; the answer is R1 (invariance across admissible grains) + the canonicity argument (witnesses tie mathematical partitions to dialectically real joints, blocking both gerrymandered inflation and apologetic deflation).

**Formal neighbor (must-cite, P0 finding).** Roche & Shogenji, "Dwindling Confirmation," *Philosophy of Science* 81(1) (2014): confirmation dwindles along chains under screening-off. Our proposition concerns burden *counting* under re-partition, not confirmation *transmission* — §7 must locate itself against this result explicitly. Fuller exchange sequence for §1: Plantinga (WCB 2000) → Swinburne (F&P 2004) → McGrew (Phil. Christi 2004) → Plantinga reply (2004; partial concession reported — verify against primary text at P1) → McGrew & McGrew (Phil. Christi 8(1), 2006) → Nickel (De Gruyter 2015). That the exchange ended in a dispute over *how evidence enters at stages* — a partition/conditionalization choice — confirms §7's positioning: that is exactly the question the witness criterion adjudicates.

---

## 8. Objections & replies map
- **O1 grain/arbitrariness of "8".** → §2 criterion + R1 + §7 canonicity. The integer is grain-relative; the *invariants* (H1/H2) are not — that is the published claim.
- **O2 Thomist entailment** ("no gap: attributes follow from pure actuality, so S3–S4 are not steps"). → The entailment is itself a contested step: witnesses rejecting it exist within theism (Hartshorne; classical-vs-personalist disputes). Entailment claims get coded as pro-α items; they do not dissolve cells. Pruss's own framing concedes the gap as the cosmological argument's "final difficulty."
- **O3 peer review ≠ truth.** → Conceded in advance; C2/C3 are claims about the structure of the record. Plus T-4 reversal.
- **O4 asymmetry** ("run it on naturalism"). → Naturalism is a low-conjunction target; the mirrored mini-audit (appendix: naturalism's burdens — cosmogenesis, fine-tuning response, consciousness) quantifies conjunctive specificity and demonstrates method neutrality. Honesty rule: publish whatever the mirror shows, including naturalism's own α-zone if present.
- **O5 hostile-prior scheme design.** → Preregistration; and the witness criterion is side-neutral — the witness list includes theists rejecting steps (Hartshorne, Lapide, Wiles, open theism).

---

## 9. Venue strategy
- **Primary: Metaphilosophy** — discipline-level empirical/methodological studies are in scope.
- **Alternative (if §7 carries weight): Synthese** — formal epistemology of cumulative cases + corpus study; genre precedent exists (computational corpus studies of philosophy-of-science literatures) — strongest analog (P0 finding): Bystranowski, Dranseika & Żuradzki, "Half a century of bioethics and philosophy of medicine: a topic-modeling study," *Bioethics* (2022), 19,488 texts across seven field journals. A field journal publishing a corpus study of its own field also supports the Religious Studies stretch option.
- **Stretch: Religious Studies** — boldest placement: the audit published inside the audited field.
- **Preprint:** PhilPapers Archive + OSF (philosophy has no arXiv; PhilPapers is the analog).
- **Framing variants,** decided at P5 by effect sizes: (a) methods-forward — "an audit methodology for cumulative-case arguments," theism as case study (most transferable); (b) results-forward — "the topography of the ditch."
- **Zero-human triage risk (v0.4).** 2024–26 methods guidelines treat human gold validation as a required item; a fully zero-human study is precedent-setting, not precedent-following. Consequences: methods-forward framing gains weight; the abstract discloses zero-human coding up front; venue order tilts Metaphilosophy/Synthese-class and computational-humanities outlets; the existing kill-criteria downgrade path (preprint + essay) absorbs a desk-reject cascade. Battery components double as the reviewer-response arsenal.

---

## 10. Phases (HITL gates; dk agent conventions)

| Phase | Work | Duration | Gate |
|---|---|---|---|
| P0 | Prior-art sweep: PhilPapers queries ("ramified natural theology", "gap problem", "dwindling probabilities", "cumulative case" × meta); cited-by walks on Gauch 2013 / Ocampo 2024 / Draper–Nichols 2013 | 1–3 d | **G0:** no substantially overlapping meta-study exists → proceed; else differentiation memo or stop |
| P1 | Codebook v1.1 + pilot: Religious Studies 2015 full year (~50 arts) + 20 canonical anchors from Table 1; tri-LLM coding (A ∥ B ∥ C) + battery pilot arms (recognition probe, cue-ablation baseline, determinism audit, raw-vs-laundered divergence); compute α | 2–3 wk | **G1:** Krippendorff α(A,B) ≥ 0.70 all dimensions |
| P2 | Corpus build: OAI/Crossref harvest, dedupe, metadata QA, abstract-coverage report, exact per-journal counts | 1–2 wk | **G2:** ≥ 90% abstract availability |
| P3 | OSF preregistration freeze | 3 d | — |
| P4 | Full coding run (tri-family) incl. full battery: vaulted synthetic half opened, recognition probes, contrast sets, per-cell floors, four-estimator stability (no human validation — zero-human rule) | 2–3 wk | — |
| P5 | Analysis; H1/H2 verdicts | 2 wk | **G5:** framing decision (§9) |
| P6 | English draft + venue-specific AI disclosure | 3–4 wk | — |

**Effort:** 2–2.5 M/M part-time; +50% risk buffer → **3–4 M/M calendar.** Cash: full-text budget USD 300–800; OSF free.
**Kill criteria:** G0 fail → differentiate or stop · G1 fail ×2 → simplify D3 to 3 levels · H1 ∧ H2 null → downgrade path (preprint + essay), no journal submission.

---

## 11. Open decisions for dk (blocking P1)

| ID | Decision | Default if silent |
|---|---|---|
| D-1 | EJPR in T2 corpus? (+~15 items/yr) | out (add in R-pass if needed) |
| D-2 | T3 set: Philosophia Christi only, or + Journal of Analytic Theology, TheoLogica? (both open-access → cheaper full text; JAT's confessional status debatable → possible T2.5 class) | PC only |
| D-3 | Books excluded from quantitative core (articles-only), used as qualitative anchors — confirm. Known cost: the field's monograph culture; stated as limitation | confirm |
| D-4 | English-only corpus — confirm | confirm |
| D-5 | §7 formal weight: light (→ Metaphilosophy) vs heavy (→ Synthese). Provisional until P5 but affects notation now | light |
| D-6 | Coder families under the zero-human rule: A = Anthropic, B = Google, C = OpenAI (adjudicator), D = open-weights archival (recommended); generator/launderer E = a non-coder family. Role-exclusivity matrix: validation-battery §B0 | **decided 2026-07-14** |
