#!/usr/bin/env python3
"""P2/G2 full recovery: Philosophia Christi missing abstracts from pdcnet.org.

For every PC record still flagged ``missing_abstract`` (corpus_pc.jsonl), resolve
the DOI (its pdcnet anonymous-search redirect embeds the ``imuse_id``), rebuild
``/pc/content/<imuse_id>`` which 307-redirects to a public landing page (HTTP 200,
no paywall gate on the landing), and read two source-authoritative fields:

  Item_Data_Type == 'Book Review'  -> route to exclusion (source-confirmed review)
  <meta og:description> (>=120 ch)  -> verbatim author abstract (source: pdcnet-og)
  neither                          -> stays honestly missing (pre-2008 no-abstract tail)

Requests are spaced 5s + jitter (pdcnet robots Crawl-delay 5). Results are appended
(resumable) to data/raw/pc_recover_results.jsonl; landing pages cached in
data/raw/pc_page_cache/. Probes + records only; merge is done separately. No model.
"""
import json
import os
import re
import subprocess
import sys
import time
import html
import random
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_pilot as FP            # noqa: E402

RAW = FP.RAW
PAGE_CACHE = os.path.join(RAW, "pc_page_cache")
RESULTS = os.path.join(RAW, "pc_recover_results.jsonl")
LOG = os.path.join(RAW, "pc_recover.log")
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
SLEEP = 5.0

_IMUSE = re.compile(r"imuse_id(?:%3A|:)([a-zA-Z0-9_]+)")
_OGDESC = re.compile(r'<meta property="og:description" content="(.*?)"\s*/?>', re.S)
_DESC = re.compile(r'<meta name="description" content="(.*?)"\s*/?>', re.S)
_ITEMTYPE = re.compile(r"Item_Data_Type=([^&\"']+)")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def logline(s):
    line = "[%s] %s" % (now(), s)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def norm_doi(d):
    if not d:
        return None
    d = d.strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if d.startswith(p):
            d = d[len(p):]
    return d or None


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")] if os.path.exists(path) else []


def sleep():
    time.sleep(SLEEP + random.uniform(0, 1.5))


def _int(x):
    try:
        return int(str(x).strip())
    except (TypeError, ValueError):
        return None


def construct_imuse(rec):
    """Fallback imuse_id from biblio: pc_YYYY_VVVV_IIII_PPPP_QQQQ."""
    y = _int(rec.get("year")); v = _int(rec.get("volume")); iss = _int(rec.get("issue"))
    pg = rec.get("page") or ""
    m = re.match(r"\s*(\d+)\s*[-–]\s*(\d+)", pg)
    if not (y and v and iss and m):
        return None
    return "pc_%04d_%04d_%04d_%04d_%04d" % (y, v, iss, int(m.group(1)), int(m.group(2)))


def resolve_imuse(doi, rec):
    r = subprocess.run(["curl", "-sS", "-L", "-o", "/dev/null", "--max-time", "50",
                        "-A", UA, "-w", "%{url_effective}", "https://doi.org/" + doi],
                       capture_output=True, text=True, errors="replace")
    m = _IMUSE.search(r.stdout or "")
    if m:
        return m.group(1), "doi-redirect"
    c = construct_imuse(rec)
    return (c, "constructed") if c else (None, "unresolved")


def process(rec):
    doi = rec.get("doi") or ""
    iid = rec.get("item_id") or FP.sha16(doi)
    res = {"key": norm_doi(doi) or iid, "doi": doi, "item_id": iid, "ts": now(),
           "year": rec.get("year")}
    if not doi:
        res.update(verdict="no_doi", trigger="no doi")
        return res
    imuse, how = resolve_imuse(doi, rec)
    res["imuse_id"] = imuse; res["imuse_via"] = how
    sleep()
    if not imuse:
        res.update(verdict="no_imuse", trigger="could not resolve imuse_id")
        return res
    page = os.path.join(PAGE_CACHE, "%s.html" % imuse)
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", UA,
                        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "-H", "Accept-Language: en-US,en;q=0.5",
                        "-H", "Sec-Fetch-Dest: document", "-H", "Sec-Fetch-Mode: navigate",
                        "-H", "Sec-Fetch-Site: none",
                        "-H", "Referer: https://www.pdcnet.org/pc",
                        "-w", "%{http_code}", "-o", page, "https://www.pdcnet.org/pc/content/" + imuse],
                       capture_output=True, text=True, errors="replace")
    res["pdc_http"] = (r.stdout or "").strip()
    sleep()
    h = open(page, encoding="utf-8", errors="replace").read() if os.path.exists(page) else ""
    it = _ITEMTYPE.search(h)
    dtype = html.unescape(it.group(1)).strip() if it else None
    res["item_data_type"] = dtype
    m = _OGDESC.search(h) or _DESC.search(h)
    ab = html.unescape(m.group(1)).strip() if m else ""
    ab = " ".join(ab.split())              # whitespace-collapse only; verbatim
    res["abs_len"] = len(ab)
    if dtype and dtype.lower() in ("book review", "editorial", "news and announcements",
                                   "announcement", "in memoriam", "obituary"):
        res.update(verdict="review", trigger="Item_Data_Type=%s" % dtype,
                   had_abstract=(len(ab) >= 120))
        return res
    if len(ab) >= 120:
        res.update(verdict="abstract", trigger="og:description")
        res["abstract"] = ab
        return res
    res.update(verdict="no_abstract", trigger="empty og:description (pre-abstract tail?)")
    return res


def main():
    os.makedirs(PAGE_CACHE, exist_ok=True)
    done = {json.loads(l)["key"] for l in open(RESULTS, encoding="utf-8")} if os.path.exists(RESULTS) else set()
    tg = [r for r in load(os.path.join(RAW, "corpus_pc.jsonl")) if r.get("missing_abstract")]
    todo = [r for r in tg if (norm_doi(r.get("doi")) or r.get("item_id")) not in done]
    logline("PC recovery start: %d missing, %d already done, %d to do" % (len(tg), len(done), len(todo)))
    from collections import Counter
    tally = Counter()
    with open(RESULTS, "a", encoding="utf-8") as out:
        for i, r in enumerate(todo, 1):
            try:
                res = process(r)
            except Exception as e:
                res = {"key": norm_doi(r.get("doi")) or r.get("item_id"), "doi": r.get("doi"),
                       "item_id": r.get("item_id"), "verdict": "error",
                       "trigger": "exc: %s" % e, "ts": now()}
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
            out.flush()
            tally[res["verdict"]] += 1
            if i % 20 == 0 or i == len(todo):
                logline("  %d/%d  running=%s" % (i, len(todo), dict(tally)))
    logline("PC recovery DONE. this-run verdicts=%s" % dict(tally))
    return 0


if __name__ == "__main__":
    sys.exit(main())
