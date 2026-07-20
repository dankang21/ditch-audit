# LaTeX package — preprint (draft v0.3, 2026-07-17)

**A Preregistered Zero-Human LLM Measurement Design, and the Confirmatory Checkpoint That
Rejected Its Instrument** — subtitle: *Lessing's Ditch as a Measurable Property of the
Literature: design, validation battery, and halt report of the audit*

## Build

    tectonic main.tex        # or: xelatex main.tex (twice), or pdflatex main.tex (twice)

Engine-agnostic preamble: pdfLaTeX uses newtx (Times); XeLaTeX/LuaLaTeX use fontspec
(TeX Gyre Termes if available, else Liberation Serif). A compiled main.pdf (42 pp.) is included.

## Files

- main.tex        — preamble, title block, abstract wrapper, inputs
- abstract.tex    — abstract (generated from docs/draft/draft-v0.md, v0.3)
- front.tex       — keywords + "How to read this document" (v0.3)
- body.tex        — full body (generated; source of truth is draft-v0.md — regenerate, don't hand-edit)
- references.tex  — 61 entries; all in-text citations covered (completeness-swept)
- main.pdf        — compiled preview

## Bibliography status (v0.3)

All entries were web-verified against publisher/DOI records in a 7-agent verification pass
(2026-07-17), including a completeness sweep that added 13 entries missing from v0.2
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

Author line and the title-page footnote: confirm before upload (main.tex).
Generated from draft-v0.md (v0.3); companion essay: docs/draft/essay-checkpoint.md.
