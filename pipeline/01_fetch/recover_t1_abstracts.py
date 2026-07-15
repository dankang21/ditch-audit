#!/usr/bin/env python3
"""ditch-audit P2 aux task 1 — recover MISSING abstracts for T1 candidate hits.

Fills the ``abstract`` field for records in ``data/raw/t1_candidates.jsonl`` that
carry ``missing_abstract`` (or an empty ``abstract``) using **verbatim database
metadata only**:

  1. OpenAlex  (api.openalex.org, ``abstract_inverted_index`` reconstructed in
     strict positional order -> the exact deposited words, no paraphrase).
  2. Semantic Scholar Graph API (fallback; ``abstract`` field verbatim).

VERBATIM GUARANTEE: OpenAlex abstracts are rebuilt token-for-token from the
inverted index (each word placed back at its recorded position, whitespace
collapsed, nothing added/dropped/summarised); Semantic Scholar abstracts are
used exactly as returned. NO model, NO generation, NO paraphrase anywhere.

Recovered records: original fields preserved, ``abstract`` filled,
``source`` set to ``"openalex"``/``"semanticscholar"``, ``missing_abstract``
flag dropped, ``recovered_at`` stamped, and ``matched_keywords`` re-applied over
(title + abstract) with the SAME keyword list as the T1 harvester (a record is
NEVER dropped -- it already matched on title; abstract match only ADDS keywords).

Does not touch: corpus_*.jsonl, fetch_corpus.py. Writes only t1_* outputs.

Outputs (data/ is .gitignore'd -- copyrighted abstracts stay local):
  data/raw/t1_candidates.jsonl        (in place; atomic replace)
  data/raw/t1_recover_log.md
  data/raw/t1_recover_cache/*.json    (raw API responses; resume-safe)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_t1_candidates as t1  # reuse KEYWORDS + matched_keywords  # noqa: E402

ROOT = t1.ROOT
RAW = t1.RAW
CAND = os.path.join(RAW, "t1_candidates.jsonl")
LOG = os.path.join(RAW, "t1_recover_log.md")
CACHE_DIR = os.path.join(RAW, "t1_recover_cache")

MAILTO = "dankang21@gmail.com"
UA = "ditch-audit/1.0 (mailto:%s)" % MAILTO
OA_BATCH = 50            # OpenAlex OR-filter batch size
OA_SLEEP = 1.0           # polite pause between OpenAlex batch calls
SS_SLEEP = 3.5           # Semantic Scholar unauthenticated: be gentle
MIN_ABS = 40             # min chars to count as a real abstract (log shorter ones)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def http_json(url, timeout=40, retries=4):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(4 * (i + 1))
                continue
            return None
        except Exception:
            if i < retries - 1:
                time.sleep(3 * (i + 1))
                continue
            return None
    return None


def norm_doi(d):
    if not d:
        return ""
    d = d.strip().lower()
    for pre in ("https://doi.org/", "http://doi.org/", "doi.org/"):
        if d.startswith(pre):
            d = d[len(pre):]
    return d


def abstract_from_inverted_index(inv):
    """Rebuild the deposited abstract token-for-token, positional order. Verbatim."""
    if not inv:
        return ""
    pairs = []
    for word, positions in inv.items():
        for p in positions:
            pairs.append((p, word))
    pairs.sort(key=lambda x: x[0])
    text = " ".join(w for _, w in pairs)
    return " ".join(text.split())  # whitespace-normalise only; no content change


# ------------------------------------------------------------------ OpenAlex ---
def openalex_batch(dois):
    """Return {norm_doi: abstract_text} for a batch (<=50) via OR-filter."""
    key = "oa_%s.json" % t1.fp.sha16("|".join(sorted(dois)))
    cache = os.path.join(CACHE_DIR, key)
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        filt = "|".join(dois)
        url = ("https://api.openalex.org/works?filter=doi:%s&per-page=%d"
               "&select=id,doi,abstract_inverted_index&mailto=%s"
               % (urllib.parse.quote(filt), OA_BATCH, MAILTO))
        data = http_json(url)
        if data is None:
            return {}
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        time.sleep(OA_SLEEP)
    out = {}
    for w in data.get("results", []):
        nd = norm_doi(w.get("doi"))
        if not nd:
            continue
        out[nd] = abstract_from_inverted_index(w.get("abstract_inverted_index"))
    return out


# ---------------------------------------------------------- Semantic Scholar ---
def semanticscholar_one(doi):
    key = "ss_%s.json" % t1.fp.sha16(doi)
    cache = os.path.join(CACHE_DIR, key)
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            data = json.load(f)
    else:
        url = ("https://api.semanticscholar.org/graph/v1/paper/DOI:%s"
               "?fields=title,abstract,year" % urllib.parse.quote(doi))
        data = http_json(url)
        if data is None:
            return ""
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        time.sleep(SS_SLEEP)
    return (data.get("abstract") or "").strip()


# ------------------------------------------------------------------- main run --
def load_rows():
    rows = []
    with open(CAND, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def is_missing(rec):
    return bool(rec.get("missing_abstract")) or not (rec.get("abstract") or "").strip()


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    rows = load_rows()
    targets = [r for r in rows if is_missing(r) and r.get("doi")]
    no_doi = [r for r in rows if is_missing(r) and not r.get("doi")]
    print("total rows=%d  missing=%d  (no-doi missing=%d)"
          % (len(rows), len(targets) + len(no_doi), len(no_doi)), flush=True)

    stat = Counter()
    recovered = {}  # doi -> (abstract, source)

    # --- pass 1: OpenAlex, batched ------------------------------------------
    tdois = [norm_doi(r["doi"]) for r in targets]
    for i in range(0, len(tdois), OA_BATCH):
        batch = tdois[i:i + OA_BATCH]
        res = openalex_batch(batch)
        for d in batch:
            a = res.get(d, "")
            if len(a) >= MIN_ABS:
                recovered[d] = (a, "openalex")
                stat["openalex"] += 1
            elif 0 < len(a) < MIN_ABS:
                stat["openalex_too_short"] += 1
        print("  OpenAlex batch %d-%d: cumulative recovered=%d"
              % (i, i + len(batch), stat["openalex"]), flush=True)

    # --- pass 2: Semantic Scholar fallback for still-missing ----------------
    still = [d for d in tdois if d not in recovered]
    print("  OpenAlex done: %d recovered, %d -> Semantic Scholar fallback"
          % (stat["openalex"], len(still)), flush=True)
    for j, d in enumerate(still):
        a = semanticscholar_one(d)
        if len(a) >= MIN_ABS:
            recovered[d] = (a, "semanticscholar")
            stat["semanticscholar"] += 1
        elif 0 < len(a) < MIN_ABS:
            stat["ss_too_short"] += 1
        else:
            stat["unrecovered"] += 1
        if (j + 1) % 20 == 0:
            print("  SS %d/%d (recovered here=%d)"
                  % (j + 1, len(still), stat["semanticscholar"]), flush=True)

    # --- apply to rows ------------------------------------------------------
    added_kw = Counter()
    for r in rows:
        if not is_missing(r) or not r.get("doi"):
            continue
        d = norm_doi(r["doi"])
        if d not in recovered:
            continue
        abs_text, src = recovered[d]
        before = set(r.get("matched_keywords", []))
        r["abstract"] = abs_text
        r["source"] = src
        r["recovered_at"] = now_iso()
        r.pop("missing_abstract", None)
        # re-apply keyword filter over title + abstract (never drops; only adds)
        mk = t1.matched_keywords(r.get("title", "") + " " + abs_text)
        merged = sorted(set(mk) | before)
        for k in set(mk) - before:
            added_kw[k] += 1
        r["matched_keywords"] = merged

    # --- atomic write back --------------------------------------------------
    tmp = CAND + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, CAND)

    write_log(rows, targets, no_doi, stat, added_kw)
    print("\nDONE. recovered OA=%d SS=%d unrecovered=%d  log-> %s"
          % (stat["openalex"], stat["semanticscholar"], stat["unrecovered"], LOG),
          flush=True)


def write_log(rows, targets, no_doi, stat, added_kw):
    total = len(rows)
    have_abs = sum(1 for r in rows if len((r.get("abstract") or "").strip()) >= MIN_ABS)
    cov = have_abs / total * 100 if total else 0.0
    miss_before = len(targets) + len(no_doi)
    L = []
    A = L.append
    A("# t1_recover_log — P2 aux task 1: T1 hit abstract recovery")
    A("")
    A("- generated: %s" % now_iso())
    A("- script: `pipeline/01_fetch/recover_t1_abstracts.py` (stdlib-only)")
    A("- sources: **OpenAlex** (inverted-index -> verbatim) then **Semantic "
      "Scholar** fallback (abstract field verbatim). No generation/paraphrase.")
    A("- copyright isolation: abstracts written under `data/` (.gitignore'd); "
      "not reproduced in this log.")
    A("")
    A("## Recovery counts (by source)")
    A("")
    A("| source | recovered | note |")
    A("|---|---|---|")
    A("| OpenAlex | %d | inverted_index reconstructed positionally |" % stat["openalex"])
    A("| Semantic Scholar | %d | abstract field (OpenAlex miss) |" % stat["semanticscholar"])
    A("| unrecovered | %d | neither DB had an abstract |" % stat["unrecovered"])
    A("| (OpenAlex too-short, <%d ch) | %d | not accepted; sent to fallback |"
      % (MIN_ABS, stat["openalex_too_short"]))
    A("| (SS too-short, <%d ch) | %d | not accepted |" % (MIN_ABS, stat["ss_too_short"]))
    A("| no-DOI missing (unreachable by DOI lookup) | %d | left flagged |" % len(no_doi))
    A("")
    A("## T1 hit abstract coverage")
    A("")
    A("- missing before recovery: **%d**" % miss_before)
    A("- recovered this run: **%d** (OA %d + SS %d)"
      % (stat["openalex"] + stat["semanticscholar"], stat["openalex"], stat["semanticscholar"]))
    A("- rows with abstract (>=%d ch): **%d / %d = %.1f%%**"
      % (MIN_ABS, have_abs, total, cov))
    A("- still missing: **%d**" % (total - have_abs))
    A("")
    A("## Keyword deltas from newly-added abstracts (abstract-only matches)")
    A("")
    if added_kw:
        A("| keyword | rows where abstract ADDED it |")
        A("|---|---|")
        for k, n in added_kw.most_common():
            A("| `%s` | %d |" % (k, n))
    else:
        A("_none — every recovered row's keywords were already covered by title._")
    A("")
    A("## Verbatim provenance")
    A("")
    A("OpenAlex: each abstract token re-placed at its recorded inverted-index "
      "position, whitespace collapsed only. Semantic Scholar: `abstract` field "
      "returned as-is. No summarisation/paraphrase/generation at any step.")
    A("")
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    run()
