#!/usr/bin/env python3
"""Generate 60 synthetic criterion items via Perplexity Agent API.

Author model (family E): perplexity/glm-5.2  (Z.AI GLM family, hosted by Perplexity)
Checker model (Kimi family): perplexity/kimi-k2.7-code (Moonshot AI, hosted by Perplexity)

Rules enforced here:
- The harness NEVER writes or edits item text; only the E model authors text.
- Every E/Kimi call is made with "tools": [] (web search structurally off);
  each response is inspected for search traces (search_results output items,
  usage.tool_calls_details, citation annotations). Any trace => output discarded.
- Per spec: at most MAX_CONTENT_ATTEMPTS E generations on content failures
  (mechanical checks or Kimi non-conform). Failure cap reached => generation_failed.
- Kimi sees ONLY: spec target codes + content_brief + constraints + candidate text.

stdlib only.
"""
import argparse
import concurrent.futures
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS_PATH = ROOT / "docs" / "synthetic-specs-v1.json"
PILOT_PATH = ROOT / "data" / "sanitized" / "pilot_rs2015.jsonl"
OUT_DIR = ROOT / "data" / "criterion"
RESULTS_PATH = OUT_DIR / "synthetic_results.jsonl"      # per-spec final records (work file)
ATTEMPTS_PATH = OUT_DIR / "generation_attempts.jsonl"   # every attempt, verbose
DEV_PATH = OUT_DIR / "synthetic_dev.jsonl"
VAULT_PATH = OUT_DIR / "synthetic_vault.jsonl"

API_URL = "https://api.perplexity.ai/v1/agent"
GEN_MODEL = "perplexity/glm-5.2"
CHECK_MODEL = "perplexity/kimi-k2.7-code"
MAX_CONTENT_ATTEMPTS = 3   # content failures (mech / kimi) per spec
MAX_TOTAL_CALLS = 6        # hard cap incl. discarded search-trace outputs
HTTP_TIMEOUT = 300
HTTP_RETRIES = 4

# ---------------------------------------------------------------- hedge lexicon
HEDGE_LEXICON_HUMAN = ("may, might, perhaps, arguably, suggest/suggests/suggested/"
                       "suggesting, seem/seems/seemed/seemingly, appear/appears/"
                       "appeared/apparently, tentative/tentatively, could, plausibly, possibly")
HEDGE_RE = re.compile(
    r"\b(?:may|might|perhaps|arguably|suggest(?:s|ed|ing)?|seem(?:s|ed|ingly)?|"
    r"appear(?:s|ed)?|apparently|tentative(?:ly)?|could|plausibly|possibly)\b",
    re.IGNORECASE)

# ------------------------------------------------------------- author blacklist
# Task-supplied list plus adjacent figures E might reach for. Matched
# case-sensitively as whole words (these are surnames; lowercase 'law' etc. is fine).
BLACKLIST = [
    "Swinburne", "Plantinga", "Rowe", "Draper", "Oppy", "Craig", "Mackie",
    "Schellenberg", "Wykstra", "Hick", "Alston", "Morriston", "van Inwagen",
    "Inwagen", "Leslie", "Bostrom", "Law", "Tuggy", "Rea", "Brower", "Allison",
    "Gonzalez", "Collins", "Hawking", "Hume", "Kant", "Leibniz", "Aquinas",
    "Anselm", "Descartes", "Spinoza", "Paley", "Penrose", "Vilenkin", "Guth",
    "Carroll", "Dawkins", "Dennett", "Pruss", "Koons", "Feser", "Grünbaum",
    "Grunbaum", "Ehrman", "Habermas", "Licona", "Wright", "McGrew", "Sober",
    "Monton", "Barnes", "Stump", "Zagzebski", "Bergmann", "Howard-Snyder",
    "Dougherty", "Almeida", "Maitzen", "Kraay", "Climenhaga", "Adams", "Lewis",
    "Russell", "Flew", "Kenny", "Polkinghorne", "Tegmark", "Susskind", "Linde",
    "Borde", "Gould", "Sagan",
]
# NOTE: "Bayes"/"Bayesian" are deliberately NOT blacklisted (technical terms).
BLACKLIST_RES = [re.compile(r"\b" + re.escape(n) + r"\b") for n in BLACKLIST]

# ------------------------------------------------------- numeric-claim patterns
CS5_NUM_RES = [
    re.compile(r"\d+(?:\.\d+)?\s*(?:to|:)\s*\d+", re.I),                       # 20 to 1 / 20:1
    re.compile(r"(?:probabilit\w*|posterior|prior|credence|odds|bayes\s*factor|"
               r"factor\s+of|likelihood\s+ratio)\W{0,6}(?:\w+\W+){0,8}?\d+(?:\.\d+)?", re.I),
    re.compile(r"\d+(?:\.\d+)?\W{0,6}(?:\w+\W+){0,8}?(?:probabilit\w*|posterior|"
               r"prior|credence|odds|bayes\s*factor)", re.I),
    re.compile(r"\d+(?:\.\d+)?\s*(?:%|percent)", re.I),
]
ANY_DIGIT_RE = re.compile(r"\d")

_env_lock = threading.Lock()
_print_lock = threading.Lock()
_file_lock = threading.Lock()


def log(msg):
    with _print_lock:
        print(msg, flush=True)


def load_env_key(name):
    envfile = ROOT / ".env"
    for line in envfile.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == name:
            return v.strip().strip('"').strip("'")
    raise SystemExit(f"missing {name} in .env")


API_KEY = None


def api_call(model, instructions, user_input, max_output_tokens):
    """POST to Agent API with tools structurally disabled. Returns parsed JSON."""
    body = {
        "model": model,
        "instructions": instructions,
        "input": user_input,
        "max_output_tokens": max_output_tokens,
        "tools": [],  # structural search-off: no web_search (or any) tool offered
    }
    data = json.dumps(body).encode()
    last_err = None
    for i in range(HTTP_RETRIES + 1):
        req = urllib.request.Request(
            API_URL, data=data, method="POST",
            headers={"Authorization": f"Bearer {API_KEY}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            payload = e.read().decode(errors="replace")[:500]
            last_err = f"HTTP {e.code}: {payload}"
            if e.code in (429, 500, 502, 503, 504) and i < HTTP_RETRIES:
                time.sleep(2 ** (i + 1))
                continue
            raise RuntimeError(last_err)
        except Exception as e:  # timeout, connection reset
            last_err = f"{type(e).__name__}: {e}"
            if i < HTTP_RETRIES:
                time.sleep(2 ** (i + 1))
                continue
            raise RuntimeError(last_err)
    raise RuntimeError(last_err)


def extract_text(resp):
    parts = []
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    parts.append(c.get("text", ""))
    return "\n".join(parts).strip()


def no_search_proof(resp, model):
    """Inspect a response for search traces; return (clean: bool, proof: dict)."""
    out_types = [o.get("type") for o in resp.get("output", [])]
    search_items = [t for t in out_types
                    if t and ("search" in t or "tool" in t or "fetch" in t)]
    tcd = resp.get("usage", {}).get("tool_calls_details")
    annotations = []
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                annotations.extend(c.get("annotations") or [])
    clean = (not search_items) and (not tcd) and (not annotations) \
        and ("search_results" not in resp)
    proof = {
        "model": model,
        "response_id": resp.get("id"),
        "request_tools_param": [],
        "output_item_types": out_types,
        "search_output_items": search_items,
        "tool_calls_details": tcd,
        "citation_annotations_count": len(annotations),
        "top_level_search_results": "search_results" in resp,
        "clean": clean,
    }
    return clean, proof


# ------------------------------------------------------------ surface statistics
def surface_stats():
    rows = [json.loads(l) for l in PILOT_PATH.read_text().splitlines() if l.strip()]
    wcs = sorted(len(r["text"].split()) for r in rows)
    hcs = [len(HEDGE_RE.findall(r["text"])) for r in rows]
    sents = []
    for r in rows:
        sents += [s for s in re.split(r"(?<=[.!?])\s+", r["text"]) if s.strip()]
    slens = [len(s.split()) for s in sents]

    def q(v, p):
        v = sorted(v)
        k = (len(v) - 1) * p
        f = int(k)
        c = min(f + 1, len(v) - 1)
        return v[f] + (v[c] - v[f]) * (k - f)

    return {
        "n_items": len(rows),
        "wordcount": {"min": wcs[0], "q1": q(wcs, .25), "median": q(wcs, .5),
                      "q3": q(wcs, .75), "max": wcs[-1],
                      "mean": round(sum(wcs) / len(wcs), 1)},
        "hedges_per_item": {"mean": round(sum(hcs) / len(hcs), 2),
                            "median": q(hcs, .5), "max": max(hcs)},
        "hedges_per_100w": round(100 * sum(hcs) / sum(wcs), 2),
        "mean_sentence_len": round(sum(slens) / len(slens), 1),
        "sentences_per_abstract": round(len(sents) / len(rows), 1),
    }


# ------------------------------------------------------------ mechanical checks
def mech_check(spec, text):
    checks = {}
    failures = []

    wc = len(text.split())
    lo, hi = spec["length_band"]
    checks["word_count"] = wc
    checks["length_band"] = [lo, hi]
    if not (lo <= wc <= hi):
        failures.append(f"word count is {wc}, must be between {lo} and {hi} words "
                        f"(whitespace-separated tokens)")

    hc = len(HEDGE_RE.findall(text))
    quota = spec["hedging_quota"]
    checks["hedge_count"] = hc
    checks["hedging_quota"] = quota
    if abs(hc - quota) > 1:
        found = sorted(set(m.group(0).lower() for m in HEDGE_RE.finditer(text)))
        failures.append(
            f"hedge-lexicon count is {hc} (found: {', '.join(found) or 'none'}), "
            f"but the quota is exactly {quota}; adjust to exactly {quota} occurrences "
            f"of lexicon words ({HEDGE_LEXICON_HUMAN})")

    is_cs5 = spec["target"].get("d3_strength") == "CS5"
    if is_cs5:
        ok = any(rx.search(text) for rx in CS5_NUM_RES)
        checks["cs5_number_present"] = ok
        if not ok:
            failures.append("no explicit hypothesis-level numeric figure found: the "
                            "abstract must state the required figure using digits in a "
                            "probability/odds/Bayes-factor context (e.g. '20 to 1', "
                            "'0.6', 'a Bayes factor of 500')")
    else:
        has_digit = bool(ANY_DIGIT_RE.search(text))
        checks["digits_present"] = has_digit
        if has_digit:
            failures.append("text contains digits; this item must contain NO digits "
                            "at all — spell out any numbers in words and state no "
                            "numeric probabilities, odds, percentages, or Bayes factors")

    hits = sorted(set(n for rx, n in zip(BLACKLIST_RES, BLACKLIST) if rx.search(text)))
    checks["blacklist_hits"] = hits
    if hits:
        failures.append(f"text mentions real scholars/scientists: {', '.join(hits)}; "
                        f"remove every real name — all principles, critics and studies "
                        f"must be invented and unnamed")

    # wrapper / formatting sanity (single abstract, no labels)
    if re.match(r"^\s*(abstract\b|title\b|#)", text, re.I) or "**" in text:
        failures.append("output must be ONLY the plain abstract text: no 'Abstract:' "
                        "label, no title, no markdown")

    checks["pass"] = not failures
    return checks, failures


# --------------------------------------------------------------- prompt builders
GEN_INSTRUCTIONS = (
    "You are an expert academic writer producing synthetic journal abstracts for a "
    "methodological validation study in analytic philosophy of religion. You follow "
    "specifications exactly. You never name real scholars, real papers, real journals, "
    "real studies, or real institutions; every principle, dataset, study, critic, and "
    "movement you mention must be invented and generic. You output only the abstract "
    "text itself: one paragraph, no title, no labels, no markdown, no commentary.")

CODE_GLOSS = (
    "d1_step = the step of an argument chain the abstract bears on (S1..S8, B = the "
    "bundled full hypothesis, M = methodological); d2_direction = the abstract's net "
    "direction toward that step's thesis (pro / contra / neutral); d3_strength = the "
    "strength of the claim (CS4 = explicit qualitative on-balance evidential claim, "
    "CS5 = explicit numeric hypothesis-level claim, NA = no directional claim is made); "
    "d4_type = the type of the load-bearing premises (alpha = a priori/conceptual, "
    "beta = contemporary empirical, gamma = historical-documentary, NA = no "
    "load-bearing premise). The content brief below spells out exactly what this "
    "means for the present item; where they seem to differ, follow the brief.")


def build_gen_input(spec, stats, feedback_history):
    t = spec["target"]
    lo, hi = spec["length_band"]
    quota = spec["hedging_quota"]
    is_cs5 = t.get("d3_strength") == "CS5"

    lines = []
    lines.append("Write ONE synthetic academic journal abstract (a single paragraph of "
                 "continuous prose) that implements the following specification "
                 "exactly. The abstract is a synthetic test item: it must be written "
                 "so that a competent content-coder reading only the abstract would "
                 "assign exactly the target codes.")
    lines.append("")
    lines.append(f"TARGET CODES: d1_step={t['d1_step']}, d2_direction={t['d2_direction']}, "
                 f"d3_strength={t['d3_strength']}, d4_type={t['d4_type']}")
    lines.append(f"(Code glossary: {CODE_GLOSS})")
    lines.append("")
    lines.append("CONTENT BRIEF (the argument the abstract must implement):")
    lines.append(spec["content_brief"])
    lines.append("")
    lines.append("HARD CONSTRAINTS:")
    for c in spec["constraints"]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append(f"LENGTH: between {lo} and {hi} words inclusive, counting words as "
                 f"whitespace-separated tokens. Aim near {int((lo + hi) / 2)} words. "
                 f"Count before finalizing.")
    lines.append("")
    lines.append(f"HEDGING QUOTA: the abstract must contain EXACTLY {quota} "
                 f"occurrence(s), in total, of words from this hedge lexicon "
                 f"(case-insensitive; these surface forms only): {HEDGE_LEXICON_HUMAN}. "
                 + ("Since the quota is 0, NO lexicon word may appear at all. "
                    if quota == 0 else
                    f"Not {quota - 1}, not {quota + 1}: exactly {quota}. ")
                 + "Every inflection listed counts toward the total, wherever it "
                   "occurs. Count occurrences one by one before finalizing.")
    lines.append("")
    if is_cs5:
        lines.append("NUMBERS: the abstract MUST state the required explicit figure "
                     "using digits (e.g. '20 to 1', 'odds of 4 to 1', 'a prior of 0.6', "
                     "'a Bayes factor of roughly 500'), at the hypothesis level required "
                     "by the constraints. Use digits for that figure; use no other "
                     "digits.")
    else:
        lines.append("NUMBERS: use NO digits anywhere in the abstract. Spell out any "
                     "quantity in words ('three datasets', 'twenty'), and make no "
                     "numeric probability, odds, percentage, or Bayes-factor claims.")
    lines.append("")
    lines.append("STYLE TARGET (match the register of real philosophy-of-religion "
                 "journal abstracts): impersonal academic or first-person authorial "
                 "voice ('I argue', 'This paper argues'); dense, formal, self-contained "
                 "prose. Reference-corpus surface profile: median abstract length "
                 f"{stats['wordcount']['median']:.0f} words (IQR "
                 f"{stats['wordcount']['q1']:.0f}-{stats['wordcount']['q3']:.0f}), mean "
                 f"sentence length ~{stats['mean_sentence_len']:.0f} words, roughly "
                 f"{stats['sentences_per_abstract']:.0f} sentences per abstract, hedge "
                 "words used sparingly (the length band and hedging quota above "
                 "override these corpus figures where they differ).")
    lines.append("")
    lines.append("OUTPUT: the abstract text only — no title, no 'Abstract:' label, no "
                 "quotation marks around the whole text, no word count, no notes.")

    if feedback_history:
        lines.append("")
        lines.append("=" * 40)
        prev_text, prev_failures = feedback_history[-1]
        lines.append("YOUR PREVIOUS ATTEMPT FAILED VALIDATION.")
        lines.append("Previous attempt:")
        lines.append(prev_text)
        lines.append("")
        lines.append("Validation failures to fix:")
        for f in prev_failures:
            lines.append(f"- {f}")
        lines.append("")
        lines.append("Write a corrected abstract that fixes ALL listed failures while "
                     "still meeting every requirement above. Do not simply resubmit "
                     "the previous text.")
    return "\n".join(lines)


CHECK_INSTRUCTIONS = (
    "You audit synthetic validation items for a content-coding instrument. You answer "
    "with a single JSON object and nothing else.")


def build_check_input(spec, text):
    t = spec["target"]
    lines = []
    lines.append("Below are the SPECIFICATION of a synthetic test item and the "
                 "CANDIDATE ABSTRACT generated for it. Judge (1) whether the abstract "
                 "faithfully implements the specification, and (2) whether a competent "
                 "content-coder reading only the abstract would assign exactly the "
                 "target codes.")
    lines.append("")
    lines.append(f"TARGET CODES: d1_step={t['d1_step']}, d2_direction={t['d2_direction']}, "
                 f"d3_strength={t['d3_strength']}, d4_type={t['d4_type']}")
    lines.append(f"(Code glossary: {CODE_GLOSS})")
    lines.append("")
    lines.append("CONTENT BRIEF:")
    lines.append(spec["content_brief"])
    lines.append("")
    lines.append("CONSTRAINTS:")
    for c in spec["constraints"]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("CANDIDATE ABSTRACT:")
    lines.append(text)
    lines.append("")
    lines.append('Answer with ONLY a JSON object, no markdown fences, no other text: '
                 '{"conforms": true|false, "rival_code": null or "d?=..." naming the '
                 'code a coder would likely assign instead of the target, "reason": '
                 '"one or two sentences"}. Set conforms=false only for substantive '
                 'failures: the argument does not implement the brief, a constraint is '
                 'violated, or a coder would likely assign a different code than the '
                 'target. Surface counts (exact word counts, exact hedge counts) are '
                 'checked elsewhere and are NOT your concern.')
    return "\n".join(lines)


def parse_kimi_json(raw):
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise ValueError("no JSON object in checker output")
    obj = json.loads(m.group(0))
    if not isinstance(obj.get("conforms"), bool):
        raise ValueError("checker JSON missing boolean 'conforms'")
    return {"conforms": obj["conforms"],
            "rival_code": obj.get("rival_code"),
            "reason": str(obj.get("reason", ""))[:600]}


def append_jsonl(path, obj):
    with _file_lock:
        with open(path, "a") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ per-spec run
def run_spec(spec, stats):
    sid = spec["spec_id"]
    feedback_history = []
    content_attempts = 0
    total_calls = 0
    t_start = time.time()

    while content_attempts < MAX_CONTENT_ATTEMPTS and total_calls < MAX_TOTAL_CALLS:
        total_calls += 1
        attempt_no = total_calls
        gen_input = build_gen_input(spec, stats, feedback_history)
        try:
            resp = api_call(GEN_MODEL, GEN_INSTRUCTIONS, gen_input, 8192)
        except RuntimeError as e:
            append_jsonl(ATTEMPTS_PATH, {"spec_id": sid, "call": attempt_no,
                                         "phase": "gen", "error": str(e)})
            log(f"[{sid}] gen call {attempt_no}: API error: {e}")
            content_attempts += 1
            feedback_history.append(("(no text produced)", [f"API error: {e}"]))
            continue

        clean, proof = no_search_proof(resp, GEN_MODEL)
        text = extract_text(resp)
        usage = resp.get("usage", {})
        base_rec = {"spec_id": sid, "call": attempt_no, "phase": "gen",
                    "model": GEN_MODEL, "text": text, "no_search_proof": proof,
                    "usage": {k: usage.get(k) for k in
                              ("input_tokens", "output_tokens", "total_tokens")}}

        if not clean:
            base_rec["outcome"] = "discarded_search_traces"
            append_jsonl(ATTEMPTS_PATH, base_rec)
            log(f"[{sid}] call {attempt_no}: SEARCH TRACES -> discard & re-call")
            continue  # does not count as content attempt

        if not text:
            content_attempts += 1
            base_rec["outcome"] = "empty_output"
            append_jsonl(ATTEMPTS_PATH, base_rec)
            feedback_history.append(("(empty output)",
                                     ["the response contained no abstract text; output "
                                      "the abstract text only"]))
            continue

        content_attempts += 1
        checks, failures = mech_check(spec, text)
        base_rec["mech_checks"] = checks
        if failures:
            base_rec["outcome"] = "mech_fail"
            base_rec["mech_failures"] = failures
            append_jsonl(ATTEMPTS_PATH, base_rec)
            log(f"[{sid}] attempt {content_attempts}: mech fail: {failures[0][:90]}")
            feedback_history.append((text, failures))
            continue

        # Kimi conformity check (spec + text only)
        verdict = None
        kimi_proof = None
        kimi_err = None
        for k in range(3):
            try:
                kresp = api_call(CHECK_MODEL, CHECK_INSTRUCTIONS,
                                 build_check_input(spec, text), 2048)
                kclean, kimi_proof = no_search_proof(kresp, CHECK_MODEL)
                if not kclean:
                    kimi_err = "checker response had search traces"
                    continue
                verdict = parse_kimi_json(extract_text(kresp))
                break
            except (RuntimeError, ValueError) as e:
                kimi_err = str(e)
                continue
        if verdict is None:
            base_rec["outcome"] = "kimi_error"
            base_rec["kimi_error"] = kimi_err
            append_jsonl(ATTEMPTS_PATH, base_rec)
            log(f"[{sid}] attempt {content_attempts}: checker error: {kimi_err}")
            feedback_history.append((text, [f"conformity checker unavailable: {kimi_err}"]))
            continue

        base_rec["kimi_verdict"] = verdict
        if not verdict["conforms"]:
            base_rec["outcome"] = "kimi_nonconform"
            append_jsonl(ATTEMPTS_PATH, base_rec)
            log(f"[{sid}] attempt {content_attempts}: kimi non-conform: "
                f"{verdict['reason'][:90]}")
            fb = (f"an independent expert reviewer judged the abstract does not "
                  f"faithfully implement the specification. Reviewer reason: "
                  f"{verdict['reason']}")
            if verdict.get("rival_code"):
                fb += (f" (a coder would likely assign {verdict['rival_code']} instead "
                       f"of the target)")
            feedback_history.append((text, [fb]))
            continue

        # success
        base_rec["outcome"] = "accepted"
        append_jsonl(ATTEMPTS_PATH, base_rec)
        record = {
            "item_id": sid,
            "half": spec["half"],
            "text": text,
            "gen_model": GEN_MODEL,
            "gen_attempts": content_attempts,
            "no_search_proof": {"generator": proof, "checker": kimi_proof},
            "mech_checks": checks,
            "kimi_verdict": verdict,
        }
        append_jsonl(RESULTS_PATH, record)
        log(f"[{sid}] OK in {content_attempts} attempt(s), "
            f"{time.time() - t_start:.0f}s, wc={checks['word_count']}, "
            f"hedges={checks['hedge_count']}/{checks['hedging_quota']}")
        return record

    # failed
    record = {
        "item_id": sid,
        "half": spec["half"],
        "text": None,
        "gen_model": GEN_MODEL,
        "gen_attempts": content_attempts,
        "generation_failed": True,
        "fail_reasons": [f for _, fs in feedback_history for f in fs][-3:],
    }
    append_jsonl(RESULTS_PATH, record)
    log(f"[{sid}] FAILED after {content_attempts} content attempts")
    return record


def main():
    global API_KEY
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", help="comma-separated spec_ids (default: all 60)")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--resume", action="store_true",
                    help="skip specs already accepted in synthetic_results.jsonl")
    args = ap.parse_args()

    API_KEY = load_env_key("PERPLEXITY_API_KEY")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    specs = json.loads(SPECS_PATH.read_text())["specs"]
    if args.specs:
        wanted = set(args.specs.split(","))
        specs = [s for s in specs if s["spec_id"] in wanted]

    done = {}
    if args.resume and RESULTS_PATH.exists():
        for line in RESULTS_PATH.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("text"):
                done[r["item_id"]] = r
        specs = [s for s in specs if s["spec_id"] not in done]
        log(f"resume: {len(done)} already accepted, {len(specs)} to run")

    stats = surface_stats()
    log(f"surface stats: {json.dumps(stats)}")

    results = list(done.values())
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_spec, s, stats): s["spec_id"] for s in specs}
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())

    # assemble dev/vault files (only when running full set or resuming toward it)
    ok = [r for r in results if r.get("text")]
    failed = [r for r in results if not r.get("text")]
    order = {s["spec_id"]: i for i, s in
             enumerate(json.loads(SPECS_PATH.read_text())["specs"])}
    ok.sort(key=lambda r: order.get(r["item_id"], 999))
    with open(DEV_PATH, "w") as fd, open(VAULT_PATH, "w") as fv:
        for r in ok:
            line = json.dumps(r, ensure_ascii=False) + "\n"
            (fd if r["half"] == "dev" else fv).write(line)
    log(f"done: {len(ok)} accepted, {len(failed)} failed "
        f"({[r['item_id'] for r in failed]})")
    log(f"dev={sum(1 for r in ok if r['half'] == 'dev')} "
        f"vault={sum(1 for r in ok if r['half'] == 'vault')}")


if __name__ == "__main__":
    main()
