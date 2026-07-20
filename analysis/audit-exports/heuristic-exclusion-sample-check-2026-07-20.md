# Sample source-check — 473 heuristic review exclusions (2026-07-20)

Purpose: the 473 "no abstract + ≤5 pages" (PDC reclassified) exclusions in
`data/raw/locks/review_exclusions.json` are a corpus-definition assumption, not
source-confirmed classifications. This memo sizes the assumption's risk with a seeded
random sample, source-confirmed against publisher item-type fields (pdcnet
`Item_Data_Type`; Asbury ePLACE `Document Type`).

**Method.** Population: the 473 lock entries with reason prefix "book review (PDC
reclassified" (469 missing+short(≤5pp) + 4 review-signature). Draw: `random.Random(20260720).sample(pool, 20)`.
Verification: DOI resolution → publisher landing page item-type field, one pass per item.
Transparency note: a transcription slip in the verification tasking caused one sampled DOI
(10.5840/faithphil201330218) to be checked twice and one (10.5840/faithphil200825446) to be
checked in a separate follow-up pass; all 20 unique sampled items are covered below.

**Result (20 unique items).**
- **17 BOOK-REVIEW-CONFIRMED** (incl. 10.5840/faithphil200825446 = Oakes on Dawkins,
  *The God Delusion*, F&P 25(4), 447–451, Document Type "Book Review")
- **2 OTHER** — editorial introductions, *Philosophia Christi* 18(1):3 and 25(1):3–4
  (correctly excluded from the coding corpus, but as editorials, not book reviews)
- **1 RESEARCH-ITEM (false exclusion)** — East, "Infinity Minus Infinity," *Faith and
  Philosophy* 30(4), 2013, 429–433: a five-page peer-reviewed discussion note replying to
  Craig's kalam defenses; pdcnet `Item_Data_Type=Article` and Asbury `Document Type: Article`;
  the pdcnet record carries an abstract the harvest missed. Sits exactly on the ≤5-page
  threshold.

**Rate.** Sample false-exclusion rate 5% (1/20; Clopper–Pearson exact 95% CI 0.13%–24.9%).
Extrapolation to the 473: ≈24 items, with wide uncertainty at this sample size (≈1–118).

**Disposition.** Disclosed in §4.1 of the preprint (v0.7); no reinstatement — the corpus
lock is a frozen artifact and the run is halted, so the finding is carried as a limitation,
not a correction. A methodological note: pdcnet book-review records place the reviewed
book's title in `Item_Title`, so title-based classification is unreliable and the item-type
field is the decisive signal.
