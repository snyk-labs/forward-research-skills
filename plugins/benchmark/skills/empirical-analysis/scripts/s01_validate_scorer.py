#!/usr/bin/env python3
"""Step 01 — validate the scorer port: reproduce every recorded per-candidate decision AND every recorded aggregate.

Reads runs.csv (columns include score, recorded_hit) and optional recorded_aggregates.csv (system, hits). Fails on any
mismatch, because every later number depends on this.
"""
import os
import sys
from collections import Counter

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
from scorer_port import decide  # noqa: E402


def main():
    claims = C.Claims(__file__)
    rows = C.read_csv(os.path.join(C.DATA, "runs.csv"))
    mism = [r for r in rows if decide(r) != int(r["recorded_hit"])]
    C.write_csv("scorer/mismatches.csv", mism, list(rows[0].keys()) if rows else None)
    claims.add("C-SCORER-01", "Scorer", "Per-candidate decisions reproduced exactly by the independent port",
               len(rows) - len(mism), numerator=len(rows) - len(mism), denominator=len(rows),
               table="scorer/mismatches.csv", caveat="Zero mismatches required before any analysis.")
    agg_path = os.path.join(C.DATA, "recorded_aggregates.csv")
    if not os.path.exists(agg_path):
        print("WARNING: recorded_aggregates.csv missing; aggregate reproduction NOT checked", file=sys.stderr)
        claims.add("C-SCORER-02", "Scorer", "Recorded per-system aggregates reproduced", "not checked (no recorded aggregates supplied)",
                   table="scorer/mismatches.csv", caveat="Supply recorded aggregates to close this gate.")
    else:
        mine = Counter()
        for r in rows:
            mine[r["system"]] += decide(r)
        diff = [(a["system"], a["hits"], mine[a["system"]]) for a in C.read_csv(agg_path) if int(a["hits"]) != mine[a["system"]]]
        claims.add("C-SCORER-02", "Scorer", "Recorded per-system aggregates reproduced (systems matching)", len(diff) == 0,
                   numerator=len(mine) - len(diff), denominator=len(mine), table="scorer/mismatches.csv",
                   caveat="Mismatching aggregates abort the run.")
        if diff:
            claims.save()
            sys.exit(f"aggregate mismatch: {diff}")
    claims.save()
    if mism:
        sys.exit(f"{len(mism)} per-candidate mismatches; fix the port before analysing")


if __name__ == "__main__":
    main()
