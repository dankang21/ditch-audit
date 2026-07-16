#!/usr/bin/env python3
# T1 relevance pass (P3 prep) — include/exclude screening ONLY (no coding).
# One call per item to coder C's endpoint (pinned gpt-5.5-2026-04-23), reusing
# the provider / retry / backoff code from pipeline/03_code/run_coders.py.
#
# Inputs : data/raw/t1_candidates.jsonl (296) + data/raw/t1_apq_hits.jsonl (10)
# Outputs: data/raw/t1_relevance_screen.jsonl  (checkpoint: judgment per item)
#          data/raw/t1_final.jsonl             (include=true items + `screen` field)
#          data/raw/t1_relevance_log.md        (counts, reasons, review handling)
#
# Rules:
#   - Items with no abstract are screened on title alone (`title_only_screen`).
#   - Mind "Review:" book reviews (15) are EXCLUDED regardless of the relevance
#     verdict (counted separately in the log); they are still screened so that
#     every one of the 306 items has a recorded judgment.
#   - Retry/backoff = run_coders style: HTTP retries with exponential backoff
#     inside post_json; 1 re-request on JSON parse/schema failure. Checkpoint
#     append + skip-existing on restart (parse failures are NOT treated as done,
#     so a re-run retries them).
#   - This is a screening pass, NOT coding: the hypothesis-firewall coder prompt
#     machinery (coder_prompt.txt / manifest) is deliberately not used.
#
# Usage: python3 pipeline/01_fetch/t1_relevance.py [--limit N] [--rebuild-only]

import argparse
import json
import os
import sys
import time
from collections import Counter, OrderedDict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "pipeline", "03_code"))

import run_coders  # provider call code reuse (OpenAICoder, backoff, JSON extraction)
from run_coders import (
    HTTPCallError,
    OpenAICoder,
    POLITE_INTERVAL,
    extract_json_block,
    load_env,
    utcnow,
)

CAND_PATH = os.path.join(REPO_ROOT, "data", "raw", "t1_candidates.jsonl")
APQ_PATH = os.path.join(REPO_ROOT, "data", "raw", "t1_apq_hits.jsonl")
SCREEN_PATH = os.path.join(REPO_ROOT, "data", "raw", "t1_relevance_screen.jsonl")
FINAL_PATH = os.path.join(REPO_ROOT, "data", "raw", "t1_final.jsonl")
LOG_PATH = os.path.join(REPO_ROOT, "data", "raw", "t1_relevance_log.md")

FLUSH_EVERY = 25

# Screening prompt — fixed wording (task spec), used verbatim.
SCREEN_PROMPT = (
    "You are screening journal articles for a corpus about arguments over the "
    "following theses: (S1) physical reality as a whole has an external cause "
    "or ground; (S2) that ground is a personal agent; (S3) it is unique, a se, "
    "uncreated; (S4) the ultimate is perfectly good; (S5) it acts specially in "
    "the world (miracles, prayer, self-disclosure); (S6) the Hebrew prophetic "
    "tradition is the authentic bearer of special revelation; (S7) Jesus of "
    "Nazareth was bodily raised; (S8) the resurrection shows Jesus is God "
    "incarnate / God is triune; plus: bundled arguments for/against God's "
    "existence (ontological, religious experience), pragmatic arguments for "
    "belief, intra-theistic attribute puzzles, and the methodology of such "
    "case-making. INCLUDE if the article's primary topic bears on ANY of "
    "these; EXCLUDE only if clearly unrelated (e.g., pure ethics, epistemology "
    "without religious target, philosophy of science with no bearing). When in "
    "doubt, INCLUDE. Given TITLE and ABSTRACT (abstract may be missing), reply "
    'JSON: {"include": true|false, "reason": "<15 words"}.'
)


def load_jsonl(path):
    items = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERROR: {path}:{n}: invalid JSON ({e})", file=sys.stderr)
                sys.exit(4)
    return items


def is_mind_review(item):
    return item.get("journal") == "Mind" and (item.get("title") or "").startswith("Review:")


def build_item_prompt(item):
    title = (item.get("title") or "").strip()
    abstract = (item.get("abstract") or "").strip()
    parts = [SCREEN_PROMPT, "", f"TITLE: {title}"]
    parts.append(f"ABSTRACT: {abstract}" if abstract else "ABSTRACT: (missing)")
    return "\n".join(parts)


def validate_screen(obj):
    """Return (include: bool, reason: str) or (None, err)."""
    if "include" not in obj:
        return None, "missing key 'include'"
    inc = obj["include"]
    if isinstance(inc, str) and inc.strip().lower() in ("true", "false"):
        inc = inc.strip().lower() == "true"
    if not isinstance(inc, bool):
        return None, f"include={obj['include']!r} not a boolean"
    reason = obj.get("reason", "")
    if not isinstance(reason, str):
        reason = json.dumps(reason, ensure_ascii=False)
    return (inc, reason.strip()), None


def screen_one(provider, item, stats):
    """1 call + 1 re-request on parse failure (run_coders style)."""
    prompt = build_item_prompt(item)
    iid = item["item_id"]
    last_text, last_meta, last_err = "", None, "no response"
    for attempt in (1, 2):
        text, meta = provider.call(prompt)
        stats["calls"] += 1
        u = meta.get("usage") or {}
        stats["tok_in"] += u.get("input_tokens") or 0
        stats["tok_out"] += u.get("output_tokens") or 0
        time.sleep(POLITE_INTERVAL)
        last_text, last_meta = text, meta
        obj = extract_json_block(text)
        if obj is None:
            last_err = "no JSON object found in output"
        else:
            res, err = validate_screen(obj)
            if res is not None:
                inc, reason = res
                stats["ok"] += 1
                return {
                    "item_id": iid,
                    "include": inc,
                    "reason": reason,
                    "title_only_screen": not (item.get("abstract") or "").strip(),
                    "mind_review": is_mind_review(item),
                    "model": meta.get("model"),
                    "params": meta.get("params"),
                    "ts": utcnow(),
                }
            last_err = err
        if attempt == 1:
            print(f"  [parse] {iid}: {last_err} — re-requesting once", file=sys.stderr)
    stats["parse_fail"] += 1
    print(f"  [parse_fail] {iid}: {last_err}", file=sys.stderr)
    return {
        "item_id": iid,
        "parse_fail": True,
        "raw": (last_text or "")[:500],
        "error": last_err,
        "ts": utcnow(),
    }


def load_done_judgments(path):
    """item_id -> last VALID judgment (parse_fail records are not 'done')."""
    done = OrderedDict()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("item_id") and not rec.get("parse_fail"):
                    done[rec["item_id"]] = rec
    return done


def norm_journal(j):
    return "Noûs" if j in ("Nous", "Noûs") else (j or "?")


def build_outputs(items, judgments):
    """Write t1_final.jsonl + t1_relevance_log.md from complete judgments."""
    missing = [i["item_id"] for i in items if i["item_id"] not in judgments]
    if missing:
        print(f"ERROR: {len(missing)} item(s) still lack a valid judgment "
              f"(e.g. {missing[:5]}) — re-run to retry.", file=sys.stderr)
        return 1

    n_final = 0
    with open(FINAL_PATH, "w", encoding="utf-8") as f:
        for item in items:
            j = judgments[item["item_id"]]
            if j["include"] and not j["mind_review"]:
                rec = dict(item)
                rec["screen"] = {
                    "include": True,
                    "reason": j["reason"],
                    "title_only_screen": j["title_only_screen"],
                    "model": j.get("model"),
                    "screened_at": j.get("ts"),
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_final += 1

    # ---- aggregate for the log ----
    per_journal = {}
    excl_reasons = Counter()
    title_only = {"n": 0, "included": 0}
    reviews = []
    for item in items:
        j = judgments[item["item_id"]]
        jn = norm_journal(item.get("journal"))
        row = per_journal.setdefault(jn, {"screened": 0, "include": 0,
                                          "exclude": 0, "review_excluded": 0})
        row["screened"] += 1
        if j["title_only_screen"]:
            title_only["n"] += 1
        if j["mind_review"]:
            row["review_excluded"] += 1
            reviews.append((item.get("title", ""), j["include"], j["reason"]))
            continue
        if j["include"]:
            row["include"] += 1
            if j["title_only_screen"]:
                title_only["included"] += 1
        else:
            row["exclude"] += 1
            excl_reasons[j["reason"].rstrip(".").lower()] += 1

    tot = {k: sum(r[k] for r in per_journal.values())
           for k in ("screened", "include", "exclude", "review_excluded")}

    lines = [
        "# T1 relevance pass — screening log",
        "",
        f"- Date: {utcnow()}",
        f"- Screener: coder C endpoint, pinned model `{run_coders.MODEL_C}` "
        f"(provider code reused from `pipeline/03_code/run_coders.py`)",
        "- Task: include/exclude relevance screening only (NOT coding). "
        "Fixed screening prompt (S1–S8 + bundled/pragmatic/attribute/methodology "
        "scope; when in doubt, INCLUDE); one call per item; 1 re-request on JSON "
        "parse failure; HTTP retries with exponential backoff.",
        f"- Inputs: `t1_candidates.jsonl` + `t1_apq_hits.jsonl` = {len(items)} items "
        f"(all screened; judgments checkpointed in `t1_relevance_screen.jsonl`).",
        "",
        "## Counts by journal",
        "",
        "| Journal | Screened | Included | Excluded (relevance) | Excluded (Mind book review) |",
        "|---|---|---|---|---|",
    ]
    for jn in sorted(per_journal):
        r = per_journal[jn]
        lines.append(f"| {jn} | {r['screened']} | {r['include']} | "
                     f"{r['exclude']} | {r['review_excluded']} |")
    lines += [
        f"| **Total** | **{tot['screened']}** | **{tot['include']}** | "
        f"**{tot['exclude']}** | **{tot['review_excluded']}** |",
        "",
        "Note: 'Noûs' merges the raw journal strings 'Nous' and 'Noûs' (same venue).",
        "",
        "## Mind \"Review:\" book reviews",
        "",
        f"{tot['review_excluded']} Mind items with titles beginning \"Review:\" are "
        "**excluded as book reviews regardless of the relevance verdict** (counted "
        "separately above, not in the relevance-exclusion column). They were still "
        "screened so that every item has a recorded judgment; model verdicts below "
        "are informational only.",
        "",
    ]
    for title, inc, reason in reviews:
        lines.append(f"- [{'model: include' if inc else 'model: exclude'}] {title}")
    lines += [
        "",
        "## Title-only screening (no abstract held)",
        "",
        f"- Items screened on title alone (`title_only_screen`): {title_only['n']}",
        f"- Of these, included (excl. book reviews): {title_only['included']}",
        "",
        "## Relevance-exclusion reasons (top)",
        "",
    ]
    for reason, n in excl_reasons.most_common(10):
        lines.append(f"- {n} × {reason}")
    lines += [
        "",
        "## Result",
        "",
        f"- **T1 final corpus: {n_final} items** -> `data/raw/t1_final.jsonl` "
        "(each with a `screen` field).",
        "- Validation: judgments exist for all "
        f"{len(items)}/{len(items)} items; JSON parse failures after retry: 0; "
        "book-review exclusion applied.",
        "",
    ]
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[done] t1_final.jsonl: {n_final} items | log -> {LOG_PATH}")
    print(f"[totals] screened={tot['screened']} include={tot['include']} "
          f"exclude={tot['exclude']} review_excluded={tot['review_excluded']}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="T1 relevance screening (coder C endpoint).")
    ap.add_argument("--limit", type=int, default=None,
                    help="screen only the first N not-yet-judged items (testing)")
    ap.add_argument("--rebuild-only", action="store_true",
                    help="skip API calls; rebuild t1_final.jsonl + log from checkpoint")
    args = ap.parse_args(argv)

    items = load_jsonl(CAND_PATH) + load_jsonl(APQ_PATH)
    ids = [i["item_id"] for i in items]
    if len(ids) != len(set(ids)):
        print("ERROR: duplicate item_ids across inputs", file=sys.stderr)
        return 4
    print(f"[input] {len(items)} items "
          f"({os.path.basename(CAND_PATH)} + {os.path.basename(APQ_PATH)})")

    judgments = load_done_judgments(SCREEN_PATH)
    todo = [i for i in items if i["item_id"] not in judgments]
    print(f"[resume] {len(judgments)} already judged; {len(todo)} to screen")

    if not args.rebuild_only and todo:
        if args.limit is not None:
            todo = todo[: args.limit]
        env = load_env(os.path.join(REPO_ROOT, ".env"))
        key = env.get("OPENAI_API_KEY")
        if not key:
            print("ERROR: OPENAI_API_KEY missing from .env", file=sys.stderr)
            return 3
        provider = OpenAICoder(key)
        stats = {"calls": 0, "tok_in": 0, "tok_out": 0, "ok": 0, "parse_fail": 0}
        pending = 0
        f = open(SCREEN_PATH, "a", encoding="utf-8")
        try:
            for idx, item in enumerate(todo, 1):
                rec = screen_one(provider, item, stats)
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                if not rec.get("parse_fail"):
                    judgments[item["item_id"]] = rec
                pending += 1
                if pending >= FLUSH_EVERY:
                    f.flush()
                    os.fsync(f.fileno())
                    pending = 0
                    print(f"  [checkpoint] {idx}/{len(todo)} "
                          f"(ok={stats['ok']} parse_fail={stats['parse_fail']})")
        except HTTPCallError as e:
            print(f"  [abort] unrecoverable HTTP error (status={e.status}): "
                  f"{e.body[:300]}", file=sys.stderr)
        finally:
            f.flush()
            os.fsync(f.fileno())
            f.close()
        print(f"[screen] calls={stats['calls']} ok={stats['ok']} "
              f"parse_fail={stats['parse_fail']} "
              f"tokens_in={stats['tok_in']} tokens_out={stats['tok_out']}")

    if args.limit is not None and not args.rebuild_only:
        print("[limit] partial run — outputs not rebuilt (run again without --limit)")
        return 0
    return build_outputs(items, judgments)


if __name__ == "__main__":
    sys.exit(main())
