#!/usr/bin/env python3
"""Final step: merge every script's claims into tables/claims.csv and regenerate evidence-ledger.md.

  python3 ledger.py            regenerate the ledger (a generated file: never hand-edit)
  python3 ledger.py --check F… fail if any claim id cited in the given markdown files is missing from the registry

Claim ids look like C-<SECTION>-<NN>, e.g. C-HEAD-01. An optional suffix must start with a letter (C-HEAD-01-macro);
C-HEAD-01-03 is read as a range, not an ID. The pattern lives in common.ID_RE; registration and loading both enforce it.
"""
import glob
import json
import os
import re
import sys
from collections import OrderedDict

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ID_RE = C.ID_RE  # re-exported: paper-authorship's idpattern.py imports it from here
# IDs must fully match ID_RE; the section order below is only for display.
SECTION_ORDER = ["Provenance", "Scorer", "Headline", "Paired", "Sensitivity", "Coverage", "Confounds"]  # extend per project

HEADER = """# Evidence ledger

> Generated file, do not hand-edit. Regenerate with `python3 scripts/run_all.py`. Every number in the memo and theses cites a claim id below. `python3 scripts/ledger.py --check <files>` fails when a cited id is missing.

## Reading conventions
- k/n is always shown next to a rate. State whether a rate is micro (pooled over items) or macro (mean of per-unit rates).
- Intervals: Wilson treats items as independent (optimistic); cluster-bootstrap resamples the natural unit.
- p-values are exact McNemar with mid-p beside it: descriptive, unadjusted, not clustered. No claim of significance is made.
- Unmatched findings are "outside the reference set", never errors by default.

## Claims
"""


def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        v = "yes" if v else "no"
    if isinstance(v, float):
        v = f"{v:.4f}".rstrip("0").rstrip(".")
    return str(v).replace("\n", " ").replace("|", "\\|")


def load_claims():
    """Load claim files. When run_all sets BENCH_STEPS, claim files from steps no longer in the pipeline are ignored (stale)."""
    items = []
    allowed = os.environ.get("BENCH_STEPS")
    allowed = set(allowed.split(",")) if allowed else None
    for p in sorted(glob.glob(os.path.join(C.CLAIMS_DIR, "*.json"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        if allowed is not None and stem not in allowed:
            print(f"WARNING: ignoring stale claim file {os.path.basename(p)} (no such step)", file=sys.stderr)
            continue
        items.extend(json.load(open(p)))
    if not items:
        sys.exit("claims registry is empty: run the pipeline first")
    ids = [c["id"] for c in items]
    malformed = sorted(i for i in ids if not ID_RE.fullmatch(i))
    if malformed:
        sys.exit(f"claim ids that do not match the claim-ID pattern (checkers could not see them): {malformed}")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        sys.exit(f"duplicate claim ids: {dup}")
    return items


def check(files):
    known = {c["id"] for c in load_claims()}
    bad = []
    for f in files:
        for m in ID_RE.finditer(open(f, encoding="utf-8").read()):
            if m.group(0) not in known:
                bad.append((os.path.basename(f), m.group(0)))
    return bad


def main():
    if "--check" in sys.argv:
        files = sys.argv[sys.argv.index("--check") + 1:]
        gone = [f for f in files if not os.path.exists(f)]
        if gone or not files:
            sys.exit(f"--check needs existing markdown files; missing: {gone or 'none given'}")
        bad = check(files)
        if bad:
            print("UNKNOWN claim ids cited:", bad)
            sys.exit(1)
        print(f"all cited claim ids exist ({len(files)} files checked)")
        return
    items = load_claims()
    C.write_csv("claims.csv", items, ["id", "section", "statement", "value", "numerator", "denominator", "unit", "table",
                                      "query", "caveat", "script"])
    by = OrderedDict((s, []) for s in SECTION_ORDER)
    for c in items:
        by.setdefault(c["section"], []).append(c)
    out = [HEADER]
    for sec, cs in by.items():
        if not cs:
            continue
        out += [f"### {sec}\n", "| ID | Claim | Value | k / n | Source table · query | Script | Caveat |", "|---|---|---|---|---|---|---|"]
        for c in cs:
            kn = ""
            if c.get("numerator") is not None and c.get("denominator") is not None:
                kn = f"{c['numerator']} / {c['denominator']}"
            elif c.get("numerator") is not None:
                kn = f"{c['numerator']}"
            src = f"`tables/{c['table']}`" + (f" · {cell(c['query'])}" if c.get("query") else "")
            out.append(f"| {c['id']} | {cell(c['statement'])} | {cell(c['value'])} | {kn} | {src} | `{c['script']}` | {cell(c.get('caveat'))} |")
        out.append("")
    with open(os.path.join(C.OUT, "evidence-ledger.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"ledger: {len(items)} claims")


if __name__ == "__main__":
    main()
