# LaTeX package — Lessing's Ditch preprint (draft v0.2, 2026-07-17)

## Build

    tectonic main.tex        # or: xelatex main.tex  (twice)

Engine: XeLaTeX. Main font: Liberation Serif (system font; swap via \setmainfont in main.tex,
e.g. 'TeX Gyre Termes' on a full TeX Live). Compiles clean; a compiled main.pdf is included.

## Files

- main.tex        — preamble, title, abstract wrapper, inputs
- abstract.tex    — abstract body (generated from docs/draft/draft-v0.md)
- body.tex        — full paper body (generated; source of truth remains draft-v0.md)
- references.tex  — References section (COMPILED FROM IN-TEXT CITATIONS — see below)
- main.pdf        — compiled preview (39 pp.)

## ⚠ Bibliography: verify before upload

The draft carried no References section; this list was reconstructed from the in-text
citations. Standard works carry full bibliographic detail believed correct; the entries
below are flagged `% VERIFY` in references.tex and MUST be checked by the author:

- Bystranowski, P., Dranseika, V., and \.{Z}uradzki, T. (2022). Half a century of bioethics and philosophy of me
  — exact title/volume
- Adams, [initial]. (2019). [Title to be verified against the in-text citation.]
  — which Adams work is cited (in-text: Adams 2019)
- Allison, D.~C. (2021). *The Resurrection of Jesus: Apologetics, Polemics, History*. T\&T Clark.
  — Allison publication details
- De Cruz, H. (2017). Religious disagreement: An empirical study among academic philosophers. *Episteme*, 14(1),
  — De Cruz 2017 exact study
- De Cruz, H. (2018). [Qualitative study of religious belief trajectories among philosophers of religion; verify
  — De Cruz 2018 exact study
- De Cruz, H., and De Smedt, J. (2016). *A Natural History of Natural Theology: The Cognitive Science of Theolog
  — year (book is commonly dated 2015)
- Gauch, H.~G., Jr. (2013). The methodology of ramified natural theology. *Philosophia Christi*, 15(2), 283--298
  — Gauch 2013 venue
- Holder, R. (2021). *Ramified Natural Theology in Science and Religion: Moving Forward from Natural Theology*. 
  — Holder 2021 details
- Lapide, P. (1983). *The Resurrection of Jesus: A Jewish Perspective*. Augsburg.
  — Lapide edition/year
- McGrew, L., and McGrew, T. (2006). On the historical argument: A rejoinder to Plantinga. *Philosophia Christi*
  — McGrew and McGrew 2006 details
- Morriston, W. (2020). [Title to be verified against the in-text citation.]
  — which Morriston 2020 work
- Nickel, [initial]. (2015). [Dwindling-probabilities exchange contribution; verify author and venue.]
  — Nickel 2015 details
- Ocampo, [initial]. (2024). [Systematic map of Stage~II bridging strategies; verify author and venue.]
  — Ocampo 2024 details
- Brower, J.~E., and Rea, M.~C. (2005). Material constitution and the Trinity. *Faith and Philosophy*, 22(1), 57
  — in-text "Rea 2005" may be Brower and Rea 2005
- Russell, B., and Copleston, F.~C. (1948). The existence of God: A debate. Reprinted in B.~Russell, *Why I Am N
  — Russell brute-fact citation form (1948 BBC debate)
- McGrew, T., McGrew, L., and Vestrup, E. (2001). Probabilities and the fine-tuning argument: A sceptical view. 
  — in-text "Vestrup 2001" may be McGrew, McGrew and Vestrup 2001
- Wildman, W.~J. (2004). The Divine Action Project, 1988--2003. *Theology and Science*, 2(1), 31--75.
  — Wildman 2004 details
- Wiles, M. (1986). *God's Action in the World*. SCM Press.
  — Wiles work cited

### In-text contexts for the flagged citations

- **Adams 2019**: …the multiverse rejoinder to fine-tuning) · contra: Oppy 2006; Malpass & Morriston 2020; McGrew, McGrew & Vestrup 2001; Adams 2019 | contested — pure metaphysics after withdrawal of the BGV inference | α (+β sub-dispute on fine-tuning degree) |
| S2 | That ground is an…
- **Morriston 2020**: …Barnes 2012; White 2000 (functional pro: rebuts the multiverse rejoinder to fine-tuning) · contra: Oppy 2006; Malpass & Morriston 2020; McGrew, McGrew & Vestrup 2001; Adams 2019 | contested — pure metaphysics after withdrawal of the BGV inference | α (+β sub-dispute on fine…
- **Nickel (2015)**: …by Plantinga (2000), answered by Swinburne (2004) and McGrew (2004), and continued through McGrew and McGrew (2006) and Nickel (2015). That debate concerns the formal behavior of chained arguments, not the empirical distribution of the arguments actually published. The cha…
- **Ocampo (2024)**: …: how does one get from a first cause to a being with the divine attributes? Rasmussen (2009) and, most systematically, Ocampo (2024) map "Stage II" bridging strategies, but for a single segment of the chain and by argument-analysis rather than corpus measurement. Second,…
- **De Cruz 2017**: …iteratures. De Cruz's studies measure philosophers: argument-strength ratings track the rater's prior religious belief (De Cruz 2017); natural-theological arguments have been evaluated experimentally (De Cruz and De Smedt 2016); and most philosophers of religion were thei…
- **De Cruz 2018**: …and most philosophers of religion were theists before entering the field, a selection effect documented qualitatively (De Cruz 2018). Draper and Nichols (2013) diagnose field-level cognitive biases and issue recommendations, without a coded corpus. The PhilPapers surveys…
- **De Smedt 2016**: …'s prior religious belief (De Cruz 2017); natural-theological arguments have been evaluated experimentally (De Cruz and De Smedt 2016); and most philosophers of religion were theists before entering the field, a selection effect documented qualitatively (De Cruz 2018). Dra…
- **Gauch 2013**: …s coinage for the pro-side program that argues from bare theism onward to specifically Christian doctrine (Holder 2021; Gauch 2013). This is a constructive project: it builds the crossing, it does not survey the traffic. Third, the *dwindling probabilities* exchange ove…
- **Rea 2005**: …is God incarnate; God is triune | Lapide (accepts S1–S7, rejects S8); Tuggy 2003 | pro-coherence: Morris 1986; Brower & Rea 2005 | defensive; truth-evidence fully S7-dependent | α (γ-dependent) |

The qualitative-prior column requires immediate discipline. Its verdict…
- **Vestrup 2001**: …al pro: rebuts the multiverse rejoinder to fine-tuning) · contra: Oppy 2006; Malpass & Morriston 2020; McGrew, McGrew & Vestrup 2001; Adams 2019 | contested — pure metaphysics after withdrawal of the BGV inference | α (+β sub-dispute on fine-tuning degree) |
| S2 | That g…
- **Wildman 2004**: …post-creation (miracles, answered prayer) | Wiles; deism | contra: Cochrane review CD000368 (2009); STEP trial (2006); Wildman 2004; Hume · pro anchors: coherence defenses only | strong headwind; the chain's only fully live empirical channel | β |
| S6 | The authentic be…
- **Holder 2021**: …— Swinburne's coinage for the pro-side program that argues from bare theism onward to specifically Christian doctrine (Holder 2021; Gauch 2013). This is a constructive project: it builds the crossing, it does not survey the traffic. Third, the *dwindling probabilities*…
- **Bystranowski**: …asure the field's composition (Bourget and Chalmers 2014). The nearest genre precedent lies outside the field entirely: Bystranowski, Dranseika and Żuradzki (2022) topic-model half a century of bioethics across seven field journals — but topics are not claims, and no dire…

Author line and the title-page footnote are placeholders — edit in main.tex.
Generated from draft-v0.md at commit 0b359fe; regenerate rather than hand-editing body.tex.