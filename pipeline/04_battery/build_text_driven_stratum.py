#!/usr/bin/env python3
"""build_text_driven_stratum.py — B2 text-driven-stratum builder + stub-conformance
verifier (validation-battery v1.3 §B2; analysis-plan v1.1 §9 row B2; freeze-manifest
item 20: "B2 stub-degradation script + text-driven-stratum builder script").

Two modes, both LOCAL ONLY (zero API calls), stdlib-only, deterministic:

(1) stratum building (default) — the mechanized predicate, 1:1 with battery §B2 v1.3:

      stratum = items whose ADJUDICATED stub-arm code differs from the
      ADJUDICATED full-text code on >= 1 denominator-relevant dimension for
      the hypothesis at hand (H1: D1/D2/D3/D4; H2: D1/D2/D3).

    * Adjudication of each arm = the majority-of-three rule of record (plan
      §3.3): unanimous -> adopted; 2-1 -> majority; 3-way -> `unresolved`.
    * The per-hypothesis denominator-relevant dimension set is an ARGUMENT
      (--hypothesis h1|h2, or an explicit --dims list), per the plan's §9 row
      B2 gated-effects split (H1 -> OR_H1 gate; H2 -> OR_pro gate — the gate
      itself is computed downstream on this script's item list output).
    * Unresolved handling (interpretation point, recorded in output): the
      predicate compares adjudicated CODES; an `unresolved` adjudication is not
      a code, so a dimension with an unresolved side contributes no difference
      under the default --unresolved=strict policy. --unresolved=stub-differs
      counts a stub-side `unresolved` (topic alone fails to determine a code)
      as a difference — published as a sensitivity, never the primary.
    * Also reports battery §B2 deliverable (i): stub-vs-full agreement per
      dimension over both-resolved items.

(2) --verify-stubs STUBS.jsonl --batch SOURCE.jsonl — machine-verification that
    an existing stub file conforms to the §B2 degradation predicate ("topic
    keywords / first clause only; scripted degradation, no argumentative
    content") as implemented by pipeline/04_battery/make_stubs.py:
      (a) line 1 = first clause of the source text's first sentence, capped at
          --max-words words, then " ..." — nothing beyond the first clause;
      (b) optional line 2 = "Topic keywords: ..." with <= --topk tokens, each a
          token of the source `text` (never `text_extra`), none a stopword/
          boilerplate token, none shorter than 3 chars, none a digit string;
      (c) no further lines.
    Verification recomputes the expected stub with make_stubs.build_stub and
    byte-compares, AND re-checks the predicate independently of make_stubs
    (so a make_stubs regression cannot self-certify). Prints the SHA256 of
    make_stubs.py and of this file for the freeze manifest (item 20).

Firewall note: this script reads coded outputs and stub files only; it never
touches hypothesis documents and emits no coder-facing content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(PKG_DIR, "..", ".."))
sys.path.insert(0, PKG_DIR)  # battery_common / make_stubs live in this package dir

DIMS = ["d1_step", "d2_direction", "d3_strength", "d4_type"]
CODERS = ["a", "b", "c"]
# plan §9 row B2 / battery §B2 v1.3: denominator-relevant dimension sets
HYP_DIMS = {
    "h1": ["d1_step", "d2_direction", "d3_strength", "d4_type"],
    "h2": ["d1_step", "d2_direction", "d3_strength"],
}
UNRESOLVED = "__unresolved__"   # sentinel; never a legal code value


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: str) -> dict:
    out = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                die(f"{path}:{n}: invalid JSON ({e})", 4)
            out[r["item_id"]] = r
    return out


def adjudicate(vals: list) -> str:
    """Majority-of-three rule of record (plan §3.3): unanimous/2-1 -> value;
    3-way -> UNRESOLVED sentinel."""
    ct = Counter(vals)
    top, top_n = ct.most_common(1)[0]
    return top if top_n >= 2 else UNRESOLVED


def adjudicate_arm(files: dict) -> dict:
    """files: coder letter -> {item_id: record}. Returns {item_id: {dim: value}}
    over the items present for ALL three coders (missing-coder items dropped,
    counted by the caller)."""
    common = set(files["a"]) & set(files["b"]) & set(files["c"])
    out = {}
    for iid in sorted(common):
        out[iid] = {d: adjudicate([files[c][iid][d] for c in CODERS]) for d in DIMS}
    return out


def build_stratum(full_adj: dict, stub_adj: dict, dims: list, unresolved_policy: str):
    items = sorted(set(full_adj) & set(stub_adj))
    per_item = []
    agree = {d: {"agree": 0, "differ": 0, "undefined": 0} for d in dims}
    for iid in items:
        diff_dims, unres_dims = [], []
        for d in dims:
            fv, sv = full_adj[iid][d], stub_adj[iid][d]
            if fv == UNRESOLVED or sv == UNRESOLVED:
                agree[d]["undefined"] += 1
                unres_dims.append({"dim": d,
                                   "full_unresolved": fv == UNRESOLVED,
                                   "stub_unresolved": sv == UNRESOLVED})
                if (unresolved_policy == "stub-differs" and sv == UNRESOLVED
                        and fv != UNRESOLVED):
                    diff_dims.append(d)
                continue
            if fv != sv:
                agree[d]["differ"] += 1
                diff_dims.append(d)
            else:
                agree[d]["agree"] += 1
        per_item.append({
            "item_id": iid,
            "in_stratum": bool(diff_dims),
            "diff_dims": diff_dims,
            "unresolved_dims": unres_dims,
            "full_adjudicated": {d: full_adj[iid][d] for d in dims},
            "stub_adjudicated": {d: stub_adj[iid][d] for d in dims},
        })
    n_in = sum(1 for r in per_item if r["in_stratum"])
    summary = {
        "n_items_compared": len(items),
        "n_in_stratum": n_in,
        "stratum_fraction": (n_in / len(items)) if items else None,
        "dims": dims,
        "unresolved_policy": unresolved_policy,
        "stub_vs_full_agreement_per_dim": {
            d: {**agree[d],
                "agreement_rate": (agree[d]["agree"] /
                                   (agree[d]["agree"] + agree[d]["differ"])
                                   if (agree[d]["agree"] + agree[d]["differ"]) else None)}
            for d in dims},
    }
    return summary, per_item


# --------------------------------------------------------- stub verification
def _import_make_stubs():
    import importlib.util
    path = os.path.join(PKG_DIR, "make_stubs.py")
    spec = importlib.util.spec_from_file_location("make_stubs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, path


def verify_stub_predicate(stub: dict, src: dict, max_words: int, topk: int,
                          stopwords, boilerplate, token_re) -> list:
    """Independent §B2 predicate re-check (no make_stubs call). Returns a list
    of violation strings (empty = conformant)."""
    errs = []
    text = stub.get("text") or ""
    lines = text.split("\n")
    if len(lines) > 2:
        errs.append("more than 2 lines")
    head = lines[0]
    if not head.endswith(" ...") and head != "...":
        errs.append("head line does not end with ' ...'")
    head_words = head[:-4].split() if head.endswith(" ...") else []
    if len(head_words) > max_words:
        errs.append(f"head exceeds {max_words} words")
    # head must be a prefix of the whitespace-normalized source text
    norm_src = " ".join((src.get("text") or "").split())
    if head_words and not norm_src.startswith(" ".join(head_words)):
        errs.append("head is not a prefix of the source text (content altered)")
    # nothing beyond the first clause: the head must not cross the first
    # sentence/clause boundary of the source (checked via make_stubs's own
    # regexes would be circular; approximate: head must contain no
    # sentence-final punctuation followed by more words)
    if any(w[-1] in ".!?" for w in head_words[:-1]):
        errs.append("head crosses a sentence boundary")
    if len(lines) == 2:
        kw_line = lines[1]
        if not kw_line.startswith("Topic keywords: "):
            errs.append("line 2 is not a 'Topic keywords: ' line")
        else:
            kws = [k.strip() for k in kw_line[len("Topic keywords: "):].split(",")]
            if len(kws) > topk:
                errs.append(f"more than {topk} keywords")
            src_tokens = set(token_re.findall(norm_src.casefold()))
            for kw in kws:
                if kw not in src_tokens:
                    errs.append(f"keyword {kw!r} not a source-text token")
                if kw in stopwords or kw in boilerplate:
                    errs.append(f"keyword {kw!r} is a stopword/boilerplate token")
                if len(kw) < 3 or kw.isdigit():
                    errs.append(f"keyword {kw!r} violates length/digit rule")
    if stub.get("text_extra") is not None:
        errs.append("text_extra must be null in a stub")
    return errs


def verify_stubs(stubs_path: str, batch_path: str, max_words: int, topk: int) -> int:
    ms, ms_path = _import_make_stubs()
    import battery_common as bc  # noqa: same package dir
    stubs = read_jsonl(stubs_path)
    src = read_jsonl(batch_path)
    missing = sorted(set(stubs) - set(src))
    if missing:
        die(f"{len(missing)} stub item(s) missing from source batch: {missing[:3]}...")
    n_exact = 0
    bad = []
    for iid in sorted(stubs):
        expected = ms.build_stub(src[iid], max_words, topk)
        if expected == {k: stubs[iid].get(k) for k in ("item_id", "text", "text_extra")}:
            n_exact += 1
        else:
            bad.append((iid, "recompute-mismatch"))
        errs = verify_stub_predicate(stubs[iid], src[iid], max_words, topk,
                                     bc.STOPWORDS, bc.BOILERPLATE, bc._TOKEN_RE)
        for e in errs:
            bad.append((iid, e))
    print(f"[verify-stubs] {len(stubs)} stub(s): {n_exact} byte-identical to "
          f"make_stubs.build_stub recomputation; {len(bad)} violation(s)")
    for iid, e in bad[:20]:
        print(f"  [violation] {iid}: {e}")
    print(f"[verify-stubs] sha256 make_stubs.py = {sha256_file(ms_path)}")
    print(f"[verify-stubs] sha256 {os.path.basename(__file__)} = "
          f"{sha256_file(os.path.abspath(__file__))}")
    return 0 if not bad else 1


# ------------------------------------------------------------------- selftest
def selftest() -> int:
    import tempfile
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    def rec(iid, d1, d2, d3, d4):
        return {"item_id": iid, "d1_step": d1, "d2_direction": d2,
                "d3_strength": d3, "d4_type": d4}

    # --- adjudication rule
    check("majority 2-1", adjudicate(["S4", "S4", "X"]) == "S4")
    check("unanimous", adjudicate(["pro", "pro", "pro"]) == "pro")
    check("3-way -> unresolved", adjudicate(["S1", "S2", "S3"]) == UNRESOLVED)

    # --- stratum predicate on a synthetic mini-set
    # i1: full=(S4,pro,POS,alpha) stub=(S4,pro,POS,alpha)   -> not in stratum
    # i2: full=(S4,pro,POS,alpha) stub=(S4,contra,POS,alpha)-> in stratum (d2)
    # i3: full=(S4,pro,POS,alpha) stub=(S4,pro,POS,beta)    -> H1 in / H2 OUT (d4 not H2-relevant)
    # i4: full 3-way on d1 -> full unresolved; stub uniform -> strict: not in stratum
    # i5: stub 3-way on d2 -> strict: not in; stub-differs: in
    full = {c: {} for c in CODERS}
    stub = {c: {} for c in CODERS}
    for c in CODERS:
        full[c]["i1"] = rec("i1", "S4", "pro", "POS", "alpha")
        stub[c]["i1"] = rec("i1", "S4", "pro", "POS", "alpha")
        full[c]["i2"] = rec("i2", "S4", "pro", "POS", "alpha")
        stub[c]["i2"] = rec("i2", "S4", "contra", "POS", "alpha")
        full[c]["i3"] = rec("i3", "S4", "pro", "POS", "alpha")
        stub[c]["i3"] = rec("i3", "S4", "pro", "POS", "beta")
        stub[c]["i4"] = rec("i4", "S4", "pro", "POS", "alpha")
        full[c]["i5"] = rec("i5", "S4", "pro", "POS", "alpha")
    full["a"]["i4"] = rec("i4", "S1", "pro", "POS", "alpha")
    full["b"]["i4"] = rec("i4", "S2", "pro", "POS", "alpha")
    full["c"]["i4"] = rec("i4", "S3", "pro", "POS", "alpha")
    stub["a"]["i5"] = rec("i5", "S4", "pro", "POS", "alpha")
    stub["b"]["i5"] = rec("i5", "S4", "contra", "POS", "alpha")
    stub["c"]["i5"] = rec("i5", "S4", "neutral", "POS", "alpha")

    fa, sa = adjudicate_arm(full), adjudicate_arm(stub)
    s_h1, items_h1 = build_stratum(fa, sa, HYP_DIMS["h1"], "strict")
    by = {r["item_id"]: r for r in items_h1}
    check("i1 not in stratum", not by["i1"]["in_stratum"])
    check("i2 in stratum via d2", by["i2"]["in_stratum"] and by["i2"]["diff_dims"] == ["d2_direction"])
    check("i3 in H1 stratum via d4", by["i3"]["in_stratum"] and by["i3"]["diff_dims"] == ["d4_type"])
    check("i4 (full-unresolved d1) strict -> not in stratum", not by["i4"]["in_stratum"])
    check("i5 (stub-unresolved d2) strict -> not in stratum", not by["i5"]["in_stratum"])
    s_h2, items_h2 = build_stratum(fa, sa, HYP_DIMS["h2"], "strict")
    by2 = {r["item_id"]: r for r in items_h2}
    check("i3 NOT in H2 stratum (d4 not H2-relevant)", not by2["i3"]["in_stratum"])
    _, items_h1s = build_stratum(fa, sa, HYP_DIMS["h1"], "stub-differs")
    bys = {r["item_id"]: r for r in items_h1s}
    check("i5 stub-differs policy -> in stratum", bys["i5"]["in_stratum"])
    check("agreement report counts undefined", s_h1["stub_vs_full_agreement_per_dim"]
          ["d1_step"]["undefined"] == 1)

    # --- stub-conformance verifier against make_stubs on synthetic text
    ms, _ = _import_make_stubs()
    import battery_common as bc
    with tempfile.TemporaryDirectory(prefix="stratum_selftest_") as td:
        src_items = [
            {"item_id": "v1", "text": "This synthetic dummy sentence, written for the "
             "selftest only, argues nothing about lighthouse tides. Second sentence adds "
             "keywords: lighthouse lighthouse tides tides tides selftest.", "text_extra": None},
            {"item_id": "v2", "text": "Short first clause here. And a second sentence "
             "with words words words.", "text_extra": "must be ignored"},
        ]
        sp, bp = os.path.join(td, "stubs.jsonl"), os.path.join(td, "batch.jsonl")
        with open(bp, "w", encoding="utf-8") as f:
            for r in src_items:
                f.write(json.dumps(r) + "\n")
        with open(sp, "w", encoding="utf-8") as f:
            for r in src_items:
                f.write(json.dumps(ms.build_stub(r, 12, 5)) + "\n")
        rcode = verify_stubs(sp, bp, 12, 5)
        check("verify-stubs passes on genuine make_stubs output", rcode == 0)
        # tampered stub (argumentative content leaked) must FAIL
        tampered = ms.build_stub(src_items[0], 12, 5)
        tampered["text"] = tampered["text"].replace(" ...", " and therefore God exists ...")
        tp = os.path.join(td, "stubs_bad.jsonl")
        with open(tp, "w", encoding="utf-8") as f:
            f.write(json.dumps(tampered) + "\n")
        rcode2 = verify_stubs(tp, bp, 12, 5)
        check("verify-stubs flags tampered stub", rcode2 == 1)
        errs = verify_stub_predicate(tampered, src_items[0], 12, 5,
                                     bc.STOPWORDS, bc.BOILERPLATE, bc._TOKEN_RE)
        check("independent predicate catches content alteration", bool(errs))
    print(f"[selftest] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="B2 text-driven-stratum builder / stub verifier.")
    ap.add_argument("--full", nargs=3, metavar=("A", "B", "C"),
                    help="full-text-arm consolidated coder files (a b c)")
    ap.add_argument("--stub", nargs=3, metavar=("A", "B", "C"),
                    help="stub-arm consolidated coder files (a b c)")
    ap.add_argument("--hypothesis", choices=sorted(HYP_DIMS),
                    help="denominator-relevant dimension set: h1 = D1-D4, h2 = D1-D3")
    ap.add_argument("--dims", nargs="+", choices=DIMS,
                    help="explicit dimension set (overrides --hypothesis)")
    ap.add_argument("--unresolved", choices=["strict", "stub-differs"], default="strict",
                    help="unresolved-side policy (default strict = primary; "
                         "stub-differs = registered sensitivity)")
    ap.add_argument("--out", help="output JSON path (default: stdout)")
    ap.add_argument("--verify-stubs", metavar="STUBS_JSONL",
                    help="verify a make_stubs output file against the §B2 predicate")
    ap.add_argument("--batch", help="source batch for --verify-stubs")
    ap.add_argument("--max-words", type=int, default=12)
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.verify_stubs:
        if not args.batch:
            die("--verify-stubs requires --batch", 2)
        return verify_stubs(args.verify_stubs, args.batch, args.max_words, args.topk)
    if not (args.full and args.stub):
        die("stratum mode requires --full A B C and --stub A B C", 2)
    dims = args.dims or (HYP_DIMS[args.hypothesis] if args.hypothesis else None)
    if not dims:
        die("provide --hypothesis h1|h2 or an explicit --dims list", 2)
    full = {c: read_jsonl(p) for c, p in zip(CODERS, args.full)}
    stub = {c: read_jsonl(p) for c, p in zip(CODERS, args.stub)}
    summary, per_item = build_stratum(adjudicate_arm(full), adjudicate_arm(stub),
                                      dims, args.unresolved)
    out = {"spec": "battery v1.3 §B2 / plan v1.1 §9 row B2 (manifest item 20)",
           "summary": summary,
           "stratum_item_ids": [r["item_id"] for r in per_item if r["in_stratum"]],
           "items": per_item,
           "script_sha256": sha256_file(os.path.abspath(__file__))}
    blob = json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(blob)
        print(f"[stratum] {summary['n_in_stratum']}/{summary['n_items_compared']} "
              f"items in the text-driven stratum -> {args.out}")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
