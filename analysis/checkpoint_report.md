# P4 Confirmatory Reliability Checkpoint — Report of Record

Date: 2026-07-17 · Tranche seed: 20260717 (OSF registration date, §2.5) ·
Statistic implementation: `pipeline/05_analysis/checkpoint_stats.py` rev 2
(sha256 `b1d113cd…`, registered in guardian log) · Machine report:
`analysis/checkpoint_dual_raw.json`

## Verdict: **FAIL — dual statistic not met on any dimension** (plan §6, frozen)

| dim | α(A,B) | α(A,C) | α(B,C) | min | 95% LB | gate |
|---|---|---|---|---|---|---|
| D1 step | .7357 | .7748 | .7777 | **.7357** | **.6499** | FAIL (LB < .667) |
| D2 direction | .6761 | .7460 | .7701 | **.6761** | **.5716** | FAIL (point < .70) |
| D3 strength | .8227 | .6913 | .7484 | **.6913** | **.3895** | FAIL (point < .70) |
| D4 type | .7053 | .7538 | .7326 | **.7053** | **.5863** | FAIL (LB < .667) |

Gate: point min-pairwise ≥ .70 on every dimension AND per-dimension bootstrap
min-pairwise 95% LB ≥ .667 (B = 1,000, seed 20260717, nearest-rank, one shared
draw per replicate). **Statistic 1: FAIL (D2, D3). Statistic 2: FAIL (all
four).** Computation integrity: n = 150/150 complete triples, id sets
identical, b_effective = 1,000 on all dimensions, 0 degenerate replicates,
frozen parameters enforced by the implementation (exit 1 = gate FAIL).

## Sub-audits (do not rescue the gate; reported per §6 "also reported")

- **B1a run-level determinism (n=50, seed 20260717): PASS** — all coders all
  dims above the 70% sanity floor (A .90–.96, B .96–.98, C .88–.90). Report:
  `data/battery/det_report_det_tranche_ckpt_s20260717.json`.
- **B1b consolidated run-split rate: PASS** — worst cell C/D1 = 1.3%; all
  ≤ 2% floor, no 5% alarm.
- **§6.3 conditional agreement P(B=C | A≠B):** .41–.52 across dims
  (trigger ≥ .90 with n ≥ 20) — **no family-lockstep alarm**. The failure mode
  is generic disagreement, not a B/C bloc.
- **B1c consolidated-pipeline determinism: NOT RUN** (PI budget stop; moot
  under gate FAIL — its consequence is a k-raise for continued coding, and
  coding is halted).
- **Laundered arm: INCOMPLETE** (coding interrupted by PI budget stop at
  r1: A 150/150, B 65/150; partial files retained under
  `data/coded/laundered_tranche_ckpt.r1_*.jsonl`, unused). Laundered-arm
  eligibility therefore unmeasured — moot under gate FAIL.

## Frozen consequence (plan §6 "On FAIL", verbatim obligations)

1. **P4 coding halted immediately.** Main coding (~3,048 items) was never
   started; no further API spend.
2. **No confirmatory claims from any already-coded material.** The G1
   conditional PASS's condition clause has now resolved **negative**: the G1
   declaration does not convert to a confirmed instrument.
3. **dk decides between descriptive downgrade and instrument redesign.** The
   G1 revision budget is exhausted — redesign restarts the gate cycle from
   scratch; it does not patch this instrument.

## Interpretation (for the record; hypothesis-free)

The checkpoint did exactly what it was preregistered to do. §6's rationale
anticipated this case: the pilot estimate (min pairwise .705–.808 at n = 89)
was a *selected* estimate after five sequential revisions with
optional-stopping structure, and the design stated "a true-α ≈ .70 instrument
will fail statistic 2 — which is the intended behavior (the checkpoint is
load-bearing, not decorative)." On 150 fresh, seeded, stratified items the
instrument's point reliability sits at .68–.74 with interval lower bounds
.39–.65 — a tentative-band instrument at best, not checkpoint-confirmable.
No coder pair, no family bloc, and no determinism pathology explains it;
the disagreement is substantive coding disagreement on fresh corpus text.

Separately and coincidentally, the PI ordered a spend stop ("더이상 비용들지
않고 마무리", 2026-07-17) while the laundered arm was in progress. The stop
and the FAIL point the same direction; the FAIL is the governing,
preregistered reason coding does not continue.

## Status of the preregistration

The OSF registration and frozen instrument remain intact and unmodified. The
honest publishable record under the frozen decision tree is the
**preregistered-trajectory disclosure**: instrument design → G1 conditional
PASS (with its declared caveats) → confirmatory checkpoint FAIL on fresh
data. Per the project's kill-criteria clause, the downgrade path is a
methods-forward preprint/essay (no journal confirmatory submission, no
salami). The outcome-blind draft v0 (`docs/draft/draft-v0.md`) provides the
shell; its Results section resolves to the descriptive/negative-instrument
branch. H1/H2 were never tested — no corpus outcome data was collected or
examined (the checkpoint measured reliability only; no yield/marginal look
was run).

## Correction addendum (2026-07-21)

Two statements above are corrected of record; the original text is left as written because
this report is the contemporaneous record. (1) The header's "Tranche seed: 20260717 (OSF
registration date, §2.5)" and (2) the closing section's "The OSF registration ... remain[s]
intact": during upload preparation (2026-07-21) the OSF account was checked and no completed
web registration existed. The preregistration of record is the git-sealed SHA256 freeze
(content commit 83d0b49, seal commit bafc712, guardian CLEAN, 2026-07-17); the seed 20260717
is the freeze date, supplied under the frozen "registration date" rule and recorded with the
tranche lock before coding; the OSF deposit is post-halt and archival. Full statement:
preprint §4.4.9 (v0.9 correction of record).
