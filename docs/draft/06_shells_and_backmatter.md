# Draft — §5 Results (preregistered shell), §6 Robustness, §8 Objections & replies, §9 What the map licenses, back matter

Draft status: outcome-blind shell, authored before any P4/P5 data exist. Every empirical cell
is marked [TO BE FILLED AT P5]. Decision rules are quoted verbatim from the frozen analysis
plan (analysis-plan-v1.md, v1.1) and may not be reworded at fill time. §7 (formal appendix) is
drafted separately.

## 5. Results

This section is written, in its entirety, before the confirmatory data exist. Its structure,
table shells, decision rules, and reporting order are fixed by the preregistered analysis plan;
at P5 the shells are filled and nothing else changes. Two constraints govern everything below.
First, the primary confirmatory estimand is the post-2008 population (the stratum on which the
corpus gate certified 92.8% abstract coverage); whole-window (2004–2024) estimates are a
preregistered extension carrying their own gate (§5.5). Second, all confirmatory verdicts are
instrument-relative: the registered sentence form is "H1 [H2] supported, as measured by the
frozen, preregistered multi-family LLM instrument," and unqualified "the law holds" phrasing is
barred from the abstract and conclusions.

### 5.1 Gate-chain status (reported first)

No headline estimate is interpreted before the confirmatory gate chain is reported. A result
may be reported as confirmatory only if all ten items hold; otherwise the run degrades to a
descriptive map. The chain is the exhaustive registry of blocking conditions — no block exists
outside it.

| # | Gate item (plan §2.4) | Status |
|---|---|---|
| 1 | P4 reliability checkpoint (dual statistic, n = 150) | [TO BE FILLED AT P5] |
| 2 | B2 text-driven stratum retention | [TO BE FILLED AT P5] |
| 3 | B3 vaulted-half synthetic accuracy ≥ frozen floors | [TO BE FILLED AT P5] |
| 4 | B3-dis′ coding-contamination check | [TO BE FILLED AT P5] |
| 5 | B6 estimator stability (directional effects only) | [TO BE FILLED AT P5] |
| 6 | B8 analysis-critical cell floors (incl. n ≥ 15 at analysis time) | [TO BE FILLED AT P5] |
| 7 | B5-strat sign persistence, unrecognized stratum (where evaluable) | [TO BE FILLED AT P5] |
| 8 | Adversarial folklore-flip survival (25% fraction) | [TO BE FILLED AT P5] |
| 9 | Missingness criteria (whole-window extension claims only) | [TO BE FILLED AT P5] |
| 10 | Hypothesis-specific decision rule met | [TO BE FILLED AT P5] |

Failure of item 1 halts P4 entirely; failure of 2–5 blocks all confirmatory claims; failure of
6–8 blocks the affected hypothesis; failure of 9 blocks only the whole-window extension. All
component results, including failures, are published (battery §B10).

### 5.2 H1 — type–direction law

Population: DEN-H1 (mainstream-venue T1∪T2, S-coded, POS-strength items), post-2008 primary.

| D2 direction | D4 = α | D4 = β∪γ | Total |
|---|---|---|---|
| pro | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| contra | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

OR_H1 with Woolf 95% CI: [TO BE FILLED AT P5]. Fisher exact p: [TO BE FILLED AT P5].
Registered prediction: OR_H1 ≥ 3.

Preregistered decision semantics, quoted verbatim from the frozen plan (§2.2):

| Outcome | Verdict |
|---|---|
| 95% CI lower bound > 1 **and** point OR ≥ 3 | H1 supported at registered magnitude |
| 95% CI lower bound > 1 and 1 < point OR < 3 | H1 directionally supported, registered magnitude not met (reported as such; no re-framing) |
| 95% CI includes 1, or point OR ≤ 1 | **H1 null** (kill-criterion input) |

Verdict returned by the frozen rule: [TO BE FILLED AT P5].

### 5.3 H2 — venue topography

Population: DEN-H2 (tiers T1∪T2 and T3), post-2008 primary. The 2×2×2 shell:

| Tier | Direction | POS | DEF |
|---|---|---|---|
| T3 | pro | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| T3 | contra | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| T1∪T2 | pro | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| T1∪T2 | contra | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

OR_pro: [TO BE FILLED AT P5] · OR_contra: [TO BE FILLED AT P5] · ROR with 95% CI:
[TO BE FILLED AT P5]. Registered predictions: (i) OR_pro > 1; (ii) OR_contra ≈ 1 or < 1;
(iii) ROR > 1.

Preregistered decision semantics, quoted verbatim from the frozen plan (§2.3):

| Outcome | Verdict |
|---|---|
| LCL(OR_pro) > 1 **and** LCL(ROR) > 1 | H2 supported |
| LCL(OR_pro) > 1 but ROR CI includes 1 | H2 partially supported (pro-shift real, asymmetry not established) — does not count as "supported" for kill-criterion purposes |
| otherwise | **H2 null** |
| contra-control, **evaluable** (both contra tier-cells at adjudicated n ≥ 15): OR_contra CI includes 1 or entirely < 1 | contra-control prediction met (scored separately) |
| contra-control **not evaluable** (either contra tier-cell n < 15) | reported as "not evaluable" — never as "met" |

An H2 confirmatory verdict additionally requires every H2 analysis-critical cell at adjudicated
n ≥ 15, and no confirmatory ROR may rest on a Haldane-corrected analysis-critical cell. If the
registered pre-freeze ROR power computation fell below .5, H2's confirmatory element is the
re-scoped OR_pro test, and this subsection reports against the re-scoped element as registered.
Verdict returned by the frozen rule: [TO BE FILLED AT P5].

### 5.4 Estimator battery

Headline effects under five preregistered estimators (E4 = majority-of-three is primary).
Confirmatory stability — sign stability, CI intersection with E4, and per-family OR ratio in
[0.5, 2] — applies to the directional effects only (OR_H1, OR_pro, ROR); OR_contra is exempt
because it is predicted ≈ 1, and is published descriptively.

| Estimator | OR_H1 (95% CI) | OR_pro (95% CI) | OR_contra (95% CI) | ROR (95% CI) |
|---|---|---|---|---|
| E0 unanimous-only | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| E1 coder A only | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| E2 coder B only | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| E3 coder C only | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| E4 majority (primary) | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

Alternative-seat co-analysis (adjudicator = A): [TO BE FILLED AT P5]. Frozen divergence rule: if
the two seatings yield different verdicts on any hypothesis, confirmatory language for that
hypothesis is withdrawn.

### 5.5 Missingness and estimand sensitivity

The pre-2008 stratum (672 items; 462 missing abstracts) is structural missingness and is
modeled, not hidden. Three preregistered deliverables:

Era×venue bias table — rows = venue, columns = era (2004–2007, 2008–2024); cells = item count,
abstract coverage, and abstract-free covariate profiles (article type, frozen-keyword topic
profile, page count): [TO BE FILLED AT P5].

Tipping-point statistics — minimum number of missing items that overturns each decision rule
under adversarial allocation over all free margins:

| Hypothesis | TP_pos | UCL comparator (POS) | TP_free | UCL comparator (in-chain) |
|---|---|---|---|---|
| H1 | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| H2 | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

Anchored scenario envelope (M1 all-pro / M2 all-contra / M3 anchored-proportional, anchor =
checkpoint-tranche adjudicated distributions): [TO BE FILLED AT P5]. A whole-window extension
claim requires the decision rule met on the whole-window estimate, survival under M3, and both
tipping-point margins exceeding their UCL comparators. The post-2008 primary claim does not
depend on any row of this subsection.

### 5.6 Descriptive step-status map (non-confirmatory)

Computed step status per step over T1∪T2 within window, by the frozen ordered decision list —
(1) contested: both directions ≥ k POS items; (2) headwind: exactly one direction ≥ k POS and
the opposing direction zero POS; (3) frozen: no POS either side in the trailing 10 years;
(4) mixed/sparse: residual — reported at k ∈ {2, 3, 5}:

| Step | Qualitative prior (Table 1, under test) | k = 2 | k = 3 | k = 5 |
|---|---|---|---|---|
| S1 | contested | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S2 | contested | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S3 | contested/frozen | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S4 | headwind | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S5 | strong headwind | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S6 | headwind/near-frozen | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S7 | strong headwind | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| S8 | defensive | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

The "qualitative prior" column restates Table 1's status verdicts for what they are: the
designers' pre-audit qualitative reading, which the computation either reproduces or corrects.
These priors are demonstrably correctable, because the instrument has already corrected its
designers twice during construction. In the A11 episode, the act of gold-coding caught a
designer mis-shelving (an item rebutting the multiverse rejoinder to fine-tuning had been filed
in the contra column; the functional-direction rule now codifies the correction). In the gold
re-adjudication episode, unanimous three-family contradictions of three gold codes triggered a
designer re-adjudication from the sanitized text alone, which found that the designer had coded
two arguments' reputations rather than the papers' abstracts — the very memorization failure
mode the battery guards against in the coders, manifest in the designer; the coders' "misses"
were correct readings, and the gold codes were revised. The prior column above therefore
carries no evidentiary weight in this paper; the computed columns do.

Also reported here, all [TO BE FILLED AT P5]: per-step direction × strength × type maps;
venue-tier topography maps; B-prevalence (input to §7); the S6 scarcity check; flag-class
tallies; per-cell unresolved rates; the published 2-1 adjudication matrix.

### 5.7 Interpretive frames — four preregistered outcome scenarios

The four possible confirmatory outcomes are stated here with equal standing, before the data
exist, so that no frame can be selected after the fact.

Scenario A (H1 and H2 both supported). The type–direction law and the venue topography both
hold as measured by the frozen instrument. The paper's discussion proceeds on both regularities;
the implications-for-cumulative-cases section draws on both. No stronger language than the
instrument-relative sentence form is licensed.

Scenario B (H1 supported, H2 not). The type–direction law holds; venue topography is null or
unestablished. The discussion is confined to the epistemic-type asymmetry; every topographic
claim in the framing is withdrawn, and the H2 null is reported with its full estimator and
sensitivity envelope, not explained away.

Scenario C (H2 supported, H1 not). Venue topography holds; the type–direction law is null or
unestablished. The discussion is confined to venue structure; the H1 null is reported with its
full envelope, and no type-asymmetry language survives anywhere in the paper.

Scenario D (H1 and H2 both null). The preregistered kill criterion executes: no journal
submission; the project downgrades to a descriptive-map preprint plus essay. No salami-slicing;
no post-hoc hypothesis swaps. The descriptive map (§5.6) and the full battery results are
published regardless — a two-null outcome is a finding about the literature's structure and is
reported as such.

## 6. Robustness (shell)

All items in this section are non-confirmatory and are published in full, whatever they show.

- R1 — alternative partitions. Headline effects recomputed at the 7-step grain (S7+S8 merged),
  the 10-step grain (S3 and S4 split; supplementary coding pass under a frozen build-variant
  prompt), and the liberal-target variant (S7 dropped). Invariance claim requires the decision
  rules re-met across all admissible grains; per-grain divergences reported.
  [TO BE FILLED AT P5]
- R2 — F&P tier flip. H2 recomputed with Faith & Philosophy assigned T3; both assignments
  published; the frozen tier table is primary. [TO BE FILLED AT P5]
- R3 — dominant-author exclusion. Items by Swinburne, Plantinga, Draper, Oppy dropped
  (metadata join, post-coding); H1/H2 recomputed. [TO BE FILLED AT P5]
- R4 — time split. 2004–2013 vs 2014–2024, plus the 2008 era boundary; topography per window.
  [TO BE FILLED AT P5]
- R5 — citation-weighted rerun. Weights = log(1 + citations), single frozen snapshot;
  robustness-only by preregistered fiat. [TO BE FILLED AT P5]
- B7a — reversed-default deletion test. D4 re-derived under reversed tie-break polarity;
  tie-break-decided fraction reported; H1 under both polarities. [TO BE FILLED AT P5]
- B7b — strata monitors and the metadata-only prior-ceiling baseline. [TO BE FILLED AT P5]

Mirror audit (exploratory appendix, preregistered for the honesty rule). A three-step
naturalism mini-chain — N1 cosmogenesis/brute-fact viability, N2 naturalistic fine-tuning
response, N3 naturalistic account of consciousness — coded over the same window with the same
coder families and blinding, using a mirror build variant of the frozen codebook, capped at
roughly 200 items. Published whatever it shows, including a naturalist a-priori zone if one is
present. No confirmatory status.

| Mirror step | Direction × strength × type map | Notes |
|---|---|---|
| N1 | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| N2 | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |
| N3 | [TO BE FILLED AT P5] | [TO BE FILLED AT P5] |

## 8. Objections and replies

O1 — the grain objection: "eight is arbitrary." The integer is grain-relative and the paper
says so. The individuation criterion (§2) admits a step only where a witness exists — an extant
scholarly position accepting all prior steps and rejecting that one — with a dedicated
disputing literature, which ties the partition to dialectically real joints rather than to the
analyst's taste. The formal section (§7) shows that the burden multiset is invariant under
re-partition, and R1 recomputes both hypotheses at the 7-step, 10-step, and liberal-target
grains. The published claim is not "there are exactly eight steps"; it is that the invariants
under study are not artifacts of any admissible grain choice — a claim R1 tests rather than
asserts.

O2 — the Thomist entailment objection: "there is no gap; the attributes follow from pure
actuality, so S3–S4 are not independent steps." The entailment claim is itself a contested
step: witnesses who reject it exist within theism (Hartshorne's dipolar theism; the
classical-versus-personalist disputes), which is precisely the witness criterion firing.
Operationally, entailment arguments are coded as pro-direction a-priori items at the step whose
thesis they support; they enter the map as data. An entailment claim can win its literature; it
cannot dissolve a cell whose boundary a witness certifies. Pruss's own framing concedes the gap
as the cosmological argument's "final difficulty."

O3 — "peer review is not truth." Conceded in advance, and built into the claim structure: H1
and H2 are claims about the structure of the published record, not about any step's truth or
about what ideal inquiry would conclude. The audit measures what the literature does, not
whether it is right to do it. The related gatekeeping variant — "mainstream venues are biased
against theism, so any venue pattern measures bias" — meets the composition reversal: the
specialist subfield is majority-theist (roughly 72% of philosophy-of-religion specialists
accept or lean toward theism in the PhilPapers survey), and mainstream specialist editors and
referees are drawn from that pool, so a hostile-gatekeeping explanation of a pro-side migration
pattern would require the gatekeepers to be hostile to their own majority position. Field
composition biases against H2, making the design conservative on that axis — a point about the
test's direction of stringency, not about its outcome.

O4 — the asymmetry objection: "run it on naturalism." We do, within budget: the mirror audit
(§6) codes a three-step naturalism mini-chain with the same instrument architecture, the same
families, and the same blinding, and its results are published under an unconditional honesty
rule — including a naturalist a-priori zone if one is present. Naturalism is a low-conjunction
target, which is itself part of what the mirror quantifies: conjunctive specificity is a
measurable property, not an accusation.

O5 — hostile-prior scheme design: "the partition was built by someone expecting a particular
topography." Three replies. First, preregistration: hypotheses, codebook, thresholds,
denominators, decision rules, and failure consequences are frozen before the confirmatory data
exist, and the frozen gate chain — not the designers — decides what may be called confirmatory.
Second, the witness criterion is side-neutral: the witness list includes theists rejecting
steps (Hartshorne, Lapide, Wiles, open theism), so the partition is certified by the field's
own internal dissent, not by the designer's priors. Third, the record shows the instrument
overruling its designers where they were wrong (the A11 and gold re-adjudication episodes,
§5.6), and the design treats designer error as a measurable, correctable event rather than an
unexaminable background assumption.

## 9. What the map licenses — and what it does not

This paper produces a map of the published dialectic: which steps of the chain are disputed, in
which direction, at what claim strength, on what kind of evidence, in which venues. The
following claims are licensed by such a map, conditional on the gate chain: claims about the
distribution of argument types over directions in the published record; claims about the
distribution of claim strengths over venue tiers; descriptive claims about each step's computed
dispute status under the frozen thresholds. All of them in instrument-relative form: "as
measured by the frozen, preregistered multi-family LLM instrument."

The following are not licensed, and the paper does not assert them.

Not first-order atheology. The audit takes no position on the truth of any step — not S1's,
not S7's, not any other's. A step's "headwind" status, if computed, is a fact about the
published record's structure, not a verdict on the step; a literature can be one-sided and
wrong. Nothing in the map is evidence that theism is false.

Not an irrationality claim. Permissibility-type warrant claims are orthogonal to the audited
dimensions; the map says nothing about whether belief in any step, or in the conjunction, can
be warranted without propositional evidence. A reader who holds a step on such grounds will
find that stance recorded in the map, not refuted by it.

Not a suppression or censorship claim. The corpus is the published record. Nothing here
supports inferences about submission flows, desk rejections, or editorial intent; the
gatekeeping discussion (§8, O3) concerns what could explain a published pattern, not what
happens to unpublished manuscripts.

Not an importance ranking. Citation weight measures fashion, not truth; it enters only as a
robustness rerun (R5) and never as a primary analysis.

Not human-equivalent annotation, and not ground truth. The instrument's accuracy on the real
corpus distribution is formally unidentified — every criterion item is either famous-real or
synthetic — and the battery bounds the identifiable artifact classes (memorization, shared
training folklore, register leakage, drift, majority-vote error-laundering) without closing
that gap. A folklore component below the battery's detection floor cannot be excluded; this is
the design's principal limitation and is stated as such wherever a verdict is reported.

What remains is exactly what the title claims: a measurement of the ditch as a property of the
literature. Whether the ditch can be crossed is a question the map locates but does not answer.

## Back matter

### AI-use disclosure

All corpus coding in this study was performed by large language models, with zero human
item-coding: no human — including the authors — coded, adjudicated, or validated any item. The
human contribution was confined to instrument design: codebook authorship, synthetic-criterion
specification and sign-off, and phase-gate approvals. The instrument is a fixed, preregistered,
multi-family ensemble — coder A (Anthropic), coder B (Google), coder C (OpenAI, adjudicator
seat assigned by a preregistered rule), a mandatory open-weights archival coder D, and an
open-weights generator/launderer E structurally barred from search — bound by a role-exclusivity
matrix and pinned to dated snapshots in the OSF manifest. Disagreements were resolved by
three-family majority vote; three-way splits were recorded as unresolved and handled by
preregistered sensitivity bounds. The paper accordingly claims measurement by this instrument,
not human-equivalent annotation, and the abstract discloses this in its own voice.

Two further disclosures. First, instrument selection at pilot: the pilot reliability estimate
that gated the instrument is a selected estimate — it followed five sequential codebook
revisions under an optional-stopping structure — and for that reason the design treats the
pilot gate as conditional on an independent confirmatory reliability checkpoint on fresh items
at the start of the full run, whose failure halts coding entirely. Second, the full design
trajectory is public: the versioned codebook with changelog, the adjudication logs (including
the episodes in which the coders corrected the designers' gold codes), the decision register
with every designer judgment call and its recorded resolution, the battery results including
failures, and the API call logs that make the no-contact claims verifiable. Prose drafting was
assisted by an LLM (Claude); all analysis code is stdlib-only Python, hashed in the freeze
manifest. Final disclosure wording follows the target venue's policy at submission.

### Data and code availability

The audit package (OSF + repository) contains: all analysis and adjudication code with hashes
and fixed seeds; the frozen codebook, prompts, battery, and analysis plan; item-level coded
data and all aggregate tables; the full battery results including failed components; the
adjudication and cost logs. Copyrighted abstracts are not republished: the raw and sanitized
text corpora are excluded from the public package, and the paper reports codes and aggregates
only, with item identifiers sufficient to relocate every source in the published record.
Because API-served models retire, one coder (D) is open-weights with weights, prompts, and
harness archived, so that the instrument supports re-execution — not merely re-inspection — of
the coding run after endpoint retirement; the availability statement in the published version
states this distinction explicitly.
