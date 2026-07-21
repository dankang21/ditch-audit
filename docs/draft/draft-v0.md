# A Prospectively Frozen Zero-Human LLM Measurement Design, and the Confirmatory Checkpoint That Rejected Its Instrument

**Lessing's Ditch as a Measurable Property of the Literature: design, validation battery, and halt report of the audit**

*Manuscript draft v0 — assembled 2026-07-16, at the close of P3 (protocol freeze) preparation and before any confirmatory (P4/P5) result existed; the companion P3 artifacts it cites (analysis plan v1.1, validation battery v1.3, codebook v1.4d/e) carry document dates of 2026-07-17, reflecting the same pre-freeze repair session in which this draft was assembled and audited. See the drafting-protocol note preceding §5.*

**Abstract.** This is a methods report of a rejected instrument: a prospectively frozen, zero-human, multi-family LLM content-analysis design whose fresh-data reliability checkpoint failed on all four coding dimensions at the start of the confirmatory run, halting the study under its frozen decision tree before any hypothesis was tested. The case was to be a corpus-scale audit of natural theology's inferential chain: The inferential chain from a bare first cause to the God of Nicene Christianity has been discussed piecewise — as the "gap problem," as "ramified natural theology," as the "dwindling probabilities" debate — but, so far as a structured prior-art sweep could determine, never measured as a whole. We introduce a witness-based criterion for individuating the chain's dialectically separable steps — logical non-derivability is carried as a witness-supported conjecture, not a theorem — yielding a precommitted eight-step working partition whose factor count, for a fixed partition, is invariant under notational bundling; the reading of those factors as separately payable evidential burdens is defended, not derived from the probability identity. We then designed, and prospectively froze in full under a hash-sealed local protocol, an audit of twenty-one issue-years (2004–2024) of the peer-reviewed philosophy-of-religion literature — 3,536 articles across eleven journals in three venue tiers, locked with the post-2008 stratum as the primary confirmatory population — under which each article's step, direction, claim strength, and the epistemic type of its load-bearing evidence was to be coded. All coding was to be performed by a fixed, precommitted, multi-family LLM instrument with zero human coding of corpus or checkpoint items (the twenty diagnostic gold-anchor labels are designer-authored instrument material, disclosed in §4.3), gated by a precommitted contamination-control battery. Two hypotheses were fixed in the sealed protocol: (1) that among positive evidential claims, pro-side items are predominantly a priori and contra-side items predominantly empirical or historical (registered odds ratio ≥ 3); (2) that positive evidential pro-side claims are more prevalent in confessionally affiliated than in mainstream venues — the confessional tier being operationalized by a single journal, with a precommitted tier-flip sensitivity. The subfield's majority-theist composition provides contextual reason not to assume a uniformly non-theistic mainstream; it does not identify editorial, referee, or submission mechanisms. A precommitted kill criterion binds the symmetric case: a two-null result downgrades the project to a descriptive-map preprint, with no journal claim. Neither hypothesis was tested. At the start of the confirmatory run, the precommitted reliability checkpoint — 150 fresh, seed-drawn items, each coded by three model families with three independent runs per family under the frozen instrument — failed its precommitted dual statistic on all four coding dimensions: the point criterion on two (minimum pairwise Krippendorff's α .676–.736 against the .70 floor) and the bootstrap lower-bound criterion on all four (95% lower bounds .390–.650 against the .667 floor), with the run-level determinism audits (B1a/B1b) clean and the precommitted family-correlation watch untriggered. Under the frozen decision tree this halts all coding, blocks every confirmatory claim, and resolves the pilot gate's conditional declaration negatively: the pilot reliability that licensed the instrument — explicitly flagged in the sealed plan as a selected estimate under optional stopping — did not survive contact with fresh data. The paper accordingly reports the measurement design, the validation battery, the locked corpus infrastructure, and the complete precommitted trajectory ending in instrument rejection, as a methods contribution and a cautionary result for LLM-based content analysis: a precommitted fresh-data reliability checkpoint is cheap relative to a full run, and it does exactly what it is designed to do.

*Keywords:* large language models; automated content analysis; inter-rater reliability; Krippendorff's alpha; protocol precommitment; confirmatory checkpoint; zero-human annotation; validation battery; philosophy of religion; natural theology; Lessing's ditch.

**How to read this document (added at v0.3, 2026-07-17).** The paper's sole confirmatory result is §5.1.1 — the confirmatory checkpoint that rejected the instrument — and its methods contribution lives in §4 (the zero-human instrument and its validation battery; §4.4.10 tabulates the battery at a glance). Sections 2–3 build the case-study apparatus: a witness-based criterion that motivates an eight-step working partition of natural theology's inferential chain (§7.2 states what is and is not claimed for it), with §7 proving a burden-invariance result that stands independently of the halted audit; §8 answers objections to the design. Sections 5.2–5.7 and 6 are precommitted result shells resolved to *not run*: they are preserved in place, unfilled with outcome data (their resolution markers are dated and inventoried), because the outcome-blind commit history of these shells is part of the paper's evidentiary claim — in the spirit of the Registered Reports program's commitment to outcome-independent publication (Chambers and Tzavella 2022) — though this is a self-registered study with a frozen decision tree, not a journal-reviewed Registered Report. Methods readers: §4, §5.1.1, §4.4.10. Philosophy readers: §§2–3, §7, §8. The change inventories of record are the back-matter resolution notes (v0.2 for the P4 resolution; v0.3 for this repositioning; v0.4–v0.10 for the post-review repairs and the v0.9 correction of record), preceded by a version-history summary. *Terminology (v0.10).* Following the v0.9 correction, the paper's own voice says *precommitted*, *prospectively frozen*, or *sealed* where earlier versions said "preregistered": the protocol was frozen locally under a SHA256 manifest, without the externally timestamped registration the earlier label implied. The frozen result shells (§§5.2–5.7, §6), verbatim quotations from the sealed documents, artifact names retaining the historical prefix (`PREREG_MANIFEST.txt`; the `prereg-guardian` agent), the proper noun Registered Reports, and the dated revision notes below keep the original vocabulary.

---

## 1. Introduction

In 1777 Lessing declared that he could not cross the "ugly, broad ditch" (Chadwick's translation, at 55) between accidental truths of history and necessary truths of reason, however often and however earnestly he had tried the leap. The figure has since led the life of an aphorism: invoked, embroidered, occasionally deconstructed — never, so far as our structured sweep could determine, operationalized. A recent sweep of the literature confirms that treatments of the ditch remain interpretive — largely within Kierkegaard scholarship — with no formal or empirical operationalization on record. This paper proposes to treat Lessing's ditch as a measurable property of a literature. The inferential chain that the ditch interrupts — from "physical reality has an external cause" to the God of Nicene Christianity — is, we argue, individuable into dialectically separable steps by a side-neutral criterion; and once individuated, the peer-reviewed record concerning each step can be audited: every article coded for the step it addresses, the direction of its primary thesis, the strength of the claim it advances, the epistemic type of its load-bearing evidence, and the venue in which it appears. The intended product was not another argument about whether the ditch can be leapt, but a map of twenty-one issue-years (2004–2024) of professional attempts, refusals, and rebuttals; what stands delivered instead is the instrument, its validation battery, and the checkpoint that rejected it — §5 records how far the attempt ran.

Three well-developed literatures already address segments of this chain, but they do not talk to one another and none measures the record as a whole. First, the *gap problem* — Pruss's (2009) name for the residue left after a cosmological argument succeeds: how does one get from a first cause to a being with the divine attributes? Rasmussen (2009) and, most systematically, Ocampo (2024) map "Stage II" bridging strategies, but for a single segment of the chain and by argument-analysis rather than corpus measurement. Second, *ramified natural theology* — Swinburne's coinage for the pro-side program that argues from bare theism onward to specifically Christian doctrine (Holder 2021; Gauch 2013). This is a constructive project: it builds the crossing, it does not survey the traffic. Third, the *dwindling probabilities* exchange over the multiplicative structure of cumulative cases, initiated by Plantinga (2000), answered by Swinburne (2004b) and McGrew (2004), and continued through McGrew and McGrew (2006) and Nickel (2015). That debate concerns the formal behavior of chained arguments, not the empirical distribution of the arguments actually published. The chain, in short, has been discussed piecewise; our sweep surfaced no measurement of it whole.

Our contribution is accordingly of an unusual type for the philosophy of religion: a design for measuring the dialectic rather than participating in it — together with the precommitted rejection of that design's instrument. The paper makes one framework claim and registers two empirical claims. The framework claim (§2) is that a witness-based criterion individuates the chain into an eight-step working partition (§7 defines the criterion's regulative ideal and states exactly what Table 1 is, and is not, claimed to satisfy), and (§7) that the count of evidential *factors* this partition exposes is invariant under logical and definitional repackaging — read as separately payable burdens under the burden principle defended there, bundling the steps into "a maximally great being exists" relocates the burdens into the bundle's prior; it does not reduce them. The empirical claims are two precommitted hypotheses about the shape of the published record, described below; their precommitted test is reported in §5, where the gate chain halted at its first item before either was run.

The empirical program this project joins — and must be distinguished from — measures people, not literatures. De Cruz's studies measure philosophers: philosophers' assessments of religious disagreement track the assessor's prior religious belief (De Cruz 2017); natural-theological arguments have been evaluated experimentally, with argument-strength ratings tracking the rater's prior belief (De Cruz and De Smedt 2016); and most philosophers of religion were theists before entering the field, a selection effect documented qualitatively (De Cruz 2018). Draper and Nichols (2013) diagnose field-level cognitive biases and issue recommendations, without a coded corpus. The PhilPapers surveys measure the field's composition (Bourget and Chalmers 2014). The nearest genre precedent lies outside the field entirely: Bystranowski, Dranseika and Żuradzki (2022) topic-model half a century of bioethics across seven field journals — but topics are not claims, and no direction, strength, or epistemic type is coded. A structured prior-art sweep (seven query families; cited-by walks on the nearest neighbors and a category-level sweep were completed at registration: 81 citing works and 281 category-screened records yielded no prior item-level coding of this literature) found no prior work that measures a philosophical literature's *argumentative structure* — step by direction by claim strength by epistemic type by venue. That is the lane this audit occupies.

Two patterns were predicted for test. **H1** (the type–direction hypothesis): among mainstream-venue articles making positive evidential claims (POS, the upper level of the two-level claim-strength scale defined in §4.2), the distribution of load-bearing evidence types differs by direction — pro-side items predominantly a priori, contra-side items predominantly empirical or historical; the precommitted prediction is an odds ratio of at least 3. **H2** (venue topography): among pro-side items, the prevalence of positive evidential (POS) claims is higher in confessionally affiliated venues than in mainstream venues, with contra-side items as a control (predicted null or reversed) — noting that the confessional tier is operationalized by *Philosophia Christi* alone, so H2 is in practice a single-confessional-journal comparison carrying a precommitted *Faith and Philosophy* tier-flip sensitivity (R2). We emphasize what these hypotheses are: predictions, exposed to the data, and defeasible. Should H2's venue pattern obtain, the field-composition evidence would make a uniformly non-theistic mainstream an unsafe assumption — the specialist subfield is majority-theist, roughly 72% of philosophy-of-religion specialists accepted or leaned toward theism in the 2009 PhilPapers survey (Bourget and Chalmers 2014), with the 2020 wave reporting a similar balance (Bourget and Chalmers 2023) — but it would not establish the direction or stringency of the venue comparison, since editorial, referee, and submission compositions were not measured; whether the pattern obtains is precisely what the audit was built to find out. A precommitted kill criterion binds us to the symmetric outcome: if both hypotheses are null, the project is downgraded to a descriptive-map preprint and no journal claim is made. Nothing in the sections that follow presupposes either verdict.

A word on the instrument, detailed in §4. All corpus coding was to be performed by a fixed, precommitted, multi-family ensemble of large language models, with zero human coding of corpus or checkpoint items — no human coder, no human item-adjudication, no human validation sample; the one designer-authored item-level artifact is the twenty-item diagnostic gold-anchor key — not used as criterion-accuracy evidence, though included in the pilot reliability estimate and material to its conditional pass (§4.3). Items are blinded (author, title, journal, and year stripped) before coding, and the instrument's validity evidence comes from a precommitted contamination-control battery rather than from human benchmark annotation. The paper therefore claims measurement by a fixed, precommitted instrument, not human-equivalent annotation; the residual limitation — accuracy on the real corpus distribution is formally unidentified without a human criterion — is stated, bounded by the battery, and carried honestly.

Equally important is what this paper does not claim. It is not first-order atheology: we take no position on the truth of any step, and the audit's categories are deliberately side-neutral. It is not a claim that theism is irrational: claims of epistemic permissibility (folded into the defensive grade, DEF, of our claim-strength scale) are orthogonal to the evidential claims the hypotheses concern. It is not a suppression or censorship claim: we measure the published record and infer nothing about submission flows or editorial conduct. And it is not a citation-weighted "importance" ranking: citation counts measure fashion, and enter only as an optional robustness check. These fences are load-bearing and are restated where they matter (§9).

The paper proceeds as follows. Section 2 states the individuation criterion. Section 3 applies it, motivating the precommitted eight-step working partition (Table 1), and explains in what sense the table's qualitative status verdicts are priors the audit was designed to test — and, if need be, overturn. Section 4 describes the corpus, the codebook, and the zero-human coding pipeline; §5 reports the gate-chain outcome (the run halted at the chain's first item); §6 the robustness battery, resolved to not run; §7 the formal treatment of burden invariance, positioned against Roche and Shogenji's (2014) result on confirmation transmission; §8 answers five objections; §9 states what such a map would license.

## 2. The witness-based individuation criterion

How many steps lie between a first cause and the Nicene creed? The question looks hopelessly rhetorical. A critic can multiply distinctions until the chain resembles a ladder with a hundred rungs, each "improbable"; an apologist can bundle the entire target into a single proposition — "a maximally great being exists" — and present one burden where there were many. Both maneuvers are cheap because mathematical partitions are free: the probability calculus permits any coarsening or refinement of a conjunctive target, relocating conditional factors without eliminating them (the formal statement is §7's business). If step-counting is to carry any weight, the count must be fixed by something other than the counter's interests.

Our criterion ties partitions to the sociology of the dispute itself. A step S_i is admitted into the partition if and only if:

1. **Necessity.** S_i is logically necessary for the target, where the target is a Nicene-minimal definition of Christian theism — the creedal core, not any richer confessional package.
2. **Dialectical separability, witness-certified.** S_i is not derivable from S_1, …, S_{i−1}; and this independence is certified by a **witness** — an extant scholarly position that accepts all prior steps and rejects, or in the boundary-marking limit formally suspends judgment on, S_i. (A reasoned refusal to affirm, issued from a position that has paid every prior toll, marks the boundary as effectively as denial; Table 1 flags its one suspension witness as such.) Source verification distinguishes the *grades* in which this condition is met — an assertoric stance-witness; a seriously defended hypothesis-level position; a structural countermodel; a second-order suspension — and the note to Table 1 states the grade each *verified* boundary currently carries (S2's witnesses, Mill's finite god, Hick's pluralism, Mormon finitism, and classical deism sat outside the verification pass and remain at design-phase status). Where the strict assertoric grade is unmet, the partition's status is correspondingly criterion-relative and provisional (§7.5, admissions (iv)–(v)). The partition the study registered is accordingly a *working* partition: the criterion is its design principle and regulative target, not a status every boundary has been shown to hold (§7.2).
3. **Dedicated dispute.** A dedicated peer-reviewed literature disputes S_i specifically, rather than only as a corollary of some other dispute.

A scope note before the work begins: what a witness certifies is dialectical, not
model-theoretic. An extant position that pays every toll to S$_{i-1}$ and declines S$_i$
demonstrates that the literature treats the boundary as real — that the step is separately
occupiable and separately disputed. It does not prove logical non-derivability (the position
might be inconsistent, or mistaken about an entailment); non-derivability is here a
witness-supported conjecture, and the partition's claims are correspondingly claims about the
structure of the published dispute. The witness condition does the main philosophical work; it constrains, though it does not eliminate, grain-selection discretion. A boundary between steps is real, on this criterion, exactly where someone in the literature actually stops: a position that has paid every toll up to S_i and declines to pay the next one demonstrates, by existing, that the next toll is a separate toll. This raises the price of gerrymandered inflation (no witness, no step) and of apologetic deflation (a bundled proposition cannot absorb a boundary at which a published position stands) — a constraint on partition discretion, not its elimination. The criterion is also side-neutral in a way that matters for the audit's credibility: the witness list is not a roster of naturalists. Hartshorne stands at one boundary, Lapide at another, Wiles at a third — theists all, each accepting the chain up to a point and rejecting the next step. Condition (3) earns its keep methodologically: it makes each admitted step conceptually codeable — a dedicated literature exists to code — though it cannot by itself guarantee a non-empty cell within the selected eleven-journal, 2004–2024 corpus; to that extent the partition and the measurement instrument are two views of one object.

The criterion also excludes. Intra-theistic attribute puzzles — the omnipotence paradox, the foreknowledge–freedom debate — are internal disputes about how to articulate an attribute, not tolls on the path to the target: following Geach (1973), Christianity needs the *pantokrator*, not the philosopher's omnipotence, and open theism shows that strong omniscience is not a Nicene-minimal component (cf. Hasker 1989). Such items are coded to a separate class and excluded from the chain. Arguments that conclude directly to a conjunctive God — ontological arguments, generic arguments from religious experience — are retained but tagged as *bundled*; the prevalence of bundling is itself a datum for §7, not noise to be discarded.

One objection deserves a forward reference now (O1, §8): is the integer eight not an artifact of grain? We acknowledge grain-dependence up front. The published claim is not "eight" but the pair of invariants: the hypotheses were required to survive the precommitted grain variants — the registration's operationalization of grain-robustness, not a survey of every admissible partition, a set §7.2 concedes is open — and the robustness battery (§6, R1) re-runs the analyses under a seven-step partition (merging S7 and S8), a ten-step partition (splitting S3's unicity/aseity from sovereignty, and splitting S4 along Mill's finite-god line), and a liberal-target variant (dropping S7) — variants that, like all of §6, never ran (§5.1). The canonicity argument — why witness-certified partitions are the *admissible* accounting units for cumulative cases, and how this adjudicates the partition choices presupposed on both sides of the dwindling-probabilities exchange — is made in §7.

## 3. The precommitted eight-step partition

Applied to the record at design time, the criterion motivated an eight-step working partition; §7.2 states exactly what is and is not claimed for it. Table 1 states each step's thesis, the boundary evidence or candidate witnesses recorded for it (in the grades the note below states), the anchor literature identified during instrument design, the qualitative status verdict carried into the audit as a *prior*, and the epistemic type of the step's characteristic evidence. Types are: **α** = a priori/metaphysical (no in-principle empirical exposure); **β** = empirical contact; **γ** = historical-singular.

**Table 1. The precommitted eight-step working partition (certification grades in the note below; §7.2 states what is not claimed), with design-phase priors to be tested (see text). Anchor citations are identifying exemplars fixed at design time, not comprehensive step bibliographies.**

| # | Thesis (the statement disputed) | Boundary evidence / candidate witness (grades in the note below) | Anchor literature (design-phase set) | Qualitative prior (testable) | Type |
|---|---|---|---|---|---|
| S1 | Physical reality as a whole has an external cause or ground (not a brute fact) | Russell (brute fact); Oppy | pro: Pruss & Rasmussen 2018; Barnes 2012; White 2000 (functional pro: rebuts the multiverse rejoinder to fine-tuning) · contra: Oppy 2006; Malpass & Morriston 2020; McGrew, McGrew & Vestrup 2001; Adams 2019 | contested — pure metaphysics after this design withdrew reliance on the BGV-based inference (Borde, Guth, and Vilenkin 2003) | α (+β sub-dispute on fine-tuning degree) |
| S2 | That ground is an agent with intentions and will | Leslie's axiarchism; Tegmark 2008 | pro: Swinburne 2004a · contra: Morriston 2000 | contested; only observational channel routes through S5 | α |
| S3 | The agent is unique, a se, uncreated; all else ontologically depends on it (*pantokrator*) | Bostrom's simulator (2003, structural countermodel — see note); Hartshorne 1984 (stance-witness, qualified — see note); Mormon finitism (Ostler 2001; design-phase) | gap-problem literature: Pruss 2009; Rasmussen 2009; Ocampo 2024 · bundling fence: Geach 1973; Hasker 1989 | contested / frozen — evidence up to S2 shared with contingent-creator hypotheses | α |
| S4 | The ultimate is perfectly good | Draper's indifference; Law's evil-god (both hypothesis-level — see note); Mill's finite god (1874) | contra: Rowe 1979; Draper 1989; Law 2010; Cahn 1977 · pro anchors: defensive items only (Plantinga 1974; Wykstra 1984) | headwind | α+β (Draper's likelihood argument has data contact) |
| S5 | The good ultimate acts specially in the world post-creation (miracles, answered prayer) | Wiles 1986; classical deism (Tindal 1730; design-phase) | contra: Roberts et al. 2009 (Cochrane CD000368); Benson et al. 2006 (STEP); Wildman 2004; Hume 1748 · pro anchors: coherence defenses only | strong headwind; the chain's only fully live empirical channel | β |
| S6 | The authentic bearer of that God's special revelation is the Hebrew prophetic tradition | Islam (supersession — see note); Hick's pluralism (1989); Judaism (re-filed to a finer-grain boundary — see note) | contra: Alston's parity argument (1991) · pro anchor: Plantinga 2000 (a permissibility claim) | headwind / near-frozen; evidence defers to S7 | β·γ |
| S7 | Jesus of Nazareth was bodily raised (~AD 30) | Carnley 1987/2019 (boundary evidence against the material-continuity construal — see note); Allison 2021 (second-order suspension — see note); Lüdemann 1994 (step-contestation — see note) | pro: Wright 2003; Swinburne 2003 (with its own dwindling-probabilities caveat) | strong headwind; evidence-frozen (fixed corpus) | γ |
| S8 | The resurrection shows Jesus is God incarnate; God is triune | Lapide (accepts S1–S7, rejects the messianic-incarnational inference — see note); Tuggy 2003 (the trinitarian conjunct) | pro-coherence: Morris 1986; Brower & Rea 2005 | defensive; truth-evidence fully S7-dependent | α (γ-dependent) |

**Witness-verification note (v0.4; revised v0.5–v0.8).** A post-draft primary/secondary-source verification of the witness column (as the column was titled through v0.6; retitled "Boundary evidence / candidate witness" at v0.7) (details in the audit package) confirmed the S1, S5, and S8 assignments as stated, and supported a *construal-dependent* S6-Islam assignment (its reading stated below) — Russell denies both any cause of the totality and the legitimacy of the demand; Wiles holds S1–S4 fixed precisely to protect S4 from selective intervention; Islam accepts S1–S5 and rejects S6 on supersession grounds (Q 33:40, "the seal of the prophets," Abdel Haleem 2004; on the doctrine's universality in Sunni Islam, Friedmann 1986), with the *taḥrīf* charge as a differentiated second ground (its classical spectrum — meaning-level distortion in most authors, textual tampering in Ibn Hazm — is documented in Adang 1996) — the rejection engages S6's definite article: on supersession, the authentic bearer of God's special revelation is now the Qur'an, so the Hebrew tradition is not *the* bearer; the step's registered wording names finality nowhere and preservation only implicitly, through "authentic" — the conjunct the *taḥrīf* ground targets — while the supersession ground bites on the definite article alone; this reading is stated explicitly as the one on which Islam's rejection engages the registered wording; Lapide accepts "the resurrection of Easter Sunday not as an invention of the community of disciples, but as a historical event" (Lapide 1983, 15 — the sentence is Braaten's introduction quoting Lapide, echoed on the volume's cover, not located in Lapide's own chapters) while rejecting the Christian messianic and incarnational inference drawn from it (the trinitarian conjunct is rejected in separately documented work: the Lapide–Moltmann dialogue, Lapide and Moltmann 1981) — and qualified the assignments in four other cells, which the table now flags. S8, note further, bundles two separately disputed conjuncts — the messianic-incarnational inference (Lapide's target) and trinitarian doctrine (Tuggy's) — which, with S3's attribute package and S6's bearer and preservation conjuncts, is evidence that the eight-step grain is not maximal by the paper's own criterion (§7.2). *Bostrom* supplies a structural countermodel, not a witness: the trilemma's author accepts neither S1 nor S2 assertorically, so the simulation hypothesis demonstrates the conceptual separability of S3 from S1–S2 (an intentional external creator that is non-unique, dependent, possibly itself created) without occupying the stopping point; for assertoric theological uptake of the simulation hypothesis, see Steinhart (2010). *Hartshorne* affirms uniqueness, uncreatedness, and necessary existence; what he rejects is the classical aseity–omnipotence–creatio-ex-nihilo package, and his acceptance of S1 runs through the "ground" disjunct under panentheism. *Draper's indifference hypothesis and Law's evil-god* certify S4's boundary at the hypothesis level — seriously defended epistemic possibilities of S1–S3 without S4 — their authors being, respectively, a professed agnostic and an atheist; among the verified entries, no witness personally stops at S4 (Mill's finite-god position, the cell's third entry, was outside the verification pass and retains its design-phase status). *Judaism* affirms S6 as worded — the revelatory authenticity of the Hebrew prophetic tradition is constitutive of it — and is therefore *not* an S6 witness under the registered reading; the v0.4 attempt to seat it via the christological construal is withdrawn at v0.6, because a christological rewrite of S6 would break the chain elsewhere: Lapide, who rejects that construal, would then stop at S6 rather than S8. What Judaism's dedicated literature rejects (Maimonides 1987, Hilkhot Melakhim 11:4 in the uncensored text; the medieval polemical corpus edited in Berger 1979; the Isaiah 53 exegetical tradition documented in Rembaum 1982) is a *finer-grain* boundary — the christological construal of the corpus — which the eight-step grain does not carve as a step of its own, and which no registered grain variant carves either (R1's ten-step splits S3 and S4 only); its existence is carried as further non-maximality evidence under §7.2, pricable only by a re-registered variant. The registered S6 boundary is carried by *Islam* (supersession, on the construal-dependent reading stated above) and by Hick's pluralism (design-phase status, unverified). *Lüdemann* rejects S7 but is not a chain-witness: the same 1994 work already discounts special divine action (S5), and he later renounced Christian belief; he is carried as step-contestation literature. The S7 boundary is instead carried by *Carnley* (1987; 2019), added at v0.5 after source verification, as construal-scoped boundary evidence — assertoric in kind, scoped in target — with one construal caveat: "bodily raised" admits readings, and Carnley's target is the material-continuity construal, precisely the one the step's pro-side anchors defend (Wright 2003; Swinburne 2003), so the evidence he supplies runs against S7 precisely as the anchor literature disputes it, not necessarily against every transformed-embodiment reading. He is an Anglican primate who accepts every upstream link — Nicene theism, God's ongoing special action as present Spirit, the scriptural revelation tradition — while arguing that the Easter event cannot be established historically (1987, the limits-of-historical-enquiry discussions clustered at 72–103) and, on his reading of Paul's "spiritual body" (1987, 231–233), should not be construed as a material-bodily raising at all; resurrection faith, on his account, rests on present acquaintance with the living Christ (his acceptance of S5 runs through the Spirit's present activity rather than a general apologetic of nature-miracles — a mode note, not a disqualification). *Allison's* suspension corroborates the same boundary at the second-order grade — it concerns what unaided historical evidence warrants, while he affirms the proposition as personal faith — and his *non liquet* label is our characterization, not a quotation. None of these qualifications removes a boundary; each sharpens what kind of occupancy certifies it.

The qualitative-prior column requires immediate discipline. Its verdicts — *contested*, *headwind*, *frozen*, *defensive* — originate in the qualitative reading of the anchor literatures that produced this design. They are not results, and the audit does not assume them. They are priors, and they are *computable*: a frozen, ordered decision list (applied in §5.6) defines each verdict as a function of coded aggregates within the mainstream tiers — a step is **contested** when both directions field at least *k* positive evidential (POS) items (default *k* = 3, reported at *k* ∈ {2, 3, 5}); a **headwind** obtains when POS items are one-sided, the opposing direction fielding none, whatever its defensive (DEF) activity — the predicate is direction-unsigned, and the computed status reports which direction fields the POS items; a step is **frozen** when neither side has produced a POS item in the trailing ten years; residual cells report as mixed/sparse. The audit was designed to reproduce this column or correct it, cell by cell, with either outcome reported; the run halted before the column was ever computed (§5.1).

That "or corrects it" is not a pious formula; the design history already contains two documented episodes of the instrument correcting its designers. First, an early design-phase version of Table 1 had shelved White (2000) in S1's contra column — a natural mistake, since the paper attacks a design argument's premise-mate. Gold-anchor coding under the codebook's net-effect rule (direction is the net effect on the *step thesis*, traced through reply chains) caught the error: White's paper rebuts the multiverse rejoinder to fine-tuning, so its net effect on S1 is functionally pro, whatever the author's worldview. The table was corrected, and the correction logged. Second, during pilot calibration, unanimous three-family contradictions of the designer's gold codes on three anchor items triggered a precommitted text-only re-adjudication; it found that two anchors had been gold-coded from the arguments' *reputations* rather than from the texts before the coders (both are reply-chain defeater-rebuttals, not positive evidential cases), and a third's evidence type fell to a newly codified dominance rule. The coders' unanimous "misses" were correct readings; the memorization failure mode the validation battery polices in the models had manifested in the designer. Both episodes are now codified as standing rules in the codebook. Table 1's verdicts should be read accordingly: as the best current qualitative priors of a design process that has twice been overruled by its own instrument, awaiting quantitative adjudication.

Read as a set of priors, the table also carries four structural impressions that motivated the hypotheses and that §5 must re-derive from the corpus rather than assume. (i) The steps whose status reads *contested* are exactly the α steps, and the steps under *headwind* are exactly those with β or γ exposure. (ii) S2 hides a dependency: the only observational channel by which agency could show itself routes through S5's special-action claim, so S2's dispute, though conducted a priori, is hostage to an empirical cell. (iii) On the design-phase reading, roughly two of the eight steps have any fully live empirical channel at all — and those are the steps whose prior status is the most contra-one-sided. (iv) Strong pro-side claims appeared, in the qualitative reading, to concentrate in particular venues. Each of these is precisely the kind of impression a qualitative reader — including this one — could have absorbed from the field's folklore rather than from the record; that is why they are here demoted to priors, why the coding instrument is firewalled from them, and why the confirmatory analysis is designed to be capable of embarrassing them.

A second objection also deserves its forward reference here (O2, §8): the Thomist will protest that there is no gap to audit — on the doctrine of divine simplicity, the attributes follow from pure actuality, so S3 and S4 are not further steps but corollaries of S1–S2. The reply, developed in §8, is that the entailment claim is itself a contested step rather than a dissolver of steps: witnesses who reject it exist *within* theism (Hartshorne's dipolar theism; the standing classical-versus-personalist dispute), and Pruss's own presentation of the gap problem concedes the transition as the cosmological argument's "final difficulty." Within the audit, entailment claims are coded as pro-side a priori items at the step whose necessity they assert; they enter the map as data, and cannot erase its cells by fiat.

With the partition fixed and its priors flagged, the measurement question becomes concrete: what, over twenty-one issue-years of the peer-reviewed record, has actually been claimed at each boundary, in which direction, at what strength, on what kind of evidence, and where? Section 4 describes the corpus and the instrument built to answer that question.

## 4. Methods: corpus, instrument, and validation

This section describes the corpus (§4.1), the coding instrument and the zero-human measurement pipeline (§§4.2–4.3), and the validation battery and protocol freeze architecture (§4.4). The full protocol documents — codebook, validation battery, and analysis plan — are frozen at registration, SHA256-hashed into its manifest, and archived with it; what follows is a complete account of every design decision that bears on the confirmatory analyses.

### 4.1 Corpus

**Venue tiers.** The corpus is drawn from three precommitted venue tiers. Tier 1 (T1, general journals): *Mind*, *Noûs*, *The Philosophical Quarterly*, *American Philosophical Quarterly*, *Analysis*, and *Philosophical Studies*, restricted to chain-relevant items by the two-stage topic filter described below. Tier 2 (T2, specialist mainstream): *Faith and Philosophy*, *Religious Studies*, the *International Journal for Philosophy of Religion*, and *Sophia*. Tier 3 (T3, confessionally affiliated): *Philosophia Christi*. Two boundary decisions were fixed before harvesting: the *European Journal for Philosophy of Religion* is excluded from T2, and T3 comprises *Philosophia Christi* alone rather than adding the *Journal of Analytic Theology* and *TheoLogica*, whose confessional status is more debatable. The corpus is English-only and articles-only; books serve as qualitative anchors, and the field's monograph culture is carried as a stated limitation.

One assignment deserves flagging rather than burial. *Faith and Philosophy* is published by the Society of Christian Philosophers but is editorially open — prominent contra-side authors publish there — so its placement in T2 rather than T3 is a genuine judgment call. We precommit it as a sensitivity axis (robustness check R2): every tier-sensitive analysis is recomputed with *Faith and Philosophy* flipped to T3. The assignment is thereby an explicit, testable modeling choice rather than a hidden one.

**Window and inclusion rules.** The window is issue-year 2004–2024. Research articles are included; book reviews are excluded; discussion notes are retained but flagged as a separate class. The corpus measures the published record of these venues, nothing more; no inference to submission or refereeing flows is made (§9).

**Harvest pipeline, T2∪T3.** The specialist corpus was harvested in July 2026 by a checkpointed, standard-library-only fetcher against the Crossref REST API (Hendricks, Tkaczyk, Lin, and Feeney 2020) by ISSN (fetch window 2002–2026, filtered to issue years 2004–2024, published-print date preferred), with publisher landing pages as an abstract fallback. The initial pass yielded 3,920 included items after excluding 950 non-research items identified by bibliographic signature (editorials, front and back matter, errata, obituaries, announcements, and signature-identifiable book reviews). Abstract coverage at this stage was sharply publisher-dependent: 100% for *Religious Studies* (Cambridge deposits abstracts with Crossref), 80.3% and 83.9% for *IJPR* and *Sophia* (Springer), but 9.6% for *Faith and Philosophy* and 14.5% for *Philosophia Christi*, whose publisher (the Philosophy Documentation Center) does not deposit abstracts with Crossref. Overall coverage stood at 56.5% (2,214/3,920) — far below the precommitted coverage gate of 90%, and concentrated in exactly the venues on which the H2 comparison depends.

Coverage was closed by a sequence of recovery passes, all verbatim: the recovery scripts copy source text with whitespace collapsing only, and no generative or search-augmented model touches the abstract-recovery path. First, database recovery pulled verbatim abstracts from OpenAlex (Priem, Piwowar, and Orr 2022) and Semantic Scholar (Kinney et al. 2023) (293 *Faith and Philosophy* abstracts came from OpenAlex alone), and a gap in Crossref's *Faith and Philosophy* deposit for 2022–2023 was backfilled from OpenAlex with issue years derived from volume numbers (year = 1983 + volume, which publisher records confirm for volumes 38–40 = 2021–2023; a post-draft verification found that *Faith and Philosophy* published no 2024 volume at all — the journal skipped from volume 40 (2023) to volume 41 (2025), re-syncing volume numbers to calendar years — so the venue's 2024 cell is empty at the source and no volume-41 item entered the corpus), adding 65 items and lifting overall coverage to 73.2%.

Second, two publisher-source recoveries addressed the Philosophy Documentation Center journals. For *Faith and Philosophy*, page-faithful PDFs served by Asbury Theological Seminary's institutional repository carry the journal's printed abstracts, which were extracted verbatim from the PDFs. A first pass was interrupted after 33 items when the repository's web-application firewall began challenging the bulk request rate, leaving 204 items temporarily blocked; a paced retry completed the recovery and raised *Faith and Philosophy* coverage from 62.1% to 90.6%. For *Philosophia Christi*, the publisher's own landing pages at pdcnet.org expose each item's abstract in an `og:description` metadata tag; harvesting these recovered 284 abstracts and source-confirmed 99 items — the journal's 2004–2007 tail — as never having carried an abstract, raising coverage from 26.3% to 81.8%.

**Review reclassification.** Because Crossref metadata for the Philosophy Documentation Center journals does not type book reviews, signature-based exclusion at harvest left many reviews sitting in the corpus as short "notes." These were removed in stages of increasing evidential strength: a conservative post-processing heuristic (no abstract and a page span of five or fewer), then source confirmation — the pdcnet.org landing pages carry an authoritative item-type field (`Item_Data_Type = Book Review`), and the Asbury PDFs permit direct inspection of the typeset pages — executed as scripted signature extraction over the PDF text layer, with no human item-reading (the zero-human rule's machine-execution discipline extended to curation; the PI approved rules, never items). Genuine discussion notes were preserved throughout where the reply-cue title signature identified them; the sampled East note below carries no reply cue, which is how it was swept. Of record, 627 review exclusions are carried on the corpus-lock exclusion list (a freeze-manifest artifact): the confirmation passes are individually source-confirmed (the pdcnet item-type field; scripted PDF inspection), the initial heuristic-stage removals are not, and the list is reconciled against the stage-wise removal tallies before the manifest is signed. Fifteen of the excluded items are review essays that do carry abstracts and are excluded reversibly, flagged for possible reinstatement. Decomposition of the 627-entry lock: 150 exclusions are individually source-confirmed (82 by Asbury PDF inspection signatures, 68 by the pdcnet `Item_Data_Type` field); 473 rest on the conservative heuristic (469 by the no-abstract-and-≤5-pages rule, 4 by the title-pattern signature); and 4 are harvest-stage signature exclusions that were never inside the post-harvest corpus but are carried on the lock because its generation rule sweeps every review-reason row. The item-flow arithmetic of record is therefore: 3,920 initially included + 65 backfilled − 623 lock entries then in the corpus = 3,362. Because every heuristic exclusion lacks a *harvested* abstract, reinstating all 473 would add no abstract-covered items as the corpus stands harvested, and would lower abstract coverage to 2,958/3,835 = 77.1% (one sampled item's publisher-side abstract escaped the harvest — see below); whether any such row could be coded at all would depend on the registered low-text supplementation path, which requires source text these rows lack in the harvest. The 473 are carried, explicitly, as a *corpus-definition assumption rather than a source-confirmed classification* — the strongest of the reviewer-visible corpus limitations. To size the assumption's risk, a seeded random sample of 20 of the 473 (seed 20260720, drawn post-halt during the fourth-review repair cycle; sampling record in the audit package) was source-confirmed against publisher item-type fields — the date-derived seed was fixed before any sampled record was inspected, and one draw was made, with no reruns or alternative seeds: 17 are book reviews, 2 are editorial introductions (correctly excluded, though not for the reason the heuristic supposed), and 1 is a research item wrongly swept — a five-page discussion note (East, "Infinity Minus Infinity," *Faith and Philosophy* 30(4), 2013, 429–433) that sits exactly on the ≤5-page threshold and whose publisher record carries an abstract the harvest missed. The sample false-exclusion rate is 5% (1/20; exact 95% CI 0.1%–24.9%), extrapolating to roughly 24 of 473 — potentially anywhere from a handful to over a hundred at this sample size. The lock ships title, journal, year, and page metadata for all 627 entries, so the classification is fully re-checkable; the one confirmed false exclusion is disclosed rather than silently reinstated, post-halt corpus changes being barred by the freeze. The resulting denominator of record is 2,818 T2 items and 544 T3 items, 3,362 in total.

**Coverage of record and the stratified gate.** The final coverage matrix is:

| Journal | Tier | Items | With abstract | Coverage | ≤2008 | 2009–2018 | 2019–2024 |
|---|---|---|---|---|---|---|---|
| Faith and Philosophy | T2 | 543 | 492 | 90.6% | 136/147 | 254/277 | 102/119 |
| Religious Studies | T2 | 799 | 799 | 100.0% | 150/150 | 342/342 | 307/307 |
| IJPR | T2 | 656 | 528 | 80.5% | 63/132 | 300/324 | 165/200 |
| Sophia | T2 | 820 | 694 | 84.6% | 84/116 | 332/400 | 278/304 |
| Philosophia Christi | T3 | 544 | 445 | 81.8% | 29/127 | 291/292 | 125/125 |
| **T2 total** | | **2,818** | **2,513** | **89.2%** | | | |
| **T3 total** | | **544** | **445** | **81.8%** | | | |
| **Total** | | **3,362** | **2,958** | **88.0%** | | | |

Overall abstract coverage of record is 88.0% (2,958/3,362). Under the R2 flip (*Faith and Philosophy* counted as T3), coverage is T2 88.8% and T3 86.2%, so the sensitivity axis does not open a coverage asymmetry between tiers.

The precommitted gate demanded ≥90% abstract availability, and the headline 88.0% does not meet it flatly. Rather than either declaring failure or quietly relaxing the threshold, the gate was ruled *stratified*, on a rationale fixed before the final *Faith and Philosophy* retry completed (post-2008 coverage excluding the firewall-blocked tranche stood at 93.3% at ruling time). The rationale is that the residual missingness is not random fetch failure but a structural era boundary: every residual missing item in *Faith and Philosophy* and *Philosophia Christi* is source-confirmed as never having published an abstract; the *IJPR* and *Sophia* residuals are prior-pass, predominantly pre-2019 items for which no probed database source held an abstract (genuine no-abstract on the harvest log's verdicts, not individually source-confirmed); and the practice of printing abstracts stabilizes across these venues around 2008. Missingness of this kind should be modeled, not hidden. The gate of record is therefore: post-2008 T2∪T3 coverage = 92.8% (2,496/2,690), passing the 90% threshold; the 2004–2008 era — issue years up to and including 2008; the registration labels it the "pre-2008" stratum, a label the frozen shells retain — in which 210 of 672 items (31.2%) lack abstracts, is declared a precommitted missingness stratum. An era-by-venue bias table is published with the corpus release, and the confirmatory analyses carry missing-abstract sensitivity scenarios for this stratum rather than silently dropping it. Residual missingness after all recovery totals 404 items (12.0%), of which 210 fall in the 2004–2008 stratum.

**T1 topic filter, stage 1: keyword prefilter.** The six general journals publish overwhelmingly non-chain-relevant material, so T1 enters through a two-stage filter designed recall-first: the prefilter is meant to over-include, and no relevance judgment is made at this stage. Of 11,225 raw in-window Crossref records across the six journals, 614 were excluded as non-research items, leaving 10,611 eligible articles and notes. A battery of 36 case-insensitive keyword substrings (from `god` and `theism` through `kalam`, `fine-tun`, `resurrection`, and `properly basic`) was matched against title and abstract — or title alone where no abstract was deposited at filter time, which held for 202 of the eventual hits, since the Oxford journals' landing pages block automated fallback. The prefilter passed 296 candidates. Abstract coverage on the candidate set was 45.9% at filter time and stands at 94.3% of record after recovery.

**T1 stage 1b: APQ backfill.** *American Philosophical Quarterly* has zero Crossref records with publication dates in 2004–2016 (verified live at harvest), so filtering Crossref alone would silently amputate thirteen years of one T1 venue. The gap was backfilled from OpenAlex with issue years derived from volume numbers (year = 1963 + volume), a mapping calibrated to 100% agreement both against every DOI-bearing OpenAlex APQ record and against Crossref's APQ records for 2017–2024 (volumes 54–61); OpenAlex's own publication-year field mis-dates pre-DOI articles and was used only as a flagged fallback (one item). The backfill added 151 articles and notes, of which 10 passed the keyword prefilter and joined the screening pool. Only 8 backfill items carry DOIs; the remainder are keyed by OpenAlex work identifiers.

**T1 stage 2: LLM relevance screen.** All 306 candidates (296 keyword hits plus the 10 APQ hits) were screened for topical relevance — an include/exclude judgment only, categorically distinct from coding — by a single pinned model endpoint (`gpt-5.5-2026-04-23`) running a fixed screening prompt that states the chain's topical scope (steps S1–S8 plus the bundled-target, pragmatic, attribute-puzzle, and methodology categories) with an explicit include-when-in-doubt default. One call was made per item; judgments are checkpointed for all 306 of 306 items with zero unresolved parse failures. The screen included 174 items and excluded 117 as irrelevant; the recorded exclusion reasons are dominated by the expected false positives of recall-first substrings — general metaphysics of ontological commitment, deflationism about truth, pure normative ethics. A further 15 *Mind* items with titles beginning "Review:" were excluded as book reviews irrespective of the model's relevance verdict (each nonetheless carries a recorded judgment). Twenty-one items were screened on title alone, of which 15 were included. The T1 corpus of record is 174 items. One limitation is carried explicitly: T1 membership is defined by a recall-oriented lexical filter followed by a single-model relevance screen, with no independent human or multi-family criterion; T1 selection recall and precision are therefore unidentified, and the corpus-infrastructure contribution is scoped accordingly.

**Deduplication and identifier integrity.** Merging is DOI-keyed wherever a DOI exists; the 143 non-DOI APQ backfill records are keyed by OpenAlex work identifiers under the backfill calibration described above. Every pipeline stage logs an identifier-uniqueness check: the final T2∪T3 corpus contains 3,362 unique DOIs in 3,362 rows with zero cross-journal duplicates; the T1 candidate set 296 unique in 296; the APQ backfill 151 unique identifiers in 151 rows (8 DOIs plus OpenAlex work IDs).

**Copyright isolation.** Abstracts are copyrighted text. They are held in local storage excluded from version control, are never pushed to public remotes, and are not reproduced in this paper, the sealed protocol, or any public release; what is published is bibliographic metadata, counts, provenance, and codes. Consistently with this, primary coding operates on the abstract and accessible front matter, with full-text retrieval reserved for candidate positive evidential (POS) items and adjudication cases.

**Corpus of record.** The corpus closed at the coverage gate with the following composition: 2,818 T2 items and 544 T3 items (denominators after the 627 locked review exclusions — 150 source-confirmed, 473 heuristic, 4 harvest-stage; see the decomposition above), plus 174 T1 items screened from 296 keyword candidates augmented by the 151-item APQ backfill. Tier assignments, denominators, the 2004–2008 ("pre-2008") missingness stratum, and the *Faith and Philosophy* sensitivity axis are frozen in the sealed manifest before any confirmatory coding begins.

### 4.2 The instrument

The coding instrument is a fixed, versioned codebook (the v1.4 lineage, frozen at the protocol freeze; every revision is logged in its changelog) that assigns four codes to one sanitized journal-article abstract at a time: the chain step the item bears on (D1), the item's net-effect direction on that step's thesis (D2), the strength of its claim (D3), and the epistemic type of its load-bearing premise (D4). A fifth variable, venue tier (D5), is never coded: it is joined from bibliographic metadata after coding, downstream of the blinded pipeline, so that no judgment about a text can be influenced by where it was published. Coding follows a fixed question order in which earlier questions gate later ones — relevance, special classes, step, direction, strength, type, then confidence, flags, and a one-sentence rationale — with an explicit stop-rule cascade: items routed out at the relevance or special-class stage carry NA on all downstream dimensions under a stated schema. A dimension-independence rule requires each dimension to be coded on its own textual evidence; no dimension's value constrains another except through the stated NA rules, so any direction may combine with any strength and any type.

### 4.2.1 D1: step

D1 locates the item's primary conclusion on the eight-step chain individuated in §3 (S1, an external cause or ground of physical reality; S2, that ground as intentional agent; S3, uniqueness and aseity; S4, perfect goodness; S5, special action post-creation; S6, the Hebrew prophetic tradition as authentic revelation bearer; S7, the bodily resurrection; S8, incarnation and Trinity), or in one of five special classes: B for bundled full-God conclusions argued directly (ontological arguments; generic religious-experience arguments, flagged RE), P for pragmatic wager-type grounds, I for intra-theistic attribute puzzles (excluded from the chain as internal disputes rather than path tolls), M for the methodology of theistic or atheistic case-making itself, and X for items out of scope. A list of binding edge anchors resolves recurrent boundary cases in advance — divine hiddenness is routed to S5 with a flag, arguments from evil to S4, cosmological arguments to a bare cause to S1, design arguments concluding to an agent to S2, resurrection historiography to S7 — trading taxonomic purity for reliability where a stipulation is defensible either way.

### 4.2.2 D2: net-effect direction

D2 codes the item's direction — pro, contra, neutral, or NA — relative to the step thesis, not relative to the paper the item immediately targets. This net-effect rule is the instrument's central dialectical convention: an item rebutting an objection to a pro-step argument is pro; an item defending an objection against a rebuttal is contra; reply chains are traced to the step thesis and the net sign taken, with a CHAIN flag. The rule deliberately detaches direction from authorial worldview: an atheist can write an item whose net effect is pro a step thesis, and conversely (the codebook's "functional direction" hazard note). The neutral code is reserved, by an explicit clarification adopted during calibration (CL-3, below), for verdict-suspension, explicit non liquet, and pure mapping only; a successful defeater-rebuttal or coherence-defense has a directional net effect even when its author asserts nothing about the thesis outright.

### 4.2.3 D3: claim strength, after the precommitted collapse

D3 began as a five-grade ordinal ladder (CS1–CS5) running from bare coherence claims, through defeater-rebuttal and permissibility-without-evidence claims, to qualitative and then explicitly quantitative evidential claims. The precommitted kill criterion for this dimension — adopted before any coding — was that a second reliability failure on D3 would trigger collapse to three levels and a re-gate. That criterion fired (§4.3.4), and the frozen instrument codes D3 at two substantive levels plus NA: DEF (defensive: the item shows a thesis coherent or possible, rebuts an objection or defeater, or claims belief can be warranted without propositional evidence) and POS (positive evidential: the item claims evidence supports, or disconfirms, the thesis, qualitatively or with explicit numbers). The scale is symmetric across directions — a contra-side POS asserts evidence against the step thesis — and the boundary is evidential import, not confidence of tone: a p-value or effect size that quantifies only a data pattern inside a defeater-rebuttal does not make an item POS; POS requires a support claim attaching to the thesis under assessment. Legacy five-grade codes in the diagnostic gold set and the synthetic criterion specifications are mapped CS1–3 → DEF and CS4–5 → POS at scoring, so the collapse preserves the boundary the precommitted analyses require while giving up finer resolution — a stated descriptive loss. D3 is NA when direction is neutral or the item is out of scope; at two categories the ordinal and nominal reliability metrics are mathematically identical; the pilot gate computed the statistic as ordinal for continuity with the five-level rounds, and the frozen plan's notation of record computes it as nominal — the same number either way.

### 4.2.4 D4: load-bearing epistemic type

D4 codes what kind of premise carries the argument: alpha (a priori, conceptual, metaphysical argumentation only), beta (empirical contact — an observational, experimental, or scientific premise carries the argument), or gamma (historical-documentary — ancient testimony or textual criticism carries it), with NA under the stop-rule cascade. The operative test for mixed items is a deletion test on the load-bearing premise: delete the empirical (or historical) premise; if the argument still runs, code alpha; if it collapses, code beta (or gamma). Three refinements, each adopted during calibration in response to logged disagreement patterns, sharpen the test. First, a best-explanation-from-a-regularity sub-rule: if deleting the specific empirical premise leaves a different, purely conceptual argument to the same conclusion, code alpha; if deletion leaves no argument, code beta or gamma. Second, a multi-fatal-premise dominance rule: when more than one premise is deletion-fatal, empirical and historical premises dominate conceptual ones — the item is beta (or gamma) if any deletion-fatal premise is empirical (or historical-documentary), and alpha only when no such premise is fatal. Third, a common-ground rule: premises the text explicitly stipulates as shared ground, presupposed rather than defended, do not count as load-bearing; the deletion test applies to the argument's novel, differentiating premise. A survey/mapping rule completes the schema: verdict-free surveys take D4 = NA unless the item itself weighs evidence, and the type of the surveyed arguments never determines D4.

### 4.2.5 Blindness architecture

The instrument is blind at three layers, each a hard constraint rather than a convention.

First, input sanitization. The coder sees only sanitized text: no author, title, journal, year, or DOI. A scripted sanitization pass — spot-checked at the orchestration level by script assertions and LLM review, with no human reading of items — strips metadata fields and scrubs in-text self-identifiers ("as I argued in [year]", proper-name self-citations that identify the author), while deliberately keeping opponent names — "Swinburne's argument", "Rowe's inference" are content, and removing them destroys codability. Numbered-reference self-citations that expose no name, year, or venue are kept verbatim, since they identify no one. Every scrub is logged, and the sanitization log ships with the corpus. The input unit is the abstract, supplemented by the sanitized first and last paragraphs only when the abstract falls below sixty words (flagged LOWTEXT).

Second, a hypothesis firewall. The prompt deployed to coders contains no hypotheses. The study's hypotheses and analysis plan live in design documents that no coder-facing context ever receives; the codebook's own rationale states the constraint in instrument-neutral terms — a coder that knows the study's expectations will drift toward them, so the instrument must be usable by a coder who has never seen the paper's thesis. The firewall is enforced by process, not intention: coder-facing contexts receive only a built prompt, generated by script from the codebook by concatenation, with the codebook as single source of truth and the prompt as a versioned, git-tracked build artifact whose manifest is machine-verified against the protocol freeze. The build script carries a forbidden-token list; manual edits to the deployed prompt are prohibited.

Third, example hygiene. The nine worked examples in the prompt are synthetic — written for the codebook, not drawn from the literature — so that no real paper's codes are taught by example. When an audit of the initial example set found it uniformly stereotype-congruent, and therefore capable of teaching topic-to-code shortcuts, three counter-stereotypical examples were added (a positive-evidential empirical item on the pro side, a positive conceptual item on the contra side, and a topic-cue-without-verdict neutral item), precisely to break any association between a topic and an expected code. The twenty real gold-anchor texts are fully held out: none appears in the prompt, and they carry no criterion-accuracy weight and are reported only within the recognition stratification as a diagnostic (§4.3.5) — though as pilot-sample members they contributed to the conditional pilot pass (§4.3.4).

### 4.3 Zero-human measurement: coders, adjudication, calibration

### 4.3.1 The zero-human rule

A binding design decision, adopted before the pilot and recorded as an absolute rule, is that no human codes or adjudicates any target-corpus or checkpoint item at any point in the pipeline — the instrument designer included. The disclosed exception at the instrument level is the twenty-item diagnostic gold-anchor key: designer-authored labels, revisable only through a document-level rule (§4.3.3, §4.3.5), excluded from headline validity evidence, and comprising 22% of the pilot gate sample — a share whose effect on the pilot pass is quantified by the gold-exclusion sensitivity in §4.3.4. The designer's labor is confined to instrument design: authoring the codebook, writing and signing off the synthetic criterion-item specifications, and approving phase gates. Item-level disagreements are resolved by a scripted majority rule (§4.3.3); a planned human validation sample was removed along with all other human item-judgment, and validity evidence was relocated to a precommitted validation battery of synthetic-criterion accuracy, recognition probes, cue-ablation baselines, and determinism audits (§4.4). The claim discipline that follows is stated here and in the abstract: this study reports measurement by a fixed, precommitted, multi-family LLM instrument. It does not claim human-equivalent annotation, and no result should be read as if it did.

### 4.3.2 Tri-family coders and the self-consistency majority

Each item is coded independently by three coders from three different model families — A: Anthropic (`claude-opus-4-8` lineage), B: Google (`gemini-3.5-flash` lineage), C: OpenAI (`gpt-5.5-2026-04-23`) — each pinned at freeze in the registration manifest's pin section: C to an immutable dated snapshot; A and B to provider-stable undated identifiers, for which the registration records a fallback protocol — per-call version-metadata logging plus the B1c consolidated-determinism floor — in place of the dated-snapshot requirement those providers' identifiers cannot satisfy. The fallback's content differs by provider and is stated exactly: B's responses carry a `modelVersion` field, logged per call; A's calls pin the API-contract version header and log the response's model-identifier echo — the provider exposes no per-response build identifier, a disclosed limit of the fallback that B1c was registered to backstop. No coder sees another's output. A fourth, open-weights archival coder (D) is mandatory for re-executability after commercial API endpoints retire; its role, like every other model role in the study, is fixed by a precommitted role-exclusivity matrix. For the record of what D actually did: D coded the 150-item checkpoint tranche, three runs per item — the raw three-run column ships with the audit package, unconsolidated, consolidation having been mooted by the halt; it sits outside the tri-family gate statistic by registered role; and no D column exists for the never-run main corpus.

A coder's code for an item is not a single model call. The pinned endpoints are not sampling-deterministic: a determinism audit that re-ran identical invocations measured per-dimension exact-match rates of 95–100% for coder A, 85–95% for B, and 80–85% for C (an earlier 70% figure for C was the all-four-dimensions joint composite, corrected in the plan's threshold register). At pilot scale this decoding noise dominated single-run reliability point estimates (§4.3.4). Each coder's output is therefore defined as the per-dimension majority of three independent runs of the identical prompt against the same pinned model — a self-consistency majority in the sense of Wang et al. (2023), applied per dimension; a three-way run split on a dimension takes the first run's value and flags the item `run_unstable`. The protocol is uniform across coders and cheap in bias terms — it is intended to reduce run-level decoding variability in the reliability signal, though it cannot correct, and may entrench, an error shared across a coder's runs — but not in cost terms: it triples per-coder coding volume for the confirmatory phase, a consequence accepted and budgeted before the freeze. In the pilot the majority was almost always well defined: across all 267 coder-items (89 items × 3 coders), exactly one produced a genuine three-way run split; it was flagged, not silently resolved.

### 4.3.3 Adjudication and the unresolved protocol

Cross-coder disagreements are resolved mechanically. Where two coders agree and one differs, the majority value is adopted and the minority coder logged; where all three differ, the cell is `unresolved`: it is excluded from the primary analysis, and sensitivity bounds are computed under each candidate resolution. The adjudication script is deterministic — re-runs are byte-identical, and the final-round script is regression-pinned byte-identical to the round-one script on the original inputs, so the mechanical rule is provably unchanged across calibration rounds. No human, the designer included, adjudicated, overrode, or tie-broke any item; the designer's only interventions were approvals of codebook document changes (never corpus item codes) before the freeze. One scoping note: the twenty-item diagnostic gold-anchor key is designer-authored instrument material — it was not used as criterion-accuracy evidence and was revisable only through the document-level gold-audit rule (§4.3.5), under which the coders twice overrode it, though as pilot-sample members the anchors did contribute materially to the conditional pilot pass (§4.3.4); the zero-human claim is about corpus and pipeline items, and is stated with that scope here and in the disclosure.

The pilot's final adjudication round gives the flavor of the machinery's output: of 356 item-dimension cells (89 items × 4 dimensions), 280 (78.7%) were unanimous, 70 were resolved 2–1, and 6 were three-way unresolved — all six sitting on the step/scope locus or the direction call that cascades from it, none on strength or type. The full 2–1 resolution matrix (which coder was outvoted, on which dimension, from which value to which) is published, and recurring disagreement patterns were tallied against a fixed recurrence threshold (≥ 3, recorded in the adjudication log) to generate candidate codebook clarifications — always as document changes for designer approval, never as item re-codings. Where a majority resolution contradicted a gold-anchor code, the conflict was flagged and the majority allowed to stand; gold anchors carry no authority over the pipeline (§4.3.5 explains why this humility turned out to be warranted). Finally, because a 2–1 rule can in principle manufacture consensus, headline results are required to be stable across five estimators — unanimous-only, each single coder (A, B, C), and majority — a stability requirement fixed in the validation battery before any confirmatory coding.

### 4.3.4 Calibration: the G1 trajectory, in full

The reliability gate (G1) required a minimum pairwise Krippendorff's α of 0.70 on every dimension, taken over all three coder pairs — a deliberate strengthening of the initial single-pair gate, adopted because all three coders code every item anyway, because gating on the minimum removes the arbitrary choice of a "reliability pair," and because it converts anomalously high agreement in any single pair from an invisible artifact into a visible red flag for correlated family priors. We report the trajectory to that gate in full. The instrument that passed is not the instrument that started the pilot, and the sequence of revisions was made with the gate in view; the honest presentation of that fact is, we contend, the only defensible one, and every round's outputs are archived.

Round 1 (codebook v1.1; coder A then pinned to `claude-sonnet-5`; five-level D3; n = 55: one venue-year plus the twenty gold anchors) failed three of four dimensions: D1 passed at .734, but D2 (.673), D3 (.608), and D4 (.569) fell below the floor. Diagnostically, every failing cell was a coder-A pair. Round 2 applied five hypothesis-neutral boundary clarifications distilled from the mechanically logged disagreement patterns — a decision order for methodology-versus-step-versus-out-of-scope routing; an explicit statement of the stop-rule NA cascade (the largest single pattern proved to be an under-specification of the NA schema, not a coding dispute); the restriction of neutral to verdict-suspension; a tie-break at the coherence/defeater boundary; and the best-explanation sub-rule for the deletion test. These clarifications did not move the gate (.733/.661/.609/.613): the failing cells remained exclusively A-pairs, which is the evidence of record that the residual disagreement was a systematic single-coder isolate rather than document ambiguity. Round 3 accordingly revised the coder-A pin from `claude-sonnet-5` to `claude-opus-4-8` — a pilot-stage instrument change, made before the freeze and fully logged, with the superseded rounds archived. The pin revision lifted D1, D2, and D4 A-pairs, but exposed the five-level D3 as unreliable in its own right (minimum pairwise .479), which triggered the precommitted kill criterion: round 4 collapsed D3 to {DEF, POS, NA}, and the collapsed scale passed on all pairs (.718/.840/.873), leaving D4 (.677) as the sole failing dimension.

The last gap was noise, and we can demonstrate that rather than merely assert it. A fresh single-run re-code of the same 55 items under the round-4 instrument fell further (D1 .647, D2 .640, D3 .868, D4 .690) — point estimates at this sample size were dominated by decoding nondeterminism, with bootstrap confidence intervals roughly ±.15 wide. The final protocol therefore made two changes aimed at the noise, not the content: the majority-of-three self-consistency rule of §4.3.2, and a one-venue-year expansion of the pilot to n = 89 (35 + 34 corpus items from two venue-years, plus the 20 anchors). On that protocol the gate passed on all four dimensions: minimum pairwise α of .736 (D1), .727 (D2), .808 (D3), and .705 (D4), with the three-way joint α clearing .70 on every dimension as well, and the round-1 pathology gone — disagreement was now distributed rather than concentrated in one coder's pairs.

Three qualifications accompany the pass, and we regard them as load-bearing. First, the interval evidence sits near the floor, not safely above it: eight of twelve pairwise bootstrap cells had 95% lower bounds below .70, and the D3 estimate rests on roughly 42 paired judgments after NA exclusion, with correspondingly wide intervals. One cell — perfect D3 agreement between coders B and C — is exactly the anomalously-high-pair signal the minimum-pairwise design exists to surface, and is carried as a named watch item for the confirmatory-phase folklore audit rather than treated as good news. Second, a sensitivity check excluding the twenty gold anchors (22% of the gate sample, and recognition-advantaged because the anchors are famous) drops three cells marginally below .70 (.696, .696, .676), confirming that the anchors contributed to the pass. Third, the five-round sequence is a real researcher-degrees-of-freedom exposure: a gate passed on the fifth look is a selected estimate with an optional-stopping structure, whatever the merits of each individual revision. The declaration of record therefore made the pass explicitly conditional: G1 was declared on the precommitted point statistic, with validity of the sequentially revised instrument conditional on a confirmatory reliability checkpoint frozen at the protocol freeze — a re-computation of the minimum pairwise α on fresh, non-pilot items from held-out venue-years early in the confirmatory run, under a stricter dual statistic (point minimum ≥ .70 and bootstrap 95% lower bound ≥ .667), with a precommitted halt-and-revise trigger. The checkpoint is not decorative; it is the mechanism by which a pilot-calibrated instrument earns the right to code the corpus.

### 4.3.5 The instrument disciplining its designers

Two episodes from calibration deserve a place in the methods narrative because they bear on how the paper's qualitative starting points should be read. The audit's background table of step-level appraisals (§3, Table 1) records qualitative priors — the designers' pre-measurement sense of each step's dialectical situation — and the study treats those priors as claims to be tested, not summarized. What the calibration record shows is that such priors are computable against text and correctable by the instrument, because twice during the pilot the instrument corrected its own designers. We note that neither episode licenses any inference about what the confirmatory measurement will show; their value is procedural.

The first episode concerns anchor A11, a fine-tuning paper that rebuts the multiverse rejoinder by diagnosing an inverse gambler's fallacy. An early working version of Table 1 had shelved it in the contra column — the natural filing for a paper written by an author with no theistic commitments and hostile to a popular naturalistic reply's dialectical neighborhood. The act of gold-coding the abstract under the net-effect rule forced the correction: an item that rebuts an objection to a pro-step argument is functionally pro, whatever its author's worldview, and the table was corrected accordingly. The error was caught not by re-reading the paper but by applying the instrument's own direction rule to it.

The second episode is the sharper one, because the correction ran from the coders to the designer. In the final calibration round, all three families unanimously contradicted the gold codes on three anchors (A04, A05, A07). Under the adjudication protocol those majorities were flagged and left standing, and gold was not overridden — but a unanimous three-family contradiction of a designer-adjudicated key is exactly the pattern one would expect if the key, not the coders, were wrong. The designer re-adjudicated the three anchors from the sanitized text alone and found precisely that: two of the three gold codes had been assigned from the arguments' reputations — a famous hiddenness monograph, the design argument as such — rather than from what the sanitized abstracts actually argue, which in both cases is a reply-chain defeater-rebuttal (defensive, conceptual) rather than a positive evidential case. The third anchor's type code changed under the newly articulated multi-fatal-premise dominance rule. In other words, the memorization failure mode the validation battery was built to guard against in the coders had manifested in the designer, and the coders' unison "misses" were correct readings of the text. The episode was codified into the instrument as the gold audit rule: any unanimous three-family contradiction of a gold code triggers a designer re-adjudication from sanitized text alone, with gold revision remaining a designer-only, document-level act. A second audit round under the same rule subsequently moved two further anchors' step codes across the S1/S2 boundary (one an abstract-versus-paper gap, duly noted) and sustained one challenged strength code with the boundary recorded as a known hard case for the instrument.

We read these episodes as the strongest available evidence that the measurement layer is doing independent work: the instrument's rules, mechanically applied, overrode the intuitions of the people who wrote them — once through a table correction forced by a coding rule, once through three blind coders outvoting their designer's memory of the literature. The confirmatory phase was to test the study's precommitted hypotheses on the frozen instrument (it halted at the reliability checkpoint, §5.1.1); nothing in this section anticipates a hypothesis result, and under the study's kill criteria a null outcome forecloses journal-format claims rather than reframing them.

### 4.4 Validation battery and the protocol freeze

No human codes or adjudicates any target-corpus or checkpoint item in this study. The rule was adopted as a binding design decision before pilot coding began: no human coder, no human item-adjudication, no human validation sample — the disclosed item-level exception being the twenty designer-authored diagnostic gold-anchor labels, instrument material outside headline validity evidence (§4.3.1). The designer's labor is confined to instrument design — codebook authorship, the writing and signing of synthetic-item specifications, and gate approvals. The paper accordingly claims measurement by a fixed, precommitted, multi-family LLM instrument, not human-equivalent annotation; the abstract discloses zero-human coding in its own voice, and every confirmatory verdict is registered in instrument-relative form ("supported, *as measured by the frozen, preregistered multi-family LLM instrument*"), with unqualified truth-of-hypothesis phrasing barred from abstract and conclusions by frozen wording rules (plan §2.6).

The choice buys machine-auditable provenance and partial re-executability (the archived open-weights coder D permits re-execution — not merely re-inspection — of its column after commercial endpoints retire; the column D actually produced is the checkpoint tranche, coded in three runs, the main-corpus column never having been started; the full tri-family ensemble remains re-executable only while the commercial endpoints are served, and exact output reproduction is neither assumed nor claimed — the endpoints are not sampling-deterministic, which is why determinism is audited rather than asserted, §4.4.1), a machine-verifiable audit trail (every judgment is an API call with logged inputs and outputs), and freedom from hypothesis-aware annotation, enforced by a firewall under which no coder-facing context ever contains the hypotheses, the analysis plan, or the battery document itself. What it costs is the ordinary criterion of validity: there is no human gold standard, and — as the battery's preamble concedes as the design's principal limitation — instrument accuracy on the real corpus distribution is *formally unidentified*, because every criterion item available to the design is either famous (hence memorization-suspect) or synthetic (hence distributionally unlike the corpus). The battery's job is therefore not to identify real-distribution accuracy, which no zero-human design can do, but to *bound every artifact class identified in the precommitted red-team battery* — memorization, shared training folklore, style and register leakage, decoding nondeterminism and version drift, majority-vote error-laundering — with precommitted, automatable tests whose pass/fail semantics are frozen at registration.

One threat dominates the architecture, recorded in the battery as the red-team finding of record: the qualitative pattern the study measures coincides with field folklore plausibly present in every coder family's training corpus, so inter-family agreement cannot by itself evidence text-driven coding — three models agreeing may only mean three models sharing a prior. The same discipline governs the study's qualitative starting points: the step-status verdicts of Table 1 (§3) enter the paper only as priors to be recomputed by frozen decision-list predicates (plan §10), never asserted. Twice the instrument has already corrected its designers on this axis — the A11 mis-shelving caught by the act of gold-coding, and the gold re-adjudication episode below — and the battery treats the designers' expectations as one more artifact class to be bounded.

### 4.4.1 Role exclusivity and instrument fixation

The instrument comprises three coder families from disjoint providers (A: Anthropic; B: Google; C: OpenAI, provisionally seated as majority adjudicator), a mandatory open-weights archival coder D of disjoint lineage, and a generator/launderer family E — a GLM-class open-weights model served through an agent API on which the `web_search` tool is structurally omitted from every call. The omission is provable, not asserted: each response's tool-call log and the absence of search results are archived with the artifact hashes. Retrieval-grounded models are barred from every blinded role for the converse reason — their grounding cannot be verified off — and serve only as an unblinded harvest aid that never touches sanitized material. No family appears in more than one role group; conformity checking of E's generations is staffed by a further lineage-disjoint family, since a generator may not certify its own output. API call logs are published with the audit package in redacted form: input payloads are recorded as cryptographic hashes plus metadata (the copyrighted sanitized texts are not republished), while model outputs, sampling parameters, and tool-call traces are published in full.

Fixation is enforced mechanically: model pins recorded in the registration manifest (one dated immutable snapshot, C; provider-stable undated identifiers under the registered version-metadata-plus-B1c fallback (its per-provider content and limits are stated in §4.3.2), A and B), provider deprecation status checked at freeze with no conflicting retirement announcement identified for the coding-plus-reproduction window, and a precommitted mid-run deprecation protocol (halt, substitute, full recode of the affected coder's column — never mixed within one column). Because the pinned endpoints are not sampling-deterministic, each coder's output is the per-dimension majority of three independent identical runs, and determinism is audited at three levels rather than asserted. **B1a**, per-run exact-match determinism, is reported descriptively with a 70% sanity floor (pilot: A 95–100%, B 85–95%, C 80–85% per dimension). **B1b**, the consolidated run-split rate, is capped at 2% with an alarm at 5% (pilot: one three-way split in 89 items for coder C, 1.1% on each affected dimension; zero for A and B). **B1c**, the binding floor, requires the full majority-of-three pipeline, re-run twice on a 50-item checkpoint subsample, to reproduce the consolidated output at ≥ 95% exact-match per dimension per coder. B1c was not measured at pilot; the plan records the projection from measured 2–1 run-split rates that coder C sits at roughly 94–95% on one dimension, and therefore registers *in advance* that the corresponding revision trigger — raising that coder to majority-of-five with mandatory re-consolidation of all its prior items — may fire at P4. A revision trigger whose firing is predicted in the registration cannot later be presented as a surprise or negotiated away.

### 4.4.2 The synthetic criterion set and the discriminator's trajectory

Construct-validity evidence lives in a synthetic criterion set of 60 items (battery §B3). Specifications are authored and signed by the designer — instrument-design labor, within the zero-human rule — each fixing target codes on all four dimensions, content constraints, an anti-folklore flag, a hedging quota, and a length band. Generation to spec is performed by family E; conformity is checked by non-coder families plus mechanical checks (a top-strength item must contain an explicit numeral; a neutral item, no verdict verb), with designer sign-off logged per item before any coding results are seen. Every spec, item, and scoring walkthrough is published, so a reader can falsify any item's claimed target code. Cell coverage is exact: at least 10 items per covered cell over four construct-critical cells — two of them *anti-folklore* cells whose correct codes run against the expected field prior — plus 20 items testing prior-filling (hedged items whose correct code is neutral) and understatement handling (hedged-register positive-evidential items).

The set is split: a development half (30 items) usable during pilot revision loops, and a vaulted half (30) generated and SHA256-hashed *before any pilot coder run*, opened exactly once at the main coding phase, its hash a registration artifact. Whatever overfitting five rounds of instrument revision may have induced, it cannot have been fit to items no model call had yet seen. Vaulted-half accuracy floors are frozen at registration (85% on step, direction, and strength; 75% on epistemic type — the strength floor raised from a provisional 70% calibrated to a since-collapsed five-level scale, vacuous at two levels where chance is 50%); vault failure at P4 blocks all confirmatory claims. The development half scored 97–100% for all three coders at pilot; §4.4.7 returns to the honest reading of that number.

The synthetic set's Achilles heel is detectability, and its handling is worth narrating because a component *failed* and the failure is part of the published record. All synthetic items pass through family-E laundering toward corpus surface statistics; each coder family then classifies real-vs-synthetic in fresh contexts, against a provisional gate of discriminator AUC (area under the ROC curve; Hanley and McNeil 1982) ≤ 0.60. The gate failed in both permitted rounds (AUC .867–.991, then .709–.909 after re-laundering, the precommitted three-round cap reached — capped because an unbounded patch loop would itself become an expectancy channel). Diagnosis attributed the failure to a family-E *style fingerprint*, not memorization: 24% of laundered real items were misread as synthetic against 0% of scrub-only items, and an entity-swap hypothesis was rejected. A natural experiment then bounded the consequence: on the ten items one coder flagged as synthetic in exam mode, its codes were *more* stable across arms, not less (mean 0.50 vs 0.81 dimensions changed) — distinguishability did not propagate into coding. The frozen disposition reports AUC descriptively and moves the gate's teeth to a targeted contamination check, B3-dis′: per coder, a one-sided Mann–Whitney U test (Mann and Whitney 1947; α = .05, ≥ 20 items per group) that flagged items do not show higher code-instability than unflagged, computed over the vaulted half and the checkpoint tranche's real items; failure strips the synthetic-accuracy result of confirmatory weight — a block, not a footnote. The episode instantiates the battery's general policy: no narrative rescue of failed components; failures are published, diagnosed, and replaced by mechanized checks whose semantics are fixed before outcomes exist.

### 4.4.3 The folklore baseline and the memorization bound

The cue-ablation baseline (battery §B2) is the primary anti-folklore instrument. For every item, each family codes, in a fresh context, a *degraded stub* — topic keywords or first clause only, produced by scripted degradation carrying no argumentative content. The stub-coding is the folklore predictor: it quantifies how much of the full-text code is recoverable from topic identity alone, which is what a coder relying on trained priors rather than text would be doing. The pilot feasibility run behaved as an anti-folklore instrument should: direction was poorly recoverable from stubs (stub-vs-full agreement .35–.51 across families) while step identity was highly recoverable (.60–.76) — benign, since a paper's topic largely fixes which step it addresses. The confirmatory machinery is a stratum requirement with mechanized semantics: the *text-driven stratum* comprises items whose adjudicated stub-arm code differs from the adjudicated full-text code on at least one denominator-relevant dimension for the hypothesis at hand, and each headline effect must be re-estimated on that stratum and survive at registered magnitude (stratum odds ratio ≥ 2, confidence interval excluding 1). Failure blocks the confirmatory claim. The point is the threat model itself: an effect existing only among items whose codes a model could have produced from the title was never measured from the literature at all.

The recognition probe (battery §B5) bounds memorization. Every real item is presented, sanitized, to each family in a fresh context with the task of naming author, title, and venue, scored by script against metadata. The probe is validated before use — it must detect ≥ 90% of a planted set of known-famous texts, and did (pooled 19/20 = 95% at pilot). Claim discipline is deliberately narrow: a negative probe excludes *verbatim, item-level recall only*; it does not exclude topic-level priors, which are the cue-ablation baseline's job (the standard caveat from the memorization literature, Duan et al. 2024). Headline effects are re-estimated on the unrecognized stratum, and sign persistence there has been promoted from sensitivity note to confirmatory block, guarded by an evaluability floor (the block applies when the stratum holds ≥ 30 items of the hypothesis's denominator; below that, the analysis is reported as not evaluable and flagged as a limitation — never as passed).

The 20 famous gold anchors carry no criterion-accuracy weight: curated, recognition-advantaged, memorization-suspect, their accuracy is reported only within the recognition stratification, as a diagnostic. They were, however, included in the pilot reliability sample (22% of it) and materially contributed to the conditional pilot pass — the contribution the gold-exclusion sensitivity quantifies (§4.3.4). The caution was vindicated from an unexpected direction. When all three families unanimously contradicted the designer's gold codes on three anchors, the gold-audit rule triggered a designer re-adjudication *from the sanitized text alone* — which found that two anchors had been gold-coded from the arguments' reputations rather than the papers' abstracts, and a third fell to a newly codified dominance rule. The coders' unison "misses" were correct readings; the memorization failure mode the battery guards against in coders had manifested in the designer. This was the second instrument-disciplines-its-makers episode (the first, A11, was a direction mis-shelving in an early version of Table 1 itself, caught by the act of gold-coding). Both episodes are why the paper presents its qualitative priors — including Table 1's qualitative-prior column — as computable, correctable quantities the audit was designed to test, not as settled judgments.

### 4.4.4 Adjudication integrity, estimator stability, and the adversarial probes

Disagreements are resolved by mechanical majority-of-three; three-way splits become `unresolved`, excluded from primary analysis and bounded by recomputation under every candidate resolution. Because majority voting can launder correlated error, the battery instruments the majority itself. A conditional-agreement diagnostic, P(B = C | A ≠ B), is computed per dimension at the confirmatory checkpoint and midpoint (pilot baseline .45–.75 — no lockstep bloc), with a frozen alarm (≥ 0.90 with conditioning n ≥ 20, sustained over two consecutive evaluations) and a frozen response: coding pauses, the adjudicator seat switches to the registered alternative family, all adjudications are mechanically recomputed, the event is logged as a precommitted deviation. No open-ended re-examination is available, because "the designers will look into it" is not a precommittable consequence.

Every headline effect is computed under five estimators — unanimous-only (E0), each single coder (E1–E3), and the primary majority-of-three (E4) — and confirmatory claims require sign stability and confidence-interval overlap across all five, on the directional headline effects only. The contrast effect whose registered prediction is approximately 1 is exempt, for a stated reason: an estimate predicted to sit near 1 will chatter across the null under resampling precisely when the design succeeds, so a stability gate keyed to it would fire on success; it is scored solely by its own registered decision row, with an evaluability floor.

Two adversarial probes give the anti-folklore program teeth on the real corpus. The decision register records why they exist: without them, every blocking gate would be a function of agreement or synthetic accuracy — quantities computed from the same three families whose shared folklore is the named threat — so an instrument in which all three families resolved ambiguous calls toward the field prior would pass every gate. First, the published 2–1 resolution matrix is audited for stub-congruence (a tie-break is stub-congruent when the adopted majority value equals the majority of the families' stub-arm codes; pilot toward-share 0.55), and the *adversarial folklore-flip test* flips the worst-case 25% of stub-congruent tie-breaks in the hypothesis's analysis-critical cells — the subset whose joint flip moves the headline effect furthest toward the null, found by deterministic greedy search from a manifest-hashed script, with denominator membership re-evaluated after each flip. The decision rule must still be met; failure blocks the hypothesis. Second, the unrecognized-stratum persistence block above. A tipping-point analysis and a full-set flip are published as sensitivity notes.

### 4.4.5 Analysis-critical cell floors

The cells that decide the headline analyses are enumerated and frozen at registration (four for the type–direction analysis; eight for the venue-topography analysis). Each carries a per-cell agreement floor (minimum pairwise raw agreement ≥ 0.60 over the three coder pairs, cell membership determined by adjudicated codes, defined at cell n ≥ 15); the four synthetic-covered construct cells additionally carry a per-cell criterion-accuracy floor (≥ 70%); and every cell carries a hard n-floor with a frozen consequence — adjudicated n < 15 at analysis time renders the hypothesis the cell enters non-confirmatory. The floor cannot be waived or read as "not failed," and a companion rule closes the residual arithmetic route: no confirmatory verdict may rest on a confidence interval that required a continuity correction on an empty analysis-critical cell. Venue-tier cells are exempt from the synthetic floor by design — tier is joined from metadata, never coded from text. Cell-wise confusion matrices are published.

### 4.4.6 Missingness and the estimand of record

The corpus gate certified 92.8% abstract coverage on the post-2008 specialist stratum (issue years 2009–2024; 2,496 of 2,690 items) but only 68.8% on the 2004–2008 stratum (462 of 672; 210 abstracts missing). This missingness is structural — an era boundary in publishing practice — not random, and any rate borrowed from post-2008 items would rest on an untestable missing-at-random assumption. The registration therefore aligns the estimand with what the gate certified: the primary confirmatory population is the post-2008 stratum; whole-window (2004–2024) estimates are a precommitted extension. The extension carries its own machinery: a published era×venue bias table built from covariates computable without abstracts; a raw adversarial bound (all 210 missing 2004–2008-stratum items assumed maximally hypothesis-relevant, adversarially allocated — reported once, expected uninformative, to demonstrate why the operative statistic is needed); tipping-point statistics giving the minimum number of missing items that would overturn each decision rule when allocated adversarially over *all* free margins (direction, type, strength, tier), read against upper-confidence-limit expected counts; and three anchored scenarios (M1 all-pro, M2 all-contra, M3 anchored-proportional), M3's anchor frozen in advance as the checkpoint tranche's adjudicated distributions under a logged fallback ladder. A whole-window claim requires the decision rule met on the whole-window estimate, survival under M3, and both tipping-point margins; the post-2008 primary claim depends on none of this.

### 4.4.7 The confirmatory checkpoint and the reliability–claim gap

The pilot reliability gate passed on its precommitted statistic — minimum pairwise Krippendorff's α of .736/.727/.808/.705 across the four dimensions at n = 89 — but the gate report itself documents why that estimate cannot be taken at face value: it is a *selected* estimate, reached on the fifth round of a revision loop with the gate in view (an optional-stopping structure); its interval evidence sits near rather than safely above the floor (8 of 12 pair×dimension bootstrap cells with a 95% lower bound below .70); and a gold-exclusion sensitivity dropped three cells marginally under .70, confirming that recognition-advantaged anchors contributed to the pass. The gate declaration was therefore made *conditional*, by its own banner, on a confirmatory checkpoint at the main coding phase: 150 fresh items with zero pilot overlap, drawn from held-out venue-years by a frozen, seeded, stratified venue×year random draw (script and seed are manifest artifacts — "the first 150 items" is undefined without them), coded in both the raw and laundered arms. The checkpoint statistic is dual, both parts required on every dimension: point minimum-pairwise α ≥ .70, *and* the per-dimension bootstrap 95% lower bound of the minimum-pairwise α — four interval quantities, the minimum over pairs recomputed inside every replicate — ≥ .667, Krippendorff's floor for tentative conclusions (Krippendorff 2004); the interval quantities are percentile-bootstrap lower bounds with nearest-rank quantiles (Efron and Tibshirani 1993). The registered rationale makes the checkpoint load-bearing rather than decorative: under the plan's stated projection — bootstrap-interval shrinkage ∝ √(89/150) ≈ 0.77 applied to the pilot-calibrated intervals — a true-α ≈ .78–.80 instrument passes the interval criterion comfortably while a true-α ≈ .70 instrument fails it. The projection inherits the pilot's category marginals, missingness, and disagreement structure; it is quoted as registered design intent, not as a distribution-free property of n = 150. Failure halts coding entirely, with no confirmatory claims from any already-coded material.

The registered reporting frame is candid about what this buys: *tentative-band reliability, checkpoint-confirmed*. Because α ≈ .70 admits substantial misclassification, and only nondifferential misclassification reliably attenuates odds ratios, a quantitative misclassification sensitivity is precommitted — the primary effect recomputed under nondifferential and direction-differential error scenarios spanning the checkpoint's observed disagreement matrices, with a frozen "reliability-sensitive" qualifier attached to any verdict that does not survive the plausible-differential range. The same candor governs the criterion set: the plan names the gap between near-ceiling development-half accuracy (97–100%) and real-corpus pairwise reliability (.70–.74) as evidence that synthetic items are easier than real ones — "near-ceiling construct validity" is weaker than it sounds, the natural experiment bounds contamination but not difficulty mismatch, and the gap is carried as a quantified limitation.

### 4.4.8 Power and yield

Power planning rests on a pre-freeze calibration sample rather than the design outline's early sketch, which pilot rates showed optimistic by roughly a factor of five. A seeded, stratified sample of 150 abstract-bearing specialist-corpus items, coded single-run by one coder family for calibration only (its confirmatory disposition is itself a registered decision), yields P(chain-step-coded) = 39.3% [31.9, 47.3] and P(positive-evidential | chain-step) = 16.9% [9.5, 28.5]: an effective rate of 6.67%, hence roughly 197 expected positive-evidential items [conservative 89, optimistic 398] on the 2,958 covered abstracts, before general-venue additions and before the full-text second pass, which may add items and may also reclassify abstract-coded ones. The plan corrects the figure per denominator (the type–direction analysis admits mainstream venues only, giving ≈ 162–190 expected items) and freezes a two-stage yield trigger: projected yield below 110 — where power for the registered effect size crosses ≈ .77 — forces harvest expansion before further spend, following a deterministic registered preference order with no discretionary choice. The mid-run yield check is performed by a firewalled script whose only surfaced outputs are the trigger boolean and marginal counts, never cross-tabulations of the quantities under test: an interim look that can change the population definition is defensible only if provably blind to the association under test and deterministic in response. The venue-topography hypothesis, unpowered in the first draft, receives registered expected counts for all eight critical cells and a registered power computation at freeze, with a frozen contingency re-scoping its confirmatory element to the main-effect contrast if interaction power falls below .5 — decided before any confirmatory data exist, the kill criterion re-read against the re-scoped element.

### 4.4.9 The freeze, the gate chain, and the principal limitation

Local protocol immutability is enforced mechanically — a SHA256 manifest with git-based guardian checks; the pre-outcome timing of the freeze lacks independent third-party verification (§4.4.9's correction of record, below). The freeze manifest enumerates twenty-five artifact classes — codebook of record, built coder prompt, the full battery and analysis-plan documents, model snapshot pins (one dated; two provider-stable under the registered fallback), the vault hash, denominator definitions, every analysis and search script with its seeds, the corpus lock, probe templates, the lexicons behind every mechanized band, and the recorded decision register — each SHA256-hashed and machine-verified at every subsequent session by a guardian agent. Post-freeze, no threshold, denominator, decision rule, seed, or consequence may change; deviations that follow a precommitted protocol are logged in the freeze documentation's transparent-changes register, carried into the OSF deposit, and any deviation outside one voids the confirmatory run. A single-authority rule closes the architecture: the analysis plan's confirmatory gate chain is the exhaustive registry of blocking conditions, every battery block maps to exactly one chain item, and no block exists outside the list. Every threshold receives a frozen numeric value and consequence class — block, sensitivity note, or revision trigger — and the audit package publishes all component results, including failures. Statistical conventions are registered at the same specificity: odds-ratio confidence intervals by Woolf's logit method (Woolf 1955) with the Haldane–Anscombe zero-cell correction (Haldane 1956); exact tests after Fisher (1934); rank comparisons by the Mann–Whitney U (Mann and Whitney 1947); bootstrap intervals percentile-based (Efron and Tibshirani 1993).

**Correction of record (v0.9): the OSF registration was not completed when reported.**
Through v0.8 this paper — following the project's contemporaneous records — described an OSF
registration completed on 2026-07-17, and the seed rule ("the OSF registration date") was
executed with 20260717 on that basis. During upload preparation (2026-07-21) the claim was
checked against the OSF account and found false: no web registration existed. What did exist
on 2026-07-17 was the locally sealed freeze — the SHA256 manifest (`PREREG_MANIFEST.txt`),
machine-verified CLEAN by the guardian agent, sealed in the now-public git history (content
commit `83d0b49`; seal commit `bafc712`). Three consequences, stated plainly. (i) The
protocol freeze of record is the sealed git freeze, not an OSF-timestamped registration; the
freeze-before-checkpoint ordering therefore rests on the git commit chain and the internal
consistency of the sealed artifacts, not on an independent third-party timestamp — a weaker
anchor than previously claimed, and the reader should weight it accordingly. (ii) The
checkpoint seed's pre-commitment survives in reduced form: the rule (seed = registration
date, YYYYMMDD) sits inside the sealed plan, and the value used, 20260717 — a pre-specified
constant, reported at the time as the registration date (we do not rename it "the freeze
date": the manifest's own generation timestamp is 2026-07-16T14:27:48Z, and the freeze was
declared on 2026-07-17) — was fixed and recorded with the tranche lock before any tranche
item was coded, and the same value sits in the sealed plan as the calibration-sample seed;
what is lost is the external timestamp the rule was designed to borrow. (iii) The OSF deposit this paper cites (osf.io/rt3zg, DOI 10.17605/OSF.IO/RT3ZG, registered 2026-07-21) is a post-halt archival deposit,
carrying the sealed freeze package and this correction in its transparent-changes section;
it timestamps nothing retroactively. The error — a registration reported complete that was
not — is disclosed rather than repaired into the record, consistent with the paper's
treatment of its other failures.

What the battery cannot do is stated as plainly as what it can. Each component bounds an identified artifact class: the recognition probe bounds verbatim recall; the cue-ablation stratum, topic-prior coding; the synthetic vault, construct failure on items whose true codes are known by construction; the perturbation arms, surface-cue dependence; the determinism audit, decoding noise; the estimator battery and adjudication audits, majority-vote laundering; the adversarial flip and stratum-persistence blocks, direction-correlated tie-breaking. But the union of these bounds is not identification. Accuracy on the real corpus distribution — obscure, hedged, contemporary professional prose, coded by models that have read an unknowable fraction of it — remains formally unidentified, because no item in that distribution comes with a criterion label a zero-human design is permitted to consult. This is the design's principal limitation, conceded in the battery's preamble, embedded in the registered verdict vocabulary, and repeated in the paper's limitation section: the direction-bias probes bound bias; they do not identify accuracy. The claim the architecture licenses is deliberately modest and, we argue, exactly calibrated to its evidence: a locally frozen instrument was built to measure the literature and was evaluated on pilot and checkpoint samples drawn from it; every artifact class identified in its precommitted red-team battery was given a frozen test with teeth (two of those tests were cut short by the halt — B1c never started, and the laundered arm was interrupted mid-run — as §5.1.1 discloses); and every one of those tests, with its outcome, pass or fail, is published.

### 4.4.10 The battery at a glance

The table rearranges results stated in §§4.4.1–4.4.7 and §5.1.1 — no new measurements.
Sample sizes differ per component and are stated in the cited sections (pilot reliability
n = 89; pilot determinism and probe arms n = 20–55; dev-half n = 30; the P4 determinism
sub-audit n = 50; the checkpoint reliability row n = 150). "Not reached" means the gate chain
halted (§5.1) before the component's confirmatory arm ran; "moot under gate FAIL" marks the
two components interrupted when coding stopped (§5.1.1 discloses the proximate interrupter).

| Component | Artifact class bounded | Frozen rule | Pilot phase | P4 checkpoint |
|---|---|---|---|---|
| B1a per-run determinism | decoding noise | descriptive; ≥ 70% sanity floor | A 95–100 / B 85–95 / C 80–85 (%) | A 90–96 / B 96–98 / C 88–90 (%) |
| B1b run-split rate | consolidation instability | ≤ 2% cap; alarm > 5% | worst C 1.1%; A = B = 0 | worst 1.3% — within cap |
| B1c consolidated determinism | majority-pipeline nondeterminism | ≥ 95% exact-match (binding) | not measured (projection: C ≈ 94–95%) | moot under gate FAIL (§5.1.1) |
| B2 cue-ablation baseline | shared folklore / topic-prior coding | text-driven stratum OR ≥ 2, CI excl. 1 | stub-recovery: direction .35–.51, step .60–.76 | stratum test not reached |
| B3-acc synthetic criterion | construct failure | vault floors 85/85/85/75 (%) | dev-half 97–100% all coders | vault unopened |
| B3-dis discriminator | synthetic detectability | AUC ≤ .60 (provisional) | **failed**: R1 .867–.991, R2 .709–.909 | teeth moved to B3-dis′ |
| B3-dis′ contamination check | detectability → coding contamination | one-sided Mann–Whitney U, α = .05 | flagged items *more* stable (0.50 vs 0.81) | moot under gate FAIL (§5.1.1) |
| B5 recognition probe | verbatim memorization | unrecognized-stratum persistence block | probe validation 19/20 = 95% | stratum test not reached |
| Conditional agreement (plan §6.3) | family lockstep | alarm ≥ .90, n ≥ 20, sustained | baseline .45–.75 | .41–.52 — no alarm |
| Estimator battery E0--E4 | majority-vote laundering | sign stability + CI overlap | — | not reached |
| Adversarial folklore-flip | direction-correlated tie-breaks | worst-case 25% flip survives rule | tie-break stub-congruence .55 | not reached |
| Cell floors | sparse-cell artifacts | agreement ≥ .60; accuracy ≥ 70%; n ≥ 15 | — | not reached |
| **Confirmatory checkpoint** | selected pilot estimate | min-pairwise α ≥ .70 **and** bootstrap LB ≥ .667 | pilot gate .705–.808 (selected) | **FAIL all dimensions** (.676–.736; LB .390–.650) |

**Drafting protocol (outcome-blind).** The remainder of this manuscript, including the Results section that follows, was drafted and assembled after the P3 protocol freeze materials were prepared — corpus lock, frozen codebook and built prompt, validation battery v1.3, analysis plan v1.1 — and before any confirmatory (P4) coding run or (P5) analysis existed. Each section was written under an explicit outcome-blind rule: no result of H1 or H2 is stated, implied, or foreshadowed anywhere in the draft, and every empirical cell was marked [TO BE FILLED AT P5] (resolved at P4 — see the §5 resolution note). The claim that the Results shells predate the results is itself mechanically checkable: the project's standing practice is to commit every phase artifact to a version-controlled repository under dated, phase-tagged messages, so this assembled draft enters the commit history before the confirmatory run begins. At P5 the shells are filled, the verdict sentences are returned by the frozen decision rules quoted verbatim below, and nothing else in the section may change; interpretation is confined to the four precommitted outcome scenarios of §5.7, stated with equal standing before the data exist.

## 5. Results

This section is written, in its entirety, before the confirmatory data exist. Its structure,
table shells, decision rules, and reporting order are fixed by the precommitted analysis plan;
at P5 the shells are filled and nothing else changes. Two constraints govern everything below.
First, the primary confirmatory estimand is the post-2008 population (the stratum on which the
corpus gate certified 92.8% abstract coverage); whole-window (2004–2024) estimates are a
precommitted extension carrying their own gate (§5.5). Second, all confirmatory verdicts are
instrument-relative: the registered sentence form is "H1 [H2] supported, as measured by the
frozen, preregistered multi-family LLM instrument" ("preregistered" being the sealed plan's own frozen wording, retained verbatim per the terminology note), and unqualified "the law holds" phrasing is
barred from the abstract and conclusions.

**P4 resolution (added 2026-07-17, dated).** The gate chain below resolved at its first item:
the confirmatory reliability checkpoint failed on all four dimensions (§5.1.1). Under the
frozen decision tree, no confirmatory coding was performed, no outcome data exist, and every
downstream shell in this section resolves to *not run* rather than to a filled cell. Per the
outcome-blind drafting protocol above, the shells, decision rules, and scenario texts are
retained verbatim as committed before the result was known; the edits dated to this resolution
are enumerated exhaustively in the back-matter resolution note (v0.2) — the change inventory
of record for the P4 resolution.

### 5.1 Gate-chain status (reported first)

No headline estimate is interpreted before the confirmatory gate chain is reported. A result
may be reported as confirmatory only if all ten items hold; otherwise the run degrades to a
descriptive map. The chain is the exhaustive registry of blocking conditions — no block exists
outside it.

| # | Gate item (plan §2.4) | Status |
|-----|-----------------------------------------------|------------------------------------------------|
| 1 | P4 reliability checkpoint (dual statistic, n = 150) | **FAIL — all four dimensions (§5.1.1)** |
| 2 | B2 text-driven stratum retention | not reached — chain halted at item 1 |
| 3 | B3 vaulted-half synthetic accuracy ≥ frozen floors | not reached — chain halted at item 1 |
| 4 | B3-dis′ coding-contamination check | not reached — chain halted at item 1 |
| 5 | B6 estimator stability (directional effects only) | not reached — chain halted at item 1 |
| 6 | B8 analysis-critical cell floors (incl. n ≥ 15 at analysis time) | not reached — chain halted at item 1 |
| 7 | B5-strat sign persistence, unrecognized stratum (where evaluable) | not reached — chain halted at item 1 |
| 8 | Adversarial folklore-flip survival (25% fraction) | not reached — chain halted at item 1 |
| 9 | Missingness criteria (whole-window extension claims only) | not reached — chain halted at item 1 |
| 10 | Hypothesis-specific decision rule met | not reached — chain halted at item 1 |

Failure of item 1 halts P4 entirely; failure of 2–5 blocks all confirmatory claims; failure of
6–8 blocks the affected hypothesis; failure of 9 blocks only the whole-window extension. All
component results, including failures, are published (battery §B10).

### 5.1.1 The checkpoint result (P4, 2026-07-17)

The checkpoint's tranche draw, sanitization, raw-arm coding, and dual statistic executed
per the frozen pipeline and thresholds, with one documented protocol discrepancy — the seed rule's stated date source (the OSF registration) never occurred, and the pre-specified constant 20260717 was used in its place (§4.4.9): n = 150 fresh items drawn by the seeded stratified
rule (seed 20260717 — a pre-specified constant, recorded with the tranche lock before coding and appearing in the sealed plan as the calibration-sample seed; the frozen rule's stated date source, the OSF registration, went unrealized — §4.4.9; five venues, twenty-one years; zero pilot
overlap; pilot venue-years excluded wholesale), sanitized by the frozen pipeline, and coded in
three independent runs by each API coder with per-dimension majority-of-three consolidation.
Coverage was complete (150/150 items in all three coder files); the bootstrap ran at the full
B = 1,000 with zero degenerate replicates; the statistic implementation enforces the frozen
parameters and refuses off-spec input, and its hash is registered in the guardian log.

| Dimension | α(A,B) | α(A,C) | α(B,C) | min pairwise | bootstrap 95% LB | dual gate |
|---|---|---|---|---|---|---|
| D1 step | .7357 | .7748 | .7777 | .7357 | .6499 | FAIL (LB) |
| D2 direction | .6761 | .7460 | .7701 | .6761 | .5716 | FAIL (point, LB) |
| D3 strength | .8227 | .6913 | .7484 | .6913 | .3895 | FAIL (point, LB) |
| D4 type | .7053 | .7538 | .7326 | .7053 | .5863 | FAIL (LB) |

Gate: point min-pairwise α ≥ .70 on every dimension **and** per-dimension bootstrap 95% lower
bound ≥ .667. Statistic 1 failed on D2 and D3; statistic 2 failed on all four dimensions.

The sub-audits do not rescue the result — they localize it. Run-level determinism (B1a, n = 50,
two extra invocations per item per coder) passed for every gate coder (A, B, C) on every dimension (A .90–.96,
B .96–.98, C .88–.90 exact-match, all above the frozen 70% sanity floor). The consolidated
run-split rate (B1b) was at most 1.3% per coder per dimension, within the 2% cap. The
family-correlation watch (plan §6.3) read P(B = C | A ≠ B) between .41 and .52 on all dimensions,
far from the .90 collusion trigger. On the audits that ran, the failure is not
explained by run-level decoding noise (B1a/B1b), the precommitted B–C correlation watch did
not trigger, and it is not a computational artifact; the consolidated-pipeline rerun (B1c)
never started, so consolidation-level nondeterminism is bounded only by the projection
registered in the plan. What remains is most directly consistent with substantive disagreement among three model
families about what fresh abstracts say, at a level the frozen gate was designed to catch. Two components of the
checkpoint did not complete: the laundered-arm coding was interrupted mid-run (coder A 150/150,
coder B 65/150 at the stop) and the B1c pipeline-rerun audit never started. The proximate
interrupter was a PI-ordered spend stop, issued the same day as — and independently of — the
gate computation; the gate failure is the governing, precommitted reason coding does not
continue, and both components, moot under it, are disclosed in the audit package.

Two readings of the gap between the pilot gate (min pairwise .705–.808 at n = 89) and the
checkpoint (.676–.736 at n = 150) present themselves. The first was anticipated in the
protocol freeze itself — selection: the pilot estimate followed five sequential codebook
revisions under an optional-stopping structure, and §6 of the frozen plan states that "a
true-α ≈ .70 instrument will fail statistic 2 — which is the intended behavior (the checkpoint
is load-bearing, not decorative)." The second is a post-hoc reading, not precommitted —
domain shift: the pilot drew on two journal-years; the tranche spans five venues and
twenty-one years, including strata (early-2000s issues, shorter abstracts) the pilot never
saw. On either reading the conclusion for the measurement claim is the same:
the instrument's reliability on the population it was built to measure is at or below the
tentative band, and the design's own rule — no confirmatory measurement on such an
instrument — governs.

### 5.2 H1 — type–direction hypothesis

Population: DEN-H1 (mainstream-venue T1∪T2, S-coded, POS-strength items), post-2008 primary.

| D2 direction | D4 = α | D4 = β∪γ | Total |
|---|---|---|---|
| pro | *not run* | *not run* | *not run* |
| contra | *not run* | *not run* | *not run* |

OR_H1 with Woolf 95% CI: *not run*. Fisher exact p: *not run*.
Registered prediction: OR_H1 ≥ 3.

Preregistered decision semantics, quoted verbatim from the frozen plan (§2.2):

| Outcome | Verdict |
|---|---|
| 95% CI lower bound > 1 **and** point OR ≥ 3 | H1 supported at registered magnitude |
| 95% CI lower bound > 1 and 1 < point OR < 3 | H1 directionally supported, registered magnitude not met (reported as such; no re-framing) |
| 95% CI includes 1, or point OR ≤ 1 | **H1 null** (kill-criterion input) |

Verdict returned by the frozen rule: *not run*.

### 5.3 H2 — venue topography

Population: DEN-H2 (tiers T1∪T2 and T3), post-2008 primary. The 2×2×2 shell:

| Tier | Direction | POS | DEF |
|---|---|---|---|
| T3 | pro | *not run* | *not run* |
| T3 | contra | *not run* | *not run* |
| T1∪T2 | pro | *not run* | *not run* |
| T1∪T2 | contra | *not run* | *not run* |

OR_pro: *not run* · OR_contra: *not run* · ROR with 95% CI:
*not run*. Registered predictions: (i) OR_pro > 1; (ii) OR_contra ≈ 1 or < 1;
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
Verdict returned by the frozen rule: *not run*.

### 5.4 Estimator battery

Headline effects under five preregistered estimators (E4 = majority-of-three is primary).
Confirmatory stability — sign stability, CI intersection with E4, and per-family OR ratio in
[0.5, 2] — applies to the directional effects only (OR_H1, OR_pro, ROR); OR_contra is exempt
because it is predicted ≈ 1, and is published descriptively.

| Estimator | OR_H1 (95% CI) | OR_pro (95% CI) | OR_contra (95% CI) | ROR (95% CI) |
|---|---|---|---|---|
| E0 unanimous-only | *not run* | *not run* | *not run* | *not run* |
| E1 coder A only | *not run* | *not run* | *not run* | *not run* |
| E2 coder B only | *not run* | *not run* | *not run* | *not run* |
| E3 coder C only | *not run* | *not run* | *not run* | *not run* |
| E4 majority (primary) | *not run* | *not run* | *not run* | *not run* |

Alternative-seat co-analysis (adjudicator = A): *not run*. Frozen divergence rule: if
the two seatings yield different verdicts on any hypothesis, confirmatory language for that
hypothesis is withdrawn.

### 5.5 Missingness and estimand sensitivity

The pre-2008 stratum (672 items; 210 missing abstracts) is structural missingness and is
modeled, not hidden. Three preregistered deliverables:

Era×venue bias table — rows = venue, columns = era (2004–2007, 2008–2024); cells = item count,
abstract coverage, and abstract-free covariate profiles (article type, frozen-keyword topic
profile, page count): *not run*.

Tipping-point statistics — minimum number of missing items that overturns each decision rule
under adversarial allocation over all free margins:

| Hypothesis | TP_pos | UCL comparator (POS) | TP_free | UCL comparator (in-chain) |
|---|---|---|---|---|
| H1 | *not run* | *not run* | *not run* | *not run* |
| H2 | *not run* | *not run* | *not run* | *not run* |

Anchored scenario envelope (M1 all-pro / M2 all-contra / M3 anchored-proportional, anchor =
checkpoint-tranche adjudicated distributions): *not run*. A whole-window extension
claim requires the decision rule met on the whole-window estimate, survival under M3, and both
tipping-point margins exceeding their UCL comparators. The post-2008 primary claim does not
depend on any row of this subsection.

### 5.6 Descriptive step-status map (non-confirmatory)

Computed step status per step over T1∪T2 within window, by the frozen ordered decision list —
(1) contested: both directions ≥ k POS items; (2) headwind: exactly one direction ≥ k POS and
the opposing direction zero POS (the status is direction-unsigned; each headwind cell reports
the direction fielding the POS items); (3) frozen: no POS either side in the trailing 10 years;
(4) mixed/sparse: residual — reported at k ∈ {2, 3, 5}:

| Step | Qualitative prior (Table 1, under test) | k = 2 | k = 3 | k = 5 |
|---|---|---|---|---|
| S1 | contested | *not run* | *not run* | *not run* |
| S2 | contested | *not run* | *not run* | *not run* |
| S3 | contested/frozen | *not run* | *not run* | *not run* |
| S4 | headwind | *not run* | *not run* | *not run* |
| S5 | strong headwind | *not run* | *not run* | *not run* |
| S6 | headwind/near-frozen | *not run* | *not run* | *not run* |
| S7 | strong headwind | *not run* | *not run* | *not run* |
| S8 | defensive | *not run* | *not run* | *not run* |

The "qualitative prior" column restates Table 1's status verdicts for what they are: the
designers' pre-audit qualitative reading, which the computation either reproduces or corrects.
These priors are demonstrably correctable, because the instrument has already corrected its
designers twice during construction (§4.3.5). In the A11 episode, the act of gold-coding caught a
designer mis-shelving (an item rebutting the multiverse rejoinder to fine-tuning had been filed
in the contra column; the functional-direction rule now codifies the correction). In the gold
re-adjudication episode, unanimous three-family contradictions of three gold codes triggered a
designer re-adjudication from the sanitized text alone, which found that the designer had coded
two arguments' reputations rather than the papers' abstracts — the very memorization failure
mode the battery guards against in the coders, manifest in the designer; the coders' "misses"
were correct readings, and the gold codes were revised. The prior column above therefore
carries no evidentiary weight in this paper; the computed columns do.

Also registered for this subsection, all *not run*: per-step direction × strength × type maps;
venue-tier topography maps; B-prevalence (input to §7); the S6 scarcity check; flag-class
tallies; per-cell unresolved rates; the published 2-1 adjudication matrix.

### 5.7 Interpretive frames — four preregistered outcome scenarios

The four possible confirmatory outcomes are stated here with equal standing, before the data
exist, so that no frame can be selected after the fact.

Scenario A (H1 and H2 both supported). The type–direction asymmetry and the venue topography
both hold as measured by the frozen instrument. The paper's discussion proceeds on both measured
patterns; the implications-for-cumulative-cases discussion draws on both. No stronger language
than the instrument-relative sentence form is licensed.

Scenario B (H1 supported, H2 not). The type–direction asymmetry holds; venue topography is null
or unestablished. The discussion is confined to the epistemic-type asymmetry, and the
implications-for-cumulative-cases discussion draws on that asymmetry alone; every topographic
claim in the framing is withdrawn, and the H2 null is reported with its full estimator and
sensitivity envelope, not explained away. No stronger language than the instrument-relative
sentence form is licensed for the supported half.

Scenario C (H2 supported, H1 not). Venue topography holds; the type–direction asymmetry is null
or unestablished. The discussion is confined to venue structure, and the
implications-for-cumulative-cases discussion is confined to what venue structure alone licenses;
the H1 null is reported with its full envelope, and no type-asymmetry language survives anywhere
in the paper. No stronger language than the instrument-relative sentence form is licensed for
the supported half.

Scenario D (H1 and H2 both null). The preregistered kill criterion executes: no journal
submission; the project downgrades to a descriptive-map preprint plus essay. No salami-slicing;
no post-hoc hypothesis swaps. The descriptive map (§5.6) and the full battery results are
published regardless — a two-null outcome is a finding about the literature's structure and is
reported as such, and the implications discussion is limited to what the descriptive map
licenses (§9).

**Realized branch (added at P4 resolution, 2026-07-17).** None of the four scenarios activated.
The realized outcome sits one node higher in the frozen decision tree: gate item 1 failed, so
no confirmatory estimate was ever computed and no outcome scenario was reached. This branch is
not an escape from the scenario discipline — it is itself preregistered, with its own frozen
consequence (halt; no confirmatory claims; PI chooses between descriptive downgrade and full
redesign, the revision budget being exhausted). The project takes the downgrade: this
manuscript is the preregistered-trajectory report, and the kill criterion's publication rule applies
by extension, verbatim from Scenario D: "no journal submission; the project downgrades to a
descriptive-map preprint plus essay. No salami-slicing; no post-hoc hypothesis swaps."

## 6. Robustness battery (preregistered shell)

*Shell-adjacent resolution note (added v0.8; the shell below is unchanged from the registration except its dated v0.2 resolution markers, inventoried in the v0.2 note): the shell's phrase "all admissible grains" is the registration's shorthand for R1's three enumerated variants (§7.5(v)); none of this section's items was run (§5.1.1).*

All items in this section are non-confirmatory and are published in full, whatever they show.

- R1 — alternative partitions. Headline effects recomputed at the 7-step grain (S7+S8 merged),
  the 10-step grain (S3 and S4 split; supplementary coding pass under a frozen build-variant
  prompt), and the liberal-target variant (S7 dropped). Invariance claim requires the decision
  rules re-met across all admissible grains; per-grain divergences reported.
  *not run*
- R2 — *Faith and Philosophy* tier flip. H2 recomputed with *Faith and Philosophy* assigned T3; both assignments
  published; the frozen tier table is primary. *not run*
- R3 — dominant-author exclusion. Items by Swinburne, Plantinga, Draper, Oppy dropped
  (metadata join, post-coding); H1/H2 recomputed. *not run*
- R4 — time split. 2004–2013 vs 2014–2024, plus the 2008 era boundary; topography per window.
  *not run*
- R5 — citation-weighted rerun. Weights = log(1 + citations), single frozen snapshot;
  robustness-only by preregistered fiat. *not run*
- B7a — reversed-default deletion test. D4 re-derived under reversed tie-break polarity;
  tie-break-decided fraction reported; H1 under both polarities. *not run*
- B7b — strata monitors and the metadata-only prior-ceiling baseline. *not run*

Mirror audit (exploratory appendix, preregistered for the honesty rule). A three-step
naturalism mini-chain — N1 cosmogenesis/brute-fact viability, N2 naturalistic fine-tuning
response, N3 naturalistic account of consciousness — coded over the same window with the same
coder families and blinding, using a mirror build variant of the frozen codebook, capped at
roughly 200 items. Published whatever it shows, including a naturalist a-priori zone if one is
present. No confirmatory status.

| Mirror step | Direction × strength × type map | Notes |
|---|---|---|
| N1 | *not run* | *not run* |
| N2 | *not run* | *not run* |
| N3 | *not run* | *not run* |

## 7. Formal appendix — burden invariance and canonical partitions

This appendix states the paper's one formal result and the definition that gives it dialectical force. We flag the division of labor at the outset, because it is easy to misread: the mathematics below is elementary — a chain-rule identity that any reader can verify in a line — and we claim no formal novelty for it. The contribution is dialectical. The identity disciplines a recurring argumentative move (definitional bundling), and the accompanying definition converts a question usually settled by stipulation — *how many steps does the chain from a bare first cause to Nicene theism contain?* — into a question about the published record that can be audited, and, as it turns out, mis-answered and corrected (§7.2). The formal weight of the paper is deliberately light; the empirical weight is carried by the audit.

### 7.1 The chain-rule identity and the burden-invariance proposition

Let the target proposition be a conjunction

> T ≡ S₁ ∧ S₂ ∧ … ∧ Sₙ,

where (S₁, …, Sₙ) partitions T's content into cells. For the chain audited in this paper n = 8, but nothing in this subsection depends on the value of n. For any body of evidence E and any ordering σ of the indices, the chain rule of probability gives

> P(T | E) = ∏ᵢ P(S_σ(i) | S_σ(1), …, S_σ(i−1), E).   (1)

Call each factor in (1) a *conditional burden*: a conditional probability that an evaluation of the cumulative case must assign and defend. Identity (1) holds for every ordering, and it holds under every coarsening of the partition into blocks: if the cells are grouped into blocks B₁, …, B_k, then

> P(T | E) = ∏ⱼ P(Bⱼ | B₁, …, B_{j−1}, E),   (2)

and each block factor in (2) itself decomposes, by the same identity, into one conditional per cell it contains. Coarsening does not delete factors; it relocates them into intra-block conditionals — that is, into the bundled proposition's own prior structure.

**Proposition 1 (burden invariance).** Fix a partition (S₁, …, Sₙ) of T. Under every ordering and every coarsening into blocks, the evaluation of P(T | E) resolves into exactly n cell-level conditional factors, one per cell. The choice of representation determines only *where* each factor appears — as an explicit factor in the displayed product, or inside a bundle's conditional — never *how many* there are. (Reading each factor as a separately payable evidential *commitment* is the burden principle, defended dialectically in §2 and conceded as an interpretive premise in §7.5(iii); it is not part of the identity.)

*Proof.* Immediate from (1) and (2): each block factor is the telescoping product of the cell factors it absorbs, under the induced ordering. ∎

**Corollary 1 (anti-bundling, conditional on the burden principle).** Given the burden principle — that each cell-level factor counts as a separately payable evidential burden (§7.5(iii)) — definitional bundling cannot reduce the number of evidential burdens. If a bundled predicate G — "maximally great being" is the canonical example — is logically equivalent to a conjunction of cells, then P(G | ·, E) simply *is* the product of the corresponding cell conditionals, now paid inside a single symbol; if G is logically stronger than the conjunction, the operation is no longer mere bundling but *target strengthening*, and its probability is bounded above by the weaker conjunction's. Either way the burdens are relocated, not retired.

Two remarks keep the proposition honest. First, it is representation bookkeeping, nothing more: the proof is the associativity of the chain rule. Second, it is axiologically silent. Invariance of the burden *count* says nothing about the burdens' *magnitudes*; every factor in (1) may, for all the proposition says, be arbitrarily close to 1. A cumulative-case advocate can accept Proposition 1 in full and argue that each burden is paid. The proposition's only bite is that the burdens must be paid severally, in whatever notation: since (1) holds for every ordering, no staging of the argument — no choice of which step "goes first," no absorption of steps into a definition — changes what there is to pay.

### 7.2 Canonical partitions

Proposition 1 is deliberately permissive: it holds for *every* partition of T, including gerrymandered ones. Precisely for that reason, counting burdens requires a privileged partition — otherwise the "number of steps" inflates or deflates with the describer's interests, and the anti-bundling corollary cuts in all directions at once. This is where the paper's individuation criterion (§2) does its formal work.

**Definition 1 (witness certification).** A cell boundary in a partition of T is *witness-certified* iff it is occupied by an extant scholarly position that accepts all prior cells and rejects — or, in the boundary-marking limit recognized in §2, formally suspends judgment on — that cell, and a dedicated peer-reviewed literature disputes that cell specifically. (On the grades in which the occupancy condition is met, see §2 and the note to Table 1.)

**Definition 2 (canonical partition).** The canonical partition of T is a maximal partition each of whose cell boundaries is witness-certified (on uniqueness, see admission (iv) in §7.5: canonicity is claimed as admissibility under the stated criterion, not as a uniqueness theorem).

Definition 2 states a regulative ideal, and the paper claims no more than that for it. The eight-step partition of Table 1 is *not* asserted to satisfy Definition 2. Its boundaries meet Definition 1 in heterogeneous grades (§2; the note to Table 1): one at the hypothesis level (S4), one partly by structural countermodel (S3), one at unverified design-phase status (S2), one construal-scoped (S7 — boundary evidence against the material-continuity construal, not an unscoped stance-witness) — with S4's third witness entry (Mill) likewise unverified, and the finer Mill cut itself an R1-variant boundary rather than one of Table 1's. And several of its cells bundle conjuncts that carry dedicated literatures of their own — S3's attribute package (Hartshorne accepts some conjuncts and rejects others, itself evidence of an internal boundary), S6's bearer and preservation conjuncts (Islam's supersession and *taḥrīf* grounds target distinct content) with the christological construal an adjacent unregistered finer boundary attested by Judaism's literature, and S8's messianic-incarnational inference alongside trinitarian doctrine (Lapide's and Tuggy's distinct targets) — so by the paper's own criterion, finer admissible partitions exist and the eight-step grain is not maximal. What the study registered is a *working partition* at a grain chosen for measurement tractability, with grain variants (R1) registered precisely because the criterion under-determines the grain; the variants were never evaluated, because the instrument failed at the checkpoint. "Canonical," where it appears, names the criterion's regulative target, not an achieved status of Table 1.

**Claim (canonicity).** Witness-certified partitions are the admissible accounting units for cumulative-case arguments; the canonical partition is that standard's maximal completion (Definition 2), a regulative ideal. Witness certification ties the mathematically arbitrary space of partitions to dialectically real joints: it raises the price of gerrymandered inflation (one may not multiply burdens by drawing boundaries no position occupies) and of apologetic deflation symmetrically (one may not erase a burden by bundling across a boundary where a live position stands — Corollary 1 says the burden survives the bundling, given the burden principle (§7.5(iii)); Definition 2 says the boundary was real).

The criterion is side-neutral in formulation, and the witness list for the audited chain shows the boundaries occupied from both sides: the witnesses include positions internal to theism — Hartshorne against the classical aseity–omnipotence package at S3 (uniqueness and uncreatedness he affirms), Wiles against special divine action at S5, Lapide accepting S1–S7 while rejecting S8's messianic-incarnational inference — alongside non-theistic witnesses. A criterion whose certified boundaries are occupied on both sides of the theism divide is a poor vehicle for a hostile prior: the mixture reduces, though it cannot eliminate, the concern that the partition encodes one.

One feature of Definition 1 carries the paper's methodological claim. Its inputs — the existence of a witness position, the existence of a dedicated literature — are *empirical claims about the published record*: findable, countable, and correctable. Table 1's witness assignments, and the qualitative status glosses attached to each cell there ("contested," "headwind," and the like), are accordingly the designers' priors, stated in advance so that the audit can test them; they are not findings, and at the time of writing no corpus results exist. That these priors are genuinely correctable is a matter of project record, twice over. First, the White (Noûs 2000) episode: an early design document (outline v0.2) had shelved that paper in the S1 contra column; the act of gold-coding under the net-effect rule caught the mis-shelving (the paper rebuts the multiverse rejoinder to fine-tuning, hence functions pro), and the table was corrected in the next revision (v0.3). Second, the gold re-adjudication episode: unanimous three-family contradictions of three gold codes triggered a designer re-adjudication from the sanitized texts alone, which found that the designer had coded the *reputations* of two famous arguments rather than the abstracts at hand — the very memorization failure mode the validation battery was built to catch in the machine coders, manifest in the designer. In both episodes the instrument corrected its makers, and the corrections are logged. The partition defended here is offered as computable and revisable under stated rules, not as an armchair fixed point.

### 7.3 Position within the dwindling-probabilities exchange

The multiplicative structure of (1) is not news to the literature; it is the engine of the dwindling-probabilities exchange. Plantinga (*Warranted Christian Belief*, 2000) argued that the probability of full Christian belief, propagated through a chain of stages on historical evidence, dwindles multiplicatively to unimpressive values. Swinburne's reply (*Faith and Philosophy*, 2004b) charged the argument with mishandling how evidence enters at each stage; T. McGrew (*Philosophia Christi*, 2004) pressed a structurally similar objection; Plantinga replied in 2006 (*Philosophia Christi* 8(1), 7–22) — a response his critics in the exchange characterize as a partial retreat: the rejoinder quotes Plantinga (2006, at 12, 17, 19, 21) disclaiming any general refutation of historical arguments and conceding difficulty in seeing how the dwindling-probabilities principle illuminates the case, while judging that his core position stands ("it *is* a retreat," McGrew and McGrew 2006, 24; summary at 37); the characterization originates with the exchange's other party and is reported here as such — followed by McGrew and McGrew (*Philosophia Christi* 8(1), 2006) and, later, Nickel (De Gruyter, 2015).

What matters for present purposes is *how the exchange ended*: not with a disagreement about the probability calculus — all parties compute correctly — but with a dispute over how evidence enters at stages, that is, over the choice of partition and conditionalization structure within which the calculation is run. Both Plantinga's argument and Swinburne's reply presuppose partition choices; neither offers a principled criterion for which choices are admissible. That is exactly the question Definitions 1–2 address. The witness criterion does not referee the exchange — it takes no position on whether the dwindling argument succeeds against any particular cumulative case — but it supplies the missing admissibility constraint that the exchange revealed a need for: a partition is an admissible frame for the multiplicative accounting iff its joints are dialectically real, in the witness-certified sense. This is the paper's claim to a contribution *inside* an existing formal-epistemology debate, rather than merely a measurement exercise adjacent to it.

### 7.4 Relation to Roche and Shogenji (2014)

The nearest formal neighbor is Roche and Shogenji, "Dwindling Confirmation" (*Philosophy of Science* 81(1), 2014), who prove that incremental confirmation dwindles along inferential chains under screening-off conditions. The two results must not be conflated, because they answer different questions with different logical strengths. Roche and Shogenji's theorem concerns confirmation *transmission*: given a chain individuated somehow, and given substantive screening-off assumptions, it tracks how evidential support degrades as it propagates from link to link. Proposition 1 concerns burden *counting* under re-partition: it is a representation identity with no screening-off assumptions and no transmission content whatever. It cannot tell you how support flows along the chain; their theorem cannot tell you whether the chain's length is an artifact of description. The results are therefore complementary rather than competing: transmission theorems presuppose an individuated chain as input, and the canonical-partition machinery says which individuations are admissible objects for such theorems in dialectically contested settings. Nothing in this appendix strengthens or weakens their result, and the paper takes no position on whether the audited chain S₁–S₈ satisfies their screening-off conditions — that is a substantive structural question about the theology, outside the audit's scope.

### 7.5 What the formalism does and does not license

Five admissions, restated compactly. (i) *Elementarity.* Proposition 1 is the chain rule read with an accountant's eye; the paper stakes no claim to mathematical novelty, and its venue case does not rest on formal depth. (ii) *Axiological silence.* Nothing here shows any burden to be heavy; the non-claims of §1 apply with full force, and the appendix is compatible with every burden being paid. The paper takes no position on the truth of any Sᵢ. (iii) *Interpretive load.* The reading of each conditional factor as a separately payable
evidential burden imports an epistemological premise — that holistic evidence does not support
several conjuncts at once at no marginal cost — which the paper defends dialectically (via the
witness criterion) but does not prove; stated exactly, Proposition 1 shows that factorization
accounting is invariant under notational bundling. (iv) *Canonicity, not uniqueness — nor achievement.* No
theorem here shows the witness criterion yields a unique maximal partition; "canonical" names
Definition 2's regulative target (§7.2), what is claimed for Table 1 being witness-anchored
admissibility at its registered working grain; and the grain-robustness check (R1) exists
precisely because rival admissible partitions may exist.
(v) *Grain-relativity.* The integer "eight" is relative to the witness criterion and to the state of the record that certifies it; the grain objection (§8, O1) lives exactly here. The reply is twofold: the paper's empirical hypotheses were required to survive the precommitted grain variants (R1, including the Mill finite-god cut) — the registered operationalization, not a quantifier over every admissible grain; the §6 shell's "all admissible grains" is the registration's shorthand for those enumerated variants, and R1, like all of §6, never ran; and the canonicity argument above ties admissible grains to occupied positions, so that the residual freedom in "eight" is the record's, not the authors'. What the formalism licenses, in the end, is modest and precise: a cumulative case may be stated in any vocabulary its proponent likes, but its burden ledger is representation-invariant, and the ledger's line items are anchored in the dialectical facts on the ground, in the certification grades those facts currently support — facts the registered design undertook to measure rather than presume; §5 records where the attempt stopped.

## 8. Objections and replies

O1 — the grain objection: "eight is arbitrary." The integer is grain-relative and the paper
says so. The individuation criterion (§2) admits a step only where a witness exists — an extant
scholarly position accepting all prior steps and rejecting (or, in the recognized limit, formally suspending judgment on) that one — in the certification grades of §2, and with a dedicated
disputing literature, which ties the partition to dialectically real joints rather than to the
analyst's taste. The formal section (§7) shows that, for a fixed partition, the burden ledger is invariant
under bundling and notational coarsening — not that it is invariant under arbitrary
re-partition — and R1 recomputes both hypotheses at the 7-step, 10-step, and liberal-target
grains. The published claim is not "there are exactly eight steps"; it is that the invariants
under study are not artifacts of the registered grain choices — a claim R1 was built to test
rather than assert, and, the run having halted, never tested (§5.1).

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
accepted or leaned toward theism in the 2009 PhilPapers survey; the 2020 wave reports a similar
balance), and mainstream specialist editors and referees are presumably drawn in part from that
pool — a compositional presumption, not measured board data: the editorial boards, referee
pools, and submission flows of the eleven audited journals were not surveyed — so a
hostile-gatekeeping explanation of a pro-side prevalence pattern would sit uneasily with the
field's composition. This is contextual evidence about composition, not an identification of
editorial or submission mechanisms, and it fixes no causal direction; read that way, it bears on
how safe a uniform-hostility assumption would be, not on the direction or stringency of the
venue comparison, which composition data alone cannot fix.

O4 — the asymmetry objection: "run it on naturalism." The registered design answers it within
budget: the mirror audit (§6) was precommitted to code a three-step naturalism mini-chain with
the same instrument architecture, the same families, and the same blinding, its results to be
published under an unconditional honesty rule — including a naturalist a-priori zone if one
were present. Like every other §6 component, it was never run: the confirmatory checkpoint
halted the study before the mirror's first item (§5.1.1). The design point survives the halt:
naturalism is a low-conjunction target, which is itself part of what the mirror was built to
quantify — conjunctive specificity is a measurable property, not an accusation.

O5 — hostile-prior scheme design: "the partition was built by someone expecting a particular
topography." Three replies. First, the protocol freeze: hypotheses, codebook, thresholds,
denominators, decision rules, and failure consequences are frozen before the confirmatory data
exist, and the frozen gate chain — not the designers — decides what may be called confirmatory.
Second, the witness criterion is side-neutral in formulation: the witness list includes
theists rejecting steps (Hartshorne, Lapide, Wiles, open theism), so the partition's certified
boundaries are occupied by the field's own internal dissent, in the grades the note to Table 1
records, not by the designer's priors. Third, the record shows the instrument
overruling its designers where they were wrong (the A11 and gold re-adjudication episodes,
§4.3.5 and §5.6), and the design treats designer error as a measurable, correctable event rather than an
unexaminable background assumption.

## 9. What the map licenses — and what it does not

**Scope note at P4 resolution (2026-07-17).** No map was produced: the gate chain halted at
item 1 before any corpus coding. This section is retained as the precommitted licensing
statement it was — binding on any future run under a repaired, re-gated instrument — and as
the record of what this design refused to claim without one. What the present paper itself
licenses is confined to the methodological findings of §5.1.1, the design contributions of
§§2–4, and the formal result of §7 (burden invariance), which stands independently of the
failed coding run.

This paper was designed to produce a map of the published dialectic: which steps of the chain are disputed, in
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

These fences guard against over-reading a chain-adverse map; they cut symmetrically. A
contested, balanced, or pro-leaning map is not evidence that any step is true or that the
cumulative case succeeds, just as a headwind map is not evidence of falsehood; the map's
silence about truth cuts both ways.

Not human-equivalent annotation, and not ground truth. The instrument's accuracy on the real
corpus distribution is formally unidentified — every criterion item is either famous-real or
synthetic — and the battery bounds the artifact classes identified in the precommitted red-team battery (memorization, shared
training folklore, register leakage, drift, majority-vote error-laundering) without closing
that gap. A folklore component below the battery's detection floor cannot be excluded; this is
the design's principal limitation and is stated as such wherever a verdict is reported.

What the registered design aimed at is exactly what the subtitle claims: a measurement of the
ditch as a property of the literature. What this paper delivers is narrower — the instrument,
its validation battery, and the precommitted checkpoint that stopped the measurement. Whether
the ditch can be crossed is a question such a map would locate but not answer; producing the
map awaits an instrument that survives its own gate.

## Back matter

### AI-use disclosure

All item coding that occurred in this study was performed by large language models, with zero
human item-coding: no human — including the authors — coded, adjudicated, or validated any
corpus or pipeline item. (The twenty-item diagnostic gold-anchor key is designer-authored
instrument material not used as criterion-accuracy evidence (though included in the pilot reliability sample; §4.3.4), revisable only via the document-level gold-audit
rule — under which the coders twice overrode the designers; see §4.3.5.) The
human contribution was confined to instrument design: codebook authorship, synthetic-criterion
specification and sign-off, and phase-gate approvals. The instrument is a fixed, precommitted,
multi-family ensemble — coder A (Anthropic), coder B (Google), coder C (OpenAI, adjudicator
seat assigned by a precommitted rule), a mandatory open-weights archival coder D, and an
open-weights generator/launderer E structurally barred from search — bound by a role-exclusivity
matrix and pinned in the sealed manifest's pin section (`PREREG_MANIFEST.txt`, Section E) (one dated immutable snapshot, coder C; provider-stable undated identifiers under the registered version-metadata-plus-B1c fallback, coders A and B). Disagreements were resolved by
the mechanical majority-of-three rule across families; three-way splits were recorded as unresolved and handled by
precommitted sensitivity bounds. The paper accordingly claims measurement by this instrument,
not human-equivalent annotation, and the abstract discloses this in its own voice.

Two further disclosures. First, instrument selection at pilot: the pilot reliability estimate
that gated the instrument is a selected estimate — it followed five sequential codebook
revisions under an optional-stopping structure — and for that reason the design treats the
pilot gate as conditional on an independent confirmatory reliability checkpoint on fresh items
at the start of the full run, whose failure halts coding entirely. That checkpoint failed
(§5.1.1), and the halt executed as designed. Second, the full design
trajectory is public: the versioned codebook with changelog, the adjudication logs (including
the episodes in which the coders corrected the designers' gold codes), the decision register
with every designer judgment call and its recorded resolution, the battery results including
failures, and the API call logs that make the no-contact claims verifiable (inputs as hashes and metadata, outputs in full — the copyright rule bars republishing the texts). Prose drafting was
assisted by an LLM (Claude); all analysis code is stdlib-only Python, hashed in the freeze
manifest. Final disclosure wording follows the hosting venue's policy — a preprint venue: the kill
criterion's no-journal-submission rule governs.

### Data and code availability

The audit package (OSF + repository) contains: all analysis and adjudication code with hashes
and fixed seeds; the frozen codebook, prompts, battery, and analysis plan; item-level coded
data and all aggregate tables for every run that occurred (pilot, calibration, and the
checkpoint tranche — the full-corpus run was never performed); the full battery results
including failed components and the two checkpoint components interrupted by the halt; the
adjudication and cost logs. The synthetic criterion vault was never opened (vault opening was
scheduled after the checkpoint) and remains sealed and hash-verifiable in the freeze manifest. The freeze manifest (`PREREG_MANIFEST.txt`, 64 artifacts plus aggregate hashes) is the verification root: any copy of a frozen artifact can be checked against its SHA256 independent of repository history. Concrete public identifiers: repository <https://github.com/dankang21/ditch-audit>; OSF <https://osf.io/rt3zg/> (DOI 10.17605/OSF.IO/RT3ZG — post-halt archival deposit, registered 2026-07-21; per the §4.4.9 correction it postdates the halt and anchors no timestamps); preprint archive **[ARCHIVE-DOI: inserted at first version update after deposit]**. The first public version must carry the repository URL and the OSF deposit URL, each labeled for what it is; the preprint DOI, issued on deposit, follows in a version update. Copyrighted abstracts are not republished: the raw and sanitized
text corpora are excluded from the public package, and the paper reports codes and aggregates
only, with item identifiers sufficient to relocate every source in the published record.
Because API-served models retire, one coder (D) is open-weights with weights, prompts, and
harness archived, so that coder D's column supports re-execution — not merely re-inspection — after endpoint retirement; the column D actually produced is the 150-item checkpoint tranche, three runs per item, shipped raw and unconsolidated, and no main-corpus D column exists, the run having halted; the availability statement in the published version
states this distinction explicitly.

### Version history (summary)

| v | date | one line |
|-------|-------------|--------------------------------------------------------------------------------|
| v0.1 | 2026-07-16 | Outcome-blind assembly: all design sections plus neutral result shells, committed before any confirmatory data existed. |
| v0.2 | 2026-07-17 | Negative-branch resolution: checkpoint FAIL reported (§5.1.1); 91 shell markers resolved to *not run*; claim-scope repairs. |
| v0.3 | 2026-07-17 | Methods-forward repositioning: title swap (registered title retained as subtitle), reading guide, battery-at-a-glance table, bibliography web-verified. |
| v0.4 | 2026-07-20 | First external-review repairs; *Faith and Philosophy* volume-year and 627-lock reconciliation; Table 1 witness-verification fold-in. |
| v0.5 | 2026-07-20 | Second external-review repairs: §8 mirror-audit tense error; dialectical-separability recast; witness grades, with Carnley added as the verified S7 stance-witness; zero-human scoping; pin-record correction; citation completions. |
| v0.6 | 2026-07-20 | Third external-review repairs: the eight-step partition demoted to a working partition (Definition 2 held as regulative ideal; maximality not claimed); Judaism's S6 witness role withdrawn (the cell entry retained only as a cross-reference to the finer-grain boundary), restoring Lapide's S8 coherence; Carnley scoped to the material-continuity construal; gold-anchor pilot contribution stated; n = 150 projection attributed to the registered heuristic; T1-selection and single-journal-H2 limitations added. |
| v0.7 | 2026-07-20 | Fourth external-review repairs: grain claims scoped to the registered variants; "pre-2008" renamed 2004–2008 at editable sites; the 473 heuristic exclusions elevated to a named corpus-definition assumption, with a seeded 20-item source-check disclosing one false exclusion (5%); Table 1's column retitled "Boundary evidence / candidate witness"; S6's definite-article reading and S7's construal scoping stated; residual canonicity-mood sentences softened; coder D's actual execution record stated; four sources added (Adang; Lapide–Moltmann; Ostler; Tindal). |
| v0.8 | 2026-07-20 | Fifth-review (conditional-approval) completions: East 2013 and the Crossref infrastructure paper (Hendricks et al. 2020) added to the references; single-draw statement for the exclusion sample; Corollary 1 made explicitly conditional on the burden principle, with the stronger-predicate case renamed target strengthening; the S6-Islam verification verdict restated as construal-dependent; a shell-adjacent resolution note added above the §6 shell; the version-metadata fallback's per-provider content and limits stated. Identifier placeholders await the registrant's values. |
| v0.9 | 2026-07-21 | **Correction of record:** the OSF registration reported complete on 2026-07-17 was found never to have been completed (account check during upload preparation). The preregistration of record is restated as the git-sealed SHA256 freeze; the seed's pre-commitment is restated (frozen rule plus freeze-date value, recorded before the draw); the OSF deposit is re-scoped as a post-halt archive. Repository published with full history; author ORCID added. |
| v0.10 | 2026-07-21 | Sixth-review repairs — the vocabulary follows the v0.9 facts: title recast to "Prospectively Frozen"; the paper's own voice moves from "preregistered" to precommitted/locally frozen/sealed (shells, quotations, artifact names, the Registered Reports proper noun, and historical notes keep the original term); the title-page footnote corrected to the post-halt deposit; the seed constant no longer called "the freeze date" (the manifest's generation timestamp is 2026-07-16T14:27:48Z); §5.1.1 states the seed-rule discrepancy instead of "executed exactly as frozen"; "exhaustively audited" withdrawn. |

The full change inventories follow below, newest first, and are retained in the preprint
deliberately: they are the in-text counterpart of the paper's outcome-blindness evidence,
whose machine form (commit-level diffs) ships with the audit package.

### Draft revision note (v0.10, 2026-07-21)

This revision responds to a sixth external review (received 2026-07-21, of the v0.9 package),
whose finding was accepted in full: after the v0.9 correction of record, the paper's
vocabulary had to follow its facts. Inventory: **(1) Title.** "A Preregistered Zero-Human
LLM Measurement Design…" becomes "A Prospectively Frozen Zero-Human LLM Measurement Design…"
(the registered title, preserved as the subtitle since v0.3, is untouched). **(2) Vocabulary
of record.** In the paper's own voice, "preregistered" becomes *precommitted* (checkpoints,
kill criterion, battery, thresholds), *prospectively frozen* (the instrument and design, at
headline sites), or *sealed*/*locally frozen* (the protocol and plan); "preregistration"
becomes the *protocol freeze*. Five categories keep the original vocabulary, listed in the
reading guide's new terminology note: the byte-frozen result shells, verbatim quotations
from the sealed documents, historical artifact names (`PREREG_MANIFEST.txt`,
`prereg-guardian`), the proper noun Registered Reports, and the dated revision notes below. **(3) Title-page footnote.** "The
audit package … accompanies the OSF registration" is corrected to a post-halt OSF archival
deposit supplying no pre-outcome timestamp. **(4) The seed constant.** 20260717 is no longer
called "the freeze date" (the sealed manifest's own generation timestamp is
2026-07-16T14:27:48Z, and the freeze was declared 2026-07-17): it is described as a
pre-specified constant, recorded with the tranche lock before coding, appearing in the
sealed plan as the calibration-sample seed, whose stated date source — the OSF registration —
went unrealized. **(5) Protocol adherence stated exactly.** §5.1.1's "executed exactly as
frozen" becomes execution per the frozen pipeline and thresholds *with one documented
protocol discrepancy* (the unrealized seed-rule date source); §4.4.9's opener now claims
mechanically enforced *local* immutability whose pre-outcome timing lacks independent
third-party verification; and "exhaustively audited" is withdrawn in favor of the battery's
identified artifact classes, with the two unrun components named. **(6) Companion documents.**
The essay and the repository README receive the same vocabulary correction; the repository
description is updated. **(7) Post-audit sweep.** A sweep-focused adversarial audit confirmed
fourteen residuals (with overlaps), all repaired before release — chief among them the sweep's
one real transgression: it had rewritten "preregistered" *inside* the sealed plan's quoted
verdict wording at three sites, making the paper misquote the very document whose integrity
it certifies; the original word is restored inside those quotation marks, with a gloss outside
them. Also repaired: two circular "frozen at freeze" substitutions; a "— :" punctuation splice
in §5.1.1; the laundered arm mis-described as "unrun" (it was interrupted mid-run; B1c never
started); a dropped article in §8 O5; the repository README's "registration date 20260717"
brought to the pre-specified-constant wording; and this note's preserved-category count
corrected from four to five (the Registered Reports proper noun). This note, the
version-history row, and the reading-guide range and terminology note are the bookkeeping
changes; nothing else in the document was altered.

### Draft revision note (v0.9, 2026-07-21)

This revision carries one correction of record and the publication bookkeeping that
surrounded it. **(1) The OSF correction.** During upload preparation, the OSF account was
checked before inserting the registration identifier the fifth review requires, and the
project's standing claim — an OSF registration completed 2026-07-17 — was found false: the
account held no registration. The correction is stated in full in §4.4.9 (new paragraph),
and its consequences are propagated: §5.1.1's seed parenthesis now derives 20260717 from the
frozen rule plus the freeze date rather than from an OSF timestamp; §4.4.9's
transparent-changes sentence now names the freeze documentation's register, carried into the
deposit; the AI-use disclosure's "OSF manifest" is corrected to the preregistration manifest
(`PREREG_MANIFEST.txt`); the availability section's identifier slot is re-scoped from
"OSF registration DOI" to a post-halt archival deposit URL, labeled as anchoring no
timestamps. The historical revision notes below, which repeat the original claim, are left
as written: they are the record of what was believed when. Parallel corrections were applied
outside the paper: a dated addendum to `analysis/checkpoint_report.md`, a dated entry in
`CONTEXT.md`, and the repository README's anchor sentence. **(2) Publication bookkeeping
since v0.8.** The repository was published with its full history at
<https://github.com/dankang21/ditch-audit> and the paper's repository placeholder filled; the
author ORCID (0009-0008-1020-9533) was added to the title page; a non-normative English
translation of the Korean operational artifacts (`CLAUDE.md`, the agent definitions) was
added to the repository as `docs/operating-rules-en.md`. This note, the version-history row,
and the reading-guide range are the bookkeeping changes; nothing else in the document was
altered.

### Draft revision note (v0.8, 2026-07-20)

This revision completes the fifth external review's conditional approval (received
2026-07-20, of the v0.7 package): its first two mandatory items — both citation completeness,
covered by item (1) below — and its three recommendations (items (2)–(4)), plus two further
repairs the review discussed short of requiring (items (5)–(6)); the remaining mandatory
item, real identifiers, is registrant-only and outstanding (item (7)). Inventory: **(1) Citation completeness.**
East (2013) — the sampled false exclusion, cited in situ in §4.1 since v0.7 — receives its
bibliography entry, and the Crossref REST API, the harvest's primary infrastructure, receives
its inline citation in §4.1 and entry (Hendricks, Tkaczyk, Lin, and Feeney 2020); references
83 → 85, both web-verified. **(2) Sample-integrity statement.** §4.1's exclusion-sample
passage and the archived memo now state that the date-derived seed was fixed before any
sampled record was inspected and that one draw was made, with no reruns or alternative
seeds. **(3) Corollary 1 conditioned.** The anti-bundling corollary is retitled and restated
as conditional on the burden principle (§7.5(iii)), and its logically-stronger-predicate case
is renamed what it is — target strengthening, not mere bundling. **(4) S6-Islam verdict
restated.** The witness note's opening now reports the S6-Islam assignment as
*construal-dependent* (supported on the definite-article reading stated in the note), not
"confirmed as stated." **(5) Shell-adjacent note.** A one-sentence resolution note above the
§6 shell states that "all admissible grains" is the registration's shorthand for R1's three
enumerated variants and that none of §6 ran; the shell text itself is otherwise byte-intact (its dated v0.2 resolution markers aside).
**(6) Version-metadata precision.** The A/B pin fallback is restated with its per-provider
content and limits: B's per-call `modelVersion` response field versus A's API-contract
version header and model-identifier echo, with the absence of a per-response build identifier
for A disclosed as the limit B1c was registered to backstop; "version-header" is renamed
"version-metadata" at the §4.4.1 and disclosure sites. **(7) Outstanding.** The identifier
placeholders (OSF registration; repository URL; archive DOI at first version update) remain
the review's third mandatory item, completable only with the registrant's values.
**(8) Post-audit sweep.** A focused post-revision audit confirmed eleven residuals (with
overlaps), repaired before release: the shell-adjacent note's "byte-intact from the
registration" overclaim weakened to except-its-v0.2-markers; the witness-note header advanced
to v0.5–v0.8; §1's framework claim brought to the factor/burden separation the abstract and
§7 already carry; the §7.2 Claim's Corollary citation given its condition inline; the Islam
carriage sentence scoped to the stated reading; this note's review-item mapping stated and
its bookkeeping clause added; the references provenance comment's missing v0.5 line restored;
and the release archive repacked (its packaged README had gone stale on the page count).
This note, the version-history row, and the reading-guide range are the bookkeeping changes;
nothing else in the document was altered.

### Draft revision note (v0.7, 2026-07-20)

This revision responds to a fourth external review (received 2026-07-20, of the v0.6 package).
Inventory: **(1) Grain claims scoped to the registration.** §2, §7.5(v), and §8 O1 no longer
quantify over "every admissible grain": the hypotheses were required to survive the
*preregistered grain variants* — the registration's operationalization, not a survey of every
admissible partition — with the §6 shell's "all admissible grains" identified as the
registration's shorthand for those enumerated variants, and R1's never having run stated at
each site. **(2) Stratum renamed.** "Pre-2008" is renamed to the 2004–2008 stratum (issue
years ≤ 2008) at the three editable sites, with the registration's label noted at first use
and the post-2008 stratum glossed as 2009–2024; the frozen shells retain the registered
label. **(3) The 473 elevated and sampled.** §4.1 now names the 473 heuristic exclusions a
*corpus-definition assumption rather than a source-confirmed classification*, and reports a
seeded random source-check of 20 of them (seed 20260720; memo in the audit package): 17
book reviews, 2 editorial introductions, and **one false exclusion** — East, "Infinity Minus
Infinity" (*Faith and Philosophy* 30(4), 2013), a five-page discussion note sitting exactly
on the ≤5-page threshold — a 5% sample rate (exact 95% CI 0.1%–24.9%), disclosed rather than
silently repaired, post-halt corpus changes being barred by the freeze. **(4) Witness-cell
precision.** Table 1's column is retitled "Boundary evidence / candidate witness"; Carnley's
entry is demoted from stance-witness to boundary evidence against the material-continuity
construal (with page loci added: 1987, 72–103 and 231–233); the note states the
definite-article reading on which Islam's supersession rejection engages S6's registered
wording; the *taḥrīf* ground receives its citation (Adang 1996), the trinitarian conjunct its
document (Lapide and Moltmann 1981), and the design-phase entries their sources (Mormon
finitism — Ostler 2001; classical deism — Tindal 1730; Wiles keyed to 1986). **(5) Residual canonicity mood.**
Four §2/§7.2 sentences are softened (the witness condition constrains rather than eliminates
grain discretion; blocking becomes raising the price; condition (3) makes steps conceptually
codeable without guaranteeing non-empty cells in the selected corpus; the mixed witness list
makes the criterion a poor vehicle for a hostile prior rather than an impossibility proof);
§1's "The result is … a map" becomes the intended product, with what stands delivered stated;
the contribution sentence now names the design *and its rejection*. **(6) H2 composition
claims unified.** §1's "uphill explanation" and §8's "conservative on this axis" are replaced
by a formulation consistent with the abstract's composition-only statement: composition
evidence makes a uniformly non-theistic mainstream unsafe to assume and fixes neither the
direction nor the stringency of the venue comparison. **(7) Coder D's record
stated.** §4.3.2, the §4.4 re-executability passage, and the availability section now say
what D actually did: it coded the
150-item checkpoint tranche in three runs (raw column shipped, unconsolidated), sits outside
the tri-family gate statistic by registered role, and produced no main-corpus column.
**(8) Formal separation.** Proposition 1 now resolves evaluations into cell-level conditional
*factors*, with the burden reading named as the interpretive premise it is (§7.5(iii)); the
Table 1 BGV phrase now attributes the withdrawal of reliance to this design, not to the BGV
authors. **(9) Apparatus.** References 79 → 83 (all four additions web-verified); the
gold-anchor phrasing at §1 is unified with the §4 sites; this note, the version-history row,
and the reading-guide range are the bookkeeping changes. The identifier placeholders remain
placeholders pending the upload-time values (review item 6), which only the registrant can
supply. **(10) Post-audit propagation sweep.** A multi-lens adversarial audit of this
revision confirmed twenty-nine residuals (many duplicates across lenses), all repaired before
release: the availability section's D sentence scoped to the tranche column; the Carnley
demotion completed inside the witness note (the residual "stance-witness" clause and the
grade-mixing "at the assertoric grade" phrase); the note header advanced to v0.5–v0.7 with a
column-retitle gloss; two residual "pre-2008" uses renamed; the heuristic-exclusion and
discussion-note universals scoped to the harvest and to the reply-cue signature; §7.2's Claim
brought to "raises the price"; the §2 grain sentence given its never-ran marker; §7.2's grade
census extended to S7's construal-scoped status; the S6 preservation conjunct bridged through
"authentic"; §3's Table 1 introduction aligned with the retitled column; §5.1.1's B1a scope
stated as gate coders A/B/C; the §2 outside-the-pass list extended to Mormon finitism and
classical deism; the sample-draw timeline corrected to the fourth-review cycle; the
Adams/Adang ordering swapped in the references; the East in-situ citation's list status noted
in the package README; and a page-provenance addendum appended to the citations memo. Nothing
else in the document was altered.

### Draft revision note (v0.6, 2026-07-20)

This revision responds to a third external review (received 2026-07-20, of the v0.5 package),
whose central finding was accepted: the partition's formal claims outran the certification its
own verification record supports. Inventory: **(1) Working partition, not achieved canon.**
Definition 2 is retained as a regulative ideal, and a new §7.2 paragraph states that Table 1
is *not* asserted to satisfy it — its boundaries meet Definition 1 in heterogeneous grades,
and its cells bundle separately disputed conjuncts (S3's attribute package; S6's bearer and
preservation conjuncts; S8's messianic-incarnational inference alongside trinitarian
doctrine), so finer admissible
partitions exist and the eight-step grain is not maximal by the paper's own criterion. The
abstract, §1's framework claim, §2, §3's opening sentence, and Table 1's caption now say
"working partition"; "side-neutral by construction" became "in formulation"; "fixed by the
dialectical facts" became "anchored in … in the certification grades those facts currently
support." **(2) The S6/Lapide repair.** The v0.4 re-grounding of Judaism as an S6 witness via
the christological construal is withdrawn — under that construal Lapide would stop at S6,
contradicting his S8 role. S6 stays at its registered wording; Judaism is re-filed as
attesting a finer-grain boundary (the christological construal — which no registered grain
variant carves; its existence is carried as non-maximality evidence, §7.2); the registered S6
boundary is carried by Islam and Hick; Lapide's S8 rejection is
narrowed to the messianic-incarnational inference, with the trinitarian conjunct carried by
Tuggy — and S8's own bundling is acknowledged as further non-maximality evidence.
**(3) Carnley scoped.** His stance-witness role is stated against the material-continuity
construal of "bodily raised" — the construal the step's pro-side anchors defend — not against
every transformed-embodiment reading. **(4) Gold anchors.** "Zero headline weight" is replaced
at three sites: the anchors carried no criterion-accuracy weight but sat in the pilot
reliability sample (22%) and materially contributed to the conditional pilot pass, as §4.3.4's
sensitivity quantifies. **(5) Registered projection, not distribution-free property.** The
§4.4.7 claim that n = 150 separates a .78–.80 from a .70 instrument is now attributed to the
plan's stated shrinkage heuristic (∝ √(89/150) ≈ 0.77 on pilot-calibrated intervals) with its
inherited assumptions named (the companion essay was synced); §5.1.1's causal conclusion is
softened to "most directly consistent with," B1c never having run. **(6) Scope repairs.** The
abstract's H2 conservativeness sentence is replaced by the composition-only statement; the
abstract and §1 disclose that the confessional tier is a single journal (with the registered
tier-flip); a T1 limitation states that selection recall and precision are unidentified
(single-model relevance screen, no independent criterion); "every identifiable way/artifact
class" is scoped to the battery's identified classes at both sites; categorical novelty claims
are sweep-scoped at three sites. **(7) Apparatus.** BGV receives its inline citation in
Table 1; the availability section now carries visible bracketed identifier placeholders and
states the first-version identifier requirement; the PDF carries title/author metadata; the
repository README notes that commits are authored as Daniel Kang, the preprint byline being
Jaehoon Kang, one and the same person. **(8) Post-audit propagation sweep.** A multi-lens
adversarial audit of this revision confirmed nineteen residuals, all repaired before release:
the R1-pricing error in the Judaism re-filing (no registered grain variant carves the
christological construal — R1's ten-step splits S3 and S4 only; corrected in the witness note,
this note, and §7.2's bundling list, which now cites S6's bearer and preservation conjuncts
instead); §7.5(iv) and §7.2's canonicity Claim brought to the regulative-target form; §7.2's
grade census corrected (Mill's cut is an R1-variant boundary, not Table 1's); §2's
outside-the-pass parenthetical extended to Hick; the witness note's header and lineage wording
versioned explicitly; the gold-anchor exclusivity claim repaired at its fourth site (§4.2);
§8 O5's blanket certification claim and §1's roadmap and the reading guide brought to
working-partition wording; §9's artifact-class clause scoped to the battery; the
version-history row's "re-filed off the cell" overstatement corrected; and the companion
essay's version anchor and coda scope synced. No new sources were consulted; no frozen
artifact was touched; beyond this note, the version-history row, and the reading-guide range
that indexes them, nothing else in the document was altered.

### Draft revision note (v0.5, 2026-07-20)

This revision responds to a second external review (received 2026-07-20, of the v0.4
package) and folds in six source-verification exercises whose memos are archived in the
audit package. Inventory: **(1) Tense of record.** §8 O4 stated that the naturalism mirror
audit "codes … and its results are published" — the manuscript's last sentence describing a
never-run analysis as performed; recast to registered-but-not-run with an explicit pointer to
the halt. The §1 instrument paragraph ("is performed") and the §7.5 close ("undertakes to
measure") were recast the same way. **(2) Separability, not non-derivability.** The abstract
and §1 no longer assert "logically independent steps": the criterion individuates
*dialectically separable* steps, with logical non-derivability carried as a witness-supported
conjecture; criterion condition 2 is retitled accordingly; the abstract now separates the
factor-count identity (invariant under notational bundling, for a fixed partition) from the
burden reading (defended, not derived); headline uses of "canonical" are softened to the
criterion-relative sense (§7.5(iv)) in the abstract, §1, the §3 heading, and Table 1's
caption; §2 now names the grades in which the witness condition is met (stance-witness;
hypothesis-level; structural countermodel; second-order suspension). **(3) Witness repairs.**
Carnley (1987; 2019) was source-verified and added as the S7 stance-witness — the boundary
previously carried only by Allison's second-order suspension — with Table 1, the
witness-verification note, and two bibliography entries updated; Bostrom's flag is corrected
from "structural witness" to "structural countermodel"; Table 1's compressed anchors are
normalized (Roberts et al. 2009; Benson et al. 2006; Hume 1748). **(4) Zero-human scope.**
The abstract, §1, and §4.3.1 now state the rule as zero human coding of *corpus or checkpoint
items*, with the twenty designer-authored gold-anchor labels disclosed as the item-level
exception at each site (their 22% pilot-sample share and the gold-exclusion sensitivity were
already reported in §4.3.4). **(5) Pin record corrected to the manifest.** §4.3.2 and §4.4.1
previously claimed full dated snapshot pins with verified retirement dates; the freeze
manifest's Section E records C as a dated immutable snapshot and A/B as provider-stable
undated identifiers under a registered fallback (per-call version-header logging plus the B1c
determinism floor), with deprecation status checked at freeze — the text now says exactly
that, and the ensemble claim is corrected from "exactly reproducible while endpoints remain
served" to re-executability with exact output reproduction neither assumed nor claimed.
**(6) Remaining claim-scope repairs.** §8's gatekeeping reply now marks the editor-composition
premise as a compositional presumption (boards, referee pools, and submission flows were not
surveyed) fixing no causal direction; the 473-reinstatement sentence claims only the loss of
abstract coverage, not blanket uncodability; the full-text second pass "may add or reclassify"
rather than "can only add"; the run-majority protocol is described as reducing run-level
decoding variability while possibly entrenching error shared across runs. **(7) Citations.**
The Plantinga (2006) characterization is upgraded from "secondary-sourced, unverified" to a
page-cited attribution through the same-issue rejoinder (Plantinga 2006, at 12, 17, 19, 21;
McGrew and McGrew 2006, 24, 37), reported as the exchange's other party's characterization;
the Lapide sentence is corrected to its verified source layer (Braaten's introduction quoting
Lapide — Lapide 1983, 15 — not Lapide's own chapters; the circulating p. 92 citation is
wrong); the Lessing "ugly, broad ditch" quotation carries its page (Chadwick trans., 55);
Maimonides (Touger trans., 1987, uncensored text) and the Qur'an (Abdel Haleem 2004) receive
full bibliography entries; the "web-verified" claims are scoped to bibliographic existence
and metadata, with interpretive uses documented in the verification memos. References
75 → 79. **(8) Apparatus.** This version-history summary was added, the reading-guide sentence now
points to it (and to the v0.4/v0.5 inventories), and the full revision notes are retained in
the preprint by decision of record. **(9) Post-audit propagation sweep.** A targeted audit of
this revision found the corrected wordings not yet propagated to four sites, now fixed: the
§4.4 preamble's zero-human sentence (scoped as in §4.3.1, with the gold-anchor exception);
the AI-use disclosure's and §4.4.9 enumeration's pin phrasing (aligned with the manifest's
Section E); §8 O1's invariance claim (fixed-partition bundling, not arbitrary re-partition);
and §2's grade-coverage sentence (scoped to verified boundaries). The companion essay's
zero-human phrase was scoped the same way. Nothing else in the document was altered.

### Draft revision note (v0.4, 2026-07-20)

This revision responds to an external review of the v0.3 package (received 2026-07-20) and
folds in two post-draft verification exercises. No frozen artifact was touched; no result
changed; every edit is inventoried here. **(1) Register and tense.** Residual performed-tense
and result-promising phrasings in the abstract, §1, and §9 were recast to the design mood
("makes two empirical claims" → "registers"; "§5 reports results" → "reports the gate-chain
outcome"; §3's column-reproduction sentence "the audit therefore either reproduces or
corrects" → "was designed to"; §4.4.9's closing claim → "was built to measure … and was
evaluated on pilot and checkpoint samples"; the §9 close now states that producing the map
awaits an instrument that survives its own gate — so the recast set spans the abstract, §1,
§3, §4.4.9, and §9); the
reading-guide sentence on Registered Reports was tightened to claim kinship of spirit only.
**(2) Precision repairs.** "Twenty years" → "twenty-one issue-years (2004–2024)" (abstract,
§1, §3); the abstract now states which arm of the dual statistic failed where, states the three
families × three runs structure in place of "triplicate," and scopes the clean sub-audits to
those that ran; §5.1.1 likewise now separates what the sub-audits exclude (run-level decoding
noise; a triggered family-correlation watch) from what was never measured (B1c consolidation
determinism). **(3) Factual corrections from verification.** The *Faith and Philosophy*
volume-year parenthesis was corrected after a publisher-record check: the year = 1983 + volume
mapping is confirmed for volumes 38–40, and the journal published no 2024 volume at all
(volume 41 = 2025), so the 2024 cell is empty at the source and no volume-41 item entered the
corpus — the previous parenthetical inferred "volume 41 = 2024, unpublished" from the formula
rather than from the record. **(4) Accounting transparency.** §4.1 now decomposes the
627-entry review-exclusion lock (150 source-confirmed; 473 heuristic; 4 harvest-stage entries
outside the post-harvest corpus), states the item-flow arithmetic of record
(3,920 + 65 − 623 = 3,362), and reports the heuristic-reinstatement sensitivity (all 473 lack
abstracts; coverage would fall to 77.1% with no codeable gain). Identifier keying is scoped
honestly (DOI-keyed where a DOI exists; 143 APQ backfill records on OpenAlex work IDs).
**(5) Claim-scope repairs.** "Exact reproducibility" is now "machine-auditable provenance and
partial re-executability," scoped to coder D's column; API-log publication now states the
redaction rule (inputs as hashes and metadata, outputs in full); the zero-human rule's
curation-stage agency is stated explicitly (scripted PDF signature extraction; orchestration-
level sanitization spot-checks; no human item-reading); the majority-theist point (§1, §8) is
hedged to composition-level contextual evidence, with the 2020 PhilPapers wave (Bourget and
Chalmers 2023) added alongside 2014; the §7.3 secondary-source bracket became hedged prose;
§7.5 gains two admissions (the epistemological reading of factorization as separately payable
burdens; canonicity claimed as admissibility, not uniqueness); §2 gains a scope note (witnesses
certify dialectical separability, not model-theoretic non-derivability). **(6)
Witness-verification fold-in.** A source-verification pass over Table 1's witness column
(archived in the audit package) confirmed four assignments and qualified four; §2's definition
now admits suspension witnesses explicitly, Table 1 cells are flagged, a witness-verification
note follows the table (Bostrom structural; Hartshorne qualified, with the §7.2 "aseity–
uniqueness" phrase corrected to the aseity–omnipotence package; Draper/Law hypothesis-level;
Judaism re-grounded on the christological construal; Lüdemann reclassified as step-contestation
literature; Allison's *non liquet* marked as our characterization). **(7) Apparatus.** Fourteen
references added (ten for methods, statistics conventions, and harvest infrastructure —
the 2020 PhilPapers survey among them — and four witness-note sources), with a
registered-conventions sentence in
§4.4.9 and inline citations at first technical use; Table 1's caption marks anchor citations
as exemplars; the availability section names the freeze manifest as verification root and
marks the identifier placeholders (OSF registration DOI, archive DOI, repository URL) to be
filled at upload. The companion essay received the same issue-years correction. Nothing else
in the document was altered.

### Draft resolution note (v0.3, 2026-07-17)

Repositioning for preprint publication, elected by the PI after a four-lens direction review.
Every preserved shell (§§5.2–5.7, §6) is byte-intact from v0.2; body changes are confined to
items (5)–(6) below. Changes of record, exhaustively: (1) title block: main title and subtitle swapped, "LLM" added to the main title
(the v0.1 registered title is preserved as the subtitle's head, converted to title case, with
a new descriptive tail appended: "design, validation battery, and halt report of the audit"); (2) abstract: a
two-sentence methods-report lead prepended (no other abstract text changed); (3) a keywords
line added; (4) a dated "How to read this document" paragraph added after the abstract, citing
the Registered Reports literature as related practice while expressly disclaiming RR status;
(5) §4.4.10 added — a battery-at-a-glance table that rearranges numbers already stated in
§§4.4.1–4.4.7 and §5.1.1, with no new measurements; (6) two bibliographic corrections found by
web verification and applied to the body: §7.3's "Plantinga replied in 2004" corrected to 2006
(*Philosophia Christi* 8(1), 7--22, per the publisher record; the partial-concession
characterization remains secondary-sourced and stays on the must-verify register, the adjacent
must-verify bracket reworded accordingly), and the two
distinct Swinburne 2004 works disambiguated as 2004a (*The Existence of God*, 2nd ed. — the
Table 1 S2 anchor) and 2004b (the *Faith and Philosophy* dwindling-probabilities article —
§§1, 7.3), and one finding re-attributed to its verified source: the argument-strength-ratings
result moved from the De Cruz (2017) key to De Cruz and De Smedt (2016), with the 2017 study's
actual finding (disagreement assessments track prior belief) stated in its place (§1);
(7) this note. All bibliography entries were web-verified against publisher records; the
four remaining judgment calls (the Registered-Reports reference, the Duan et al. 2024
identification, the Hume edition, and the Swinburne 2004a anchor mapping) were approved by
the author on 2026-07-20.

### Draft resolution note (v0.2, 2026-07-17)

At P4 the confirmatory checkpoint failed (§5.1.1) and the PI elected the preregistered
descriptive downgrade. This version resolves the outcome-blind v0.1 shells to the realized
branch. The baseline for the diff is v0.1 as amended by the pre-freeze corpus-lock
reconciliation (commit `83d0b49`, review-exclusion count 620 → 627 in §4.1 — an outcome-blind
edit dated before the checkpoint run). Changes of record in v0.2, exhaustively:

- title block: subtitle added;
- abstract: the final bracket resolved to the negative outcome, and three sentences recast
  from performed/present to design mood ("designed, and preregistered in full, an audit",
  "was to be performed", "Two hypotheses were preregistered"), with the sub-audit clause
  scoped to B1a/B1b;
- §1: two sentences recast ("their preregistered test is reported in §5, where the gate chain
  halted…"; "Two patterns were predicted for test");
- §4.3.3 and the AI-use disclosure: the zero-human claim scoped to corpus and pipeline items,
  with the designer-authored gold-anchor key disclosed as instrument material;
- §4.3.5: the confirmatory-phase sentence recast to past-design mood with the halt noted;
- §1 (roadmap) and §4.4: two "the audit will test" clauses recast to design mood;
- §5 preamble: dated resolution paragraph added, pointing here as the single change inventory;
- §5.1: gate table resolved (item 1 FAIL; items 2–10 not reached);
- §5.1.1 added: checkpoint numbers, sub-audits, the spend-stop disclosure, and the
  selection (preregistered) vs domain-shift (post-hoc) readings;
- all downstream `[TO BE FILLED AT P5]` markers resolved to *not run* (one §5.6 frame word
  adjusted: "Also registered for this subsection");
- §5.7: realized-branch note appended, quoting the Scenario D publication rule verbatim;
- §9: scope note added, and the opening sentence recast to "was designed to produce";
- the drafting-protocol paragraph's marker meta-reference moved to past tense;
- back matter: AI-use disclosure and availability statements updated for the halt (vault
  unopened; coded data = pilot, calibration, checkpoint tranche only; disclosure-venue line
  aligned to the no-journal-submission rule); this note added.

No shell, threshold, denominator, decision rule, or scenario text committed at the baseline
was altered. The baseline commits precede the checkpoint run in the repository history, and
the diff between the baseline and v0.2 is itself part of the audit package.

### Draft repair note (v0.1, 2026-07-16)

This assembled draft was audited against the project record (G1 report, adjudication log,
corpus harvest log, analysis plan v1.1, validation battery v1.3) immediately after assembly and
repaired in place; the section source files (`docs/draft/0*.md`) remain unmodified pre-audit
snapshots. Repairs of record: the pre-2008 covered/missing inversion corrected to 462 covered /
210 missing in §4.4.6 and §5.5, matching the same-session correction in analysis-plan v1.1
(§4.1 already stated it correctly); coder C per-run determinism corrected to 80–85% per
dimension (§4.3.2); the estimator-stability list restored to the battery's five estimators
(§4.3.3); the *IJPR*/*Sophia* residual characterization aligned to the harvest log's prior-pass,
not-individually-source-confirmed verdicts (§4.1); the coder-pin sentence aligned to the
manifest's dated-snapshot requirement, under which the A/B strings are lineage identifiers
(§4.3.2); the prior-art cited-by walks restated as a registered pre-freeze closure step (§1);
outcome-neutrality repairs — the abstract's hypothesis statements recast as subjunctive
that-clauses at registered magnitudes with the kill criterion added, "type–direction law"
renamed "type–direction hypothesis/asymmetry" in all pre-verdict text, migration/needs
phrasing replaced with prevalence/dependence language, Table 1's "defenses only" glosses
scoped to the design-phase anchor set, the headwind predicate annotated as direction-unsigned,
scenario parallelism completed (language cap and implications sentence in all four), and a
symmetric over-reading fence added to §9; plus register and date-coherence repairs (§4 intro,
§4.1 review-exclusion scope, §4.2.3 D3 notation, header note). No shell, threshold,
denominator, or decision rule was altered.
