# The Checkpoint That Killed Our Study — and Why We're Glad It Did

*Companion essay to the preprint "A Preregistered Zero-Human LLM Measurement Design, and the
Confirmatory Checkpoint That Rejected Its Instrument" (draft v0.3). Every empirical figure
below is stated in, and citable from, the preprint; section references point there. This essay
is the second half of the study's preregistered kill-criterion output ("descriptive-map
preprint plus essay") and makes no claim beyond the preprint's.*

---

We built a measurement instrument through five calibration rounds, froze it under a preregistration manifest,
and then a same-day reliability check on 150 fresh items rejected it — all four coding
dimensions, no appeal. The study halted. No hypothesis was ever tested.

This is a success story. Not in the consolation-prize sense. In the boring, procedural sense
that a smoke detector going off during a fire is a success: the checkpoint did the one thing it
was designed to do, on the first occasion it had to do it, against our interests, and we had
frozen ourselves out of every way of arguing with it.

## The setup

The study was an attempt to measure a literature rather than argue with it: twenty-one issue-years
(2004–2024) of peer-reviewed philosophy of religion, ~3,500 articles, each to be coded for which step of
natural theology's inferential chain it addresses, in which direction, at what claim strength,
on what kind of evidence (preprint §§2–4). The coding was to be done with zero human
coding of corpus or checkpoint items — three LLM coder families from disjoint providers, disagreements resolved by
mechanical majority, the whole thing wrapped in a validation battery targeting the artifact
classes that make "three models agree" weaker evidence than it sounds: shared training
folklore, memorization, style leakage, decoding noise, majority-vote error laundering
(preprint §4.4, table at §4.4.10).

Why zero-human? Because the alternative was worse. A human coder who knows the hypotheses is a
bias vector; a human coder who doesn't is expensive fiction after the first hallway
conversation. Machines can be firewalled: the coder-facing prompt never contained the
hypotheses, the analysis plan, or the battery document. And a pinned open-weights coder can be
re-executed after every commercial endpoint retires — reproducibility humans cannot offer.
What zero-human coding costs is stated in the preprint with a bluntness we would defend as its
best sentence: real-corpus accuracy is *formally unidentified*. Everything the battery does is
bound artifacts, not prove validity. Keep that asymmetry in mind; it is the whole story.

## The trap we documented ourselves setting

Our pilot reliability gate passed: minimum pairwise Krippendorff's α of .705–.808 across four
dimensions at n = 89 (preprint §4.4.7). If you have ever run a coding study, you know what
that number conceals: it was the *fifth* round. Four earlier rounds had failed or
under-performed; each triggered an instrument revision — codebook clarifications, a coder-model
swap, a preregistered scale collapse, a run-consolidation protocol change — followed by a
prompt rebuild and a re-code. Round five cleared the bar, and we stopped.

Stopping when you clear the bar has a name — optional stopping — and its effect on the
estimate has a name too: selection. The pilot α was not a measurement of the instrument's
reliability; it was the first of five correlated attempts to clear the bar. The
preregistration says this about itself, in those words ("a selected estimate," §4.4.7), which
is the only unusual part. A score born that way would ordinarily be reported at face value —
ours would have been too, except for one design decision.

## The checkpoint

The pilot pass was declared *conditional* — by its own banner — on a confirmatory checkpoint:
150 fresh items, zero pilot overlap, pilot venue-years excluded wholesale, drawn by a seeded
stratified script frozen in the manifest, coded by the frozen instrument in triplicate, judged
by a dual statistic fixed in advance: point minimum-pairwise α ≥ .70 on every dimension, *and*
a per-dimension bootstrap 95% lower bound ≥ .667. The sample size was chosen so the test would
be load-bearing: a true-α ≈ .78 instrument passes comfortably; a true-α ≈ .70 instrument
fails the interval criterion. The consequence of failure was frozen before the draw: halt
everything, no confirmatory claims from any already-coded material (preprint §5.1.1).

The result: point minima .676–.736 (two dimensions under the .70 floor), bootstrap lower
bounds .390–.650 (all four under .667). Fail, everywhere.

The obvious escape hatches were checked and closed by the sub-audits, which were clean. It was
not decoding noise: run-level determinism passed for every coder (88–98% exact-match across
dimensions). It was not two families ganging up on the third: the family-collusion watch read
.41–.52 against a .90 trigger. It was not a partial batch or a computation artifact: complete
coverage, full bootstrap, frozen parameters enforced by the statistic implementation itself.
Three model families, coding fresh professional prose under a frozen codebook, substantively
disagreed with each other — at a level the pilot, after five rounds of tuning on a
two-journal-year sample, had been selected not to show.

## Four lessons, scoped to one case

Everything below generalizes from exactly one instrument in one domain, rejected by its own
gate. That scope restriction is not modesty theater; over-reading a single rejection is the
same error as over-reading a single pass.

**1. A pilot reliability score measured after revision loops is an advertisement, not an
estimate.** If the loop stops when the score clears the bar, the reported score is the maximum
of several tries. You cannot fix this by being honest about the loop; you fix it by paying for
fresh data the loop never touched.

**2. The checkpoint is absurdly cheap relative to what it protects.** Ours cost a small
fraction of the full coding run it halted (the abstract calls it "cheap relative to a full
run"; the cost logs ship with the audit package), and a fully-run study on an unreliable
instrument doesn't fail loudly — it publishes confidently wrong numbers with three models'
worth of false consensus behind them.

**3. Freeze the consequence, not just the threshold.** The reason our halt actually happened
is not that we are disciplined people. It is that the consequence was written down before the tranche was drawn — the preprint's
realized-branch note records it as "halt; no confirmatory claims; PI chooses between
descriptive downgrade and full redesign, the revision budget being exhausted" (§5.7). (A
coincident PI spend stop, disclosed in the preprint, pointed the same way; the frozen rule is
the governing reason.) A discretionary halt evaluated after seeing .676 would have lost
to "the point estimates are basically .70, and D3's AC pair is an outlier" — we know, because
we felt the pull of that sentence while reading the output.

**4. Publish the corpse.** The preprint reports the design, the battery with its own failed
component (a discriminator gate that lost to a style fingerprint, §4.4.2), the selected pilot,
the rejection, and pages of preregistered result shells resolved to *not run* — preserved
because the commit history of those unfilled shells is part of the proof the study was
outcome-blind.
Negative instrument results appear to be rare in the LLM-annotation literature; we suspect
that is not because instruments rarely fail.

## What we are not saying

Not "LLMs cannot code philosophy." One instrument failed one gate; a better codebook, or a
harder collapse of the taxonomy, might pass — the preregistration's own kill criteria priced
that path (full redesign, gate cycle restarted from zero) and the project declined to spend
it. Not "the agreement was low because the task is subjective" — if the construct is real,
inter-family disagreement is a measurement problem; if it isn't, no amount of agreement would
have helped. And not "the pilot was fraudulent" — the pilot was ordinary. That is the point.
The ordinary practice, executed carefully and documented completely, produced a number that
fresh data contradicted within days.

## Coda

Lessing's ditch — the gap between historical evidence and doctrinal certainty that the
original study meant to measure as a property of a literature — remains unmeasured. What got
measured instead is narrower and, we think, worth the substitution for what it teaches:
exactly how far a carefully tuned pilot number stands from the same instrument's behavior on
data it has never seen, and what it takes, procedurally, to be forced to believe the second
number over the first.

The full audit trail — frozen manifests, coder logs, the checkpoint's machine report, the
unfilled shells, and the diff proving the shells predate the result — accompanies the preprint.

*[Preprint DOI/link to be inserted at upload.]*
