#!/usr/bin/env python3
# STUB — untested in the seed-generation environment (network-restricted).
# Verify endpoints locally before first run.
# Prereqs: Python 3.10+, requests. Env: none (public APIs).
#
# Job: fetch (a) Religious Studies 2015 research articles, (b) the 20 gold anchors
# (docs/gold-anchors-v1.json), into data/raw/*.jsonl per the harvester agent schema:
#   {"item_id": sha256(doi)[:16], "doi","title","authors","journal","year",
#    "abstract","source","fetched_at"}
#
# Sources (priority order; VERIFY before use):
#   1. Crossref REST:  https://api.crossref.org/journals/{ISSN}/works
#        Religious Studies ISSN: 0034-4125 (print) / 1469-901X (online) — VERIFY
#        filter=from-pub-date:2015-01-01,until-pub-date:2015-12-31&rows=100&cursor=*
#        NOTE: Crossref abstracts are patchy for CUP — expect fallback traffic.
#   2. PhilPapers OAI-PMH: https://philpapers.org/oai.pl (ListRecords, oai_dc) — VERIFY set names
#   3. Publisher abstract pages (Cambridge Core) — polite scraping, 1 req/2s, UA string set.
#
# Exclusions: book reviews, editorials. Discussion notes kept with flag "note".
# Output: data/raw/pilot_rs2015.jsonl, data/raw/gold_anchors.jsonl, harvest_log.md
raise SystemExit("stub: implement per harvester agent spec (see .claude/agents/harvester.md)")
