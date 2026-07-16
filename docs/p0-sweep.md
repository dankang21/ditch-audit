# ditch-audit — P0 Prior-Art Sweep · G0 Gate Report

2026-07-14 · Executor: Claude (web sweep) · Reviewer: dk
**Verdict: G0 PASS** — no substantially overlapping study found. The lane "literature-level structural measurement of the theism chain (step × direction × claim strength × epistemic type × venue)" is unoccupied. Proceed to P1.

---

## 1. Probes executed (7)

| # | Query family | Yield |
|---|---|---|
| Q1 | "ramified natural theology" | Pro-side program confirmed (Swinburne coinage; Holder, Routledge 2021; Gauch, Phil. Christi 2013; SEP coverage). Constructive project, not an audit. |
| Q2 | "gap problem" / Stage II | Pruss naming; Rasmussen (IJPR 2009); **Ocampo (IJPR 2024)** — formalized systematization of Stage-II strategies. Single segment (S1→S3), pro-side argument mapping, no corpus. |
| Q3 | Bibliometrics of philosophy of religion | Bibliometric work exists for religion-and-health and for religious studies as a discipline; nothing on PoR argumentative structure. |
| Q4 | Topic modeling / corpus studies of philosophy | **Genre precedent found:** Bystranowski, Dranseika & Żuradzki, "Half a century of bioethics and philosophy of medicine: a topic-modeling study," *Bioethics* (2022) — 19,488 texts, 7 field journals. Topics, not claims; different field. |
| Q5 | "dwindling probabilities" | Exchange fuller than documented: Plantinga (WCB 2000) → Swinburne (F&P 2004) → McGrew (Phil. Christi 2004) → Plantinga reply (2004; partial concession reported) → McGrew & McGrew (Phil. Christi 8(1), 2006) → Nickel (De Gruyter 2015). **New Tier-A formal neighbor:** Roche & Shogenji, "Dwindling Confirmation," *Philosophy of Science* 81(1) (2014). No meta-study. |
| Q6 | De Cruz / empirical studies of philosophers of religion | **Person-level empirical program exists:** De Cruz (Episteme 14(1), 2017 — argument-strength ratings track prior belief; 8 pro / 8 contra arguments); De Cruz & De Smedt (Bloomsbury 2016 — experimental evaluation of natural-theology arguments); De Cruz (Res Philosophica 2018 — qualitative, n=151, selection-bias evidence). Measures *people*, not the literature. Title correction logged: Draper & Nichols, "Diagnosing cognitive biases in philosophy of religion," Monist 96(3): 420–444. |
| Q7 | "Lessing's ditch" formal/empirical | Kierkegaard-scholarship treatments only (e.g., the "modal gap / three ditches" line). No formal or empirical operationalization. |

## 2. Nearest-neighbor delta table

| Neighbor | What it does | What it does not do (= our delta) |
|---|---|---|
| Ramified natural theology (Swinburne/Holder/Gauch) | Constructs the pro-side cumulative case bare theism → Christian doctrine | Does not individuate steps neutrally, audit venues, or measure the record |
| Gap-problem literature incl. Ocampo (IJPR 2024) | Maps/formalizes Stage-II bridging strategies | One segment only; argument mapping, not corpus measurement |
| Dwindling-probabilities exchange + Roche–Shogenji (2014) | Formal results on confirmation transmission along chains | No partition-adjudication criterion; no empirical audit; our §7 concerns burden *counting* under re-partition, not confirmation *transmission* |
| De Cruz program (2016–2018) | Measures philosophers (surveys, experiments): belief–evaluation correlation, selection bias | Measures persons, not the literature's claim structure |
| Draper & Nichols (Monist 2013) | Diagnoses field-level cognitive bias | Diagnosis + recommendations; no coded corpus |
| PhilPapers surveys (Bourget & Chalmers 2014) | Field composition (~72% theism among PoR specialists) | Composition, not content |
| Bystranowski et al. (Bioethics 2022) | Corpus/topic-model study of a philosophy field by its own journals | Different field; topics, not claim strength/direction/epistemic type |

One-sentence differentiation for the paper's §1: existing empirical work measures the *believers* (De Cruz program) or the *field's composition and biases* (surveys; Draper–Nichols); no prior work measures the *literature's argumentative structure*.

## 3. Incorporated into outline v0.2 (edit log)

1. Header: decisions D-1..D-5 locked (defaults); G0 PASS recorded.
2. §2/§1-note: differentiation sentence (person-level vs literature-level measurement).
3. §6 T-4: De Cruz composition + selection-bias data added (strengthens the gatekeeping reversal: composition is prior to and independent of gatekeeping).
4. §7: Roche & Shogenji (2014) added as must-cite formal neighbor; fuller exchange sequence logged, including Plantinga's reported partial concession — which confirms §7's positioning: the exchange resolved into a dispute over *how evidence enters at stages*, i.e., exactly the partition-choice question the witness criterion adjudicates.
5. §9: Bioethics 2022 added as strongest genre precedent (a field journal publishing a corpus study of its own field → supports the Religious Studies stretch option).

## 4. Residual risk and closure conditions

- Web sweep ≠ exhaustive. Before the P3 freeze, run: (a) structured PhilPapers category crawl (Philosophy of Religion subcategories + Natural Theology), (b) Google Scholar cited-by walks on Gauch 2013, Ocampo 2024, Draper–Nichols 2013, De Cruz 2017. Est. 0.5 d. **Verdict-downgrade trigger:** any item that codes PoR literature by claim strength/direction.
- Non-English literature unchecked — consistent with D-4 (English-only), logged as a stated limitation.
- Plantinga's partial concession is currently sourced to secondary reporting; verify against Plantinga's 2004 reply text during P1 anchor-coding before using it in the paper.

---

## Addendum: residual closure (2026-07-17)

Discharges the two closure conditions registered in §4 (and CONTEXT §5): (a) structured
category crawl, (b) cited-by walks on the four anchor works. Executor: Claude (OpenAlex
API + web search). **Verdict: no downgrade trigger fired. G0 PASS stands; residual
closure complete.**

### Method substitution (to be carried into the paper's methods note)

- PhilPapers blocks automated crawling (bot protection); Google Scholar has no public
  API. Both planned instruments were substituted with the **OpenAlex API**:
  cited-by walks via the `cites:` filter; category crawl via topic/concept filters
  (topic T13150 "Study and Philosophy of Religion"; concepts C81698637 "Philosophy of
  religion", C40455488 "Natural theology") crossed with method-signal terms in
  `title_and_abstract.search`. WebSearch used as auxiliary verification.
- Screening: all citing records fetched with abstracts (inverted-index reconstructed);
  mechanical keyword screen (regex family: cod(e|ing), corpus, quantitativ*, content
  analysis, systematic review, annotat*, topic model*, bibliometr*, text mining,
  survey of arguments, argument/claim strength, meta-analys*, distant reading,
  experimental, rated…arguments) followed by manual review of every hit and a full
  manual pass over all titles.

### (b) Cited-by walks — four anchors

| Anchor | OpenAlex ID | Citing works | Keyword hits | Trigger candidates |
|---|---|---|---|---|
| Gauch, *Phil. Christi* 2013 | W2900261788 | 2 | 0 | none — a Spanish pro-RNT essay; a Russian book review of Holder |
| Ocampo, *IJPR* 2024 ("Strategies for stage II of cosmological arguments") | W4396789438 | 3 | 0 | none — CUP Element *Modelling the Divine* (2025); *Analysis* 2024 evil-god/gap note; *Philosophia* 2025 Ibn Sina paper; all argumentative/formal |
| Draper & Nichols, *Monist* 2013 | W1965091132 | 52 | 5 | none (see screen-outs) |
| De Cruz, *Episteme* (FirstView 2015; print 14(1) 2017) | W2215351015 | 24 | 6 | none (see screen-outs) |

Total 81 citing records (~79 unique; *Religious Disagreement* CUP 2018 and the 2025
x-phi problem-of-evil paper appear on two lists). Screen-outs, with reasons:

- W2767750958 (*J. Asian Studies* 2018) — topic modeling of an early-Chinese corpus;
  different field, topics not claims.
- W2888801925 (De Cruz & De Smedt 2015, Bloomsbury) — person-level experimental
  ratings of 8 pro / 8 contra arguments; already in the §2 delta table.
- W4408122613 (*Religious Studies* 2025, "Experimental philosophy and the problem of
  evil") — x-phi on participants' interpretations of suffering; measures persons.
- W4399458239 (*Phil. Compass* 2024, "Data Over Dogma") — survey of experimental
  philosophy of religion; the entire program it reviews is person-level (intuitions,
  psychology); no corpus-coding study surveyed.
- W4388577862/W4246811308 (*Phil. Review* 2023, "Rational Polarization") — formal
  epistemology; W3177139720 (*Erkenntnis* 2021) — x-phi methods; W4401450052/W4386462261
  (*J. Religion & Popular Culture*) — media representation; W2562179263 — experimental
  metaethics dissertation; W4210614551 — French-language false positive ("code").

### (a) Category-crawl substitute

Five crossed OpenAlex queries (PoR/natural-theology topic-concept × method signals;
281 records returned, all titles reviewed, hits read in full) plus four auxiliary
scholarly web queries. Heavy tagging noise (OpenAlex humanities concepts), zero items
coding PoR literature by claim strength or direction. Nearest methodological
neighbors found, each judged non-triggering:

1. **"The Nature of the Arguments for Creationism, Intelligent Design, and Evolution"
   (*Science & Education* 2017; W2591489551)** — closest find of the whole sweep:
   codes 72 *internet advocacy documents* by argument type (appeal to authority /
   empirical evidence / reason) and topic. Not PoR scholarly literature; coding
   dimensions are argument type/topic, not claim strength or direction along a
   theistic chain. No trigger. Candidate must-cite as a genre precedent for
   item-level argument coding in a religion-adjacent debate.
2. **"Are You There God? Lightweight Narrative Annotation of Christian Fiction with
   LMs" (2025; W4416264837)** — human+LM codebook annotation of "acts of God" in
   Christian fiction novels. Method precedent (LM codebook annotation of religious
   text); fiction corpus, not the PoR record. No trigger.
3. Tobia, "Does Religious Belief Infect Philosophical Analysis?" (*Religion, Brain &
   Behavior* 6(1), 2016) — experimental, person-level; belongs to the De Cruz cluster
   in the §2 delta table.
4. Stance-annotated NLP debate corpora (e.g., Internet Argument Corpus 2.0, LREC 2016)
   include "existence of God" as a forum-debate topic — lay internet posts with
   stance labels; neither scholarly PoR literature nor claim-strength coding.
5. "Content Analysis of the Demonstration of the Existence of God Proposed by Leibniz
   in 1666" (*Roczniki Filozoficzne* 2017) — single-text exegesis despite the title.
6. Philosophy-of-science full-text corpus, 8 journals 1931–2017 (Malaterre et al.
   topic-modeling program) — second genre precedent alongside Bystranowski et al.
   (Bioethics 2022); topics, not claims.

### Verdict and limitations

- **Trigger test** ("any item that codes PoR literature by claim strength/direction"):
  **not fired** on any of the 81 cited-by records or the crawl/search yield. §4
  closure conditions (a) and (b) are discharged; the lane remains unoccupied.
- Limitations, carried as stated: OpenAlex undercounts citations located in books and
  edited volumes (Gauch 2013 shows cited_by = 2 despite known uptake in the RNT
  book literature — e.g., Holder 2021); PhilPapers category listings themselves were
  not enumerable (bot block) and are proxied by the OpenAlex topic/concept crawl;
  non-English literature unchecked, consistent with D-4.
