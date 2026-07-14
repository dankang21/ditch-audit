#!/usr/bin/env python3
# Tri-family blind coder runner (zero-human design, codebook v1.1).
# Prereqs: Python 3.10+, stdlib only (urllib.request, json, hashlib, time, argparse, os, re).
# Env (.env): ANTHROPIC_API_KEY (A), GOOGLE_API_KEY + CODER_B_PROVIDER=google (B),
#             OPENAI_API_KEY (C, adjudicator). Optional coder D = open-weights archival.
#
# HARD RULES (coder-runner agent, CLAUDE.md rules 1 & 5):
#   - Prompt = pipeline/03_code/coder_prompt.txt ONLY (docs/codebook-v1.md is BANNED;
#     the output schema is embedded in the prompt's [OUTPUT] block).
#   - Before any call: recompute sha256(coder_prompt.txt) and match the LAST line
#     of PROMPT_MANIFEST.txt; mismatch -> abort (non-zero exit).
#   - Substitute {{text}} / {{text_extra}}; call coders A, B, C independently
#     (temperature 0 attempted; pinned snapshots; per-call provider version headers
#     recorded in each output record's _meta — validation-battery B1). No coder's
#     output ever enters another coder's input (cross-contamination ban).
#   - Validate output against the prompt-embedded schema; 1 retry on parse failure,
#     then record {"item_id": ..., "parse_fail": true, "raw": <first 500 chars>}.
#   - Checkpoint: append + skip-existing item_ids on restart; flush+fsync every 50.
#   - Append batch summary (model id, effective params, calls, token sums, failures,
#     timestamp) to data/coded/cost_log.md. APPEND ONLY — existing content preserved.
#   - API keys are never printed or logged.
#
# Usage:
#   python3 pipeline/03_code/run_coders.py --batch data/sanitized/<file>.jsonl \
#       --coders a,b,c [--limit N]
#   python3 pipeline/03_code/run_coders.py --smoke        # built-in dummy item only;
#                                                         # writes nothing under data/coded
# Out: data/coded/{batch}_a.jsonl, {batch}_b.jsonl, {batch}_c.jsonl

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
PROMPT_PATH = os.path.join(SCRIPT_DIR, "coder_prompt.txt")
MANIFEST_PATH = os.path.join(SCRIPT_DIR, "PROMPT_MANIFEST.txt")
CODED_DIR = os.path.join(REPO_ROOT, "data", "coded")
COST_LOG_PATH = os.path.join(CODED_DIR, "cost_log.md")
ENV_PATH = os.path.join(REPO_ROOT, ".env")

# ---- pinned models & endpoints (dk-confirmed pins, see data/coded/cost_log.md) ----
MODEL_A = "claude-sonnet-5"
MODEL_B = "gemini-3.5-flash"
MODEL_C = "gpt-5.5-2026-04-23"
URL_A = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
URL_B = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_B}:generateContent"
URL_C = "https://api.openai.com/v1/chat/completions"

HTTP_TIMEOUT = 240          # seconds per request
RETRY_DELAYS = [1.0, 2.0, 4.0]  # exponential backoff, 3 retries on network/429/5xx
POLITE_INTERVAL = 0.5       # seconds between requests
FLUSH_EVERY = 50            # checkpoint cadence (flush + fsync)

D1_VALUES = {"S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "B", "P", "I", "M", "X"}
D2_VALUES = {"pro", "contra", "neutral", "NA"}
D3_VALUES = {"CS1", "CS2", "CS3", "CS4", "CS5", "NA"}
D4_VALUES = {"alpha", "beta", "gamma", "NA"}
SCHEMA_KEYS = [
    "item_id", "d1_step", "d2_direction", "d3_strength", "d4_type",
    "flags", "confidence", "uncertain_dimensions", "rationale",
]

# Built-in SYNTHETIC dummy for --smoke. Written for this script; NOT sourced from
# data/raw|sanitized|coded and not a real abstract.
SMOKE_ITEM = {
    "item_id": "SMOKE-001",
    "text": (
        "This is a synthetic pipeline-validation abstract. It argues that recent "
        "measurements narrowing the life-permitting range of the cosmological "
        "constant provide modest evidential support for the claim that physical "
        "reality as a whole has an external cause rather than being a brute fact. "
        "The observational premise is load-bearing: remove it and the inference "
        "collapses."
    ),
    "text_extra": None,
}


# --------------------------------------------------------------------------- utils

def utcnow() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def load_env(path: str) -> dict:
    """Minimal .env parser: KEY=VALUE lines, '#' comments and blanks ignored.
    Values are never printed anywhere."""
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k:
                    env[k] = v
    for k in ("ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY", "CODER_B_PROVIDER"):
        if not env.get(k) and os.environ.get(k):
            env[k] = os.environ[k]
    return env


def verify_prompt_manifest() -> str:
    """sha256(coder_prompt.txt) must equal the prompt= hash on the LAST line of
    PROMPT_MANIFEST.txt. Mismatch -> abort (hypothesis firewall / P3 freeze)."""
    if not os.path.exists(PROMPT_PATH):
        die(f"prompt not found: {PROMPT_PATH} (run scripts/build_coder_prompt.py)", 2)
    if not os.path.exists(MANIFEST_PATH):
        die(f"manifest not found: {MANIFEST_PATH}", 2)
    with open(PROMPT_PATH, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    last = ""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line.strip()
    m = re.search(r"\bprompt=([0-9a-f]{64})\b", last)
    if not m:
        die(f"manifest last line has no prompt= hash: {last!r}", 2)
    expected = m.group(1)
    if actual != expected:
        die(
            "PROMPT HASH MISMATCH — coder_prompt.txt does not match the last "
            f"PROMPT_MANIFEST.txt entry.\n  actual   sha256={actual}\n  manifest sha256={expected}\n"
            "Aborting before any API call (CLAUDE.md rule 1 / rule 2).",
            2,
        )
    print(f"[ok] prompt manifest verified (sha256={actual[:16]}…)")
    return actual


def build_prompt(template: str, item: dict) -> str:
    text = item.get("text") or ""
    extra = item.get("text_extra")
    return template.replace("{{text}}", text).replace("{{text_extra}}", extra or "")


def resolve_path(p: str) -> str:
    if os.path.isabs(p):
        return p
    if os.path.exists(p):
        return os.path.abspath(p)
    return os.path.join(REPO_ROOT, p)


def pick_version_headers(headers: dict) -> dict:
    """Keep versioning-ish response headers (request-id, *-version, model,
    processing-ms). Auth/request headers are never in this set."""
    out = {}
    for k, v in headers.items():
        lk = k.lower()
        if any(t in lk for t in ("version", "request-id", "processing-ms", "model")):
            out[k] = v
    return out


# ------------------------------------------------------------------------ HTTP core

class HTTPCallError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body or ""
        super().__init__(f"HTTP {status}: {self.body[:200]}")


def post_json(url: str, headers: dict, payload: dict):
    """POST JSON with retries on network errors / 429 / 5xx (exponential backoff,
    3 retries). Non-retryable HTTP errors raise HTTPCallError with the body so
    callers can inspect (e.g. temperature-unsupported 400 fallback)."""
    data = json.dumps(payload).encode("utf-8")
    hdrs = dict(headers)
    hdrs["content-type"] = "application/json"
    last_err = None
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                body = resp.read().decode("utf-8", "replace")
                return json.loads(body), dict(resp.headers), resp.status
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8", "replace") if e.fp else ""
            except Exception:
                body = ""
            if e.code == 429 or e.code >= 500:
                last_err = HTTPCallError(e.code, body)
                if attempt >= len(RETRY_DELAYS):
                    break
                delay = RETRY_DELAYS[attempt]
                ra = e.headers.get("retry-after") if e.headers else None
                if ra:
                    try:
                        delay = max(delay, float(ra))
                    except ValueError:
                        pass
                print(f"  [retry] HTTP {e.code}; backing off {delay:.1f}s", file=sys.stderr)
                time.sleep(delay)
                continue
            raise HTTPCallError(e.code, body)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last_err = HTTPCallError(None, f"network error: {e}")
            if attempt >= len(RETRY_DELAYS):
                break
            delay = RETRY_DELAYS[attempt]
            print(f"  [retry] network error; backing off {delay:.1f}s", file=sys.stderr)
            time.sleep(delay)
        except json.JSONDecodeError as e:
            raise HTTPCallError(None, f"non-JSON response body: {e}")
    raise last_err


# ------------------------------------------------------------------------ providers

class ProviderBase:
    """One provider = one independent coder. Optional-parameter fallback: if a 400
    names one of our optional params (e.g. temperature unsupported on this model),
    drop it once, record the drop, and retry — effective params end up in _meta and
    the cost log."""

    coder = "?"
    model = "?"

    def __init__(self):
        self.dropped_params = []
        self.model_reported = None

    # subclasses set self.opt_params (dict of droppable request params)

    def effective_params(self) -> dict:
        p = dict(self.fixed_params)
        p.update(self.opt_params)
        if self.dropped_params:
            p["dropped_after_400"] = list(self.dropped_params)
        return p

    def _maybe_drop_param(self, err_body: str) -> bool:
        low = (err_body or "").lower()
        for name in list(self.opt_params):
            if name.lower() in low:
                del self.opt_params[name]
                self.dropped_params.append(name)
                print(
                    f"  [fallback] coder {self.coder}: 400 names '{name}' — "
                    f"dropping it and retrying once (effective params will be logged)",
                    file=sys.stderr,
                )
                return True
        return False

    def call(self, prompt: str):
        while True:
            try:
                return self._call_once(prompt)
            except HTTPCallError as e:
                if e.status == 400 and self._maybe_drop_param(e.body):
                    continue
                raise

    def _call_once(self, prompt: str):
        raise NotImplementedError


class AnthropicCoder(ProviderBase):
    coder = "a"
    model = MODEL_A

    def __init__(self, api_key: str):
        super().__init__()
        self._key = api_key
        self.fixed_params = {"max_tokens": 1024}
        # temperature 0 attempted per spec; some sonnet-5-era models reject
        # non-default sampling params -> generic 400-drop fallback applies.
        # thinking disabled so the 1024-token budget goes to the JSON answer.
        self.opt_params = {"temperature": 0, "thinking": {"type": "disabled"}}

    def _call_once(self, prompt: str):
        payload = {
            "model": self.model,
            "max_tokens": self.fixed_params["max_tokens"],
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update(self.opt_params)
        headers = {"x-api-key": self._key, "anthropic-version": ANTHROPIC_VERSION}
        data, resp_headers, _ = post_json(URL_A, headers, payload)
        self.model_reported = data.get("model", self.model)
        text = "".join(
            b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"
        )
        usage = data.get("usage") or {}
        meta = {
            "coder": self.coder,
            "model": self.model_reported,
            "params": self.effective_params(),
            "usage": {
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
            },
            "version_headers": pick_version_headers(resp_headers),
            "ts": utcnow(),
        }
        return text, meta


class GoogleCoder(ProviderBase):
    coder = "b"
    model = MODEL_B

    def __init__(self, api_key: str):
        super().__init__()
        self._key = api_key
        self.fixed_params = {}
        self.opt_params = {"temperature": 0}

    def _call_once(self, prompt: str):
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        }
        if self.opt_params:
            payload["generationConfig"] = dict(self.opt_params)
        headers = {"x-goog-api-key": self._key}
        data, resp_headers, _ = post_json(URL_B, headers, payload)
        self.model_reported = data.get("modelVersion", self.model)
        text = ""
        candidates = data.get("candidates") or []
        if candidates:
            parts = (candidates[0].get("content") or {}).get("parts") or []
            text = "".join(p.get("text", "") for p in parts if isinstance(p, dict))
        um = data.get("usageMetadata") or {}
        out_tok = (um.get("candidatesTokenCount") or 0) + (um.get("thoughtsTokenCount") or 0)
        meta = {
            "coder": self.coder,
            "model": self.model_reported,
            "params": self.effective_params(),
            "usage": {
                "input_tokens": um.get("promptTokenCount"),
                "output_tokens": out_tok or None,
            },
            "version_headers": pick_version_headers(resp_headers),
            "ts": utcnow(),
        }
        return text, meta


class OpenAICoder(ProviderBase):
    coder = "c"
    model = MODEL_C

    def __init__(self, api_key: str):
        super().__init__()
        self._key = api_key
        self.fixed_params = {}
        # gpt-5-family models may reject non-default temperature -> spec-mandated
        # one-shot fallback: drop temperature, log effective params.
        self.opt_params = {"temperature": 0}

    def _call_once(self, prompt: str):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        payload.update(self.opt_params)
        headers = {"Authorization": f"Bearer {self._key}"}
        data, resp_headers, _ = post_json(URL_C, headers, payload)
        self.model_reported = data.get("model", self.model)
        choices = data.get("choices") or []
        text = ""
        if choices:
            text = (choices[0].get("message") or {}).get("content") or ""
        usage = data.get("usage") or {}
        meta = {
            "coder": self.coder,
            "model": self.model_reported,
            "params": self.effective_params(),
            "usage": {
                "input_tokens": usage.get("prompt_tokens"),
                "output_tokens": usage.get("completion_tokens"),
            },
            "version_headers": pick_version_headers(resp_headers),
            "ts": utcnow(),
        }
        return text, meta


def make_provider(coder: str, env: dict) -> ProviderBase:
    if coder == "a":
        key = env.get("ANTHROPIC_API_KEY")
        if not key:
            die("ANTHROPIC_API_KEY missing from .env — coder a unavailable", 3)
        return AnthropicCoder(key)
    if coder == "b":
        prov = env.get("CODER_B_PROVIDER", "google")
        if prov != "google":
            die(f"CODER_B_PROVIDER={prov!r} not supported (only 'google' implemented)", 3)
        key = env.get("GOOGLE_API_KEY")
        if not key:
            die("GOOGLE_API_KEY missing from .env — coder b unavailable", 3)
        return GoogleCoder(key)
    if coder == "c":
        key = env.get("OPENAI_API_KEY")
        if not key:
            die("OPENAI_API_KEY missing from .env — coder c unavailable", 3)
        return OpenAICoder(key)
    die(f"unknown coder {coder!r} (expected a, b, c)", 3)


# ------------------------------------------------------------ parsing & validation

def extract_json_block(text: str):
    """Extract a JSON object from model output. Code fences allowed."""
    if not text:
        return None
    candidates = []
    for m in re.finditer(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE):
        candidates.append(m.group(1))
    i, j = text.find("{"), text.rfind("}")
    if i != -1 and j > i:
        candidates.append(text[i : j + 1])
    for cand in candidates:
        cand = cand.strip()
        for attempt_text in (cand,):
            try:
                obj = json.loads(attempt_text)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                pass
        i, j = cand.find("{"), cand.rfind("}")
        if i != -1 and j > i:
            try:
                obj = json.loads(cand[i : j + 1])
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                pass
    return None


def validate_record(obj: dict):
    """Validate against the prompt-embedded output schema. Returns
    (clean_record, None) or (None, error_string). item_id is NOT trusted from the
    model — the caller force-overwrites it with the known input item id."""
    errs = []
    for k in SCHEMA_KEYS:
        if k == "item_id":
            continue  # overwritten regardless of what the model emitted
        if k not in obj:
            errs.append(f"missing key {k}")
    if errs:
        return None, "; ".join(errs)

    d1, d2 = obj["d1_step"], obj["d2_direction"]
    d3, d4 = obj["d3_strength"], obj["d4_type"]
    if d1 not in D1_VALUES:
        errs.append(f"d1_step={d1!r} not in allowed set")
    if d2 not in D2_VALUES:
        errs.append(f"d2_direction={d2!r} not in allowed set")
    if d3 not in D3_VALUES:
        errs.append(f"d3_strength={d3!r} not in allowed set")
    if d4 not in D4_VALUES:
        errs.append(f"d4_type={d4!r} not in allowed set")

    flags = obj["flags"]
    if flags is None:
        flags = []
    if isinstance(flags, str):
        flags = [flags]
    if not isinstance(flags, list) or not all(isinstance(x, str) for x in flags):
        errs.append("flags must be a list of strings")

    conf = obj["confidence"]
    if isinstance(conf, bool) or not isinstance(conf, (int, float)):
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            errs.append("confidence must be numeric")

    ud = obj["uncertain_dimensions"]
    if ud is None:
        ud = []
    if not isinstance(ud, list) or not all(isinstance(x, str) for x in ud):
        errs.append("uncertain_dimensions must be a list of strings")

    rationale = obj["rationale"]
    if not isinstance(rationale, str):
        errs.append("rationale must be a string")

    if errs:
        return None, "; ".join(errs)
    clean = {
        "item_id": None,  # force-overwritten by caller
        "d1_step": d1,
        "d2_direction": d2,
        "d3_strength": d3,
        "d4_type": d4,
        "flags": flags,
        "confidence": conf,
        "uncertain_dimensions": ud,
        "rationale": rationale,
    }
    return clean, None


# ------------------------------------------------------------------- coding driver

class Stats:
    def __init__(self):
        self.calls = 0
        self.tok_in = 0
        self.tok_out = 0
        self.coded = 0
        self.parse_fail = 0
        self.skipped = 0
        self.rationale_over_40w = 0
        self.sample_headers = None

    def add_call(self, meta: dict):
        self.calls += 1
        u = meta.get("usage") or {}
        self.tok_in += u.get("input_tokens") or 0
        self.tok_out += u.get("output_tokens") or 0
        if self.sample_headers is None:
            self.sample_headers = meta.get("version_headers") or {}


def code_one(provider: ProviderBase, prompt: str, item_id: str, stats: Stats) -> dict:
    """Call the provider; 1 re-request on parse/schema failure; then parse_fail record."""
    last_text, last_meta, last_err = "", None, "no response"
    for attempt in (1, 2):
        text, meta = provider.call(prompt)
        stats.add_call(meta)
        time.sleep(POLITE_INTERVAL)
        last_text, last_meta = text, meta
        obj = extract_json_block(text)
        if obj is None:
            last_err = "no JSON object found in output"
        else:
            clean, err = validate_record(obj)
            if clean is not None:
                clean["item_id"] = item_id  # force-overwrite, whatever the model emitted
                clean["_meta"] = meta
                if len((clean["rationale"] or "").split()) > 40:
                    stats.rationale_over_40w += 1
                stats.coded += 1
                return clean
            last_err = err
        if attempt == 1:
            print(f"  [parse] {item_id}: {last_err} — re-requesting once", file=sys.stderr)
    stats.parse_fail += 1
    print(f"  [parse_fail] {item_id}: {last_err}", file=sys.stderr)
    return {
        "item_id": item_id,
        "parse_fail": True,
        "raw": (last_text or "")[:500],
        "error": last_err,
        "_meta": last_meta,
    }


def load_done_ids(path: str) -> set:
    done = set()
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
                if rec.get("item_id"):
                    done.add(rec["item_id"])
    return done


def load_batch(path: str) -> list:
    items = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                die(f"{path}:{n}: invalid JSON ({e})", 4)
            if not rec.get("item_id"):
                die(f"{path}:{n}: item missing item_id", 4)
            items.append(rec)
    return items


def append_cost_log(batch_name: str, provider: ProviderBase, stats: Stats):
    os.makedirs(CODED_DIR, exist_ok=True)
    lines = [
        "",
        f"## {utcnow()} batch={batch_name} coder={provider.coder}",
        f"- model: {provider.model_reported or provider.model} (pinned request id: {provider.model})",
        f"- effective_params: {json.dumps(provider.effective_params(), ensure_ascii=False)}",
        f"- calls: {stats.calls}",
        f"- tokens: input={stats.tok_in} output={stats.tok_out}",
        f"- items: coded={stats.coded} parse_fail={stats.parse_fail} skipped_existing={stats.skipped}",
        f"- rationale_over_40_words: {stats.rationale_over_40w}",
        f"- version_headers_sample: {json.dumps(stats.sample_headers or {}, ensure_ascii=False)}",
    ]
    with open(COST_LOG_PATH, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_batch(batch_path: str, coders: list, limit, env: dict, template: str) -> int:
    items = load_batch(batch_path)
    if limit is not None:
        items = items[:limit]
    batch_name = os.path.splitext(os.path.basename(batch_path))[0]
    os.makedirs(CODED_DIR, exist_ok=True)
    print(f"[batch] {batch_name}: {len(items)} item(s), coders={','.join(coders)}")

    # fail fast: instantiate all providers (key checks) before any API call
    providers = [make_provider(c, env) for c in coders]

    exit_code = 0
    for provider in providers:
        out_path = os.path.join(CODED_DIR, f"{batch_name}_{provider.coder}.jsonl")
        done = load_done_ids(out_path)
        stats = Stats()
        print(f"[coder {provider.coder}] model={provider.model} -> {out_path}"
              f" (resume: {len(done)} already coded)")
        pending_flush = 0
        f = open(out_path, "a", encoding="utf-8")
        try:
            for idx, item in enumerate(items, 1):
                iid = item["item_id"]
                if iid in done:
                    stats.skipped += 1
                    continue
                prompt = build_prompt(template, item)
                rec = code_one(provider, prompt, iid, stats)
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                done.add(iid)
                pending_flush += 1
                if pending_flush >= FLUSH_EVERY:
                    f.flush()
                    os.fsync(f.fileno())
                    pending_flush = 0
                    print(f"  [checkpoint] coder {provider.coder}: {idx}/{len(items)}")
        except HTTPCallError as e:
            print(
                f"  [abort] coder {provider.coder}: unrecoverable HTTP error "
                f"(status={e.status}): {e.body[:300]}",
                file=sys.stderr,
            )
            exit_code = 1
        finally:
            f.flush()
            os.fsync(f.fileno())
            f.close()
        append_cost_log(batch_name, provider, stats)
        print(
            f"[coder {provider.coder}] done: coded={stats.coded} parse_fail={stats.parse_fail} "
            f"skipped={stats.skipped} calls={stats.calls} "
            f"tokens_in={stats.tok_in} tokens_out={stats.tok_out}"
        )
        if exit_code:
            break
    return exit_code


# ------------------------------------------------------------------------- smoke

def run_smoke(coders: list, env: dict, template: str) -> int:
    """One call per provider with the built-in dummy item. Exercises endpoint,
    param fallback, JSON extraction, and schema validation. Writes NOTHING under
    data/coded (no output files, no cost log)."""
    print("[smoke] built-in dummy item only — no files under data/coded will be written")
    prompt = build_prompt(template, SMOKE_ITEM)
    all_ok = True
    for c in coders:
        provider = make_provider(c, env)
        stats = Stats()
        print(f"\n[smoke:{c}] model={provider.model} …")
        try:
            rec = code_one(provider, prompt, SMOKE_ITEM["item_id"], stats)
        except HTTPCallError as e:
            print(f"[smoke:{c}] FAIL — HTTP error status={e.status}: {e.body[:300]}")
            all_ok = False
            continue
        meta = rec.get("_meta") or {}
        ok = not rec.get("parse_fail")
        all_ok &= ok
        print(f"[smoke:{c}] http=OK model_reported={meta.get('model')}")
        print(f"[smoke:{c}] effective_params={json.dumps(meta.get('params'), ensure_ascii=False)}")
        print(f"[smoke:{c}] usage={json.dumps(meta.get('usage'))}")
        print(f"[smoke:{c}] version_headers={json.dumps(meta.get('version_headers'))}")
        if ok:
            print(
                f"[smoke:{c}] parse=OK schema=OK -> "
                f"d1={rec['d1_step']} d2={rec['d2_direction']} d3={rec['d3_strength']} "
                f"d4={rec['d4_type']} flags={rec['flags']} conf={rec['confidence']}"
            )
        else:
            print(f"[smoke:{c}] parse/schema FAIL: {rec.get('error')}")
            print(f"[smoke:{c}] raw[:200]={rec.get('raw', '')[:200]!r}")
    print(f"\n[smoke] overall: {'OK (all providers passed)' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


# -------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Tri-family blind coder runner (A=Anthropic, B=Google, C=OpenAI)."
    )
    ap.add_argument("--batch", help="sanitized JSONL batch, e.g. data/sanitized/pilot_rs2015.jsonl")
    ap.add_argument("--coders", default="a,b,c", help="comma list among a,b,c (default a,b,c)")
    ap.add_argument("--limit", type=int, default=None, help="process only the first N items")
    ap.add_argument("--smoke", action="store_true",
                    help="1 call per provider with a built-in dummy text; no data/coded writes")
    args = ap.parse_args(argv)

    coders = [c.strip() for c in args.coders.split(",") if c.strip()]
    bad = [c for c in coders if c not in ("a", "b", "c")]
    if bad or not coders:
        die(f"--coders must be a comma list among a,b,c (got {args.coders!r})", 2)

    verify_prompt_manifest()  # abort before anything else on mismatch

    with open(PROMPT_PATH, encoding="utf-8") as f:
        template = f.read()
    if "{{text}}" not in template:
        die("coder_prompt.txt has no {{text}} placeholder — refusing to run", 2)

    env = load_env(ENV_PATH)

    if args.smoke:
        return run_smoke(coders, env, template)

    if not args.batch:
        die("--batch is required unless --smoke is given", 2)
    batch_path = resolve_path(args.batch)
    if not os.path.exists(batch_path):
        die(f"batch file not found: {batch_path}", 2)
    return run_batch(batch_path, coders, args.limit, env, template)


if __name__ == "__main__":
    sys.exit(main())
