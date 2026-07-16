#!/usr/bin/env python3
"""fetch_citation_snapshot.py — R5 citation snapshot fetcher (analysis-plan
v1.1 §8 R5; freeze-manifest item 22).

Freeze semantics (item 22, amended wording): the SCRIPT is frozen now
(hashed in the manifest); the SNAPSHOT DATA is pulled once at P5 — citation
counts are analysis-time covariates, not part of the instrument. At pull
time the downloaded snapshot file itself is hashed and its source and date
recorded (the accompanying *_manifest.json), and R5 weights are computed as
log(1 + citations) from that single frozen snapshot (robustness-only by
outline fiat).

Mechanics (stdlib-only):
  * source: OpenAlex `/works` with a batched DOI filter
    (filter=doi:<doi1>|<doi2>|..., <= 50 DOIs per request,
    select=doi,id,cited_by_count; mailto polite-pool parameter attached);
  * input: the locked corpus JSONL(s) (item_id + doi rows) or a plain DOI
    list file (one DOI per line);
  * output: one JSONL row per input item, sorted by DOI —
      {"doi", "item_id", "openalex_id", "cited_by_count", "matched"}
    unmatched DOIs are kept with matched=false and cited_by_count=null
    (never fabricated); plus <out>_manifest.json with source, retrieval
    date, input/output SHA256 and match counts;
  * deterministic given the same API responses: input DOIs are normalized
    (casefolded, doi.org prefixes stripped) and deduplicated, output is
    sorted, retries with backoff on 429/5xx.

--selftest is fully offline (URL construction, DOI normalization, response
parsing, output assembly on fixture responses). The real pull is a P5
action; running it earlier would just produce a snapshot that P5 must not
use (the manifest records the pull date).

Usage (at P5):
  python3 pipeline/05_analysis/fetch_citation_snapshot.py \
      --corpus data/raw/corpus_*.jsonl data/raw/fp_backfill.jsonl \
               data/raw/t1_final.jsonl \
      --out data/raw/citation_snapshot.jsonl --mailto <contact>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OPENALEX_WORKS = "https://api.openalex.org/works"
BATCH_SIZE = 50            # OpenAlex OR-filter limit per request
SELECT = "doi,id,cited_by_count"
PER_PAGE = 100
HTTP_TIMEOUT = 120
RETRY_DELAYS = [1.0, 2.0, 4.0]
POLITE_INTERVAL = 0.25


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def utcnow() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def normalize_doi(doi) -> str | None:
    """Casefold; strip doi.org URL prefixes and a leading 'doi:'."""
    if not doi or not isinstance(doi, str):
        return None
    d = doi.strip().casefold()
    for pre in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/",
                "http://dx.doi.org/", "doi:"):
        if d.startswith(pre):
            d = d[len(pre):]
            break
    return d or None


def batch_url(dois: list, mailto: str | None, cursor: str = "*") -> str:
    filt = "doi:" + "|".join(dois)
    params = {"filter": filt, "select": SELECT, "per-page": str(PER_PAGE),
              "cursor": cursor}
    if mailto:
        params["mailto"] = mailto
    return OPENALEX_WORKS + "?" + urllib.parse.urlencode(params)


def http_get_json(url: str):
    last = None
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "ditch-audit R5 citation snapshot (stdlib urllib)"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                last = e
                if attempt >= len(RETRY_DELAYS):
                    break
                delay = RETRY_DELAYS[attempt]
                ra = e.headers.get("retry-after") if e.headers else None
                if ra:
                    try:
                        delay = max(delay, float(ra))
                    except ValueError:
                        pass
                print(f"  [retry] HTTP {e.code}; backing off {delay:.1f}s",
                      file=sys.stderr)
                time.sleep(delay)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError,
                json.JSONDecodeError) as e:
            last = e
            if attempt >= len(RETRY_DELAYS):
                break
            time.sleep(RETRY_DELAYS[attempt])
    die(f"OpenAlex request failed after retries: {last}", 3)


def parse_works_page(page: dict) -> dict:
    """-> {normalized_doi: {"openalex_id", "cited_by_count"}}."""
    out = {}
    for w in page.get("results") or []:
        d = normalize_doi(w.get("doi"))
        if not d:
            continue
        out[d] = {"openalex_id": w.get("id"),
                  "cited_by_count": w.get("cited_by_count")}
    return out


def fetch_batch(dois: list, mailto: str | None, get=http_get_json) -> dict:
    """One <=50-DOI OR-filter query, cursor-paginated. `get` is injectable
    for the offline selftest."""
    found = {}
    cursor = "*"
    while cursor:
        page = get(batch_url(dois, mailto, cursor))
        found.update(parse_works_page(page))
        cursor = (page.get("meta") or {}).get("next_cursor")
        if cursor:
            time.sleep(POLITE_INTERVAL)
    return found


def load_input_dois(corpus_paths: list, doi_file: str | None):
    """-> (ordered unique normalized DOIs, doi -> [item_id, ...])."""
    dois, items_of = [], {}
    seen = set()

    def add(doi, item_id=None):
        d = normalize_doi(doi)
        if not d:
            return
        if d not in seen:
            seen.add(d)
            dois.append(d)
        if item_id:
            items_of.setdefault(d, []).append(item_id)

    for p in corpus_paths or []:
        with open(p, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError as e:
                    die(f"{p}:{n}: invalid JSON ({e})", 4)
                add(r.get("doi"), r.get("item_id"))
    if doi_file:
        with open(doi_file, encoding="utf-8") as f:
            for line in f:
                add(line.strip())
    return sorted(dois), items_of


def assemble_rows(dois: list, items_of: dict, found: dict) -> list:
    rows = []
    for d in sorted(dois):
        hit = found.get(d)
        iids = sorted(items_of.get(d, []))
        rows.append({
            "doi": d,
            "item_id": iids[0] if len(iids) == 1 else (iids or None),
            "openalex_id": hit["openalex_id"] if hit else None,
            "cited_by_count": hit["cited_by_count"] if hit else None,
            "matched": bool(hit),
        })
    return rows


def r5_weight(cited_by_count) -> float | None:
    """R5 weight = log(1 + citations) (§8 R5); None where unmatched."""
    if cited_by_count is None:
        return None
    return math.log1p(cited_by_count)


def run(args) -> int:
    dois, items_of = load_input_dois(args.corpus, args.dois)
    if not dois:
        die("no DOIs found in the inputs", 2)
    print(f"[snapshot] {len(dois)} unique DOI(s); batches of {BATCH_SIZE}; "
          f"source=OpenAlex ({OPENALEX_WORKS})")
    found = {}
    for i in range(0, len(dois), BATCH_SIZE):
        chunk = dois[i:i + BATCH_SIZE]
        found.update(fetch_batch(chunk, args.mailto))
        print(f"  [batch] {i + len(chunk)}/{len(dois)} queried; "
              f"matched so far {len(found)}")
        time.sleep(POLITE_INTERVAL)
    rows = assemble_rows(dois, items_of, found)

    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    out_sha = sha256_file(args.out)
    manifest = {
        "spec": ("plan v1.1 §8 R5 / §11 item 22 — citation snapshot "
                 "(script frozen at P3; data pulled at P5; citation counts "
                 "are analysis-time covariates, not instrument)"),
        "source": "OpenAlex /works cited_by_count (batched DOI filter)",
        "retrieved_at": utcnow(),
        "n_dois": len(dois),
        "n_matched": sum(1 for r in rows if r["matched"]),
        "inputs_sha256": {p: sha256_file(p)
                          for p in sorted((args.corpus or [])
                                          + ([args.dois] if args.dois else []))},
        "snapshot_sha256": out_sha,
        "weight_rule": "R5 weight = log(1 + cited_by_count), single frozen snapshot",
    }
    mpath = args.out + "_manifest.json"
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"[snapshot] {manifest['n_matched']}/{len(dois)} matched -> {args.out}")
    print(f"[snapshot] sha256={out_sha}")
    print(f"[snapshot] manifest -> {mpath} (hash this file pair at P5)")
    return 0


# ------------------------------------------------------------------ selftest
def selftest() -> int:
    """Fully offline: normalization, URL, parsing, assembly, weights."""
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    check("DOI normalization strips prefixes and casefolds",
          normalize_doi("https://doi.org/10.1017/S003441251400016X")
          == "10.1017/s003441251400016x"
          and normalize_doi("DOI:10.5840/PC2004618") == "10.5840/pc2004618"
          and normalize_doi("  ") is None and normalize_doi(None) is None)

    url = batch_url(["10.1/a", "10.1/b"], "x@y.z")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    check("batch URL carries OR-joined doi filter + select + mailto + cursor",
          q["filter"] == ["doi:10.1/a|10.1/b"] and q["select"] == [SELECT]
          and q["mailto"] == ["x@y.z"] and q["cursor"] == ["*"])
    check("mailto omitted when not given",
          "mailto" not in urllib.parse.parse_qs(
              urllib.parse.urlparse(batch_url(["10.1/a"], None)).query))
    check("batch size constant respects the OpenAlex OR limit", BATCH_SIZE <= 50)

    page = {"meta": {"next_cursor": None},
            "results": [
                {"doi": "https://doi.org/10.1/A", "id": "https://openalex.org/W1",
                 "cited_by_count": 12},
                {"doi": None, "id": "https://openalex.org/W2", "cited_by_count": 3},
            ]}
    parsed = parse_works_page(page)
    check("page parsing keys by normalized DOI and drops null DOIs",
          parsed == {"10.1/a": {"openalex_id": "https://openalex.org/W1",
                                "cited_by_count": 12}})

    # injectable-get pagination
    pages = [
        {"meta": {"next_cursor": "c2"},
         "results": [{"doi": "https://doi.org/10.1/a", "id": "W1",
                      "cited_by_count": 5}]},
        {"meta": {"next_cursor": None},
         "results": [{"doi": "https://doi.org/10.1/b", "id": "W2",
                      "cited_by_count": 0}]},
    ]
    calls = []

    def fake_get(u):
        calls.append(u)
        return pages[len(calls) - 1]

    found = fetch_batch(["10.1/a", "10.1/b"], None, get=fake_get)
    check("cursor pagination followed until exhausted",
          len(calls) == 2 and "cursor=c2" in calls[1]
          and set(found) == {"10.1/a", "10.1/b"})

    with tempfile.TemporaryDirectory(prefix="cites_selftest_") as td:
        cpath = os.path.join(td, "corpus.jsonl")
        with open(cpath, "w") as f:
            for r in [{"item_id": "i1", "doi": "https://doi.org/10.1/A"},
                      {"item_id": "i2", "doi": "10.1/b"},
                      {"item_id": "i3", "doi": "10.1/b"},   # shared DOI
                      {"item_id": "i4"},                    # no DOI
                      {"item_id": "i5", "doi": "10.1/c"}]:
                f.write(json.dumps(r) + "\n")
        dpath = os.path.join(td, "extra.txt")
        with open(dpath, "w") as f:
            f.write("10.1/d\n\n10.1/B\n")   # dup of b, case-varied
        dois, items_of = load_input_dois([cpath], dpath)
        check("input DOIs unique, normalized, sorted; item map kept",
              dois == ["10.1/a", "10.1/b", "10.1/c", "10.1/d"]
              and items_of["10.1/b"] == ["i2", "i3"])

        rows = assemble_rows(dois, items_of,
                             {"10.1/a": {"openalex_id": "W1", "cited_by_count": 7},
                              "10.1/b": {"openalex_id": "W2", "cited_by_count": 0}})
        check("rows sorted by DOI; unmatched kept with null count",
              [r["doi"] for r in rows] == dois
              and rows[2]["matched"] is False
              and rows[2]["cited_by_count"] is None)
        check("shared DOI keeps all item_ids; single id stays scalar",
              rows[1]["item_id"] == ["i2", "i3"] and rows[0]["item_id"] == "i1")
        check("assembly deterministic",
              rows == assemble_rows(dois, items_of,
                                    {"10.1/a": {"openalex_id": "W1",
                                                "cited_by_count": 7},
                                     "10.1/b": {"openalex_id": "W2",
                                                "cited_by_count": 0}}))

    check("R5 weight rule log(1+c); None propagates",
          r5_weight(0) == 0.0 and abs(r5_weight(9) - math.log(10)) < 1e-12
          and r5_weight(None) is None)

    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="R5 OpenAlex citation snapshot (script frozen at P3; "
                    "data pulled at P5).")
    ap.add_argument("--corpus", nargs="+",
                    help="corpus JSONL(s) with item_id + doi rows")
    ap.add_argument("--dois", help="plain DOI list file (one per line)")
    ap.add_argument("--out", default="data/raw/citation_snapshot.jsonl")
    ap.add_argument("--mailto", help="contact email for the OpenAlex polite pool")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.corpus and not args.dois:
        die("required: --corpus ... and/or --dois (or --selftest)", 2)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
