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
