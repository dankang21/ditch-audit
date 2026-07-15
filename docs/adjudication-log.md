# ditch-audit — Adjudication Log (P1, raw arm)

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

