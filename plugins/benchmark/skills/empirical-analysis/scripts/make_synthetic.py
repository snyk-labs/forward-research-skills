#!/usr/bin/env python3
"""Generate a tiny synthetic dataset to dry-run the pipeline: 3 systems x 2 groups x 12 items, one deliberate confound.

  python3 make_synthetic.py OUT_DIR

Systems B and C differ in BOTH effort and tool access (the deliberate confound), so s06 must flag the pair as descriptive-only.
"""
import csv
import hashlib
import os
import random
import sys


def main(out):
    os.makedirs(out, exist_ok=True)
    rng = random.Random(7)
    skill = {"A": 0.55, "B": 0.65, "C": 0.8}
    rows = []
    for s in "ABC":
        for unit in ("g1", "g2"):
            for i in range(12):
                p = skill[s] - (0.15 if unit == "g2" else 0)
                score = round(min(1.0, max(0.0, rng.gauss(p + 0.1, 0.25))), 3)
                rows.append(dict(system=s, unit=unit, arm="main", group="g", item=f"{unit}-{i:02d}", score=score, recorded_hit=int(score >= 0.5),
                                 hit=int(score >= 0.5)))
    with open(os.path.join(out, "runs.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(out, "systems.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["system", "family", "model", "effort", "tool_access"])
        w.writerow(["A", "f1", "m1", "high", "t0"])
        w.writerow(["B", "f1", "m1", "medium", "t0"])
        w.writerow(["C", "f1", "m1", "high", "t1"])
    with open(os.path.join(out, "recorded_aggregates.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["system", "hits"])
        for s in "ABC":
            w.writerow([s, sum(r["hit"] for r in rows if r["system"] == s)])
    with open(os.path.join(out, "SHA256SUMS"), "w") as fh:
        for f in ("runs.csv", "systems.csv", "recorded_aggregates.csv"):
            fh.write(f"{hashlib.sha256(open(os.path.join(out, f), 'rb').read()).hexdigest()}  {f}\n")


if __name__ == "__main__":
    main(sys.argv[1])
