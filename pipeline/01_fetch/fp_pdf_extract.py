#!/usr/bin/env python3
"""F&P Asbury-PDF classifier + verbatim abstract extractor (precision-biased).

Shared by the full recovery run and its validation harness. NO model, NO
paraphrase: the abstract is the blank-line-delimited paragraph that F&P prints
at the head of p.2 (after the ePLACE cover sheet on p.1), taken verbatim with
whitespace collapsed only. Book reviews (no printed abstract) are detected from
source signatures and routed to exclusion. Items whose head paragraph is not a
clean abstract (e.g. discussion notes) stay honestly missing -- never fabricated.

Ground-truth calibration on the G2 probe (n=20 cached PDFs): the decisive
article-vs-note discriminator is that a printed F&P abstract carries NO digits
(no footnote markers, page refs, or section numbers), whereas a discussion
note's first body paragraph does. Bias is toward precision -- a digit-bearing or
malformed candidate stays honestly missing rather than risk storing body text.
"""
import re
import subprocess

# ---- review signatures (F&P print layout) ----
_BOOK_REVIEWS_HDR = re.compile(r"\bBOOK\s+REVIEWS?\b")
# all-caps reviewer name + institution on its own line: "JOANNA LEIDENHAG, University of Leeds"
_REVIEWER_SIG = re.compile(
    r"(?m)^\s*[A-Z][A-Z.’'\- ]{2,40},\s+"
    r"(University|College|Seminary|Institute|School|Universi|Uniwersytet|Universit)")
# book citation head: "..., by Name. Publisher, YEAR." / "ed. Name" + publisher/price/pages
_BOOK_CITE = re.compile(
    r",\s+(by|edited by|ed\.)\s+[A-Z][A-Za-z.\-]+"
    r"[\s\S]{0,220}?"
    r"(University Press|Press|Publishing|Publishers|Eerdmans|Routledge|Blackwell|"
    r"Baker|Brill|Continuum|Ashgate|Clarendon|\$\d|\bPp\.\s*\d|\bpages\b)")

_CAPS_LINE = re.compile(r"^[A-Z0-9 .,:;'’\"\-–—?!()&]+$")
# spaced-out single letters that mark a bad OCR scan: "A d a m", "w h i c h"
_SPACED = re.compile(r"\b(?:[A-Za-z]\s){2,}[A-Za-z]\b")


def pdftotext(pdf, first, last):
    r = subprocess.run(["pdftotext", "-f", str(first), "-l", str(last), pdf, "-"],
                       capture_output=True, text=True, errors="replace")
    return r.stdout or ""


def _blocks(text):
    """Blank-line-delimited blocks, each collapsed to single spaces; keep order."""
    out = []
    for b in re.split(r"\n\s*\n", text):
        s = " ".join(b.split())
        if s:
            out.append(s)
    return out


def ocr_score(s):
    """OCR-noise heuristic. Ignores legitimate single-letter words (I/a/A/O) and
    period-terminated initials; keys on runs of spaced letters and soft hyphens."""
    if not s:
        return 0.0
    toks = s.split()
    weird_one = sum(1 for t in toks if len(t) == 1 and t.isalpha() and t not in "IaAO")
    spaced = len(_SPACED.findall(s))
    soft = s.count("­")
    denom = max(len(toks), 1)
    return (3 * spaced + weird_one) / denom + soft / max(len(s), 1)


def detect_review(text3):
    """(is_review, trigger) from first ~3 pages of body text."""
    head = text3[:1400]
    if _REVIEWER_SIG.search(text3):
        return True, "reviewer-signature"
    if _BOOK_CITE.search(head):
        return True, "book-citation-head"
    if _BOOK_REVIEWS_HDR.search(text3[:120]):    # running header at top of a body page
        return True, "book-reviews-header"
    return False, None


def extract_abstract(p2_text):
    """(abstract|None, reason). Precision-biased: only a clean digit-free head paragraph."""
    blks = _blocks(p2_text)
    if len(blks) < 3:                      # need title/author, candidate, and a following body
        return None, "too-few-blocks"
    cand = blks[1]
    n = len(cand)
    if n < 80:
        return None, "cand-too-short"
    if n > 1500:
        return None, "cand-too-long"
    if _CAPS_LINE.match(cand):
        return None, "cand-all-caps"
    if re.search(r"\d", cand):             # footnote/page/section digit -> body, not abstract
        return None, "cand-has-digit(body/note)"
    if not re.search(r"[.!?]", cand):
        return None, "cand-no-sentence"
    return cand, "ok"


def classify_pdf(pdf):
    """Full verdict for one Asbury PDF path.
    returns dict: verdict in {review, abstract, no_abstract}, + fields."""
    t3 = pdftotext(pdf, 2, 4)              # article body starts p.2 (p.1 = ePLACE cover)
    if not t3.strip():
        t3 = pdftotext(pdf, 1, 3)
    is_rev, rtrig = detect_review(t3)
    if is_rev:
        return {"verdict": "review", "trigger": rtrig, "abstract": None, "ocr_suspect": False}
    p2 = pdftotext(pdf, 2, 2)
    ab, reason = extract_abstract(p2)
    if ab is None:                         # newer issues without a cover sheet: try p.1 head
        ab2, reason2 = extract_abstract(pdftotext(pdf, 1, 1))
        if ab2:
            ab, reason = ab2, reason2 + "(p1)"
    if ab is None:
        return {"verdict": "no_abstract", "trigger": reason, "abstract": None, "ocr_suspect": False}
    return {"verdict": "abstract", "trigger": "ok", "abstract": ab,
            "ocr_suspect": ocr_score(ab) > 0.06}


if __name__ == "__main__":
    import sys, json
    print(json.dumps(classify_pdf(sys.argv[1]), ensure_ascii=False))
