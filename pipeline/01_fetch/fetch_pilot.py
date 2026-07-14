#!/usr/bin/env python3
"""ditch-audit P1 harvester — Religious Studies 2015 + gold anchors.

Implements the harvester agent spec (.claude/agents/harvester.md). stdlib-only
(urllib, json, hashlib, time, re, html). No third-party deps.

Outputs (data/ is .gitignore'd — copyrighted abstracts stay local):
  data/raw/pilot_rs2015.jsonl  — RS vol.51 (2015) research articles + discussion notes
  data/raw/gold_anchors.jsonl  — the 20 gold anchors (item_id == anchor_id)

Schema (one JSON object per line):
  {"item_id","doi","title","authors","journal","year","abstract","source","fetched_at"}
  optional flags: "note" (discussion note/reply), "missing_abstract",
                  "book_blurb" (A20 publisher blurb in lieu of abstract),
                  provenance: "volume","issue","page","anchor_id"

Target population for the pilot is the *annual table of contents* = Religious
Studies **volume 51, issues 1-4** (the 2015 volume), NOT "pub-date 2015" (which
also catches online-first articles belonging to vols 52/53). We fetch a wide
date window and filter client-side on volume == "51".

Sources / fallback (3 attempts, then missing_abstract):
  1. Crossref REST (ISSN 0034-4125) — primary metadata + abstract.
  2. Publisher landing page via doi.org — JSON-LD description / citation_abstract
     meta / abstract div (Springer, Cambridge Core, ...). Polite 2s spacing.
  Abstracts unavailable from any source are flagged, never fabricated.
"""

import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

UA = "ditch-audit/0.1 (mailto:dankang21@gmail.com)"
ISSN = "0034-4125"                     # Religious Studies (print)
CROSSREF_SLEEP = 1.0                   # between Crossref pages
POLITE = 2.0                           # between publisher-page scrapes
WIN_FROM, WIN_UNTIL = "2013-06-01", "2017-06-01"   # wide enough to bracket vol.51

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "data", "raw")
GOLD_JSON = os.path.join(ROOT, "docs", "gold-anchors-v1.json")
OVERRIDES = os.path.join(RAW, "gold_overrides.json")   # verbatim abstracts fetched
                                                       # out-of-band (kept inside data/)

# --- gold DOI map (curated + validated against Crossref; DOIs are not copyright) --
GOLD_DOI = {
    "A01": "10.2307/20009775",          # Rowe 1979 APQ — JSTOR (not deposited to Crossref)
    "A02": "10.2307/2215486",           # Draper 1989 Nous (JSTOR)
    "A03": "10.1007/bf00136567",        # Wykstra 1984 IJPR (Springer)
    "A04": "10.1017/s0034412509990369", # Law 2010 RS
    "A05": "10.1017/S0034412505007614", # Schellenberg 2005 RS (I)  [from citation]
    "A06": "10.5840/faithphil200017215",# Morriston 2000 F&P (PDC)
    "A07": "10.1017/S0031819100009189", # Swinburne 1968 Philosophy [from citation]
    "A08": "10.1017/s0034412500016243", # Craig 1984 RS
    "A09": "10.1017/S0034412500020837", # Oppy 1991 RS           [from citation]
    "A10": "10.1093/pq/pqaa005",        # Malpass & Morriston 2020 PQ
    "A11": "10.1111/0029-4624.00210",   # White 2000 Nous (Wiley)
    "A12": "10.1093/mind/110.440.1027", # McGrew et al. 2001 Mind (OUP)
    "A13": "10.1007/s11153-008-9191-8", # Rasmussen 2009 IJPR (Springer)
    "A14": "10.1017/s0034412509990217", # Gwiazda 2009 RS
    "A15": "10.2307/2215239",           # Plantinga 1981 Nous     [from citation]
    "A16": "10.1111/1467-9213.00309",   # Bostrom 2003 PQ (Wiley)
    "A17": "10.1017/s0034412503006437", # Tuggy 2003 RS
    "A18": "10.5840/faithphil200522134",# Brower & Rea 2005 F&P (PDC)
    "A19": "10.5840/faithphil200421446",# Swinburne 2004 F&P (PDC)
    "A20": None,                        # Allison 2021 monograph — no DOI
}
# For DOIs Crossref cannot serve metadata for (A01 JSTOR 404, A20 no DOI):
GOLD_FALLBACK_META = {
    "A01": {"title": "The Problem of Evil and Some Varieties of Atheism",
            "authors": ["William L. Rowe"],
            "journal": "American Philosophical Quarterly", "year": 1979},
    "A20": {"title": "The Resurrection of Jesus: Apologetics, Polemics, History",
            "authors": ["Dale C. Allison Jr"],
            "journal": "T&T Clark (Bloomsbury)", "year": 2021},
}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read()


def crossref_message(url):
    _, body = http_get(url)
    return json.loads(body.decode("utf-8"))["message"]


def crossref_work(doi):
    """Full single-work record, or None on HTTP error (e.g. JSTOR not in Crossref)."""
    try:
        return crossref_message("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None


def clean_abstract(a):
    if not a:
        return ""
    a = re.sub(r"(?is)<jats:title>.*?</jats:title>", " ", a)
    a = re.sub(r"<[^>]+>", " ", a)
    a = html.unescape(a)
    a = re.sub(r"\s+", " ", a).strip()
    a = re.sub(r"^(Abstract|ABSTRACT)\s*[:.]?\s*", "", a)
    return a


def clean_title(item):
    t = (item.get("title") or [""])
    t = t[0] if t else ""
    sub = item.get("subtitle") or []
    sub = sub[0] if sub else ""
    full = t + (". " + sub if sub else "")
    full = re.sub(r"<[^>]+>", "", full)
    return html.unescape(full).strip()


def authors_from(item):
    out = []
    for a in item.get("author", []) or []:
        nm = " ".join(x for x in [a.get("given"), a.get("family")] if x) or a.get("name")
        if nm:
            out.append(nm.strip())
    return out


def year_from(item, default=None):
    for key in ("published-print", "published-online", "published", "issued"):
        dp = (item.get(key) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return default


def page_span(item):
    p = item.get("page") or ""
    m = re.match(r"^\s*(\d+)\s*[-–]\s*(\d+)\s*$", p)
    if not m:
        return None
    return int(m.group(2)) - int(m.group(1)) + 1


# --- publisher-page abstract fallback (best-effort, strict about what counts) ----
def _jsonld_descriptions(text):
    """Yield candidate abstract strings from JSON-LD blocks, incl. nested
    mainEntity / @graph nodes (Springer nests the abstract under mainEntity)."""
    for m in re.finditer(r"(?is)<script[^>]+application/ld\+json[^>]*>(.*?)</script>", text):
        try:
            j = json.loads(m.group(1))
        except Exception:
            continue
        nodes = []
        for obj in (j if isinstance(j, list) else [j]):
            if not isinstance(obj, dict):
                continue
            nodes.append(obj)
            me = obj.get("mainEntity")
            if isinstance(me, dict):
                nodes.append(me)
            g = obj.get("@graph")
            if isinstance(g, list):
                nodes += [x for x in g if isinstance(x, dict)]
        for node in nodes:
            d = node.get("description")
            if d and len(d) > 60 and not re.match(r"(?i)^\s*by .+ published on", d):
                yield d


def publisher_abstract(doi):
    """Follow doi.org and extract a *real* abstract: JSON-LD description,
    citation_abstract meta, or an abstract-classed div. Deliberately does NOT use
    generic og:description (repositories put "By AUTHOR, Published on ..." there)."""
    try:
        _final, body = http_get("https://doi.org/" + doi, timeout=45)
    except Exception:
        return ""
    text = body.decode("utf-8", "replace")
    for d in _jsonld_descriptions(text):        # Springer et al.
        return clean_abstract(d)
    m = re.search(r'(?is)<meta[^>]+name="citation_abstract"[^>]+content="([^"]{60,})"', text)
    if m:                                       # Cambridge Core, HighWire
        return clean_abstract(m.group(1))
    m = re.search(r'(?is)id="Abs1-content"[^>]*>(.*?)</(?:div|section)>', text)
    if m:                                       # Springer abstract block
        t = clean_abstract(m.group(1))
        if len(t) > 60:
            return t
    m = re.search(r'(?is)<div[^>]+class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>', text)
    if m:                                       # generic abstract div
        t = clean_abstract(m.group(1))
        if len(t) > 60:
            return t
    return ""


def resolve_abstract(doi, cr_item):
    """3 attempts (Crossref -> publisher -> publisher retry). Returns (text, source)."""
    a = clean_abstract((cr_item or {}).get("abstract"))
    if len(a) > 40:
        return a, "crossref"
    if not doi:
        return "", ""
    for _ in range(2):
        time.sleep(POLITE)
        a = publisher_abstract(doi)
        if len(a) > 40:
            return a, "publisher-page"
    return "", ""


# --------------------------------- classification --------------------------------
FRONT_BACK = re.compile(r"(?i)(cover and (front|back) matter|^front matter$|^back matter$)")
# reply/discussion-register cues (NOT bare 'critique of': many full articles critique
# a position; a reply is a response to a *specific prior paper*).
NOTE_TITLE = re.compile(r"(?i)\b(reply to|reply\b|response to|rejoinder|comment on|"
                        r"revisited|a note on|postscript)\b")
# RS 2015 discussion notes/replies whose 'note' status is a metadata-invisible
# editorial judgment. PROVISIONAL — flagged for HITL confirmation in harvest_log.
PILOT_NOTE_DOIS = {
    "10.1017/s0034412514000328",   # Sovik & Eikrem, reply to Shearn (2013)
    "10.1017/s0034412515000323",   # Kapitan, "Tough choices still" (reply/continuation)
    "10.1017/s0034412515000347",   # "Whither philosophy of religion?" (anniversary forum)
}


def classify(item):
    """Return (kind, reason). kind in {'article','note','exclude'}."""
    title = clean_title(item)
    tl = title.lower()
    page = (item.get("page") or "").lower()
    doi = (item.get("DOI") or "").lower()

    if re.match(r"^[bf]\d", page) or FRONT_BACK.search(tl):
        return "exclude", "front/back matter"
    if "corrigendum" in tl or "erratum" in tl:
        return "exclude", "corrigendum/erratum"
    if tl == "editorial" or tl.startswith("editorial"):
        return "exclude", "editorial"
    if "essay prize" in tl:
        return "exclude", "announcement (prize notice)"
    if "fifty years of religious studies" in tl:
        return "exclude", "editorial retrospective (50th-anniversary)"
    # book reviews (RS reviews are typed journal-article; use bibliographic signals)
    if item.get("type") == "book-review":
        return "exclude", "book review (crossref type)"
    if re.search(r"\bISBN\b", title) or re.search(r"\bPp\.\s", title):
        return "exclude", "book review (bibliographic signature)"

    span = page_span(item)
    if doi in PILOT_NOTE_DOIS or NOTE_TITLE.search(title) or (span is not None and span <= 5):
        return "note", ""
    return "article", ""


# ------------------------------------- pilot -------------------------------------
def fetch_pilot_records():
    items, cursor = [], "*"
    while True:
        url = ("https://api.crossref.org/journals/%s/works?"
               "filter=from-pub-date:%s,until-pub-date:%s&rows=100&cursor=%s"
               "&select=DOI,title,subtitle,type,volume,issue,page,author,abstract,"
               "container-title,published-print,published-online"
               % (ISSN, WIN_FROM, WIN_UNTIL, urllib.parse.quote(cursor)))
        msg = crossref_message(url)
        its = msg["items"]
        items += its
        cursor = msg.get("next-cursor")
        if not its or not cursor:
            break
        time.sleep(CROSSREF_SLEEP)

    v51 = [it for it in items if it.get("volume") == "51"]
    records, excluded, seen = [], [], set()
    for it in sorted(v51, key=lambda x: (int(x.get("issue") or 0), x.get("page") or "")):
        kind, reason = classify(it)
        doi = it["DOI"]
        if kind == "exclude":
            excluded.append({"doi": doi, "issue": it.get("issue"), "page": it.get("page"),
                             "title": clean_title(it), "reason": reason})
            continue
        if doi in seen:                       # dedup by DOI
            continue
        seen.add(doi)
        abs_text, src = resolve_abstract(doi, it)
        rec = {
            "item_id": sha16(doi),
            "doi": doi,
            "title": clean_title(it),
            "authors": authors_from(it),
            "journal": (it.get("container-title") or ["Religious Studies"])[0],
            "year": year_from(it, 2015),
            "abstract": abs_text,
            "source": src or "crossref",
            "fetched_at": now_iso(),
            "volume": "51",
            "issue": it.get("issue"),
            "page": it.get("page"),
        }
        if kind == "note":
            rec["note"] = True
        if not abs_text:
            rec["missing_abstract"] = True
        records.append(rec)
    return records, excluded


# -------------------------------------- gold -------------------------------------
def fetch_gold_records():
    gold = json.load(open(GOLD_JSON, encoding="utf-8"))["anchors"]
    overrides = {}
    if os.path.exists(OVERRIDES):
        overrides = json.load(open(OVERRIDES, encoding="utf-8"))

    records = []
    for a in gold:
        aid = a["anchor_id"]
        doi = GOLD_DOI.get(aid)
        cr = crossref_work(doi) if doi else None
        fb = GOLD_FALLBACK_META.get(aid, {})

        if cr:
            title = clean_title(cr)
            authors = authors_from(cr)
            journal = (cr.get("container-title") or [fb.get("journal", "")])[0]
            year = year_from(cr, fb.get("year"))
        else:
            title = fb.get("title", "")
            authors = fb.get("authors", [])
            journal = fb.get("journal", "")
            year = fb.get("year")

        ov = overrides.get(aid) or {}
        if ov.get("abstract"):
            abs_text, src = ov["abstract"], ov.get("source", "override")
        else:
            abs_text, src = resolve_abstract(doi, cr)

        rec = {
            "item_id": aid,                   # CONTRACT: gold item_id == anchor_id
            "anchor_id": aid,
            "doi": doi or "",
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "abstract": abs_text,
            "source": src or "crossref",
            "fetched_at": now_iso(),
        }
        if ov.get("book_blurb"):
            rec["book_blurb"] = True
        if not abs_text:
            rec["missing_abstract"] = True
        records.append(rec)
        if doi:
            time.sleep(CROSSREF_SLEEP)
    return records


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def coverage(records):
    n = len(records)
    have = sum(1 for r in records if not r.get("missing_abstract"))
    return have, n, (have / n if n else 0.0)


def main():
    os.makedirs(RAW, exist_ok=True)

    print("== PILOT: Religious Studies vol.51 (2015) ==")
    pilot, excluded = fetch_pilot_records()
    write_jsonl(os.path.join(RAW, "pilot_rs2015.jsonl"), pilot)

    have, n, cov = coverage(pilot)
    notes = [r for r in pilot if r.get("note")]
    dois = [r["doi"] for r in pilot]
    print("  included items      :", n, "(articles %d + notes %d)" % (n - len(notes), len(notes)))
    print("  excluded            :", len(excluded))
    print("  excluded by reason  :", dict(Counter(e["reason"] for e in excluded)))
    per_issue = Counter(r["issue"] for r in pilot)
    print("  included by issue   :", dict(sorted(per_issue.items(), key=lambda x: str(x[0]))))
    print("  DOI uniqueness      :", "%d unique / %d rows" % (len(set(dois)), len(dois)))
    print("  abstract coverage   :", "%d/%d = %.1f%%" % (have, n, cov * 100))
    if cov < 0.90:
        print("  *** HARD STOP: pilot abstract coverage < 90% ***")
        print("  missing:", [(r["doi"], r["page"]) for r in pilot if r.get("missing_abstract")])

    print("\n== GOLD: 20 anchors ==")
    goldrecs = fetch_gold_records()
    write_jsonl(os.path.join(RAW, "gold_anchors.jsonl"), goldrecs)
    ghave, gn, gcov = coverage(goldrecs)
    print("  items               :", gn, "(expected 20)")
    gdois = [r["doi"] for r in goldrecs if r["doi"]]
    print("  DOI uniqueness      :", "%d unique / %d with-DOI" % (len(set(gdois)), len(gdois)))
    print("  abstract coverage   :", "%d/%d = %.1f%%" % (ghave, gn, gcov * 100))
    print("  item_id==anchor_id  :", all(r["item_id"] == r["anchor_id"] for r in goldrecs))
    print("  missing_abstract    :",
          [(r["anchor_id"], r["doi"] or "(no doi)") for r in goldrecs if r.get("missing_abstract")])
    for r in goldrecs:
        tag = "MISSING" if r.get("missing_abstract") else ("BLURB" if r.get("book_blurb") else "OK")
        print("   %-4s %-7s src=%-16s %s" % (r["anchor_id"], tag, r["source"], (r["abstract"][:55])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
