# ditch-audit — Codebook v1.3 (Coding Instrument)

2026-07-14 · Owner: dk · Status: ready for pilot (P1) · Companion files: `gold-anchors-v1.json`, `validation-battery-v1.md`
Frozen at P3 preregistration; any post-freeze edit voids the confirmatory run.
v1.1 (2026-07-14): zero-human-coding amendment · v1.2 (2026-07-14): G1 = min pairwise α — see §12.

---

## 1. Scope and blindness architecture

**What this instrument does.** Assigns four codes (D1 step, D2 direction, D3 claim strength, D4 epistemic type) to one journal-article abstract at a time. D5 (venue tier) is **never coded** — it is joined from metadata after coding, downstream.

**Blindness rules (hard constraints):**
- The coder sees **only** sanitized text: no author, no title, no journal, no year, no DOI.
- The coder prompt (§7) contains **no hypotheses**. The study's hypotheses and analysis plan live in the outline document only. Rationale: a coder that knows the study's expectations will drift toward them. The instrument must be usable by a coder who has never seen the paper's thesis. Coder-facing contexts receive only the built prompt (`pipeline/03_code/coder_prompt.txt`) — never this file.
- Three coders from **three different model families** (all three pairwise αs gate G1; C additionally serves as the majority adjudicator), run independently; none sees another's output.
- **No human codes any item** (zero-human rule, binding dk decision 2026-07-14). The instrument designer's labor is confined to: codebook authorship, synthetic-criterion item specs and sign-off, and gate approvals.

**Pipeline position:**
`harvest → sanitize → [CODER A ∥ CODER B ∥ CODER C] → A/B agreement? → (yes: accept) / (no: majority-of-three; 3-way split → unresolved protocol, validation-battery §B6) → join D5 venue metadata → compute step-status (outline §4.4)`

## 2. Input sanitization spec

Input unit: abstract (+ optionally first/last paragraph when abstract < 60 words).
Sanitization pass (scripted + manual spot-check):
1. Strip metadata fields (author/title/journal/year/DOI/volume).
2. Regex-scrub in-text self-identifiers: "In this journal", "as I argued in [year]", proper-name self-citations where they identify the author. Numbered-reference self-citations that expose no name, year, or venue (e.g. "In [4] I argued...") are kept verbatim — they do not identify the author (dk adjudication, P1: anchor A15).
3. Replace named interlocutors with role tags ONLY when the name identifies the item's own author; otherwise **keep** opponent names (e.g., "Swinburne's argument", "Rowe's inference") — they are content, and removing them destroys codability.
4. Log every scrub; sanitization log ships with the corpus.

**Input JSON schema:**
```json
{
  "item_id": "string (opaque hash; no metadata leakage)",
  "text": "string (sanitized abstract)",
  "text_extra": "string | null (sanitized first/last paragraph, only if abstract < 60 words)"
}
```

## 3. Coding procedure (ordered; earlier questions gate later ones)

- **Q0 Relevance.** Does the primary conclusion bear on any chain-step thesis (S1–S8, listed in §4), on a bundled God-conclusion, on pragmatic grounds for belief, on intra-theistic attribute puzzles, or on the methodology of such arguments? If none → `X`, stop.
- **Q1 Special classes.** Bundled full-God target (ontological arguments; generic religious-experience arguments) → `B` (+flag `RE` if experience-based). Pragmatic (wager-type) → `P`, stop after direction. Intra-theistic attribute puzzle (omnipotence paradox, foreknowledge–freedom) → `I`, stop. Methodology of the case itself (structure, probability machinery, epistemology of cumulative cases) → `M`, continue to D2–D4.
  - *M / step / X decision order:* (a) primary conclusion is a claim about the case-making itself and takes a verdict on that machinery → `M`; (b) the text merely uses an argument's topic as illustration, with no verdict on any thesis or on the machinery → `X`; (c) the text takes a verdict on a first-order step thesis *through* a methodological critique → code the step, not `M`. Applies alike whichever side's case-making is discussed.
- **Q2 Step (D1).** Assign the single step whose thesis the primary conclusion most directly supports or opposes.
- **Q3 Direction (D2).** Relative to the **step thesis**, not the immediately targeted paper (net-effect rule, §4-D2).
- **Q4 Strength (D3).** CS1–CS5 per definitions; `NA` if D2 = neutral or D1 ∈ {X, I}.
- **Q5 Type (D4).** Deletion test on the load-bearing premise.
- **Stop-rule cascade (NA schema).** Q1 stop codes cascade to NA on all un-coded downstream dimensions: `X` → D2, D3, D4 = NA · `I` → D2, D3, D4 = NA · `P` → D3, D4 = NA (direction is still coded) · pure-mapping neutral → D3 = NA, while D4 may still carry a type where a load-bearing empirical or historical premise exists (WE6 pattern).
- **Q6 Confidence + flags + one-sentence rationale (≤40 words).**
- **Dimension independence.** Code each dimension on its own textual evidence; no dimension's value constrains another except the stated NA rules. Any direction may combine with any strength and any type.

## 4. Dimension definitions

### D1 — Step (S1–S8, B, P, I, M, X)

| Code | Thesis the item must bear on |
|---|---|
| S1 | Physical reality as a whole has an external cause or ground (not a brute fact) |
| S2 | That ground is an agent with intentions and will |
| S3 | The agent is unique, a se, uncreated; all else ontologically depends on it |
| S4 | The ultimate is perfectly good |
| S5 | The good ultimate acts specially in the world post-creation (miracles, answered prayer, self-disclosure) |
| S6 | The authentic bearer of special revelation is the Hebrew prophetic tradition |
| S7 | Jesus of Nazareth was bodily raised (~AD 30) |
| S8 | The resurrection shows Jesus is God incarnate; God is triune |
| B | Bundled full-God conclusion argued directly (flag `RE` if via religious experience) |
| P | Pragmatic grounds for belief (wager-type) |
| I | Intra-theistic attribute puzzle (excluded from chain) |
| M | Methodology of theistic/atheistic case-making itself |
| X | Out of scope |

**Edge anchors (binding):** divine hiddenness → S5, flag `H` · evil (logical and evidential) → S4 · fine-tuning/cosmological to a bare cause → S1 · teleological/design arguments concluding to a designer-agent → S2 · miracles-general and petitionary prayer → S5 · resurrection historiography → S7 · incarnation/trinity coherence → S8 · religious experience as evidence for God → B, flag `RE` · simulation/multiverse papers with no bearing on a step thesis → X.

### D2 — Direction (pro / contra / neutral / NA)

Direction is the item's **net effect on the step thesis**, not on the paper it immediately targets.
- Rebutting an objection to a pro-step argument = **pro** (e.g., defending a fine-tuning argument against the multiverse rejoinder).
- Defending an objection against a rebuttal = **contra** (reply-chain items: trace the chain to the step thesis and take the net sign).
- Verdict-suspension / explicit non liquet / pure mapping = **neutral**. `neutral` is reserved for these cases **only**: a *successful* defeater-rebuttal or coherence-defense has a directional net effect on the step thesis (pro, typically at CS1–CS2), and a successful objection to a pro-step argument is contra — without either author asserting or denying the thesis outright.
- D1 ∈ {X, I} → NA.

### D3 — Claim strength (CS1–CS5, NA)

| Code | Definition | Calibration phrase |
|---|---|---|
| CS1 | Coherence/possibility | "X is not incoherent / has a consistent model" |
| CS2 | Defeater rebuttal (incl. undercutting) | "Argument A for/against X fails" |
| CS3 | Epistemic permissibility | "Belief in X can be warranted/rational without propositional evidence" |
| CS4 | Positive evidential, qualitative | "E confirms X / X is more probable than not on E" |
| CS5 | Positive evidential, quantitative | explicit probabilities or Bayes factors |
| NA | — | D2 = neutral, or D1 ∈ {X, I} |

Symmetric across directions (a contra-side CS4 asserts evidence *against* the step thesis). Comparative-likelihood claims without numbers = CS4, not CS5. For CS5 the explicit number must attach to the thesis under assessment (a probability, odds, or a factor comparing the thesis with rivals); numbers that quantify only a data pattern (p-values, effect sizes, sample statistics) do not by themselves make CS5.
**CS1 vs CS2 tie-break:** code CS1 when the load-bearing move is the exhibition of a consistent model/possibility with no specific stated opponent argument as its target; code CS2 when it is showing that a specific stated objection or defeater fails. When an item does both, code CS2 (the rebuttal presupposes and subsumes the coherence claim).

### D4 — Load-bearing epistemic type (alpha / beta / gamma / NA)

- **alpha**: a priori / conceptual / metaphysical argumentation only.
- **beta**: empirical contact — an observational, experimental, or scientific premise carries the argument.
- **gamma**: historical-documentary — ancient testimony, textual criticism carries it.
- **Deletion test** for mixed items: delete the empirical (or historical) premise; if the argument still runs, code alpha. If it collapses, code beta (or gamma).
- *Best-explanation-from-a-regularity sub-rule:* if deleting the specific empirical/measured premise leaves a **different** argument (a purely conceptual one) that reaches the same conclusion, code alpha; if deletion leaves **no** argument to the conclusion, code beta (or gamma).
- Premises the text explicitly stipulates as common ground (presupposed, not defended) do not count as load-bearing for the type; apply the deletion test to the argument's novel, differentiating premise.
- NA when D1 ∈ {X, I}, or when the item is pure mapping with no load-bearing empirical/historical premise (stop-rule cascade, §3).

## 5. Output JSON schema

```json
{
  "item_id": "string",
  "d1_step": "S1|S2|S3|S4|S5|S6|S7|S8|B|P|I|M|X",
  "d2_direction": "pro|contra|neutral|NA",
  "d3_strength": "CS1|CS2|CS3|CS4|CS5|NA",
  "d4_type": "alpha|beta|gamma|NA",
  "flags": ["H","RE","CHAIN","MULTI","LOWTEXT"],
  "confidence": 0.0,
  "uncertain_dimensions": ["d1_step"],
  "rationale": "string, <= 40 words"
}
```
Flags: `H` hiddenness · `RE` religious experience · `CHAIN` reply-chain item (net-effect rule applied) · `MULTI` credible multi-step candidate (primary coded, note in rationale) · `LOWTEXT` abstract too thin, `text_extra` used.

## 6. Worked examples (SYNTHETIC — written for this codebook; not real abstracts)

**WE1** — "Some instances of intense suffering appear to serve no outweighing good. If an omnipotent, perfectly good being existed, such suffering would not occur. Observation of such cases therefore renders the existence of a perfectly good ultimate improbable."
→ `S4 / contra / CS4 / beta`. (Positive evidential claim; the observational premise is load-bearing — delete it and nothing runs.)

**WE2** — "Arguments from apparently pointless suffering assume that if there were a justifying good, we would likely see it. Given the cognitive distance between humans and an omniscient being, that assumption is unwarranted; the inference from 'we see no reason' to 'there is no reason' fails."
→ `S4 / pro / CS2 / alpha`. (Undercuts the inference; asserts no positive evidence for goodness.)

**WE3** — "A recent defense of the argument that the universe began and therefore has a cause replies to the objection that an actual infinite past is possible. I show the reply fails: the objection stands, and the argument's second premise remains unsupported."
→ `S1 / contra / CS2 / alpha`, flag `CHAIN`. (Reply-to-a-reply; net effect on S1 thesis is negative.)

**WE4** — "Belief in God need not rest on propositional evidence. Like perceptual beliefs, it can be properly basic: formed by a truth-aimed faculty in appropriate circumstances, and warranted so long as no defeater is in play."
→ `B / pro / CS3 / alpha`. (Bundled God-target; permissibility claim, not evidence.)

**WE5** — "At least one of the following holds: technological civilizations almost never reach maturity; mature civilizations run almost no ancestor simulations; or we almost certainly live in a simulation. I defend the disjunction without endorsing any disjunct."
→ `X / NA / NA / NA`. (No chain-step thesis is supported or opposed.)

**WE6** — "Weighing the early testimony, rival explanations, and the limits of historical method, I argue the evidence concerning the fate of Jesus's body permits no confident verdict in either direction."
→ `S7 / neutral / NA / gamma`, and note verdict-suspension in rationale.

**WE7** — "Recent observational work shows that the range of physical constants compatible with complex chemistry is far narrower than earlier estimates suggested. Taking this measured narrowness as evidence, I argue that intentional selection of the constants is better supported than chance on the total observational data."
→ `S2 / pro / CS4 / beta`. (Positive evidential claim for agency; the measured-narrowness premise is load-bearing — delete it and nothing runs.)

**WE8** — "Without appeal to any observational premise, I argue that the concept of an uncreated ground that depends on nothing harbors a deep tension: absolute independence excludes the relational properties required for grounding everything else. On reflection, the existence of such a ground is less credible than its denial."
→ `S3 / contra / CS4 / alpha`. (Positive claim against the step thesis, carried entirely by conceptual analysis; nothing empirical to delete.)

**WE9** — "The literature on arguments from suffering has grown rapidly over two decades. I classify the replies into four families, trace their dialectical relations, and identify the questions each leaves open, without endorsing any verdict about what suffering shows."
→ `S4 / neutral / NA / NA`. (Pure mapping; the topic alone does not fix a direction — code the verdict, and there is none.)

## 7. Coder prompt (self-contained; deploy verbatim; contains no hypotheses)

```text
You are coding one sanitized journal-article abstract for a study of argumentative
structure in philosophy of religion. You will assign four codes. Do not guess the
author or venue; if you recognize the text, ignore that recognition and code only
what the text asserts.

[STEP THESES] — paste §4-D1 table
[SPECIAL CLASSES] — paste Q1 rules
[DIRECTION: NET-EFFECT RULE] — paste §4-D2
[STRENGTH SCALE] — paste §4-D3 table
[TYPE + DELETION TEST] — paste §4-D4
[EDGE ANCHORS] — paste binding list
[EXAMPLES] — paste WE1–WE9 with codes
[OUTPUT] — paste §5 schema. Return JSON only.

Procedure: relevance → special classes → step → direction (net effect on the STEP
thesis, tracing reply-chains) → strength → type (deletion test) → confidence,
flags, one-sentence rationale (<= 40 words).

TEXT TO CODE:
{{text}}
{{text_extra}}
```

Assembly note: the deployed prompt is generated from this file by concatenation; the codebook is the single source of truth (prompt = versioned build artifact, git-tracked).

## 8. Gold anchor set (held-out diagnostic set; see companion JSON)

20 real items with adjudicated gold codes. **Usage rules:**
- All 20 are **held out**: none appears in the coder prompt (worked examples WE1–WE9 are synthetic). All 20 are valid validation targets.
- The 20 real texts are fetched and sanitized at pilot; all coders run on them; accuracy scored against gold.
- **Contamination caveat:** these are famous papers; an LLM may recognize them from the abstract text despite blinding. Gold-set accuracy therefore **upper-bounds** expected accuracy on obscure corpus items.
- **Diagnostic role only (v1.1).** The anchors are famous (memorization-suspect) and were coded by the hypothesis-aware instrument designer; they carry **zero headline construct-validity weight**. Report accuracy stratified by the recognition-probe identifiability score (validation-battery §B5); never aggregate into a headline accuracy claim. Construct validity lives in the synthetic criterion set and the battery (`validation-battery-v1.md`).
- Coverage: S1×5, S2×2, S3×2, S4×4, S5×1, S7×1, S8×2, B×1, M×1, X×1. **S6 has no anchor** — mainstream S6 items are scarce; the first clear S6 item found in the pilot year gets promoted to anchor A21 (log the promotion). CS5 likewise has no in-corpus anchor: the known CS5 exemplars (Swinburne 2003, 0.97; McGrew & McGrew 2009, Bayes factor 10^44) live in books/edited volumes outside the corpus — itself an expected-distribution observation, recorded here, not encoded in the prompt.
- Adjudication notes of record: **A11 (White, Noûs 2000)** codes *pro/CS2* by the net-effect rule (it rebuts the multiverse rejoinder to fine-tuning); the outline v0.2 Table 1 had shelved it in the S1 contra column — correction applied in outline v0.3. This mis-shelving was caught *by the act of gold-coding*: the instrument is already doing its job.

## 9. Reliability spec (v1.1 — zero-human)

- **Coders:** A = Anthropic, B = Google, C = OpenAI (adjudicator), all pinned to dated model snapshots at P3; optionally D = open-weights archival coder (re-executability after API endpoints retire). Role-exclusivity matrix in `validation-battery-v1.md` §B0. No human codes any item.
- **Krippendorff's α**: nominal for D1, D2, D4; **ordinal for D3** (CS1–CS5 is ordered; NA excluded pairwise).
- **Gate G1 (v1.2): min pairwise α over {(A,B), (A,C), (B,C)} ≥ 0.70 on every dimension.** All three coders code every item, so the three pairwise αs cost nothing extra; gating on the minimum removes the arbitrariness of naming one pair the "reliability pair" and turns anomalously high single-pair agreement into a visible red flag (correlated priors, not quality). Report the 3-way joint α alongside. Fail → codebook revision loop (max 2). Second failure on D3 → collapse to 3 levels {defense = CS1–CS3, positive = CS4–CS5, NA} and re-gate.
- **Per-cell floors:** in addition to the marginal gate, the analysis-critical cells (defined and frozen at P3; see validation-battery §B8) carry preregistered per-cell agreement and criterion-accuracy floors — marginal α can mask garbage in rare cells.
- **Disagreement resolution:** A/B disagreement → majority-of-three with C. 3-way split → `unresolved` (excluded from primary analysis; sensitivity bounds under each candidate resolution). The full 2-1 resolution matrix is published; headline results must be stable across four estimators (drop-disagreements / A-only / B-only / majority) — validation-battery §B6.
- All disagreements logged with all rationales by adjudication-logger (scripted majority, no human item-judgment); recurring patterns become codebook clarification drafts — dk approves the *document change* (instrument design), never the item codes — before P3 freeze only.

## 10. Pilot spec (P1, v1.1)

1. Fetch Religious Studies 2015, all research articles (~50 est.; actual harvest: 35 incl. 5 notes; book reviews out), abstracts via publisher/PhilPapers.
2. Fetch the 20 gold-anchor texts.
3. Sanitize both sets (§2); log scrubs.
4. Run coders A, B, C on all ~55 items, independently.
5. Score: (a) all three pairwise αs on ~55 — gate = the minimum (v1.2) — plus the 3-way joint α; (b) coder-vs-gold accuracy on the 20 anchors, per dimension, stratified by recognition score (diagnostic only).
6. Battery pilot arms (validation-battery §B): recognition probe (all items) · cue-ablation folklore baseline (all items) · determinism audit (re-code a 20-item subsample) · raw-vs-laundered coding divergence on the 55 (informs the P3 primary-arm decision) · dev-half synthetic coding scored against the §B3 accuracy floors (discriminator AUC gate passes first).
7. Calibrate: chain-relevance rate for the corpus N estimate (outline §4.1).
8. Gate G1 decision (dk approves; recommendation prepared by alpha-scorer); log every majority resolution.

## 11. Hazards (coder- and adjudicator-facing)

- **Functional direction** (A11 pattern): items attacking a rival explanation are pro the step thesis even when the author is neutral on theism. Code the argumentative net effect, not the author's worldview.
- **Reply chains**: always resolve to the step thesis; flag `CHAIN`.
- **Review/survey articles**: mapping without a thesis → neutral; with a verdict → code the verdict.
- **Discussion notes/replies**: code normally, flag `CHAIN`; they are analyzed separately (outline §4.1).
- **Author worldview ≠ direction**: an atheist can write a pro-CS2 item (A11) and a theist a contra one; D2 tracks the argument.
- **Abstract understatement**: philosophy abstracts often undersell strength ("I suggest..."). CS4/CS5 candidates flagged by any coder trigger full-text retrieval before final coding (outline §4.5 cost line).
- **Low-information priors** (v1.1): when the text underdetermines a code, a temperature-0 model outputs its prior deterministically — identical across runs, invisible to reliability statistics. Coders must use `confidence` and `uncertain_dimensions` honestly; the battery's hedged-synthetic items (§B3) and confidence-stratified estimates (§B7) monitor this failure mode.

## 12. Changelog

- **v1.3 (2026-07-15, G1 revision loop round 1 of 2 — dk-approved CL-1..CL-5 from docs/adjudication-log.md §7):** G1 round 1 FAILED at min pairwise α (D2 .673, D3 .608, D4 .569; D1 passed .734); mechanical adjudication of 64 disagreement cells identified 9 recurring patterns rooted in five boundary under-specifications, all clarified hypothesis-neutrally: (1) CL-1 §3-Q1 M/step/X decision order; (2) CL-2 stop-rule NA cascade stated explicitly in §3 and aligned in §4-D3/D4 ({X, I} wording reconciled — the largest pattern, 9× D4 NA/alpha, was an NA-schema under-specification, not a coding dispute); (3) CL-3 §4-D2 neutral reserved for verdict-suspension/non-liquet/pure mapping only; successful rebuttals/coherence-defenses take the net-effect direction; (4) CL-4 §4-D3 CS1/CS2 tie-break (specific-target rule; both → CS2); (5) CL-5 §4-D4 best-explanation-from-a-regularity sub-rule for the deletion test. Prompt rebuilt (manifest logged); round-1 coded outputs archived to data/coded/round1/; full 55-item tri-coder re-code follows for the re-gate.
- **v1.2a (2026-07-14, synthetic-spec audit fixes):** two §4 clarifications surfaced by adversarial audit of the synthetic criterion specs, both recurring coding boundaries: (1) §4-D3 — CS5's explicit number must attach to the thesis under assessment; data-pattern statistics (p-values, effect sizes) alone do not make CS5; (2) §4-D4 — explicitly stipulated common-ground premises are not load-bearing for the type; the deletion test applies to the novel, differentiating premise. Both ship in the coder prompt (rebuilt, manifest logged).
- **v1.2 (2026-07-14, dk-approved):** Gate G1 redefined from α(A,B) to **min pairwise α over all three coder pairs** (every dimension ≥ 0.70) — all coders code every item, so this costs nothing, removes the arbitrary choice of gate pair, and exposes correlated-prior artifacts as anomalously high single-pair agreement. §1/§9/§10 updated. Coder-facing content unchanged (prompt hash stable). Companion role changes recorded in validation-battery §B0 (E = GLM-class open-weights via Perplexity Agent API with search structurally off; Sonar retired from all blinded roles; conformity checker staffed = Kimi-class; coder D promoted to mandatory).
- **v1.1a (2026-07-14, firewall-audit fixes):** §1 hypothesis-naming sentence rewritten neutrally (no dimension/direction named); coder-runner now banned from this file entirely (built prompt only — agent def + CLAUDE.md rule 1 updated in tandem); WE5/WE7/WE8 parenthetical notes trimmed (design-register and crosstab-flagging language removed); §3 dimension-independence rule added (symmetric, hypothesis-neutral); §8 heading retitled diagnostic; §10 step 1 actual harvest count annotated, step 6 adds the dev-half synthetic arm; §11 battery reference corrected §B4→§B3; build-script FORBIDDEN token list extended. Prompt rebuilt; manifest logged.
- **v1.1 (2026-07-14, P1 session 1 — zero-human amendment, dk-approved):** (1) binding zero-human rule: no human codes any item, anywhere in the pipeline; the designer's labor = codebook authorship, synthetic-criterion specs/sign-off, gate approvals. dk pilot hand-coding and the P4 150-item human sample are **removed**; validity now rests on the battery in `validation-battery-v1.md` (new canonical companion). (2) Third coder family added (C = OpenAI, adjudicator); disagreements resolved by majority-of-three, 3-way splits → unresolved protocol; dk item-level HITL adjudication removed. (3) Counter-stereotypical worked examples **WE7–WE9** added to §6 (pro/CS4/beta · contra/CS4/alpha · topic-cue-without-verdict neutral) — rationale: the prior example set was uniformly stereotype-congruent and could teach topic-to-code shortcuts; coder prompt content changes accordingly (rebuilt, manifest logged). (4) Gold-anchor set demoted to diagnostic role (§8); headline construct validity moves to the synthetic criterion set. (5) §9 rewritten (tri-family, per-cell floors, four-estimator stability); §10 rewritten (battery pilot arms); §11 low-information-priors hazard added. Claim-discipline note: the paper claims measurement by a fixed, preregistered, multi-family LLM instrument — not human-equivalent annotation.
- v1.0 (2026-07-14, P1 session 1, addendum 2): §2.2 clarification per dk adjudication — numbered-reference self-citations without name/year/venue are kept verbatim (case: A15 first_para "In [4] I argued..."). Sanitized outputs unchanged.
- v1.0 (2026-07-14, P1 session 1, addendum): 9 abstract-less gold anchors sourced with verbatim texts, dk-approved: printed author abstracts recovered from journal originals where they exist (A06/A18/A19 — Faith & Philosophy prints abstracts Crossref lacks), else first/last body paragraphs verbatim (A01/A02/A11/A15 journal scans; A03 Adams & Adams 1990 reprint; A12 Manson 2003 reprint). Extraction dual-checked by independent verbatim verifiers; OCR restorations image-verified and logged (data/raw/gold_fulltext_excerpts.json). No summarization or paraphrase anywhere. G1 gold-accuracy reporting must stratify by text_source (crossref_abstract 11 / printed_abstract 3 / first_last_para 6). No gold-code changes.
- v1.0 (2026-07-14, P1 session 1): gold anchors A05/A07/A15 web-verified (Crossref/Cambridge Core); citations completed (A05 = RS 41.2, 201-215, part I/II structure confirmed; A07 = Philosophy 43.165, 199-212; A15 = Nous 15.1, 41-51); verify_at_pilot cleared. No gold-code changes.
- v1.0 (2026-07-14): initial instrument. Verified anchors added: Craig RS 20 (1984) 367–375; Oppy RS 27 (1991) 189–197; Gwiazda RS 45 (2009) 487–493 (Swinburne reply, same issue, 495–498, logged as optional CHAIN anchor). Outline Table 1 correction (White → pro-functional) applied as outline v0.3. Future corpus note: Gellman, "Prospects for a sound stage 3 of cosmological arguments," RS 36 (2000) 195–201 — direct S3 item for the corpus.
