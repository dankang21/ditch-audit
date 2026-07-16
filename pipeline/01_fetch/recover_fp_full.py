#!/usr/bin/env python3
"""P2/G2 full recovery: F&P missing abstracts from Asbury open-access PDFs.

For every F&P record still flagged ``missing_abstract`` (corpus_fp.jsonl +
fp_backfill.jsonl), resolve the DOI to its place.asburyseminary.edu landing,
download the article PDF with a browser header set + session cookie jar, and run
fp_pdf_extract.classify_pdf:

  verdict = review        -> route to exclusion (source-confirmed book review)
  verdict = abstract      -> verbatim printed abstract (source: asbury-pdf)
  verdict = no_abstract   -> stays honestly missing (discussion note / no head abstract)

THROTTLE HANDLING: the bepress viewcontent.cgi endpoint rate-limits bursts,
returning a small non-PDF body under 403 / 202 / 429 / 5xx. A single process
paces FP_SLEEP s between requests, keeps a cookie jar, and on any such throttle
response backs off [45,120,300] s (retrying the same PDF) while tracking
consecutive throttles -- 3 in a row triggers a 300 s cooldown. Runs are resumable
(results keyed by DOI); only non-terminal verdicts (no_pdf/no_landing/error) are
retried on a re-launch after the results file is cleaned. Records only; merge is
separate. No model.
"""
import json
import os
import re
import subprocess
import sys
import time
import html
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fp_pdf_extract as X          # noqa: E402
import fetch_pilot as FP            # noqa: E402

RAW = FP.RAW
PDF_CACHE = os.path.join(RAW, "fp_pdf_cache")
RESULTS = os.path.join(RAW, "fp_recover_results.jsonl")
LOG = os.path.join(RAW, "fp_recover.log")
COOKIES = os.path.join(PDF_CACHE, "cookies.txt")
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
SLEEP = float(os.environ.get("FP_SLEEP", "12"))
BACKOFF = [45, 120, 300]
THROTTLE_CODES = ("403", "202", "429", "500", "502", "503", "504")

_PDF_META = re.compile(r'bepress_citation_pdf_url"\s+content="([^"]+)"')
_CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
_consec = 0


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


def curl(url, out, referer=None, accept="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"):
    cmd = ["curl", "-sS", "-L", "--max-time", "80", "-A", UA,
           "-b", COOKIES, "-c", COOKIES,
           "-H", "Accept: " + accept,
           "-H", "Accept-Language: en-US,en;q=0.5",
           "-H", "Sec-Fetch-Dest: document", "-H", "Sec-Fetch-Mode: navigate",
           "-H", "Sec-Fetch-Site: same-origin",
           "-w", "%{http_code} %{url_effective}"]
    if referer:
        cmd += ["-H", "Referer: " + referer]
    cmd += ["-o", out, url]
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    st = r.stdout.strip().splitlines()
    return (st[-1] if st else "")


def targets():
    out = []
    for path, sf in [(os.path.join(RAW, "corpus_fp.jsonl"), "fp"),
                     (os.path.join(RAW, "fp_backfill.jsonl"), "bf")]:
        for r in load(path):
            if r.get("missing_abstract"):
                out.append((sf, r))
    return out


def download_pdf(pdf_url, pdf_path, referer):
    """Return (ok, http_status, bytes). Retries on throttle responses with backoff."""
    global _consec
    st, size = "", 0
    for attempt in range(len(BACKOFF) + 1):
        st = curl(pdf_url, pdf_path, referer=referer, accept="application/pdf,*/*;q=0.8")
        size = os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0
        ok = size > 2000 and open(pdf_path, "rb").read(5).startswith(b"%PDF")
        if ok:
            _consec = 0
            return True, st, size
        throttled = st.startswith(THROTTLE_CODES) or (0 <= size < 2000)
        if throttled:
            _consec += 1
            if attempt < len(BACKOFF):
                logline("    throttle on PDF (%s, %dB, attempt %d) -> backoff %ds"
                        % (st[:3], size, attempt + 1, BACKOFF[attempt]))
                time.sleep(BACKOFF[attempt])
                continue
        break
    return False, st, size


def process(sf, rec):
    doi = rec.get("doi") or ""
    iid = rec.get("item_id") or FP.sha16(doi or rec.get("alt_id", ""))
    res = {"key": norm_doi(doi) or iid, "doi": doi, "item_id": iid, "source_file": sf, "ts": now()}
    if not doi:
        res.update(verdict="no_doi", trigger="no doi (backfill alt_id)")
        return res
    land = os.path.join(PDF_CACHE, "land_%s.html" % iid)
    res["landing_http"] = curl("https://doi.org/" + doi, land)
    time.sleep(SLEEP)
    h = open(land, encoding="utf-8", errors="replace").read() if os.path.exists(land) else ""
    m = _PDF_META.search(h)
    if not m or "asburyseminary.edu" not in res["landing_http"]:
        res.update(verdict="no_landing", trigger="no bepress pdf_url / not Asbury")
        return res
    pdf_url = html.unescape(m.group(1))
    cm = _CANON.search(h)
    referer = html.unescape(cm.group(1)) if cm else ("https://doi.org/" + doi)
    pdf_path = os.path.join(PDF_CACHE, "%s.pdf" % iid)
    ok, st2, size = download_pdf(pdf_url, pdf_path, referer)
    res["pdf_http"] = st2
    res["pdf_bytes"] = size
    time.sleep(SLEEP)
    if not ok:
        res.update(verdict="no_pdf", trigger="download failed / throttle / not pdf")
        return res
    v = X.classify_pdf(pdf_path)
    res.update(verdict=v["verdict"], trigger=v["trigger"], ocr_suspect=v["ocr_suspect"])
    if v["verdict"] == "abstract":
        res["abstract"] = v["abstract"]
    return res


def main():
    global _consec
    os.makedirs(PDF_CACHE, exist_ok=True)
    done = {json.loads(l)["key"] for l in open(RESULTS, encoding="utf-8")} if os.path.exists(RESULTS) else set()
    tg = targets()
    todo = [(sf, r) for sf, r in tg if (norm_doi(r.get("doi")) or r.get("item_id")) not in done]
    logline("FP recovery start: %d missing, %d done, %d to do (SLEEP=%.0fs)"
            % (len(tg), len(done), len(todo), SLEEP))
    tally = Counter()
    with open(RESULTS, "a", encoding="utf-8") as out:
        for i, (sf, r) in enumerate(todo, 1):
            if _consec >= 3:
                logline("    %d consecutive throttles -> 300s cooldown" % _consec)
                time.sleep(300)
                _consec = 0
            try:
                res = process(sf, r)
            except Exception as e:
                res = {"key": norm_doi(r.get("doi")) or r.get("item_id"), "doi": r.get("doi"),
                       "item_id": r.get("item_id"), "source_file": sf, "verdict": "error",
                       "trigger": "exc: %s" % e, "ts": now()}
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
            out.flush()
            tally[res["verdict"]] += 1
            if i % 15 == 0 or i == len(todo):
                logline("  %d/%d  running=%s" % (i, len(todo), dict(tally)))
    logline("FP recovery DONE. this-run verdicts=%s" % dict(tally))
    return 0


if __name__ == "__main__":
    sys.exit(main())
