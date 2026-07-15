# ditch-audit — Adjudication Log (P1)

Two mechanical adjudication rounds are recorded here, both zero-human (absolute rule 5).
**Round 1** (raw arm, 55 items; codebook v1.1–v1.2) is preserved **verbatim** below for
provenance. The **Final round** (v1.4a consolidated union, n=89 — per-dimension majority of
three identical runs, IJPR 2015 expansion, D3 collapsed to `{DEF, POS, NA}`) is the operative
adjudication for the G1 re-gate and appears in the last top-level section (search
`Final round — v1.4a`). Both rounds are reproduced by `scripts/adjudicate.py` — Round 1 with no
arguments, the Final round with `--dataset all89`; the no-arg output is regression-pinned
byte-identical to the pre-refactor script, so the mechanical rule is provably unchanged across
rounds.

---

# Round 1 — raw arm, 55 items (superseded by the v1.4a re-gate; preserved for provenance)

2026-07-15 · Owner: adjudication-logger (scripted) · Phase: P1 (pre-P3-freeze)
Companion: `codebook-v1.md` §9/§12, `validation-battery-v1.md` §B2/§B6.

## 0. Method and zero-human attestation

**Absolute rule 5 (zero-human).** No human — dk included — judged any item in this log.
Every `majority` / `unresolved` verdict below is a deterministic function of the three
coders' output files, applied by `scripts/adjudicate.py` (stdlib-only). The script was
re-run and produced byte-identical output (deterministic). dk's only role in adjudication
is (i) approving codebook clarification *documents* (§7 below, instrument design, never item
codes) and (ii) gate approval. dk did not adjudicate, override, or tie-break any item.

**Inputs (raw arm, P1 本코딩):**

| file | items | role |
|---|---|---|
| `data/coded/pilot_rs2015_{a,b,c}.jsonl` | 35 | Religious Studies 2015 pilot |
| `data/coded/gold_anchors_{a,b,c}.jsonl` | 20 | gold anchors (diagnostic; codebook §8) |
| `data/coded/stubs_{pilot_rs2015,gold_anchors}_{a,b,c}.jsonl` | 55 | cue-ablation baseline (§B2), §6 audit input |
| `docs/gold-anchors-v1.json` | 20 | gold codes for §5 conflict flags |

Coders A = Anthropic, B = Google, C = OpenAI (majority adjudicator seat, §B6). Item-ID
order verified equal across A/B/C for both groups; parse_fail = 0; every record carries all
four dimensions. Reproduce: `python3 scripts/adjudicate.py`.

**Decision rule (per dimension, per item):** unanimous → not a disagreement; two coders
agree, one differs → `majority` (adopt the 2-vote value; log which coder was minority);
all three differ → `unresolved` (excluded from primary analysis; sensitivity bounds computed
downstream — §B6). Dimensions: D1 `d1_step`, D2 `d2_direction`, D3 `d3_strength`, D4 `d4_type`.

## 1. Adjudication summary

- Item-dimension cells: **220** (55 items × 4 dimensions).
- Unanimous (A=B=C): **156** (70.9%). Disagreements: **64** (29.1%) across **27 distinct items**.
- Resolved by majority (2-1): **60**. Unresolved (3-way): **4**.

| dimension | disagreements | majority (2-1) | unresolved (3-way) |
|---|---|---|---|
| D1 step | 17 | 16 | 1 |
| D2 direction | 16 | 13 | 3 |
| D3 strength | 16 | 16 | 0 |
| D4 type | 15 | 15 | 0 |
| **total** | **64** | **60** | **4** |

Every disagreement carries a verdict and a full record (Appendix A). Coverage check: 60 + 4 = 64.

## 2. 2-1 resolution matrix (minority coder × dimension)

Cell = number of 2-1 resolutions on that dimension in which the named coder was the lone
dissenter (i.e. was outvoted 2-to-1). Total = 60.

| minority coder | D1 | D2 | D3 | D4 | row total | share |
|---|---|---|---|---|---|---|
| A (Anthropic) | 4 | 7 | 8 | 6 | **25** | 41.7% |
| B (Google) | 6 | 3 | 2 | 2 | **13** | 21.7% |
| C (OpenAI) | 6 | 3 | 6 | 7 | **22** | 36.7% |
| **column total** | **16** | **13** | **16** | **15** | **60** | |

**Minority-transition cells (minority value → adopted majority value), by coder × dimension.**
This is the "× 셀" layer of the matrix required by the agent spec.

| coder | dim | transitions (min→maj : count) |
|---|---|---|
| A | D1 | M→I 1 · S8→S5 1 · M→B 1 · I→M 1 |
| A | D2 | neutral→pro 4 · NA→pro 2 · pro→contra 1 |
| A | D3 | NA→CS1 3 · CS3→CS2 2 · NA→CS2 2 · CS2→CS1 1 |
| A | D4 | NA→alpha 3 · alpha→beta 3 |
| B | D1 | X→M 3 · S2→M 1 · B→S2 1 · P→X 1 |
| B | D2 | NA→neutral 2 · contra→NA 1 |
| B | D3 | CS1→NA 1 · CS4→CS1 1 |
| B | D4 | alpha→NA 1 · NA→gamma 1 |
| C | D1 | M→S2 2 · S4→I 1 · S5→S8 1 · X→B 1 · B→I 1 |
| C | D2 | pro→NA 1 · contra→neutral 1 · contra→NA 1 |
| C | D3 | CS2→NA 3 · CS1→CS2 2 · CS4→NA 1 |
| C | D4 | alpha→NA 5 · beta→NA 1 · beta→alpha 1 |

**Read of the matrix (descriptive, not a verdict):** A is the most frequent minority (25/60),
concentrated on D2/D3/D4 where A applies a Q0/Q1 stop (X/I/M/neutral) and cascades downstream
dimensions to NA while B and C code the item as in-scope and directional (A's `neutral→pro`,
`NA→CS1/CS2`, `NA→alpha`). C's minority cases concentrate on D4 (`alpha→NA` ×5) and on finer D1
splits (`M→S2`, `S5→S8`). B's minority cases concentrate on D1 scope (`X→M` ×3). No coder is a
persistent global outlier; the asymmetry is dimension-specific and traced to the boundaries in §4/§7.

## 3. Unresolved (3-way splits)

4 cells; excluded from primary analysis. Sensitivity bounds under each candidate resolution are
an analysis-stage task (§B6), not computed here. All four are relevance/direction boundaries.

| item | dim | A | B | C | note |
|---|---|---|---|---|---|
| `c7235013ee238bf8` | D2 | neutral | pro | NA | D1 resolved I (majority); A=neutral, B=pro, C=NA on direction |
| `99fa3cbf1908eea8` | D1 | X | S8 | S5 | Eucharistic Real Presence: out-of-scope vs S8 vs S5 |
| `7863b2b2e05fb3fa` | D2 | neutral | pro | NA | Christian-art/faith experience: neutral vs pro vs NA |
| `004c8a3184da5ff2` | D2 | neutral | NA | pro | ontological-arg-as-progress: neutral vs NA vs pro |

Full rationales in Appendix A. Distribution: D2 ×3, D1 ×1. D3 and D4 had zero 3-way splits.

## 4. Recurrence pattern tally

A "pattern" = (dimension, competing value pair) for a 2-1 split. Patterns recurring **≥ 3 times**
qualify for a codebook clarification draft (§7). Direction shown as the {minority, majority} pair
(undirected) with the dominant directed transition noted.

| # | dimension | competing values | count | dominant directed transition |
|---|---|---|---|---|
| P1 | D4 type | NA / alpha | **9** | alpha→NA 6 (C ×5, B ×1), NA→alpha 3 (A) |
| P2 | D3 strength | CS2 / NA | **5** | CS2→NA 3 (C), NA→CS2 2 (A) |
| P3 | D2 direction | neutral / pro | **4** | neutral→pro 4 (A) |
| P4 | D3 strength | CS1 / NA | **4** | NA→CS1 3 (A), CS1→NA 1 (B) |
| P5 | D4 type | alpha / beta | **4** | alpha→beta 3 (A), beta→alpha 1 (C) |
| P6 | D2 direction | NA / pro | **3** | NA→pro 2 (A), pro→NA 1 (C) |
| P7 | D1 step | M / S2 | **3** | M→S2 2 (C), S2→M 1 (B) |
| P8 | D1 step | M / X | **3** | X→M 3 (B) |
| P9 | D3 strength | CS1 / CS2 | **3** | CS1→CS2 2 (C), CS2→CS1 1 (A/B) |

Sub-threshold (2×, logged, no draft): D3 CS2/CS3, D1 S5/S8, D1 I/M, D2 NA/neutral, D2 NA/contra.

**Structural note.** P1/P2/P4/P6 are largely *cascade* disagreements: when coders split on
relevance/direction (D1 scope or D2 neutral-vs-directional), the downstream D3/D4 NA-vs-scored
split follows mechanically. P7/P8 (D1 M-vs-S2, M-vs-X) and P3/P6 (D2 neutral/NA-vs-pro) are the
upstream roots; P1/P2/P4 are their downstream shadows. The genuinely intra-dimensional recurrences
are P5 (D4 deletion-test alpha/beta) and P9 (D3 CS1/CS2 gradation). §7 drafts are organized by root.

## 5. Gold-conflict flags

Per verification criterion (b): majority resolutions that conflict with a gold anchor code are
flagged here and NOT overridden — the majority verdict stands (zero-human rule). Gold is
**diagnostic only** (codebook §8 v1.1; zero headline construct-validity weight; recognition-
stratified). Gold revision is **dk's sole authority and only as instrument design** — this log
neither revises gold nor changes any item code. 9 conflicts across 5 anchors:

| anchor | dim | majority (adopted) | gold | minority coder | minority value | minority == gold? |
|---|---|---|---|---|---|---|
| A04 | D4 | beta | alpha | A | alpha | **yes** |
| A12 | D1 | S2 | S1 | C | M | no |
| A13 | D1 | S2 | S3 | C | M | no |
| A13 | D3 | CS1 | CS4 | B | CS4 | **yes** |
| A14 | D1 | I | S3 | C | B | no |
| A14 | D2 | NA | contra | C | contra | **yes** |
| A14 | D3 | NA | CS2 | C | CS2 | **yes** |
| A14 | D4 | NA | alpha | C | alpha | **yes** |
| A17 | D3 | CS1 | CS2 | A | CS2 | **yes** |

**Flag detail (for dk diagnostic review; not an item-adjudication request):**

- **A14 (Gwiazda, simplicity via the infinite) — 4/4 dimensions conflict.** A and B both coded
  A14 = `I` (intra-theistic attribute puzzle → stop → NA cascade). Gold = `S3 / contra / CS2 /
  alpha`. Only C coded it in-scope (`B / contra / CS2 / alpha`) and C matches gold on D2/D3/D4
  (not D1: C said B, gold S3). The 2-vote `I` classification zeroed the item out relative to gold.
  This is the single largest gold divergence and couples to pattern P7/P8 (the M/I/scope boundary)
  and to the D4-NA cascade (P1).
- **A12 / A13 (fine-tuning sceptic; necessary-being-to-God).** Majority D1 = `S2` where gold =
  `S1` (A12) / `S3` (A13). This is the S1↔S2↔S3 boundary on cosmological/fine-tuning items
  ("bare cause" S1 vs "designer-agent" S2 vs "necessary being's attributes" S3 — codebook edge
  anchors). C dissented to `M` on both (a methodology reading of the probability machinery).
- **A13 / A17 (D3).** Majority `CS1` where gold `CS4` (A13) / `CS2` (A17); in both the lone
  dissenter matched gold (B=CS4 on A13; A=CS2 on A17) — see the 7/9 pattern below.

**Cross-cutting observation (diagnostic).** In **7 of 9** conflicts the dropped minority coder
was the one who matched gold — i.e. majority-of-three moved *away* from the diagnostic gold and
the lone dissenter was "right" by gold. This is expected under the zero-human design (gold carries
zero headline weight and the anchors are memorization-suspect), but it is a recognizability-
stratification signal for §B5/§B8 and is surfaced here for dk's instrument-design review, not acted on.

## 6. Cue-ablation stub-congruence audit (§B6 input)

Question (validation-battery §B6): does the tie-breaker systematically break **toward the
stub-predictable code** — i.e. toward the folklore/topic-cue baseline (§B2)? For each 2-1
resolution the stub predictor is the **mode of the three coders' stub codes** for that (item,
dim); classification:

- `toward_stub` — adopted majority value == stub mode (resolution agrees with folklore baseline);
- `away_stub` — dropped minority value == stub mode (resolution overrode folklore baseline);
- `uninformative` — stub mode is ambiguous (no unique mode / 3-way stub split) or equals neither.

**Result (over 60 2-1 resolutions):**

| dimension | toward_stub | away_stub | uninformative | toward-share* |
|---|---|---|---|---|
| D1 step | 4 | 4 | 8 | 0.50 |
| D2 direction | 6 | 5 | 2 | 0.55 |
| D3 strength | 7 | 4 | 5 | 0.64 |
| D4 type | 8 | 4 | 3 | 0.67 |
| **total** | **25** | **17** | **18** | **0.60** |

\*toward-share = toward / (toward + away), among informative resolutions only.

**Support metric (stub-vote count, all 60 resolutions).** For each resolution, count how many of
the 3 stub coders predicted the adopted value vs the dropped value: majority-value favored **28**,
minority-value favored **21**, tie **11**.

**Read.** There is a **mild lean toward the stub-predictable (folklore) code** — 60% of informative
2-1 resolutions and a 28-vs-21 stub-vote edge — concentrated on **D4 (0.67) and D3 (0.64)**; D1 is
even (0.50) and mostly uninformative. This is **not** a strong systematic break toward folklore, but
the D4/D3 lean is non-trivial and coincides with the largest recurrence pattern (P1, D4 NA/alpha) and
with the §5 gold divergences on D3. Reported here as **§B6 audit input**; the confirmatory cross-tab
against analysis-predicted cells, the four-estimator stability, and the tipping-point fraction are
analysis-stage tasks (§B6) — deferred, not computed here (they require the firewalled critical-cell
list). No P1 gate turns on this number.

## 7. Codebook clarification drafts (dk approval pending — instrument design, NOT item codes)

Patterns recurring ≥ 3 times (§4) generate the following **draft** clarifications. These are
proposed *document changes* to `codebook-v1.md`; per codebook §9 and the agent contract, **dk
approves the document change** (never the item codes), and only **before P3 freeze** (we are at
P1, so drafting is in-window). Each draft is written to be hypothesis-neutral and symmetric across
directions/values. If dk approves, the change ships to codebook §12 changelog and the prompt is
rebuilt (manifest logged). **Nothing here has been applied; the codebook is unchanged.**

> Firewall note: these drafts name only dimension boundaries, not hypotheses or predicted cells.

### CL-1 — D1 scope routing: M vs substantive step vs X (roots P7 `M/S2`, P8 `M/X`; also I/M)
Recurrence: 3× `M/S2`, 3× `M/X`, 2× `I/M`. Coders split on whether a paper *about how theistic/
atheistic arguments should proceed* is `M` (methodology, in-scope, continues to D2–D4), `X` (out
of scope), or routed to the substantive step it comments on (`S2`, etc.). **Draft:** add to §3 Q1 /
§4-D1 a decision order — (a) if the primary conclusion is a claim *about the case-making itself*
(its structure, probability machinery, epistemology of cumulative cases) and takes a verdict on
that machinery → `M`; (b) if it merely *uses* an argument's topic as an illustration with no verdict
on any thesis or on the machinery → `X`; (c) if it takes a verdict on a first-order step thesis
*through* a methodological critique, code the step, not `M`. Symmetric (applies to pro- and
anti-theistic methodology alike). Companion note: the fine-tuning items also expose S1↔S2↔S3
(bare-cause / designer-agent / necessary-being-attributes) — recommend restating the three edge
anchors adjacently in §4-D1 without changing their content.

### CL-2 — D4 (and D3) NA conditions aligned to the Q1 stop rules (root P1 `NA/alpha`, P2/P4 `NA` cascades)
Recurrence: 9× `NA/alpha` (D4), 5× `CS2/NA` + 4× `CS1/NA` (D3). Diagnosis: this is a codebook
**under-specification**, not a substantive coding dispute. §4-D3 lists NA for "D2 = neutral, or
D1 ∈ {X, I}", but §4-D4 lists NA only for "D1 ∈ {X} or pure mapping" — so for an `I` item (and
for `P` after direction) the *intended* stop-rule NA on D4 is not stated, and coders split
(A codes NA by the stop rule; B/C code alpha from the literal §4-D4). **Draft:** state explicitly
in §3 (Q4/Q5) and §4-D4 that the Q1 stop-rule codes cascade to NA on the un-coded downstream
dimensions — `I` → D2, D3, D4 = NA; `P` → D3, D4 = NA; `X` → all NA; pure-mapping neutral → D3 = NA
(D4 may still carry a type where a load-bearing empirical/historical premise exists, per WE6). Purely
mechanical alignment of the NA schema; no directional content. (Also reconcile the §3-Q4 "D1 ∈ {X}"
vs §4-D3-table "D1 ∈ {X, I}" wording — the table is the intended rule.)

### CL-3 — D2 net-effect: successful objection-rebuttal / coherence-defense = pro, not neutral (root P3 `neutral/pro`, P6 `NA/pro`)
Recurrence: 4× `neutral/pro`, 3× `NA/pro`. Coders split on whether an item that *rebuts an objection
to* or *defends the coherence of* a step-relevant claim, without asserting the claim's truth, is
`pro` (net-effect / functional-direction rule, §4-D2 + §11) or `neutral`/`NA`. **Draft:** clarify in
§4-D2 that a *successful* defeater-rebuttal or coherence-defense has a directional net effect on the
step thesis (`pro` at the corresponding CS level — typically CS1/CS2) and that `neutral` is reserved
for **explicit verdict-suspension / non liquet / pure mapping only** (WE6/WE9 pattern). Symmetric: a
successful objection *to* a pro-step argument is `contra`. This is a restatement of the existing
net-effect and functional-direction rules, tightened at the neutral boundary; no new directional claim.

### CL-4 — D3 CS1 vs CS2 boundary (root P9 `CS1/CS2`)
Recurrence: 3× `CS1/CS2`. Coders split on whether establishing a doctrine's *coherence* is CS1
("has a consistent model") or CS2 ("an objection/defeater fails"), because a coherence-defense
usually also rebuts an incoherence charge. **Draft:** add a tie-break to §4-D3 — code CS1 when the
item's load-bearing move is the *exhibition of a consistent model/possibility* with no specific
opponent argument as its target; code CS2 when the load-bearing move is *showing a specific stated
objection/defeater fails*. When an item does both, code the **higher-numbered** dialectical move
(CS2), since the rebuttal presupposes and subsumes the coherence claim. Symmetric across directions.

### CL-5 — D4 alpha vs beta deletion test for best-explanation-from-a-regularity items (root P5 `alpha/beta`)
Recurrence: 4× `alpha/beta` (3 directed `alpha→beta`). Coders split on items that argue to an agent/
cause as the *best explanation of an empirical regularity* (mind–brain interaction; measured
constant-narrowness): is the empirical premise load-bearing (`beta`) or merely a common-ground
launch point for an a-priori inference (`alpha`)? **Draft:** extend the §4-D4 deletion test with the
explicit sub-rule already implied by WE7 vs WE8 — if deleting the specific empirical/measured premise
leaves a *different* argument (a purely conceptual one) that reaches the same conclusion, code `alpha`;
if deletion leaves *no* argument to the conclusion, code `beta` (resp. `gamma`). Reaffirm the v1.2a
common-ground clause (stipulated common ground is not load-bearing). Fully symmetric; sharpens an
existing test rather than adding content.

**Status of §7:** all five are drafts for dk's document-change decision. None is applied; no item
code in §1–§6 depends on them. If P3 freeze arrives before dk rules on any draft, that draft is
frozen out and its pattern is reported as a P4 analysis limitation (agent contract).

## 8. Deliverable verification checklist

- **(a) every disagreement has a verdict + record** — 64/64: 60 `majority` + 4 `unresolved`;
  full register in Appendix A; summary §1; per-item rationales retained.
- **(b) gold-conflict flags** — §5: 9 conflicts flagged, majority verdicts NOT overridden, gold
  unchanged (gold revision = dk-only, instrument-design-only).
- **(c) 2-1 matrix + recurrence tally** — §2 (minority × dimension × cell) and §4 (patterns, ≥3
  flagged for §7 drafts).
- **(d) zero human item-judgment** — attested §0; verdicts are pure `scripts/adjudicate.py` output,
  re-run byte-identical; dk performed no item adjudication, tie-break, or override.

---

## Appendix A — full disagreement register (grouped by item)

All 27 items with ≥ 1 disagreement. Each shows the disagreeing dimensions (A/B/C values, verdict,
adopted value, minority coder) and the three coders' one-sentence rationales (verbatim from the
coded files). Values are the coders' own outputs; the adjudicator only tallied them.

#### `316b879f61c13613` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | I | S4 | majority | I | c |
| D2 | NA | NA | pro | majority | NA | c |
| D3 | NA | NA | CS2 | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Defends divine command theory against Morriston's counterpossible objection; an intra-theistic metaethical/attribute dispute, excluded from the chain per codebook.
- B: The paper defends divine command theory against Morriston's counterpossible objection, which constitutes an intra-theistic attribute puzzle concerning the relationship between God's commands and moral goodness.
- C: The abstract rebuts a conceptual objection that divine command theory implies a morally terrible deity, thereby indirectly defending divine goodness rather than offering positive evidence.

#### `8a36d47b3663565f` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | neutral | pro | pro | majority | pro | a |

- A: Interpretive/exegetical reading of James's pragmatic argument; no direct evidential claim for or against belief, so coded neutral per Q1 stop rule.
- B: Defends a charitable, contextualist reading of James's 'Will to Believe,' supporting the epistemic permissibility of pragmatic grounds for belief.
- C: Reads James as allowing context-sensitive evidential sufficiency for responsible belief when action is urgent, supporting pragmatic permissibility rather than a chain-step thesis.

#### `8de10cee13eacd75` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D3 | CS3 | CS2 | CS2 | majority | CS2 | a |

- A: Defends a qualified basicality but argues basic Christian beliefs remain evidentially vulnerable, undermining reformed epistemology's protective function against evidence.
- B: The text critiques Plantinga's Reformed Epistemology, arguing that Christian belief remains vulnerable to evidential challenges. This rebuts a major defense of bundled belief (B), resulting in a contra direction at CS2 strength.
- C: The abstract argues that reformed epistemology cannot insulate Christian belief from evidential defeaters, undercutting a pro-Christian basicality defense without relying on empirical or historical premises.

#### `cabd8f6e0c2ae4a5` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S8 | S8 | S5 | majority | S8 | c |
| D2 | neutral | pro | pro | majority | pro | a |
| D3 | NA | CS1 | CS1 | majority | CS1 | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Develops a coherence model of Eucharistic real presence via incarnation Christology; no evidential claim about incarnation/Trinity itself, just internal coherence exposition.
- B: The author defends the coherence of a Christological theory of the Eucharist (impanation) using the metaphysics of the incarnation, supporting S8 (incarnation coherence) at the level of conceptual possibility (CS1) via a priori metaphysical analysis (alpha).
- C: The abstract offers a coherent metaphysical account of Eucharistic real presence, supporting special divine presence/action; it also overlaps with incarnation-coherence themes, but primarily concerns sacramental presence.

#### `c7235013ee238bf8` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | I | I | majority | I | a |
| D2 | neutral | pro | NA | unresolved | — | — |

- A: Explores a metaphorical framework's implications for philosophy-of-religion puzzles and religious language; no chain-step thesis defended or opposed, purely exploratory.
- B: The text explores how the theological assumption of divine idealism/determinism solves intra-theistic riddles (such as free will and providence) in the thought of Rabbi Leiner, making it an intra-theistic attribute puzzle study.
- C: The abstract assumes God and claims the dream/story model solves philosophy-of-religion riddles and clarifies religious language, suggesting intra-theistic puzzle-solving rather than evidence for a chain step.

#### `96500bd556cbf82a` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | S2 | M | majority | M | b |
| D2 | neutral | pro | pro | majority | pro | a |
| D3 | NA | CS2 | CS2 | majority | CS2 | a |

- A: Discusses methodology of conceiving God (personal vs. apophatic), rejects both standard objections, and suspends verdict, endorsing pluralism of research programmes instead.
- B: Defends the coherence of personal theism (S2) and alterity theism (S3) by rebutting standard objections against both, showing both are legitimate conceptual frameworks.
- C: The abstract gives a methodological verdict: standard objections between personal and alterity theism fail, leaving both as legitimate philosophical-theology research programmes; the argument appears conceptual.

#### `09537da8126493d3` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | M | majority | M | b |
| D2 | neutral | NA | neutral | majority | neutral | b |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Discusses methodology/purpose of philosophy of religion itself (contemplative vs. guiding roles), not any step thesis; no verdict on God-conclusions offered.
- B: The text focuses on the meta-philosophical purpose of the philosophy of religion, advocating D.Z. Phillips's contemplative approach over argumentative approaches, which lies outside the scope of theistic/atheistic case-making.
- C: The abstract concerns the purpose and method of philosophy of religion, advocating a contemplative Wittgensteinian approach without supporting or opposing any theistic step thesis.

#### `924861649ecbf24e` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S2 | B | S2 | majority | S2 | b |
| D4 | alpha | beta | beta | majority | beta | a |

- A: Argues psychophysical laws and soul thisness are best explained by an intentional agent-creator, supporting an agent-ground; conceptual argument, no empirical premise load-bearing.
- B: The text argues that the existence of souls and psychophysical laws provides a qualitative evidential argument (CS4) for God's existence (B), relying on the empirical observation of mind-body causal interaction (beta).
- C: The abstract offers a qualitative probabilistic design-style argument from souls and psychophysical laws to God as intentional creator; empirical mind-brain connections help carry the inference.

#### `5c6d3904d9518732` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | neutral | neutral | contra | majority | neutral | c |
| D3 | NA | NA | CS2 | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Critiques methodology and scope of philosophy of religion, complaining about focus on God-existence derivations; no step thesis or verdict endorsed.
- B: The text critiques the methodology of contemporary philosophy of religion, specifically its obsession with arguments for and against God's existence, without taking a side on theism itself.
- C: The abstract offers a methodological critique of philosophy of religion’s focus on derivations for or against God’s existence, not an empirical or historical argument about a chain step.

#### `877ec4f5ab18c8b9` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S8 | S5 | S5 | majority | S5 | a |
| D3 | CS2 | CS2 | CS1 | majority | CS2 | c |

- A: Defends coherence of bodily resurrection identity against a duplicate objection via conceptual analogy, purely a priori; rebuts a defeater to resurrection-related doctrine.
- B: Defends the coherence of the general resurrection (S5) against the identity objection, arguing that a dual-period existence intended by God is conceptually coherent (CS2, alpha).
- C: The abstract offers a conceptual defense of the possibility of divine resurrection as a special post-creation act, answering an identity objection without empirical or historical premises.

#### `68e994b35f15323e` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | M | majority | M | b |
| D2 | neutral | NA | neutral | majority | neutral | b |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Explicitly takes no stance on evil's effect on theistic belief; instead examines methodological implications for religious fictionalism, not a step thesis directly.
- B: The article explicitly disclaims taking a stance on theism or the problem of evil's effect on it, focusing instead on the coherence of religious fictionalism, which is out of scope.
- C: The abstract explicitly withholds any verdict on evil’s effect on theism and instead studies a dialectical use of the evil argument against fictionalism, so it is methodological and neutral.

#### `99fa3cbf1908eea8` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | S8 | S5 | unresolved | — | — |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | CS1 | CS1 | majority | CS1 | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Eucharistic Real Presence doctrine is an intra-theistic/sacramental coherence puzzle, not bearing on any chain-step thesis, B, P, or I categories.
- B: Defends the conceptual coherence of the Real Presence of Christ (S8-related Christology) using a metaphysical model of time travel, establishing coherence (CS1) via a priori conceptual analysis (alpha).
- C: The abstract offers a conceptual model showing Eucharistic Real Presence coherent, bearing most directly on special divine presence/action in the world rather than historical revelation or incarnation.

#### `5346f277ae60ce14` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | B | B | majority | B | a |
| D3 | CS2 | CS2 | CS1 | majority | CS2 | c |

- A: Reply-chain critique of probabilistic machinery underlying Plantinga's cumulative case; defends earlier objection, arguing replies fail to rebut prior probabilistic criticisms.
- B: The author defends their critique of Plantinga's probabilistic claims against his replies, arguing that Plantinga's EAAN and theism's logical non-contingency jointly imply theism's necessary falsehood.
- C: The article replies to Plantinga and argues probabilistic/conceptual commitments still imply theism’s necessary falsehood, a direct bundled anti-theism conclusion rather than an empirical case.

#### `7863b2b2e05fb3fa` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | B | B | X | majority | B | c |
| D2 | neutral | pro | NA | unresolved | — | — |
| D3 | NA | CS1 | NA | majority | NA | b |
| D4 | NA | alpha | NA | majority | NA | b |

- A: Argues Christian art gives believers experiential access to God, a bundled religious-experience claim about faith, not asserting God's existence or its probability.
- B: Defends a conceptual model of Christian faith and art as genuine modes of experiencing God (B, flag RE). This is an a priori/conceptual defense of the coherence of this experience (CS1, alpha).
- C: The abstract concerns phenomenology of Christian art and faith, not an argument for God, a chain-step thesis, pragmatic belief, attribute puzzle, or case-making methodology.

#### `004c8a3184da5ff2` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | M | majority | M | b |
| D2 | neutral | NA | pro | unresolved | — | — |
| D3 | NA | NA | CS4 | majority | NA | c |
| D4 | NA | NA | beta | majority | NA | c |

- A: Reflects on philosophical progress generally, citing ontological-argument literature as illustration; no verdict on any step thesis, purely methodological/meta-commentary.
- B: The text argues for general progress in analytic philosophy, using the ontological argument literature merely as an illustration of this progress, making it out of scope for theistic argument analysis.
- C: The text argues that analytic work on ontological arguments shows philosophical progress, a methodological claim about theistic argumentation rather than a direct God-conclusion.

#### `eb8c6195fce7b54e` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | neutral | pro | pro | majority | pro | a |
| D3 | NA | CS1 | CS1 | majority | CS1 | a |

- A: Defends coherence of Kierkegaardian faith regarding Incarnation via Stump's union account; a coherence defense internal to faith/incarnation theology, not a direct pro/contra on incarnation's truth.
- B: Defends the coherence of Kierkegaard's account of the Incarnation against charges of incoherence using Stump's model of divine-human union, making it a CS1 pro-S8 conceptual (alpha) argument.
- C: The abstract defends the coherence of faith centered on the historical Incarnation, primarily a conceptual solution to a faith/history problem, with secondary methodological overtones about evidence.

#### `ca506d1433c426ca` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D3 | CS3 | CS2 | CS2 | majority | CS2 | a |

- A: Defends Plantinga's warrant-based epistemology (proper function, Pandora's Box objection) for belief in God against objections, sustaining the permissibility-without-evidence claim.
- B: Defends Plantinga's proper basicality model against two conceptual objections, thereby supporting the epistemic permissibility of belief in God without propositional evidence.
- C: The article addresses objections to Plantinga’s claim that belief in God can be warranted without evidence, so it most likely rebuts defeaters to bundled God-belief warrant conceptually.

#### `fd34401766fbbd82` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | P | X | majority | X | b |
| D2 | NA | contra | NA | majority | NA | b |

- A: Addresses the nature/definition of religious faith as doxastic venture, not any chain-step thesis, pragmatic grounds, attribute puzzle, or case-methodology.
- B: The text critiques John Bishop's 'doxastic venture' model of pragmatic religious faith, arguing it is too permissive and restrictive, thus failing to provide a satisfactory account.
- C: The abstract evaluates a model of religious faith, not a God-conclusion, chain-step thesis, wager-style pragmatic argument, attribute puzzle, or methodology of theistic case-making.

#### `cf6c7a966fb376fd` (pilot)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | M | M | majority | M | a |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | CS2 | CS2 | majority | CS2 | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Targets an omniscience-impossibility argument, an intra-theistic attribute puzzle excluded from the chain; codes stop after class assignment per Q1 rule for I.
- B: The article critiques a general atheological strategy (specifically Whitcomb's), arguing it is doomed to failure. This methodological critique of arguments against God's existence is a conceptual (alpha) defeater-rebuttal (CS2) supporting theistic case-making (pro).
- C: The article rebuts an atheistic attribute-impossibility strategy and draws a general methodological conclusion about how arguments against God must proceed, using conceptual reasoning.

#### `A01` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D4 | alpha | beta | beta | majority | beta | a |

- A: Presents evidential argument from evil against a perfectly good ultimate, while conceding theists may rationally resist it; net effect on S4 is negative evidential.
- B: The author presents an evidential argument from evil against theism, targeting S4. This positive qualitative evidential claim (CS4) relies on the empirical existence of instances of suffering (beta).
- C: The abstract foregrounds a strong evidential argument from evil for atheism, opposing a perfectly good ultimate; it also discusses theistic defense and friendly atheism.

#### `A04` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D4 | alpha | beta | beta | majority | beta | a |

- A: Argues problem of evil and problem of good are symmetric, undermining grounds for asymmetric confidence in a good (vs evil) ultimate; net effect opposes S4.
- B: The paper presents the evil-god challenge, using the empirical problem of evil to argue against the reasonableness of believing the ultimate is perfectly good (S4).
- C: Using observed evil/good symmetry, the paper argues that evil gives grounds to dismiss an all-good God comparable to grounds against an evil god, directly opposing perfect goodness.

#### `A05` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | pro | contra | contra | majority | contra | a |

- A: Defends the hiddenness argument against objections deemed irrelevant, rebutting defeaters; net effect supports the hiddenness case against divine special action/disclosure.
- B: Defends the atheistic argument from divine hiddenness (S5) by showing that objections to it are irrelevant, yielding a net contra-S5 effect of CS2 strength through conceptual analysis.
- C: The essay defends the divine hiddenness argument by arguing that objections to it are irrelevant, so its net effect opposes divine self-disclosure under S5.

#### `A12` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S2 | S2 | M | majority | S2 | c |
| D4 | alpha | alpha | beta | majority | alpha | c |

- A: Argues fine-tuning inference lacks probative force absent a reference class of universes, undercutting the design inference to an agent-cause.
- B: The text argues that the Fine-Tuning Argument lacks probative force because we cannot obtain statistical data on other universes, undercutting a key design argument (S2) using conceptual/epistemic limits (alpha, CS2).
- C: Critiques fine-tuning/design probability methodology: because universes are not observable samples, expected alternatives cannot be assessed, undercutting design inferences to an agent; M versus S2 is the main uncertainty.

#### `A13` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S2 | S2 | M | majority | S2 | c |
| D3 | CS1 | CS4 | CS1 | majority | CS1 | b |

- A: Purely conceptual paths from necessary being to volition/power/knowledge/goodness; primarily supports agency (S2) though S3/S4 also implicated; exploratory, not evidential.
- B: The paper outlines arguments (CS4, alpha) connecting a necessary being to agency (S2), power (S3), and goodness (S4), making it a multi-step case starting with S2.
- C: The abstract constructs conceptual stage-II paths from a necessary being to volition and divine attributes, chiefly methodological but pro-theistic across S2/S4 candidates.

#### `A14` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | I | B | majority | I | c |
| D2 | NA | NA | contra | majority | NA | c |
| D3 | NA | NA | CS2 | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Concerns coherence of omniscience with perfect freedom in Swinburne's theism, an intra-theistic attribute puzzle; coded I and stopped per procedure.
- B: The paper critiques the coherence of divine omniscience and perfect freedom, which is an intra-theistic attribute puzzle.
- C: The paper presents an internal problem for Swinburne’s argument that God likely exists and rejects responses, using conceptual claims about omniscience and freedom.

#### `A17` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D3 | CS2 | CS1 | CS1 | majority | CS1 | a |

- A: Argues both major Trinitarian frameworks fail to achieve coherence; conceptual critique undercuts trinitarian doctrine, purely a priori analysis, no empirical/historical premise load-bearing.
- B: The text argues that existing Trinitarian models are incoherent and unintelligible, challenging the conceptual coherence of the Trinity (S8) using a priori metaphysical analysis.
- C: The abstract argues existing Trinitarian theories remain inconsistent or unintelligible, directly challenging Trinity coherence under S8; the load-bearing case is mainly conceptual rather than empirical or historical.

#### `A20` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D4 | gamma | NA | gamma | majority | gamma | b |

- A: Surveys sources, traditions, and comparative parallels, offering both apologetic and sceptical views; 'modest results' signals verdict-suspension rather than a directional claim.
- B: The text examines historical evidence for Jesus' resurrection from both apologetic and skeptical viewpoints, offering nuanced 'modest results' rather than a definitive pro or contra verdict.
- C: The abstract concerns resurrection historiography using ancient sources, but reports nuanced modest results and both apologetic and skeptical perspectives without a clear verdict.

---

# Final round — v1.4a consolidated union (n = 89)

2026-07-15 · Owner: adjudication-logger (scripted) · Phase: P1 (pre-P3-freeze), G1 re-gate
Companion: `codebook-v1.md` §9/§12 (v1.4/v1.4a), `validation-battery-v1.md` §B2/§B6.

## F0. Method and zero-human attestation (v1.4a)

**Absolute rule 5 (zero-human).** No human — dk included — judged any item in this round.
Every `majority` / `unresolved` verdict below is a deterministic function of the three
coders' consolidated output files, applied by `scripts/adjudicate.py --dataset all89`
(stdlib-only). The script was re-run and produced byte-identical output twice
(deterministic; the default no-arg output is regression-pinned byte-identical to the
pre-refactor Round-1 script, so the mechanical rule is provably unchanged). dk's only role
remains (i) approving codebook clarification *documents* and (ii) gate approval; dk did not
adjudicate, override, or tie-break any item.

**What changed vs Round 1.** The operative dataset is the **v1.4a consolidated union**: each
coder's per-item code is the per-dimension majority of three independent identical runs
(`scripts/consolidate_runs.py`, codebook §9), the pilot is expanded by one venue-year (IJPR
2015, +34), and D3 is the collapsed 3-level scheme `{DEF, POS, NA}` (codebook v1.4). This round
supersedes Round 1 for the G1 re-gate; Round 1 is retained above for provenance only.

**Inputs (v1.4a, n=89):**

| file | items | role |
|---|---|---|
| `data/coded/all89_{a,b,c}.jsonl` | 89 | consolidated union: RS 2015 (35) + gold (20) + IJPR 2015 (34) |
| `data/coded/stubs_{pilot_rs2015,gold_anchors}_{a,b,c}.jsonl` | 55 | cue-ablation baseline (§B2) — **RS+gold only; no IJPR stubs** |
| `docs/gold-anchors-v1.json` | 20 | gold codes for §F5 flags (D3 legacy-mapped CS1-3→DEF, CS4-5→POS per codebook v1.4 §12) |

`all89_*.jsonl` was verified byte-for-byte equal to the concatenation of the three consolidated
group files (`pilot_rs2015`, `gold_anchors`, `pilot_ijpr2015`); item-ID order equal across A/B/C;
parse_fail = 0; every record carries all four dimensions. Gold items are keyed by anchor_id
(A01–A20). Reproduce: `python3 scripts/adjudicate.py --dataset all89`.

Coders A = Anthropic (claude-opus-4-8, v1.4a pin), B = Google, C = OpenAI (majority adjudicator
seat, §B6). **Decision rule unchanged** (per dimension, per item): unanimous → not a disagreement;
two agree, one differs → `majority`; all three differ → `unresolved` (excluded from primary
analysis; sensitivity bounds downstream, §B6).

## F1. Adjudication summary

- Item-dimension cells: **356** (89 items × 4 dimensions).
- Unanimous (A=B=C): **280** (78.7%). Disagreements: **76** (21.3%) across **30 distinct items**.
- Resolved by majority (2-1): **70**. Unresolved (3-way): **6**.

| dimension | disagreements | majority (2-1) | unresolved (3-way) |
|---|---|---|---|
| D1 step | 23 | 18 | 5 |
| D2 direction | 20 | 19 | 1 |
| D3 strength | 16 | 16 | 0 |
| D4 type | 17 | 17 | 0 |
| **total** | **76** | **70** | **6** |

By group (descriptive): RS 2015 41 disagreement-cells / 15 distinct items / 5 unresolved; gold 14 disagreement-cells / 5 distinct items / 0 unresolved; IJPR 2015 21 disagreement-cells / 10 distinct items / 1 unresolved. Coverage check: 70 + 6 = 76.

## F2. 2-1 resolution matrix (minority coder × dimension)

Cell = number of 2-1 resolutions on that dimension in which the named coder was the lone
dissenter (outvoted 2-to-1). Total = 70.

| minority coder | D1 | D2 | D3 | D4 | row total | share |
|---|---|---|---|---|---|---|
| A (Anthropic) | 9 | 10 | 8 | 6 | **33** | 47.1% |
| B (Google) | 6 | 3 | 3 | 2 | **14** | 20.0% |
| C (OpenAI) | 3 | 6 | 5 | 9 | **23** | 32.9% |
| **column total** | **18** | **19** | **16** | **17** | **70** | |

**Minority-transition cells (minority value → adopted majority value), by coder × dimension.**

| coder | dim | transitions (min→maj : count) |
|---|---|---|
| A | D1 | M->X 3 · M->B 2 · I->M 1 · S1->S2 1 · S3->S2 1 · I->S8 1 |
| A | D2 | NA->pro 4 · neutral->NA 3 · neutral->contra 1 · contra->pro 1 · neutral->pro 1 |
| A | D3 | NA->DEF 5 · DEF->POS 2 · NA->POS 1 |
| A | D4 | NA->alpha 4 · alpha->NA 2 |
| B | D1 | S4->M 2 · B->S2 1 · P->X 1 · B->M 1 · S4->X 1 |
| B | D2 | contra->NA 1 · pro->neutral 1 · pro->NA 1 |
| B | D3 | DEF->NA 3 |
| B | D4 | alpha->NA 2 |
| C | D1 | I->S4 1 · S5->X 1 · B->I 1 |
| C | D2 | NA->pro 2 · pro->contra 1 · contra->neutral 1 · pro->NA 1 · contra->NA 1 |
| C | D3 | NA->DEF 2 · DEF->NA 2 · POS->NA 1 |
| C | D4 | alpha->NA 4 · NA->alpha 3 · gamma->alpha 1 · beta->alpha 1 |

**Read (descriptive, not a verdict).** A is the most frequent minority (33/70, 47%),
spread across all four dimensions; A's dissents cluster on the scope/direction *stop*
(`M→X`, `neutral→NA`, `NA→pro`, `NA→DEF`) — A applies a Q1 stop or a neutral verdict where B/C
code the item in-scope and directional. C (23/70) concentrates on **D4** (9, chiefly `alpha→NA` ×4
and `NA→alpha` ×3) and **D3** (5). B is lightest overall (14/70) and leans to D1 scope. No coder
is a persistent global outlier; the asymmetry is dimension-specific and traced to the boundaries
in §F4/§F7. Expanding to n=89 did not change the qualitative shape of the Round-1 matrix (A the
modal minority on the cascade dimensions).

## F3. Unresolved (3-way splits)

6 cells; excluded from primary analysis. Sensitivity bounds under each candidate
resolution are an analysis-stage task (§B6), not computed here.

| item | group | dim | A | B | C | note |
|---|---|---|---|---|---|---|
| `877ec4f5ab18c8b9` | RS 2015 | D1 | S8 | S7 | S5 | resurrection-identity: S8 vs S7 vs S5 step-locus split |
| `96500bd556cbf82a` | RS 2015 | D1 | M | B | I | personal-vs-alterity theism methodology: M vs B vs I (D1); neutral vs pro vs NA (D2) |
| `96500bd556cbf82a` | RS 2015 | D2 | neutral | pro | NA | personal-vs-alterity theism methodology: M vs B vs I (D1); neutral vs pro vs NA (D2) |
| `99fa3cbf1908eea8` | RS 2015 | D1 | X | S8 | S5 | Eucharistic Real Presence: out-of-scope vs S8 vs S5 |
| `cabd8f6e0c2ae4a5` | RS 2015 | D1 | X | S8 | S5 | Eucharistic/impanation Christology: out-of-scope vs S8 vs S5 |
| `ac22588cd48f3d59` | IJPR 2015 | D1 | S5 | S2 | I | IJPR item: S5 vs S2 vs I step/scope split |

Distribution: D1 ×5, D2 ×1. All 3-way splits sit on D1 (step/scope locus) or the D2 direction that cascades from it; D3 and D4 had zero 3-way splits (their disagreements are all clean 2-1 cascade shadows).

## F4. Recurrence pattern tally

A "pattern" = (dimension, competing value pair) for a 2-1 split. Patterns recurring **≥ 3 times**
qualify for a codebook clarification draft (§F7). Direction shown as the {minority, majority} pair.

| # | dimension | competing values | count | dominant directed transition | minority coders |
|---|---|---|---|---|---|
| P1 | D4 type | NA/alpha | **15** | alpha→NA 8 · NA→alpha 7 | C×7, A×6, B×2 |
| P2 | D3 strength | DEF/NA | **12** | NA→DEF 7 · DEF→NA 5 | A×5, C×4, B×3 |
| P3 | D2 direction | NA/pro | **8** | NA→pro 6 · pro→NA 2 | A×4, C×3, B×1 |
| P4 | D1 step | B/M | **3** | M→B 2 · B→M 1 | A×2, B×1 |
| P5 | D1 step | M/X | **3** | M→X 3 | A×3 |
| P6 | D2 direction | NA/neutral | **3** | neutral→NA 3 | A×3 |

Sub-threshold (2×, logged, no draft): D1 M/S4, D2 NA/contra, D2 contra/neutral, D2 contra/pro, D2 neutral/pro, D3 DEF/POS, D3 NA/POS.

**Structural note.** As in Round 1, the largest patterns are **cascade** disagreements: an upstream
split on relevance/direction (D1 scope `M/X`, `B/M`; D2 `NA/pro`, `NA/neutral`) mechanically
produces the downstream `NA`-vs-scored split on D3 (`DEF/NA` ×12) and D4 (`NA/alpha` ×15). These
are the same NA-cascade and net-effect boundaries that CL-2/CL-3 addressed in v1.3; **they persist
at a reduced-but-nonzero rate after the v1.3/v1.4 clarifications**, which is the key finding of this
round — the residue is a measurement property (coder priors on the scope/neutral boundary), not a
remaining under-specification with an obvious fix. See §F7.

## F5. Gold-conflict flags

Per verification criterion (b): majority resolutions that conflict with a gold anchor code are
flagged and **NOT overridden** — the majority verdict stands (zero-human rule). Gold is **diagnostic
only** (codebook §8; zero headline weight; recognition-stratified). Gold revision is **dk's sole
authority and only as instrument design**. D3 gold codes are legacy-mapped (CS1-3→DEF, CS4-5→POS,
codebook v1.4 §12) before comparison. **6 conflicts across 3 anchors:**

| anchor | dim | majority (adopted) | gold | minority coder | minority value | minority == gold? |
|---|---|---|---|---|---|---|
| A11 | D1 | S2 | S1 | A | S1 | **yes** |
| A13 | D1 | S2 | S3 | A | S3 | **yes** |
| A14 | D1 | I | S3 | C | B | no |
| A14 | D2 | NA | contra | C | contra | **yes** |
| A14 | D3 | NA | DEF | C | DEF | **yes** |
| A14 | D4 | NA | alpha | C | alpha | **yes** |

**Cross-cutting (diagnostic).** In **5 of 6** conflicts the dropped minority coder was the one
matching gold — majority-of-three moved *away* from the diagnostic gold and the lone dissenter was
"right" by gold. Expected under the zero-human design (gold carries zero headline weight and anchors
are memorization-suspect); surfaced for dk's instrument-design review (§B5/§B8), **not acted on**.

- **A14 (omniscience ∧ perfect freedom in Swinburne) — full 4-dimension cascade conflict.** A and B
  both read A14 as an intra-theistic attribute puzzle (`I`) and stop → NA on D2/D3/D4. Gold =
  `S3 / contra / DEF / alpha`. Only C coded it in-scope (`B / contra / DEF / alpha`) and C matches
  gold on D2/D3/D4 (not D1: C said B, gold S3). The 2-vote `I` zeroed the item relative to gold. Same
  A14 pattern flagged in Round 1 — persistent under v1.4a, coupled to the M/I scope boundary and the
  D4 NA cascade (P1). Largest single gold divergence.
- **A11 / A13 (D1).** Majority `S2` where gold `S1` (A11, White fine-tuning) / `S3` (A13, necessary
  being → attributes); in both the lone dissenter (A) matched gold. This is the S1↔S2↔S3
  cosmological/fine-tuning edge boundary. D3 on both now **agrees** with gold after the legacy
  CS→{DEF,POS} map (Round-1's D3 gold conflicts on these were a scoring-notation artifact).

## F6. Cue-ablation stub-congruence audit (§B6 input)

Question (§B6): does the tie-breaker break systematically **toward the stub-predictable (folklore/
topic-cue) code** (§B2)? Stub predictor = mode of the three coders' stub codes for that (item, dim).
`toward_stub` = adopted value == stub mode; `away_stub` = dropped minority value == stub mode;
`uninformative` = stub mode ambiguous or equals neither.

**Coverage caveat (load-bearing).** The cue-ablation stub set exists only for the **55 RS+gold**
items; the **34 IJPR** items have **no stub arm**. Of the 70 2-1 resolutions, **50 are stub-covered
(audited below) and 20 are IJPR with no stub** (excluded from the congruence denominator): D1 5, D2 5, D3 4, D4 6. The audit therefore covers RS+gold only;
IJPR congruence is **not measurable** with the current battery data and is reported as a gap.

**Result (over the 50 stub-covered 2-1 resolutions):**

| dimension | toward_stub | away_stub | uninformative | toward-share* |
|---|---|---|---|---|
| D1 step | 5 | 4 | 4 | 0.56 |
| D2 direction | 6 | 5 | 3 | 0.55 |
| D3 strength | 4 | 4 | 4 | 0.50 |
| D4 type | 6 | 4 | 1 | 0.60 |
| **total** | **21** | **17** | **12** | **0.55** |

\*toward-share = toward / (toward + away), informative resolutions only.

**Support metric (stub-vote count, all 50 stub-covered resolutions).** Adopted value favored
**23**, dropped value favored **20**, tie **7**.

**Read.** Congruence is a **near-even 0.55 toward-share** (21 toward vs 17 away among informative)
with a slim 23-vs-20 stub-vote edge — **no strong systematic break toward folklore**. The
small lean sits on D4 (0.60); D3 is exactly even (0.50). This is *weaker* than Round 1's 0.60 overall
lean, consistent with the D3 collapse and IJPR expansion diluting the topic-cue signal. Reported as
**§B6 audit input**; the confirmatory cross-tab against analysis-predicted cells, the four-estimator
stability, and the tipping-point fraction are analysis-stage tasks (§B6), deferred — they require the
firewalled critical-cell list. No P1 gate turns on this number.

## F7. Codebook clarification drafts — recurrence ≥3 (revision budget EXHAUSTED)

6 patterns recur ≥3× (§F4). Per the agent contract they would each generate a codebook
clarification draft. **However, the formal G1 codebook-revision loop budget (max 2, codebook §9) is
spent**: round 1 = v1.3 (CL-1..CL-5), round 2 = v1.4 (D3 collapse, kill-criterion path). The patterns
below are therefore **not** issued as fresh numbered clarifications. They are logged as **residual,
post-clarification** boundaries and marked **"P3-freeze 전 dk 재량"** — any further edit is dk's sole
discretion as an out-of-loop instrument-design change *before* P3 freeze, weighed against the salami/
over-fitting risk of continued codebook tuning. **Nothing here is applied; the codebook is unchanged.**
After P3 freeze these become P4 analysis limitations (agent contract).

> Firewall note: these name only dimension boundaries, not hypotheses or predicted cells.

### R1 — D4 NA-cascade residual (D4 NA/alpha, 15×)  *(pattern P1; "P3-freeze 전 dk 재량")*
Largest pattern: the `I`/`P`/neutral → D4=`NA` stop-rule cascade vs a literal `alpha`. CL-2 (v1.3) already stated the NA cascade and it measurably shrank the pattern, but coders still split at the *upstream* R3–R6 scope/neutral calls, which propagate here. **No new D4 text would help** — the residue is inherited from the D1/D2 decision, not a D4 rule gap. dk-discretion: none recommended; cascade shadow.

### R2 — D3 NA-cascade residual (D3 DEF/NA, 12×)  *(pattern P2; "P3-freeze 전 dk 재량")*
Same cascade on D3 (`NA↔DEF`): when coders split on whether the item is in-scope/directional, one codes DEF and the other NA. Inherited from D1/D2. The v1.4 collapse to {DEF,POS,NA} removed the CS1/CS2 gradation disputes (Round-1 P9) entirely — good — but the NA boundary is upstream. dk-discretion: none recommended; cascade shadow.

### R3 — D2 net-effect boundary residual (D2 NA/pro, 8×)  *(pattern P3; "P3-freeze 전 dk 재량")*
Coders split on whether a successful coherence-defense / defeater-rebuttal is `pro` (net-effect rule) or `NA`/stop. CL-3 (v1.3) tightened `neutral` to verdict-suspension only; the residual is now the NA-vs-pro call on items an out-of-loop reader would route to a stop. **Genuine upstream root of R1/R2.** dk-discretion candidate IF budget existed: a one-line reaffirmation that a *successful* defense of a step-relevant claim is pro at DEF even under defensive framing — but this restates existing §4-D2 and risks over-fitting the pilot. **Left to dk.**

### R4 — D1 B-vs-M bundled-vs-methodology residual (D1 B/M, 3×)  *(pattern P4; "P3-freeze 전 dk 재량")*
Split between a bundled God-target (`B`) and methodology (`M`) on cumulative-case / atheological-strategy items. Not previously isolated (Round-1 had M/S2, M/X). dk-discretion: monitor; 3× is at threshold and may be pilot-specific. Not drafted.

### R5 — D1 M-vs-X scope routing residual (D1 M/X, 3×)  *(pattern P5; "P3-freeze 전 dk 재량")*
Methodology-vs-out-of-scope on papers *about* how theistic/atheistic arguments should proceed. CL-1 (v1.3) added the M/step/X decision order; 3× residual (all A-minority, A→X). dk-discretion: none recommended; within expected boundary noise post-CL-1.

### R6 — D2 NA-vs-neutral labeling residual (D2 NA/neutral, 3×)  *(pattern P6; "P3-freeze 전 dk 재량")*
Split between coding a verdict-suspension as `neutral` (D2 scored, cascade to D3=NA) vs `NA` (full stop). A codes neutral, others NA. A labeling seam between CL-2 (stop→NA) and CL-3 (neutral=suspension). dk-discretion candidate: a note that pure-mapping/non-liquet takes `neutral` (not `NA`) when D1 is in-scope M, reserving `NA` for the Q1 stop codes. **Left to dk; not drafted.**

**Status of §F7:** none applied; no verdict in §F1–§F6 depends on any of these. The revision loop is
closed; issuing them would be an out-of-budget, dk-only, pre-freeze discretionary edit. Recommended
disposition: **carry R1/R2/R4/R5 as cascade/boundary noise (no edit)** and **flag R3 and R6 to dk as
the only two with a plausible one-line, hypothesis-neutral fix** — for dk to accept or decline before P3.

## F8. Deliverable verification checklist

- **(a) every disagreement has a verdict + record** — 76/76: 70 `majority` + 6 `unresolved`; full
  register in Appendix F; summary §F1; per-item rationales retained.
- **(b) gold-conflict flags** — §F5: 6 conflicts flagged (D3 legacy-mapped), majority verdicts NOT
  overridden, gold unchanged (gold revision = dk-only, instrument-design-only).
- **(c) 2-1 matrix + recurrence tally** — §F2 (minority × dimension × cell) and §F4 (6 patterns ≥3).
- **(d) zero human item-judgment** — attested §F0; verdicts are pure `adjudicate.py --dataset all89`
  output, re-run byte-identical; default no-arg output regression-pinned identical to Round 1.

## Appendix F — full disagreement register (v1.4a, grouped by item)

All 30 items with ≥ 1 disagreement, in dataset order. Each shows the disagreeing dimensions
(A/B/C values, verdict, adopted value, minority coder) and the three coders' one-sentence rationales
(verbatim). Values are the coders' own outputs; the adjudicator only tallied them.

#### `09537da8126493d3` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | X | majority | X | a |
| D2 | neutral | NA | NA | majority | NA | a |

- A: Primary conclusion concerns the aim/method of philosophy of religion itself (contemplative vs. guidance conception), a verdict on case-making methodology; no first-order step thesis is supported or opposed.
- B: The text discusses the metaphilosophy of religion (specifically D.Z. Phillips's contemplative approach) rather than any specific chain-step thesis, theistic/atheistic case-making methodology, or arguments for or against religious belief.
- C: The abstract concerns the purpose and contemplative practice of philosophy of religion, not any chain-step thesis, God-conclusion, pragmatic belief, attribute puzzle, or case-making machinery.

#### `0a3182e07ae1b6cb` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | contra | contra | pro | majority | contra | c |

- A: Explicitly brackets the historical question; raises conceptual concerns about whether any good justifies a perfectly good being orchestrating societal destruction—an objection pressing against divine goodness (S4), carried by a priori analysis.
- B: The text raises conceptual concerns against a proposed theodicy justifying societal destruction, thereby challenging a defense of S4 (divine goodness) using purely philosophical (alpha) analysis.
- C: The abstract treats whether divine permission or orchestration of societal destruction can be morally justified, a problem-of-evil issue bearing on perfect goodness, using conceptual rather than historical premises.

#### `316b879f61c13613` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S4 | S4 | I | majority | S4 | c |
| D2 | pro | pro | NA | majority | pro | c |
| D3 | DEF | DEF | NA | majority | DEF | c |
| D4 | alpha | alpha | NA | majority | alpha | c |

- A: Rebuts Morriston's counterpossible objection to divine command theory, defending the good-ultimate thesis against a defeater; conceptual argument about counterpossibles, net-effect pro-S4.
- B: The authors defend divine command theory against Morriston's counterpossible objection, defending the coherence of theistic morality (S4) against a conceptual challenge using purely a priori metaphysical arguments (alpha).
- C: The abstract defends divine command theory against a counterpossible objection about God’s morally troubling commands, making it an intra-theistic metaethical/coherence dispute rather than evidence for or against a chain-step thesis.

#### `5346f277ae60ce14` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | B | B | majority | B | a |
| D2 | neutral | contra | contra | majority | contra | a |
| D3 | NA | POS | POS | majority | POS | a |

- A: Primary conclusion targets the probability machinery in Plantinga's case-making (a probabilistic blunder and its consequences for his probabilistic claims), taking a verdict on that machinery, not a first-order step thesis; conceptual/probabilistic argumentation.
- B: The author argues that Plantinga's replies fail, concluding that the Evolutionary Argument against Naturalism and theism's logical non-contingency jointly imply theism's necessary falsehood.
- C: The paper rebuts Plantinga’s reply and says his probabilistic commitments still imply theism’s necessary falsehood; net effect is contra bundled theism, via conceptual/probability analysis rather than empirical premises.

#### `5c6d3904d9518732` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | neutral | neutral | contra | majority | neutral | c |
| D3 | NA | NA | DEF | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Primary conclusion is a verdict about how philosophy of religion should be practiced (scope and obsession with existence-derivations), a methodological critique of the case-making itself, not a first-order step thesis.
- B: The text critiques the narrow focus of contemporary philosophy of religion on arguments for and against God's existence, presenting a methodological critique of the discipline rather than defending or opposing any specific step thesis.
- C: The passage gives a methodological complaint against philosophy of religion’s focus on God-existence derivations, not a first-order step thesis; the critique is conceptual and non-empirical.

#### `783821566b91c8c1` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | S4 | M | majority | M | b |

- A: Meta-level dispute about the moral propriety and legitimacy of theodicy as a practice, not a verdict on any first-order step thesis (S4); addresses case-making methodology, so M with no directional import on a chain thesis.
- B: Defends the moral acceptability and comforting function of theodicies against Shearn's critiques, thereby defending the viability of theodicies (S4) against moral objections.
- C: The article defends the moral acceptability and function of theodicy against critique, chiefly as methodology of evil-response rather than a first-order S4 verdict.

#### `7863b2b2e05fb3fa` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | X | S5 | majority | X | c |
| D2 | NA | NA | pro | majority | NA | c |
| D3 | NA | NA | POS | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Claim is about phenomenology of experiencing Christian art differing for believers vs secularists; it neither supports nor opposes any chain-step thesis, God-conclusion, pragmatic grounds, attribute puzzle, or case-making methodology.
- B: The primary conclusion concerns the difference between secular and Christian experiences of art, which does not bear on any chain-step thesis or bundled God-conclusion.
- C: The abstract argues that Christian faith and art involve direct experience of God, bearing most directly on divine self-disclosure rather than a generic evidential argument from experience.

#### `877ec4f5ab18c8b9` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S8 | S7 | S5 | unresolved | — | — |

- A: Rebuts a coherence objection to bodily resurrection identity via conceptual analogy; defensive, purely a priori. Doctrine of resurrection of the dead falls nearest S8's incarnation/trinity doctrinal cluster rather than S7's historiography.
- B: Defends the metaphysical coherence of bodily resurrection against identity objections under physicalism, supporting the possibility of resurrection (S7, also S5) defensively through conceptual analysis.
- C: The abstract rebuts a conceptual objection to God’s ability to resurrect persons as identical, supporting the coherence of special divine action rather than offering historical evidence.

#### `924861649ecbf24e` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S2 | B | S2 | majority | S2 | b |

- A: Argues psychophysical laws connecting souls and brains are most improbable absent an intentional creator; positive evidential support for a purposive agent-ground (S2). Load-bearing premise is the empirical existence of mind-brain causal connections.
- B: The text argues that the empirical existence of psychophysical laws correlating mental and physical events provides positive evidential support for God's existence, making it a positive, empirical argument for a bundled God conclusion.
- C: The abstract presents souls and psychophysical laws as improbable without God, offering positive evidence for a bundled God-conclusion; empirical claims about mind-brain causal connections appear load-bearing.

#### `96500bd556cbf82a` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | B | I | unresolved | — | — |
| D2 | neutral | pro | NA | unresolved | — | — |
| D3 | NA | DEF | NA | majority | NA | b |
| D4 | alpha | alpha | NA | majority | alpha | c |

- A: Primary conclusion assesses case-making viability of two theological research programmes, showing both standard knockdown objections fail; verdict on methodology of the debate, not any first-order step thesis. Conceptual argumentation carries it.
- B: The text addresses an intra-theistic debate concerning the proper conception of God (personal vs. alterity theism), defending the coherence of both models against standard objections.
- C: The abstract evaluates competing theological conceptions of God and their objections, concluding both are legitimate, an intra-theistic conceptual dispute rather than a chain-step argument.

#### `99fa3cbf1908eea8` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | S8 | S5 | unresolved | — | — |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | DEF | DEF | majority | DEF | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Coherence defense of Eucharistic Real Presence via time-travel analogy bears on no chain-step thesis (S1–S8), attribute puzzle, pragmatic ground, or case-making methodology; it is out of scope.
- B: Defends the coherence of the Real Presence of Christ (S8/Christology) using a conceptual model of time-travel and multiple location, making it a pro-directional, defensive (DEF), and a priori (alpha) metaphysical argument.
- C: The article offers a conceptual coherence model for Real Presence, an internal Christian doctrinal puzzle rather than a chain-step thesis about God, revelation, or resurrection.

#### `c7235013ee238bf8` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | X | majority | X | a |
| D2 | neutral | NA | NA | majority | NA | a |
| D4 | alpha | NA | NA | majority | NA | a |

- A: Explores how a 'world-as-God's-dream' assumption reshapes solutions to philosophy-of-religion riddles and religious-language nature—a methodological/framework claim about case-making, not a verdict on any first-order step thesis.
- B: The text explores the conceptual utility of a Hasidic theological assumption for solving unspecified riddles and understanding religious language, without defending or opposing any specific step thesis or named intra-theistic puzzle.
- C: The abstract assumes God for theological analysis and discusses unspecified riddles and religious language, but asserts no verdict on a chain thesis, bundled God argument, pragmatic case, attribute puzzle, or case methodology.

#### `cabd8f6e0c2ae4a5` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | S8 | S5 | unresolved | — | — |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | DEF | DEF | majority | DEF | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Eucharistic real-presence/impanation coherence bears on sacramental metaphysics, not on any chain-step thesis (S1–S8), a bundled God-target, pragmatic grounds, an attribute puzzle, or case-making methodology; out of scope.
- B: The author defends the coherence of Type-S Impanation (a Christological theory of the Eucharist) using the metaphysics of the Incarnation, supporting S8 (incarnation coherence) defensively via a priori metaphysical analysis.
- C: Defends a coherent metaphysical account of Christ’s real Eucharistic presence, a special post-creation divine presence/action; argument is conceptual and objection-rebutting, though it also invokes incarnation themes.

#### `cf6c7a966fb376fd` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | M | M | majority | M | a |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | DEF | DEF | majority | DEF | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Concerns omniscience (an attribute) and how attribute-based disproofs must proceed; primarily an intra-theistic attribute puzzle rather than a chain-step verdict. Methodology angle noted but the target is the omniscience-impossibility puzzle.
- B: The text argues that a general strategy for proving God's non-existence via attribute impossibility is doomed to failure, presenting a methodological, conceptual defense of theism.
- C: The article makes a methodological claim that a broad atheistic strategy from impossible divine attributes fails, using conceptual reasoning rather than empirical or historical premises.

#### `fd34401766fbbd82` (RS 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | P | X | majority | X | b |
| D2 | NA | contra | NA | majority | NA | b |

- A: Critique of a model of the nature of religious faith (doxastic venture); bears on no chain-step thesis, pragmatic wager, attribute puzzle, or case-making methodology—out of scope.
- B: The text critiques John Bishop's 'doxastic venture' model of religious faith, arguing it is unsatisfactory. This targets pragmatic/volitional grounds for belief (P), yielding a contra direction.
- C: The abstract evaluates a model of religious faith, not a chain-step thesis, God-conclusion, wager-style pragmatic argument, attribute puzzle, or methodology of theistic case-making.

#### `3ac4bba14e8e4bf0` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | B | M | majority | M | b |

- A: Primary conclusion proposes a reorganized rationalist atheology framework (seven PSR-based rules) as case-making machinery; the five refutations are illustrative, so verdict targets methodology, net contra to theistic case, purely conceptual.
- B: The text refutes five major arguments for God using logical rules derived from the principle of sufficient reason, presenting an undercutting (defensive) conceptual critique of the bundled theistic thesis.
- C: Although methodological, its verdict is that multiple major arguments for God fail by PSR-derived logical rules, undercutting a bundled God-conclusion without empirical or historical load-bearing premises.

#### `54987374b4cedb6c` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | contra | pro | pro | majority | pro | a |

- A: Author argues an explanatory evidential-evil argument is not immune to skeptical-theist defeaters; reinstating that defeater weakens a contra-S4 argument, netting pro-S4 defensively—wait, net effect favors the goodness thesis.
- B: The author argues that an explanatory argument from evil fails to escape skeptical theism. This defends a skeptical theist defense of S4 against an undercutting attempt, making the net effect pro-S4, defensive, and conceptual (alpha).
- C: By denying that an evidential evil argument evades skeptical theism, the paper defensively undercuts a contra-S4 argument; the reasoning appears conceptual rather than empirical.

#### `5d1bd412166d70ef` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D3 | DEF | POS | POS | majority | POS | a |

- A: Argues divine self-knowledge requires multiple centers of consciousness, grounding a coherent triune psychological model; a conceptual coherence-defense of the trinitarian thesis, carried entirely by a priori argumentation.
- B: The text argues that God's omniscience conceptually entails a multi-personal nature, supporting Trinity coherence (S8) via positive (POS) a priori reasoning (alpha).
- C: The abstract offers a conceptual argument that divine omniscience requires multiple subjective centers, supporting a Trinitarian conception of God rather than merely defending coherence.

#### `5e28c9784692cbe0` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | B | B | majority | B | a |

- A: Critiques the case-making machinery of divine conceptualism—that logic's necessary propositions bridge to 'God exists'—arguing the inference merely renames necessary truth and fails to refer; verdict on the argumentative machinery, carried by conceptual analysis.
- B: The author argues that divine conceptualist arguments for God's existence fail because they merely rename necessary truths and face severe epistemic limitations, undercutting a conceptual argument for a bundled God-conclusion.
- C: The abstract critiques a conceptual bridge from necessary truths to God’s existence, arguing it fails to refer to God rather than giving evidence against God.

#### `612e7d8514a8e807` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | S4 | M | majority | M | b |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Primary conclusion concerns how theoretical and practical responses to evil interact—a verdict on the case-making methodology itself, not on S4's truth. Survey/mapping with no evidential weighing, so D3/D4 NA.
- B: The text analyzes the relationship between theoretical theodicies and practical responses to evil without endorsing a verdict on the problem of evil itself, rendering it neutral on S4.
- C: The abstract treats problem-of-evil/theodicy responses and argues theoretical and practical approaches can interact to yield a more comprehensive reply, defending rather than evidentially proving divine goodness.

#### `8e6122ca60308a49` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D2 | neutral | pro | neutral | majority | neutral | b |
| D3 | NA | DEF | NA | majority | NA | b |
| D4 | NA | alpha | NA | majority | NA | b |

- A: Primary conclusion concerns case-making machinery itself (presumption of atheism, epistemic justification of atheism), not a first-order step thesis; verdict-orientation unclear from thin abstract, coded neutral pending.
- B: The text provides a methodological assessment of a defense of New Atheism and discusses the presumption of atheism without asserting a definitive first-order verdict, making it a neutral methodological item.
- C: The abstract concerns assessment of atheistic argumentation and epistemic presumption, but gives no clear verdict on any step thesis or machinery beyond critical discussion.

#### `ac22588cd48f3d59` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S5 | S2 | I | unresolved | — | — |
| D2 | pro | pro | NA | majority | pro | c |
| D3 | DEF | DEF | NA | majority | DEF | c |
| D4 | alpha | alpha | NA | majority | alpha | c |

- A: Rebuts objection that chance/randomness contradicts divine providence/sovereignty; shows theistic conceptions coherently accommodate chance—a conceptual defeater-rebuttal defending God's special action/providence (S5), net pro via reply-chain.
- B: Defends the compatibility of divine agency/providence with a chancy world against cosmological and evolutionary objections, arguing that various models of theism can conceptually account for randomness.
- C: The abstract addresses coherence of divine providence/omniscience/sovereignty with chance and randomness, an intra-theistic attribute puzzle rather than a chain-step argument.

#### `ba177a99d426ddc9` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D4 | alpha | alpha | gamma | majority | alpha | c |

- A: Defends Berkeley's proof by reinterpreting its conclusion as a powerful God whose agency pervades nature (S2, agent-ground); rebuts the overreach objection—net pro, defensive, conceptual. MULTI: possibly M (interpretive) but yields first-order verdict.
- B: The author defends Berkeley's argument for a powerful, pervasive agent (S2) against the objection of overreaching, showing the limited proof succeeds (DEF). The underlying argument is metaphysical (alpha).
- C: The abstract defends Berkeley’s proof as establishing only a powerful, pervasive divine agent, rebutting an overreach objection; its support turns on interpreting Berkeley’s texts rather than new empirical evidence.

#### `d7dcc5ffc1f76535` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | M | X | X | majority | X | a |
| D2 | neutral | NA | NA | majority | NA | a |
| D4 | alpha | NA | NA | majority | NA | a |

- A: Primary conclusion is a verdict about the method of philosophy of religion—whether a contemplative philosopher may deploy the superstition/genuine-religion distinction—not any first-order step thesis; conceptual argumentation carries it.
- B: The text discusses Wittgensteinian methodology regarding the conceptual distinction between genuine religion and superstition, which does not bear on any chain-step thesis, bundled God-conclusion, or the methodology of theistic/atheistic case-making.
- C: The abstract analyzes Phillips’s contemplative use of “superstition” to classify religious practices, not any chain-step thesis, bundled God argument, pragmatic wager, attribute puzzle, or case-making methodology.

#### `ebd44375f93052cf` (IJPR 2015)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | X | S4 | X | majority | X | b |
| D2 | NA | pro | NA | majority | NA | b |
| D3 | NA | DEF | NA | majority | NA | b |
| D4 | NA | alpha | NA | majority | NA | b |

- A: Debate over the escapist doctrine of hell is an intra-theistic doctrinal/attribute dispute bearing on no chain-step thesis (S1-S8), pragmatic ground, or case-making methodology; out of scope.
- B: The authors defend the escapist model of hell against Matheson's critique, thereby defending the compatibility of hell with God's perfect goodness (S4) using purely conceptual, defensive arguments.
- C: The abstract only says it defends an escapist theory of hell against critique; it does not assert a verdict on any listed chain-step thesis or machinery.

#### `A11` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S1 | S2 | S2 | majority | S2 | a |
| D2 | neutral | pro | pro | majority | pro | a |
| D3 | NA | DEF | DEF | majority | DEF | a |

- A: Critiques the fine-tuning-to-many-universes inference on probabilistic grounds; neither affirms nor denies a bare cause (S1) or designer (S2), so net effect on step thesis is neutral. Load-bearing premise is conceptual/probabilistic.
- B: The author argues that fine-tuning does not support the multiverse hypothesis, thereby defending the teleological argument (S2) against a key rival explanation. This is a conceptual, defensive argument.
- C: Critiques multiverse as an explanation for fine-tuning, thereby defensively aiding the design inference to an agent; the argument turns on conceptual probability/indexical reasoning rather than new empirical evidence.

#### `A12` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D4 | alpha | alpha | beta | majority | alpha | c |

- A: Undercuts the design inference to a designer-agent by denying we can assign probabilities across universes; a conceptual objection to the pro-S2 argument, no positive counter-evidence, no empirical premise load-bearing.
- B: The text presents an undercutting methodological critique of the Fine-Tuning Argument (S2), arguing we lack the statistical basis to make probability claims about cosmic constants, rendering the design conclusion unsupported.
- C: The abstract offers a methodological undercutting of fine-tuning design arguments: lacking observable universes, their probabilistic expectations lack force; this negatively affects design-argument case-making.

#### `A13` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | S3 | S2 | S2 | majority | S2 | a |
| D3 | DEF | POS | POS | majority | POS | a |

- A: Argues conceptual paths from a necessary being to theistic properties (volition, power, knowledge, goodness), supporting stage-II identification of the ultimate as a se; conceptual, defensive. MULTI: could touch S2/S4.
- B: The author proposes positive, a priori arguments deriving the bundled attributes of God (volition, power, knowledge, goodness) from a necessary being, representing Stage II of the cosmological argument.
- C: The abstract offers conceptual paths from a necessary being to theistic properties, especially volition; it also mentions goodness, making S2 primary but with credible S4 overlap.

#### `A14` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | I | B | majority | I | c |
| D2 | NA | NA | contra | majority | NA | c |
| D3 | NA | NA | DEF | majority | NA | c |
| D4 | NA | NA | alpha | majority | NA | c |

- A: Turns on the compatibility of omniscience and perfect freedom—an intra-theistic attribute puzzle (I); though framed as damaging Swinburne's cumulative case, the load-bearing issue is the attribute tension itself.
- B: The text focuses on a conflict between omniscience and perfect freedom, which constitutes an intra-theistic attribute puzzle.
- C: The paper raises and defends a problem for Swinburne’s argument that God likely exists, undercutting a bundled God-argument via conceptual attribute analysis rather than empirical evidence.

#### `A18` (gold)

| dim | A | B | C | verdict | resolved | minority |
|---|---|---|---|---|---|---|
| D1 | I | S8 | S8 | majority | S8 | a |
| D2 | NA | pro | pro | majority | pro | a |
| D3 | NA | DEF | DEF | majority | DEF | a |
| D4 | NA | alpha | alpha | majority | alpha | a |

- A: Intra-theistic attribute puzzle: coherence of the Trinity (one being vs. three), addressed via analogy to material constitution; this is an excluded attribute-puzzle, so stop after D1=I.
- B: The paper defends the coherence of the Trinity (S8) by applying a metaphysical solution from material constitution, making it a defensive, a priori argument.
- C: The abstract offers a conceptual solution to the apparent incoherence of the Trinity, supporting S8 defensively through metaphysical analogy with material constitution.

---

*End of Final round (v1.4a, n=89). Round 1 (raw arm, 55 items) is preserved above.*
