# ditch-audit — Codebook v1.0 (Coding Instrument)

2026-07-14 · Owner: dk · Status: ready for pilot (P1) · Companion file: `ditch-audit-gold-anchors-v1.json`
Frozen at P3 preregistration; any post-freeze edit voids the confirmatory run.

---

## 1. Scope and blindness architecture

**What this instrument does.** Assigns four codes (D1 step, D2 direction, D3 claim strength, D4 epistemic type) to one journal-article abstract at a time. D5 (venue tier) is **never coded** — it is joined from metadata after coding, downstream.

**Blindness rules (hard constraints):**
- The coder (LLM or human) sees **only** sanitized text: no author, no title, no journal, no year, no DOI.
- The coder prompt (§7) contains **no hypotheses**. H1/H2 and the expected topography live in the outline document only. Rationale: a coder that knows "pro-CS4 is predicted to be α-type" will drift toward confirming it. The instrument must be usable by a coder who has never seen the paper's thesis.
- Dual coders from **different model families**, run independently; neither sees the other's output.

**Pipeline position:**
`harvest → sanitize → [CODER A ∥ CODER B] → agreement? → (yes: accept) / (no: dk adjudication) → join D5 venue metadata → compute step-status (outline §4.4)`

## 2. Input sanitization spec

Input unit: abstract (+ optionally first/last paragraph when abstract < 60 words).
Sanitization pass (scripted + manual spot-check):
1. Strip metadata fields (author/title/journal/year/DOI/volume).
2. Regex-scrub in-text self-identifiers: "In this journal", "as I argued in [year]", proper-name self-citations where they identify the author.
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
- **Q2 Step (D1).** Assign the single step whose thesis the primary conclusion most directly supports or opposes.
- **Q3 Direction (D2).** Relative to the **step thesis**, not the immediately targeted paper (net-effect rule, §4-D2).
- **Q4 Strength (D3).** CS1–CS5 per definitions; `NA` if D2 = neutral or D1 ∈ {X}.
- **Q5 Type (D4).** Deletion test on the load-bearing premise.
- **Q6 Confidence + flags + one-sentence rationale (≤40 words).**

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
- Verdict-suspension / explicit non liquet / pure mapping = **neutral**.
- D1 ∈ {X} → NA.

### D3 — Claim strength (CS1–CS5, NA)

| Code | Definition | Calibration phrase |
|---|---|---|
| CS1 | Coherence/possibility | "X is not incoherent / has a consistent model" |
| CS2 | Defeater rebuttal (incl. undercutting) | "Argument A for/against X fails" |
| CS3 | Epistemic permissibility | "Belief in X can be warranted/rational without propositional evidence" |
| CS4 | Positive evidential, qualitative | "E confirms X / X is more probable than not on E" |
| CS5 | Positive evidential, quantitative | explicit probabilities or Bayes factors |
| NA | — | D2 = neutral, or D1 ∈ {X, I} |

Symmetric across directions (a contra-side CS4 asserts evidence *against* the step thesis). Comparative-likelihood claims without numbers = CS4, not CS5.

### D4 — Load-bearing epistemic type (alpha / beta / gamma / NA)

- **alpha**: a priori / conceptual / metaphysical argumentation only.
- **beta**: empirical contact — an observational, experimental, or scientific premise carries the argument.
- **gamma**: historical-documentary — ancient testimony, textual criticism carries it.
- **Deletion test** for mixed items: delete the empirical (or historical) premise; if the argument still runs, code alpha. If it collapses, code beta (or gamma).
- NA when D1 ∈ {X} or the item is pure mapping.

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
→ `X / NA / NA / NA`. (No chain-step thesis is supported or opposed; framework-adjacent items are witnesses, not corpus evidence.)

**WE6** — "Weighing the early testimony, rival explanations, and the limits of historical method, I argue the evidence concerning the fate of Jesus's body permits no confident verdict in either direction."
→ `S7 / neutral / NA / gamma`, and note verdict-suspension in rationale.

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
[EXAMPLES] — paste WE1–WE6 with codes
[OUTPUT] — paste §5 schema. Return JSON only.

Procedure: relevance → special classes → step → direction (net effect on the STEP
thesis, tracing reply-chains) → strength → type (deletion test) → confidence,
flags, one-sentence rationale (<= 40 words).

TEXT TO CODE:
{{text}}
{{text_extra}}
```

Assembly note: the deployed prompt is generated from this file by concatenation; the codebook is the single source of truth (prompt = versioned build artifact, git-tracked).

## 8. Gold anchor set (held-out validation; see companion JSON)

20 real items with adjudicated gold codes. **Usage rules:**
- All 20 are **held out**: none appears in the coder prompt (worked examples WE1–WE6 are synthetic). All 20 are valid validation targets.
- dk fetches the 20 real abstracts at pilot, sanitizes, runs both coders, scores against gold.
- **Contamination caveat:** these are famous papers; an LLM may recognize them from the abstract text despite blinding. Gold-set accuracy therefore **upper-bounds** expected accuracy on obscure corpus items. True validation = the 150-item stratified human-coded sample at P4.
- Coverage: S1×5, S2×2, S3×2, S4×4, S5×1, S7×1, S8×2, B×1, M×1, X×1. **S6 has no anchor** — mainstream S6 items are scarce; the first clear S6 item found in the pilot year gets promoted to anchor A21 (log the promotion). CS5 likewise has no in-corpus anchor: the known CS5 exemplars (Swinburne 2003, 0.97; McGrew & McGrew 2009, Bayes factor 10^44) live in books/edited volumes outside the corpus — itself an expected-distribution observation, recorded here, not encoded in the prompt.
- Adjudication notes of record: **A11 (White, Noûs 2000)** codes *pro/CS2* by the net-effect rule (it rebuts the multiverse rejoinder to fine-tuning); the outline v0.2 Table 1 had shelved it in the S1 contra column — correction applied in outline v0.3. This mis-shelving was caught *by the act of gold-coding*: the instrument is already doing its job.

## 9. Reliability spec

- Coder A vs Coder B (different model families), plus dk on the pilot subset.
- **Krippendorff's α**: nominal for D1, D2, D4; **ordinal for D3** (CS1–CS5 is ordered; NA excluded pairwise).
- **Gate G1: α ≥ 0.70 on every dimension.** Fail → codebook revision loop (max 2). Second failure on D3 → collapse to 3 levels {defense = CS1–CS3, positive = CS4–CS5, NA} and re-gate.
- All disagreements logged with both rationales; adjudication decisions become codebook clarifications (appended, versioned) — before P3 freeze only.

## 10. Pilot spec (P1)

1. Fetch Religious Studies 2015, all research articles (~50; book reviews out), abstracts via publisher/PhilPapers.
2. Fetch the 20 gold-anchor abstracts.
3. Sanitize both sets (§2); log scrubs.
4. Run dual coders on all ~70 items; dk hand-codes the pilot-year items independently.
5. Score: (a) coder-vs-coder α on ~70; (b) coder-vs-gold accuracy on the 20 anchors, per dimension; (c) dk-vs-coder α on pilot year.
6. Calibrate: chain-relevance rate for the corpus N estimate (outline §4.1).
7. Gate G1 decision; log every adjudication.

## 11. Hazards (coder- and adjudicator-facing)

- **Functional direction** (A11 pattern): items attacking a rival explanation are pro the step thesis even when the author is neutral on theism. Code the argumentative net effect, not the author's worldview.
- **Reply chains**: always resolve to the step thesis; flag `CHAIN`.
- **Review/survey articles**: mapping without a thesis → neutral; with a verdict → code the verdict.
- **Discussion notes/replies**: code normally, flag `CHAIN`; they are analyzed separately (outline §4.1).
- **Author worldview ≠ direction**: an atheist can write a pro-CS2 item (A11) and a theist a contra one; D2 tracks the argument.
- **Abstract understatement**: philosophy abstracts often undersell strength ("I suggest..."). CS4/CS5 candidates flagged by either coder trigger full-text retrieval before final coding (outline §4.5 cost line).

## 12. Changelog

- v1.0 (2026-07-14, P1 session 1): gold anchors A05/A07/A15 web-verified (Crossref/Cambridge Core); citations completed (A05 = RS 41.2, 201-215, part I/II structure confirmed; A07 = Philosophy 43.165, 199-212; A15 = Nous 15.1, 41-51); verify_at_pilot cleared. No gold-code changes.
- v1.0 (2026-07-14): initial instrument. Verified anchors added: Craig RS 20 (1984) 367–375; Oppy RS 27 (1991) 189–197; Gwiazda RS 45 (2009) 487–493 (Swinburne reply, same issue, 495–498, logged as optional CHAIN anchor). Outline Table 1 correction (White → pro-functional) applied as outline v0.3. Future corpus note: Gellman, "Prospects for a sound stage 3 of cosmological arguments," RS 36 (2000) 195–201 — direct S3 item for the corpus.
