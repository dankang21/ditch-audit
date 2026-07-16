# guardian_log — prereg-guardian verification ledger (ditch-audit)

Accumulating record of SHA256-manifest generation and re-verification runs.
Each run: what was checked, PASS/FAIL, and — on any violation — **what / when / which commit**.
Never edit `PREREG_MANIFEST.txt` to mask a mismatch (absolute rule 2).

---

## Run 1 — P3 manifest GENERATION (initial)

- when (utc): 2026-07-16T13:46:57Z
- git commit: `993b8f836e8ca9eb6242293c37a5400d2255f723`
- working tree: clean for all tracked non-data files (`git status` = only `docs/draft/` untracked,
  which is a P6 draft, not a freeze artifact). `data/{raw,sanitized,coded,criterion,gold}`
  confirmed `.gitignore`'d (abs-rule 3 copyright isolation intact — HASH ONLY).
- authority: `docs/analysis-plan-v1.md` §11 (+ §11.1), read in full; orchestrator minimum list.
- output: `PREREG_MANIFEST.txt` — 52 itemized artifacts + 16 corpus-lock hashes +
  5 batch/aggregate directory hashes + seed constants + model pins.

### Internal-consistency checks

| # | Check | Result | Evidence |
|---|---|---|---|
| C1 | vault v2 recompute == `VAULT_MANIFEST.txt` recorded v2 | **PASS** | both `19074e3d…ee087`, items=30 |
| C2 | vault v1 recompute == `VAULT_MANIFEST.txt` recorded v1 | **PASS** | both `36237137…d5d9b`, items=30 |
| C3 | `docs/gold-anchors-v1.json` == `data/gold/gold-anchors-v1.json` | **PASS** | byte-identical, `0cb5a722…f249` |
| C4 | `coder_prompt.txt` actual sha == `PROMPT_MANIFEST.txt` last-row prompt hash | **PASS** | both `7e77804b…16bb` (row `2026-07-16T13:15:31Z`) |
| C5 | `codebook-v1.md` actual sha == `PROMPT_MANIFEST.txt` last-row codebook hash | **PASS** | both `5eba8c60…bfd1` → frozen prompt built from frozen codebook (v1.4e) |
| C6 | copyright dirs gitignored (abs-rule 3) | **PASS** | `git check-ignore` positive for raw/coded/sanitized/criterion |
| C7 | model pins present for A/B/C/D/E + checker (item 7 / §B0) | **PASS** | cost_log + generation_log + battery §B0; D digest `2a654d98e6fb` |
| C8 | calibration disclosure present (item 25) | **PASS** | `calib_sample_manifest.json` (150 ids, seed 20260717) + `calib_sample_b.jsonl` |
| C9 | role-exclusivity matrix present (item 8) | **PASS** | battery §B0 (covered by item 3 hash) — no family in >1 blinded role |

### FREEZE-BLOCKING findings (dk decision required before OSF registration is signed)

**F1 — §B10 / PROVISIONAL literal precondition tripped (guardian bright-line).**
- what: the string `PROVISIONAL` remains in `docs/validation-battery-v1.md` (≥12 occurrences,
  incl. §B10 line 284 and the Status line 3). My agent-definition precondition is
  "§B10 임계값이 수치로 확정되었는지 검사 — PROVISIONAL 문자열 잔존 시 중단" (halt if PROVISIONAL remains).
- when / commit: observed at generation, commit `993b8f8`.
- design-of-record context (NOT a silent override — surfaced for dk): plan §11 row 3 explicitly
  makes "the FULL battery document the frozen artifact" and explicitly rejects the old
  "§B10 numeric table finalized" wording; battery Status line delegates numeric freeze to plan §9;
  plan §9 assigns every PROVISIONAL threshold a **numeric PROPOSED frozen value**, and §12 records
  dk's batch ruling "approved 2026-07-17 — default adopted." So the thresholds ARE numerically
  fixed *in §9*; the battery body retains PROVISIONAL as descriptive/historical labels by design.
- guardian disposition: **substantive PASS, literal FAIL.** I did not silently pass this and I did
  not unilaterally halt the whole freeze. dk must give an explicit one-line ruling for the record:
  either (a) confirm the plan §11-row-3 design-of-record supersedes the literal string precondition
  (recommended wording: "battery PROVISIONAL body labels are intentional; §9 carries the frozen
  numerics"), or (b) resolve/relabel the strings in the battery body and re-run the guardian.

**F2 — §11-named artifacts not present as distinct files (manifest cannot hash a nonexistent file).**
Orchestrator instruction: report §11 items absent as a freeze-halt condition. Enumerated:
- item 11 "H1/H2 analysis and bootstrap scripts to be added pre-freeze": **no standalone file.**
  Bootstrap logic exists embedded in `scripts/alpha.py` (α CIs), `pipeline/05_analysis/tipping_point.py`,
  and `adversarial_flip.py`; the primary H1/H2 headline OR estimator (§5 IPF / Newton–Raphson
  logistic) is not committed as a distinct hashable script. dk: confirm embedded-is-sufficient, or
  add the estimator script before sign.
- item 12 machine-readable id lists (review-exclusion 620 · review-essay 15 · missingness-stratum
  672/462 · confirmatory-exclusion 89): **not materialized as files.** `data/sanitized/exclusions.jsonl`
  is 0 bytes (empty-string hash `e3b0c442…b855`). Corpus JSONL hashes ARE present; the derived id
  lists are not. dk: produce the id-list files pre-freeze, or register them as post-lock derivations.
- item 18 "§4.1 frozen title-keyword list": **absent** (plan §4.1 says "the keyword list is
  freeze-manifest item 18" but only references it; no distinct frozen list file exists).
- item 21 B9 venue-inference probe template + B7b metadata-only baseline template: **absent**
  (only B5 `recognition_probe.py` present).
- item 22 R5 citation snapshot file: **absent.**
- item 23 R1 split-rule build-variant prompt: **absent** (required — §12 item 9 approved option (a),
  so this build-variant is in scope; the post-P4 sensitivity prompt is not yet generated).

### NOTES (non-blocking; recorded for cleanliness before OSF sign)

- N1 item 19 B4-cue lexicon is **embedded** in `generate_synthetics.py` (`HEDGE_RE`) and
  `launder.py` (`MODAL_RE`) — captured by those file hashes; acceptable, no standalone list file.
- N2 model pins A/B are **undated IDs** (`claude-opus-4-8`, `gemini-3.5-flash`); Anthropic/Google
  expose no dated variant. Resolved by plan §1.1 fallback = per-call version-header/modelVersion
  logging + B1c consolidated-determinism drift detector (recorded in cost_log "Pre-freeze registered
  actions"). Not a blocker; the §B1 "dated snapshot" ideal is met via the documented fallback.
- N3 `data/coded/cost_log.md` header pin table (lines 6–9) is **stale** (lists A=claude-sonnet-5,
  D=TBD); superseded by the same file's later "Pin revision (2026-07-15)" (A→claude-opus-4-8) and
  "Coder D pin confirmed (2026-07-17)" (qwen3.5:4b) sections + battery §B0. Operative pins are
  correct and recorded; recommend refreshing the header table for a clean frozen artifact.
- N4 codebook is **v1.4e** (advanced past item-1's anticipated v1.4c/v1.4d). Consistent: prompt was
  rebuilt from v1.4e (C4/C5 hash chain verified). item 1 explicitly permits dk to advance the
  version pre-freeze; the frozen version of record is v1.4e.
- N5 seeds §2.5 bootstrap / §6 tranche / §3.6 FN-audit / §3.8 subsample = **OSF registration date
  (YYYYMMDD), bound at registration** per the §2.5 convention. Deferred-by-design, not a defect;
  `build_checkpoint_tranche.py` takes `--seed` as a required CLI arg (no hardcoded value to drift).
- N6 date-label vs filesystem: changelog/freeze are labeled 2026-07-17 while git commit + file
  mtimes are 2026-07-16 (KST offset). Cosmetic; manifest records actual mtimes.

### Guardian conclusion for Run 1
Manifest generated and internally consistent on all 9 machine checks (C1–C9 PASS). **Freeze is NOT
yet clean:** F1 (PROVISIONAL precondition) needs an explicit dk ruling, and F2 enumerates six
§11-named artifacts absent from the tree. Per absolute rule 2 and the guardian mandate, I am NOT
advancing the freeze as signed; these findings go to dk. No manifest values were altered to mask any
condition. Re-run the guardian after dk resolves F1/F2 (the OSF-signed manifest should be generated
against the commit that carries the resolutions).

---

## OSF upload list DRAFT (public-safe only; abs-rule 3 — no copyrighted abstract text)

Rule: publish code + docs + **hashes**; NEVER the `data/{raw,sanitized,coded}` original texts
or the synthetic vault texts (vault opens once at P4). Copyrighted-corpus provenance is proven by
the SHA256 rows in `PREREG_MANIFEST.txt`, not by the text.

INCLUDE (upload at registration):
- `PREREG_MANIFEST.txt`                    (the hash manifest — core registration artifact)
- `analysis/guardian_log.md`               (verification ledger)
- `docs/codebook-v1.md` (v1.4e)
- `docs/validation-battery-v1.md` (v1.3)
- `docs/analysis-plan-v1.md` (v1.1+§11.1)
- `docs/gold-anchors-v1.json` (v1.3 — citations+codes+rationale only; no verbatim abstracts)
- `docs/synthetic-specs-v1.json` (dk-signed targets/briefs; NOT the vault texts)
- `pipeline/03_code/coder_prompt.txt` + `pipeline/03_code/PROMPT_MANIFEST.txt`
- `pipeline/00_criterion/VAULT_MANIFEST.txt` (hashes only)
- all analysis/battery/pipeline scripts (stdlib, no secrets):
  `scripts/{alpha,adjudicate,consolidate_runs,build_coder_prompt}.py`,
  `pipeline/05_analysis/{build_checkpoint_tranche,tipping_point,adversarial_flip,firewalled_yield}.py`,
  `pipeline/04_battery/{make_stubs,build_text_driven_stratum,recognition_probe,determinism_audit,discriminator,launder,battery_common}.py`,
  `pipeline/03_code/run_coders.py`, `pipeline/02_sanitize/sanitize.py`,
  `pipeline/00_criterion/{generate_synthetics,relaunder_synthetics}.py`,
  `pipeline/01_fetch/t1_relevance.py` (+ remaining `01_fetch/*.py` provenance scripts)
- `README.md`

EXCLUDE (hash-only in manifest, or withhold entirely):
- `data/raw/*`, `data/sanitized/*`, `data/coded/*` original texts  (copyright — hash-only)
- `data/criterion/synthetic_vault*.jsonl`  (VAULTED until P4 — hash-only)
- `data/raw/*_cache*`, `__pycache__`  (intermediate)
- `.env` / any secret  (abs-rule 4)
- `CONTEXT.md`  (intellectual-lineage / hypothesis-firewall internal doc — not a registration artifact)
- `docs/draft/*`  (P6 draft — not registered)

Post-P4 (deferred publication, not at registration): vault texts + full coded data may be released
per the data-availability statement once the vault is opened and copyright-safe aggregates are ready.

---

## Run 2 — P3 manifest REGENERATION (after dk resolved F1 + F2) — FREEZE-CLEAN

- when (utc): 2026-07-16T14:27:48Z
- git commit: `83d0b499c1f5065417bef70206c9ae4d86fa6991` (was `993b8f8` at Run 1)
- working tree: clean (`git status` empty; Run 1 manifest/log + all resolutions committed).
- output: `PREREG_MANIFEST.txt` regenerated — **64 itemized artifacts** (Section A = 48,
  incl. 13 new F2 files; Section B = 16 corpus-lock JSONL) + **6 batch/aggregate dir hashes**
  (data/raw/locks added) + seeds + pins. Prior Run-1 manifest values NOT reused — full recompute.

### F1 resolution verified
- what: `docs/validation-battery-v1.md` PROVISIONAL count **0** (was ≥12 at `993b8f8`);
  12 occurrences relabeled to `ADOPTED-FROZEN`, header Status line included. Bright-line
  precondition ("halt if PROVISIONAL remains") now **PASSES**. Numeric values of record remain
  in analysis-plan §9.

### F2 resolution verified — all six §11-named artifacts materialized (0 absent)
- item 11: `pipeline/05_analysis/headline_effects.py` (40,558 B) — H1/H2 headline-effect + bootstrap.
- item 12: `data/raw/locks/{review_exclusions(627), review_essays(15), missingness_stratum(672;210 missing;462 covered), confirmatory_exclusions(89=69real+20gold)}.json` + `pipeline/01_fetch/build_locks.py`. Counts reconcile with plan §1.2/§4/§3.8/§11 (C10a–d PASS). Legacy 0-byte `data/sanitized/exclusions.jsonl` superseded (retained only in sanitized batch hash).
- item 18: `pipeline/01_fetch/t1_keywords_frozen.json` + `freeze_t1_keywords.py`.
- item 21: `pipeline/04_battery/{venue_inference_probe,metadata_null_baseline}.py` (B5 probe already present).
- item 22: `pipeline/05_analysis/fetch_citation_snapshot.py` — plan §11 line 768 authoritative path (coordinator note said `01_fetch/`; the plan governs). Script frozen now; snapshot data pulled at P5 by design (deferred like the seeds). Resolved.
- item 23: `scripts/build_coder_prompt_r1split.py` + `pipeline/03_code/coder_prompt_r1split.txt`. PROMPT_MANIFEST last row extended: `... prompt=7e77804b… r1split_prompt=9babf168…`.

### Machine checks (all PASS)

| # | Check | Result | Evidence |
|---|---|---|---|
| — | 64 itemized rows re-hash | **PASS** | 0 mismatch |
| C1 | vault v2 == VAULT_MANIFEST | **PASS** | `19074e3d…` |
| C2 | vault v1 == VAULT_MANIFEST | **PASS** | `36237137…` |
| C3 | gold docs == data (identity) | **PASS** | `0cb5a722…` |
| C4 | primary prompt == PROMPT_MANIFEST `prompt=` | **PASS** | `7e77804b…` (row 2026-07-16T14:20:24Z) |
| C4b | r1split prompt == `r1split_prompt=` | **PASS** | `9babf168…` |
| C5 | codebook == PROMPT_MANIFEST `codebook=` | **PASS** | `5eba8c60…` (v1.4e; unchanged from Run 1) |
| C6 | copyright dirs gitignored | **PASS** | raw/coded/sanitized/criterion |
| C7 | pins A/B/C/D/E + checker present | **PASS** | D digest `2a654d98e6fb` |
| C8 | calibration disclosure present | **PASS** | manifest + 150 ids seed 20260717 |
| C9 | role matrix §B0 present | **PASS** | item03 hash |
| C10 | item-12 lock counts == plan (627/15/672·210/89) | **PASS** | C10a–d |
| F1 | PROVISIONAL bright-line == 0 | **PASS** | battery count 0 |
| F2 | §11 named artifacts absent == 0 | **PASS** | all 13 new files present |

### Guardian conclusion for Run 2
No blocking findings. All Run-1 F1/F2 conditions resolved and machine-verified at commit
`83d0b499`. Manifest internally consistent; no value altered to mask any condition.

**FREEZE-CLEAN** — the OSF-signed manifest may be registered against commit `83d0b499` (bind the
registration-date seeds and pull the R5 citation snapshot per their deferred-by-design schedule).

### OSF upload list — Run 2 update
Same policy as Run 1 (docs + scripts + hashes; never `data/{raw,sanitized,coded}` abstract text
or the vault texts). ADD to INCLUDE:
- `pipeline/05_analysis/{headline_effects,fetch_citation_snapshot}.py`
- `pipeline/01_fetch/{build_locks,freeze_t1_keywords}.py`, `pipeline/01_fetch/t1_keywords_frozen.json`
- `pipeline/04_battery/{venue_inference_probe,metadata_null_baseline}.py`
- `scripts/build_coder_prompt_r1split.py`, `pipeline/03_code/coder_prompt_r1split.txt`
- `data/raw/locks/*.json` (DOIs/item-ids only, no abstract text — publish as the machine-readable
  item-12 lists; the only `data/raw/` files cleared for upload)
Unchanged EXCLUDE: `data/{raw(except locks/),sanitized,coded}` texts, `data/criterion/synthetic_vault*`
(vaulted until P4), caches, `.env`, `CONTEXT.md`, `docs/draft/*`.

---

## Session-start VERIFY (post-freeze #1, P4 kickoff)

- when (utc): 2026-07-16T14:43:05Z
- HEAD commit: `bafc712db95cdd31b1cbf00040ea4c1bcf1dd352` (seal commit; sealed `PREREG_MANIFEST.txt`
  + `analysis/guardian_log.md` + CONTEXT.md §4.9e + CLAUDE.md phase table against content commit `83d0b499`).
- mode: VERIFY only — manifest re-hashed & compared against working tree. **No regeneration; manifest not touched.**
- working tree: clean (`git status` empty).

### Comparison result

| Basis | Result |
|---|---|
| Section A itemized (48) | 48/48 SHA256 match |
| Section B corpus-lock JSONL (16) | 16/16 SHA256 match |
| **Section A+B total** | **64/64 match** (0 mismatch, 0 missing, 0 size-mismatch) |
| Section C batch aggregates (6) | **6/6 match** (data/sanitized, data/coded, data/criterion, data/battery, data/raw, data/raw/locks) |

- Verification basis is file-content SHA256 (not commit hash), per the freeze definition. Aggregate
  recompute reproduces each recorded `aggregate_sha256` via the documented rule
  (`sha256` over sorted `"filehash␠␠relpath\n"` lines, full repo-relative paths).
- mtime not treated as a criterion (git does not preserve mtime across checkout); every hash matched
  regardless, so all frozen content is byte-identical to the sealed manifest.

### Non-frozen changes confirmed benign
- `CONTEXT.md`, `CLAUDE.md`: NOT in the frozen list (operational docs). Their update in seal commit
  `bafc712` (CONTEXT §4.9e freeze note; CLAUDE phase table P3->FREEZE) is expected and permitted.
- Extra on-disk files in batch dirs (`data/{sanitized,coded,raw}/.gitkeep`,
  `data/raw/{fp_recover,pc_recover}.log`, `data/raw/{fp_recover,pc_recover}.run.out`,
  `data/raw/{t1_recover,t1_run}.out`): all **untracked + .gitignore'd**, absent from the `bafc712`
  tree, and outside every declared batch file set — operational logs/placeholders, not frozen
  artifacts. No effect on the 6 aggregates (recomputed over the manifest's declared file lists).

### Guardian verdict — Run 3 (session-start VERIFY)
**INTACT.** 64/64 itemized + 6/6 aggregates reproduce against working tree at HEAD
`bafc712`. No frozen artifact altered since seal; no violation. Manifest left unmodified.
P4 (main coding) may proceed.

---

## Post-freeze operational tooling registered (P4 kickoff prep)

- when (utc): 2026-07-16T15:13:59Z
- HEAD commit at registration: `827d718471b7ec97bfbc621ec38286f0f757915d`
- mode: **log-registration only — NOT a manifest edit.** Per absolute-rule 2 the frozen set is
  immutable; per analysis-plan-v1 §11 item 11 (analysis-script hash convention) the SHA256 of
  post-freeze operational scripts is recorded here in the guardian log. These three tools are
  **not** members of `PREREG_MANIFEST.txt` (grep count 0) and were deliberately NOT added to it —
  the manifest was left byte-for-byte unmodified this session.

### Precondition re-verified this session (independent VERIFY, Run 4)
Before registering, the sealed manifest was independently re-hashed against the working tree at HEAD
`827d718`: **INTACT — 48/48 Section A itemized + 16/16 Section B corpus-lock (64/64) SHA256 match,
and 6/6 Section C batch aggregates reproduce.** Aggregate rule reconfirmed = `sha256` over
**path-sorted** `"<filehash>␠␠<repo-relative-path>"` lines with a trailing `\n` (individual Section C
member hashes all match; the aggregate is order-sensitive on path, not on the hash-prefixed line).
No frozen artifact altered since the seal. So the "frozen files untouched" claims below rest on a
fresh machine check, not on assertion. Manifest not touched.

### Registered tools — direct SHA256 recompute (this session)

| Tool (repo-relative path) | SHA256 | size (B) | commit provenance |
|---|---|---|---|
| `pipeline/05_analysis/checkpoint_stats.py` | `c4f7c39010d9705f86d3edd64a168bfba59f5b9adf09821cee60552676740530` | 18242 | introduced `827d718` — **SUPERSEDED, see rev 2 below** |
| `pipeline/02_sanitize/sanitize_batch.py` | `f1c08bc6a60f7b69bdeb65a96c6d944230d8ffd80cf4831b9224cc1c85bf44cd` | 4947 | added `9a74408`, repaired `164e1b4` |
| `pipeline/05_analysis/extract_tranche_items.py` | `592e80598baf25f42a3122631084ce24bb391ca1832b5bdb38632f91c44d56cc` | 4854 | added `9a74408`, repaired `164e1b4` |

### What each implements, and why it does not touch the frozen set
Each tool only **implements** a definition that is frozen in the plan; none redefines one, and none
writes to any freeze-listed artifact.

- **`checkpoint_stats.py`** — computes the analysis-plan **§6 dual statistic** (point min-pairwise α
  + per-dimension **bootstrap min-pairwise 95% lower bound**, drawn under the **§2.5** nearest-rank
  bootstrap convention), the **§6.3** conditional-agreement watch, and the **§9 B1b** run-split
  rates + **§9 B1c** consolidated exact-match. α is `import alpha` from the **frozen `scripts/alpha.py`
  (manifest item 11)** — reused unmodified, per the in-file line-55 marker "FROZEN α harness …
  imported, never edited." Statistical definitions live in the plan (§6/§2.5/§9), not in this script.
- **`sanitize_batch.py`** — a batch wrapper that does `import sanitize as S` and reuses the **frozen
  `sanitize.py` `process()` (manifest item 24)** unmodified (line-34 marker: "FROZEN module …
  imported, never edited"). All scrub/redaction logic is the frozen item-24 sanitizer; the wrapper
  adds only batching plus a freeze-listed-file inviolability guard and path-traversal / symlink /
  namespace defenses. (Adversarial-audit BLOCKER — a `'../sanitized/pilot_rs2015'` write that
  truncated a frozen file in an isolated repro — was repaired at `164e1b4` before this registration.)
- **`extract_tranche_items.py`** — materializes a checkpoint tranche's raw items from the locked P2
  corpus by manifest id (supports §6/§15 checkpoint tranche builds). It defines no statistic. It
  enforces a **corpus-drift guard** (recomputes every recorded input `sha256`, aborts on any
  mismatch), strip-invariance on each matched line (aborts rather than silently normalizing), and
  `data/`-containment + symlink refusal on all paths. It reads only corpus locks and writes under
  `data/` (`.gitignore`'d, copyright-isolated per absolute-rule 3); it modifies nothing frozen.

### Guardian note
Frozen artifacts confirmed untouched (precondition VERIFY / Run 4 above); `PREREG_MANIFEST.txt` not
modified. These three entries are the §11-item-11 hash record for post-freeze operational scripts,
to be re-checked on drift like any registered analysis script. **No freeze violation observed at
HEAD `827d718`.**

### Revision — `checkpoint_stats.py` rev 2 (3-lens adversarial-audit repair, FIX-REQUIRED ×2)

- when (utc): 2026-07-16T15:29:03Z
- HEAD commit: `fb1f68daaba8ed362cb9109e1b7582b8aa8a608c`
- repair commit: `fb1f68d` ("checkpoint_stats hardened per 3-lens adversarial audit …")
- **rev 2 SHA256 (direct recompute, verified):** `b1d113cd32e63ad080d075209d69ffaf60090c094d6e86afef323642d6e92bd9`  (30004 B)
- **rev 1 SHA256:** `c4f7c39010d9705f86d3edd64a168bfba59f5b9adf09821cee60552676740530` (18242 B, `827d718`) —
  retained as history, **superseded by rev 2 (pre-first-use repair; never used in a gate run).** No
  prior gate/checkpoint result depends on the superseded hash.

Two FIX-REQUIRED findings from the 3-lens adversarial audit drove rev 2. All repairs are inside
`checkpoint_stats.py` only — no frozen artifact touched, and the plan §6/§2.5/§6.3/§9 statistical
**definitions are unchanged**; they are implemented more strictly (fail-closed), not redefined:
1. **Consolidated-input enforcement** — every record must carry `_runs` (per-run file misfeed and
   the silent 0% B1b it would otherwise produce are blocked).
2. **Refuse-to-adjudicate (exit 3)** on coder-seat / coverage-completeness / tranche-n validation failure.
3. **B1c denominator = union of the two re-runs** — item loss counts as a mismatch, not a silent drop.
4. **Degenerate-replicate refusal** — if a degenerate replicate is present, that dimension's
   **Statistic-2 = FAIL** (`b_eff == B` required).
5. **Frozen-parameter hard-lock** (B=1000 / α-gate .70 / conditional .667 / CI .95 / n=150); any
   deviation ⇒ **NON-CONFIRMATORY branding (exit 5)**.
6. **B1b > 5% ⇒ alarm-only (exit 4)**.
- selftest: **10 cases PASS** (incl. CLI-guard battery).

### Frozen-set reconfirmation (rev 2)
Per coordinator scope, no full manifest VERIFY was required for this revision — only a frozen-set
no-touch check. `git diff --stat -- PREREG_MANIFEST.txt` = **empty ⇒ manifest byte-for-byte
unchanged.** `checkpoint_stats.py` is an operational (non-manifest) script; this is a §11-item-11
hash-record update, not a freeze modification. **No freeze violation at HEAD `fb1f68d`.**
