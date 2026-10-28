#!/usr/bin/env python3
"""Step 05 — coverage: overlap, union ceiling, unique coverage, and the items nobody found (shared blind spots).

Add here, per project: a failure taxonomy (why a system missed an item) and consensus clusters of unmatched findings
from EVERY system, the reference tool included (prioritised by >= k systems from >= 2 families, plus a same-size random
sample of each system's single-system findings; see references/sensitivity-and-coverage.md): that is an adjudication
QUEUE, not a verdict. Unmatched findings are "outside the reference set", never "false positives" or "hallucinations".
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def main():
    claims = C.Claims(__file__)
    rows = C.load_runs()
    systems = sorted({r["system"] for r in rows})
    items = sorted({(r["unit"], r["item"]) for r in rows})
    found = {s: {(r["unit"], r["item"]) for r in rows if r["system"] == s and r["hit"]} for s in systems}
    union = set().union(*found.values())
    out = []
    for j, s in enumerate(systems, 1):
        others = set().union(*(found[o] for o in systems if o != s))
        out.append(dict(system=s, found=len(found[s]), unique=len(found[s] - others)))
        claims.add(f"C-COV-{10 + j}", "Coverage", f"{s}: items found by no other system", len(found[s] - others),
                   numerator=len(found[s] - others), denominator=len(items), table="coverage/overlap.csv", query=f"system={s}")
    C.write_csv("coverage/overlap.csv", out)
    claims.add("C-COV-01", "Coverage", "Union ceiling: items found by at least one system", len(union), numerator=len(union),
               denominator=len(items), table="coverage/overlap.csv", caveat="Ceiling of this system set, not of the task.")
    claims.add("C-COV-02", "Coverage", "Shared blind spots: items found by no system", len(items) - len(union),
               numerator=len(items) - len(union), denominator=len(items), table="coverage/overlap.csv")
    claims.save()


if __name__ == "__main__":
    main()
