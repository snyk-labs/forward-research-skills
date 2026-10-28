#!/usr/bin/env python3
"""Step 06 — confounds register: flag system pairs that differ in more than one factor.

Reads systems.csv (system plus one column per factor, e.g. family, model, effort, tool_access, prompt). Any pair differing
in >1 factor cannot support a causal comparison: the memo must mark it descriptive-only. Also record per project:
repetitions per cell (one run means no repeatability claim) and cost (observed known cost; unavailable is not $0).
"""
import itertools
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def main():
    claims = C.Claims(__file__)
    systems = C.read_csv(os.path.join(C.DATA, "systems.csv"))
    factors = [k for k in systems[0] if k != "system"]
    out = []
    for a, b in itertools.combinations(systems, 2):
        diff = [f for f in factors if a[f] != b[f]]
        out.append(dict(a=a["system"], b=b["system"], n_factors_differ=len(diff), factors=diff,
                        causal_reading="single-factor" if len(diff) == 1 else "descriptive-only"))
    C.write_csv("confounds/pair_factors.csv", out)
    multi = sum(1 for r in out if r["n_factors_differ"] > 1)
    claims.add("C-CONF-01", "Confounds", "System pairs differing in more than one factor (descriptive-only)", multi,
               numerator=multi, denominator=len(out), table="confounds/pair_factors.csv",
               caveat="Single-factor pairs still need a control before a causal verb is used.")
    reps = os.environ.get("BENCH_REPS", "1")
    claims.add("C-CONF-02", "Confounds", "Repetitions per (system, unit) cell", int(reps), unit="runs",
               table="provenance/verification.json", caveat="One run per cell: no run-to-run variance or repeatability claim.")
    claims.save()


if __name__ == "__main__":
    main()
