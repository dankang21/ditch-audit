# LaTeX package — preprint (draft v0.10, 2026-07-21)

**A Prospectively Frozen Zero-Human LLM Measurement Design, and the Confirmatory Checkpoint
That Rejected Its Instrument** — subtitle: *Lessing's Ditch as a Measurable Property of the
Literature: design, validation battery, and halt report of the audit*

## Build

    tectonic main.tex        # or: xelatex main.tex (twice), or pdflatex main.tex (twice)

Engine-agnostic preamble: pdfLaTeX uses newtx (Times); XeLaTeX/LuaLaTeX use fontspec
(TeX Gyre Termes if available, else Liberation Serif). A compiled main.pdf (58 pp.) is included.

## Files

- main.tex        — preamble, title block, abstract wrapper, inputs
- abstract.tex    — abstract (generated from docs/draft/draft-v0.md, v0.10)
- front.tex       — keywords + "How to read this document" (v0.10)
- body.tex        — full body (generated; source of truth is draft-v0.md — regenerate, don't hand-edit)
- references.tex  — 85 entries; all in-text citations covered (completeness-swept at v0.3; 14 added at v0.4, 4 at v0.5, 4 at v0.7, 2 at v0.8 — East 2013 and Hendricks et al. 2020)
- main.pdf        — compiled preview

## Bibliography status (v0.3)

All entries were web-verified against publisher/DOI records in a 7-agent verification pass
(2026-07-17) — verification scope: bibliographic existence and metadata, not interpretive
support, which the verification memos document separately — including a completeness sweep that added 13 entries missing from v0.2
(Table 1 anchors: Adams 2019 = F. C. Adams, Physics Reports 807; Malpass & Morriston 2020,
PQ 70(281); Nickel 2015 = G. Nickel, De Gruyter chapter; Ocampo 2024, IJPR 96(1); Cochrane
CD000368; STEP trial; Leslie 1979; Hick 1989; Alston 1991; Hume; Russell & Copleston
1948/1957; Borde–Guth–Vilenkin 2003; Krippendorff 2004).

**All entries finalized.** The four flagged judgment calls (Chambers & Tzavella 2022;
Duan et al. 2024 identification; Hume edition; Swinburne 2004a anchor mapping) were approved
by the author on 2026-07-20. No outstanding bibliography actions.

Three body corrections found during verification were applied and inventoried in the draft's
v0.3 resolution note: Plantinga reply year 2004 → 2006 (Philosophia Christi 8(1), 7–22);
Swinburne 2004 disambiguated to 2004a/2004b; the argument-strength-ratings finding re-keyed
from De Cruz (2017) to De Cruz & De Smedt (2016).

## v0.4 additions (2026-07-20)

Fourteen entries added with the post-review repair cycle: ten methods/infrastructure
references (statistical conventions, bootstrap, AUC, self-consistency, OpenAlex, Semantic
Scholar, the 2020 PhilPapers survey) and four sources cited by the new Table 1
witness-verification note (Berger 1979; Friedmann 1986; Rembaum 1982; Steinhart 2010).
All fourteen were web-verified on 2026-07-20 with no corrections required (verification
memos in analysis/audit-exports/). Lessing entry now carries the Chadwick translation
pages (51--56).

## v0.5 additions (2026-07-20)

Four entries added with the second-review repair cycle: Carnley 1987 and 2019 (the verified
S7 stance-witness), Maimonides (Touger trans., 1987, uncensored 11:4), and Abdel Haleem 2004
(Qur'an translation of record). All four web-verified; memos in analysis/audit-exports/.

## v0.10 changes (2026-07-21)

No bibliography changes (85 entries). Sixth-review vocabulary correction: title recast to
"Prospectively Frozen"; authorial-voice "preregistered" -> precommitted / prospectively
frozen / sealed (shells, quotations, artifact names, historical notes keep the original
term); title-page footnote corrected to the post-halt deposit; seed constant no longer
called "the freeze date"; §5.1.1 seed-rule discrepancy stated.

## v0.9 changes (2026-07-21)

No bibliography changes (85 entries). Correction of record: the OSF registration reported
complete 2026-07-17 was never completed; preregistration of record restated as the
git-sealed freeze, seed pre-commitment restated, OSF slot re-scoped as post-halt archival
deposit (§4.4.9 correction paragraph + propagations). Author ORCID on the title page;
repository URL of record filled.

## v0.8 changes (2026-07-20)

Fifth-review conditional-approval completions: East 2013 and Hendricks et al. 2020 (Crossref)
added (83 -> 85, both web-verified); single-draw statement; Corollary 1 conditioned on the
burden principle; S6-Islam verdict restated construal-dependent; shell-adjacent §6 note;
version-metadata fallback precision. Identifier placeholders await registrant values.

## v0.7 changes (2026-07-20)

Four bibliography entries added, all web-verified (Adang 1996; Lapide & Moltmann 1981;
Ostler 2001; Tindal 1730). Body: fourth-review repairs (grain scoping to registered
variants; 2004–2008 stratum renaming; 473 corpus-definition assumption + seeded 20-item
source-check with one disclosed false exclusion; Table 1 column retitle; Carnley demotion
with page loci; coder D execution record; canonicity-mood softenings).

## v0.6 changes (2026-07-20)

No bibliography changes (79 entries unchanged). Text changes only — abstract, front matter,
and body (third-review repairs:
working-partition demotion, S6/Lapide repair, Carnley construal scoping, gold-anchor weight
wording, n=150 projection attribution, T1/single-journal limitations). PDF now carries
Title/Author metadata (hypersetup in main.tex).

Author line and the title-page footnote: confirm before upload (main.tex).
Generated from draft-v0.md (v0.10); companion essay: docs/draft/essay-checkpoint.md.
