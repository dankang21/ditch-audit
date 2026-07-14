#!/usr/bin/env python3
"""Shared helpers for the P1 validation-battery arms (pipeline/04_battery/).

Provider-call logic (pinned models, endpoints, retry/backoff, optional-param
400 fallback, .env handling, JSON extraction) is REUSED from
pipeline/03_code/run_coders.py by importing that file as a module.
run_coders.py itself is never modified.

The coding prompt (pipeline/03_code/coder_prompt.txt) is NOT used by any
battery probe in this package — recognition/discrimination probes send their
own minimal prompts because they are probes, not coding runs. (The stub arm
produced by make_stubs.py IS later coded, but via run_coders.py itself.)

stdlib only, Python 3.10+.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(PKG_DIR, "..", ".."))
RUN_CODERS_PATH = os.path.join(REPO_ROOT, "pipeline", "03_code", "run_coders.py")
BATTERY_DIR = os.path.join(REPO_ROOT, "data", "battery")

FAMILIES = ("a", "b", "c")  # a=Anthropic, b=Google, c=OpenAI (run_coders pins)

_rc_module = None


def rc():
    """Import pipeline/03_code/run_coders.py exactly once; return the module.

    Import has no side effects (main() is __main__-guarded) and does NOT
    verify the prompt manifest — battery probes never touch the coding prompt.
    """
    global _rc_module
    if _rc_module is None:
        spec = importlib.util.spec_from_file_location("run_coders", RUN_CODERS_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot import {RUN_CODERS_PATH}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _rc_module = mod
    return _rc_module


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_families(spec: str) -> list:
    fams = [x.strip() for x in (spec or "").split(",") if x.strip()]
    bad = [x for x in fams if x not in FAMILIES]
    if bad or not fams:
        die(f"--families must be a comma list among a,b,c (got {spec!r})", 2)
    return fams


def make_providers(families: list) -> dict:
    """family letter -> provider instance (keys checked up front; fail fast).
    API keys come from .env via run_coders.load_env and are never printed."""
    m = rc()
    env = m.load_env(m.ENV_PATH)
    return {f: m.make_provider(f, env) for f in families}


def call_provider(provider, prompt: str):
    """One fresh, independent API call (no conversation state), polite pause."""
    m = rc()
    text, meta = provider.call(prompt)
    time.sleep(m.POLITE_INTERVAL)
    return text, meta


def read_jsonl(path: str) -> list:
    items = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                die(f"{path}:{n}: invalid JSON ({e})", 4)
    return items


def batch_tag(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def ensure_battery_dir() -> str:
    os.makedirs(BATTERY_DIR, exist_ok=True)
    return BATTERY_DIR


def utcnow() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def pct(num: int, den: int) -> str:
    return f"{100.0 * num / den:.1f}%" if den else "n/a"


# ------------------------------------------------------------------ text utils

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list:
    """Casefolded alphanumeric tokens (deterministic)."""
    return _TOKEN_RE.findall((text or "").casefold())


# Fixed English stopword list (embedded — stdlib has none). Deterministic.
STOPWORDS = frozenset("""
a about above across after again against all almost also although always am
among amongst an and another any anyone anything are around as at
be because been before being below between beyond both but by
can cannot could did do does doing done down during
each either else enough even ever every few first for from further
had has have having he hence her here hers herself him himself his how however
i if in indeed into is it its itself just least less
made many may me might more moreover most much must my myself
neither never nevertheless no nor not nothing now
of off often on once one only onto or other others our ours ourselves out over
own per perhaps quite rather same she should since so some something such
than that the their theirs them themselves then there therefore these they
this those though through thus to too toward towards
under until up upon us very
was we well were what whatever when whence where whether which while who whom
whose why will with within without would yet you your yours yourself yourselves
""".split())

# Academic discourse boilerplate — high-TF in abstracts but non-topical.
# Used only for stub keyword selection (make_stubs.py), NOT for recognition
# title scoring. Deliberately excludes philosophy-topical terms
# (e.g. 'problem', 'reason', 'evil' are kept as candidate keywords).
BOILERPLATE = frozenset("""
abstract account addresses argue argued argues arguing argument arguments
article articles author authors chapter claim claimed claims contend contended
contends conclude
concludes conclusion conclusions consider considered considers defend defends
discuss discussed discusses discussion essay examine examined examines explore
explores gives given journal maintain maintains offer offers paper papers
present presented presents propose proposed proposes provide provides recent
recently reply respond response section seek seeks several show shown shows
suggest suggested suggests thesis view views
""".split())
