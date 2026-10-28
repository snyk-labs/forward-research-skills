#!/usr/bin/env python3
"""Step 02 — headline: micro and macro rate per system, Wilson interval, cluster bootstrap over the unit of analysis."""
import os
import sys
from collections import defaultdict

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import stats as S  # noqa: E402

N_BOOT = 2000


def main():
    claims = C.Claims(__file__)
    rows = C.load_runs()
    systems = sorted({r["system"] for r in rows})
    units = sorted({r["unit"] for r in rows})
    by = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # system -> unit -> [hits, n]
    for r in rows:
        c = by[r["system"]][r["unit"]]
        c[0] += r["hit"]
        c[1] += 1
    sizes = sorted({sum(1 for r in rows if r["system"] == systems[0] and r["unit"] == u) for u in units})
    out = []
    for i, s in enumerate(systems, 1):
        k = sum(c[0] for c in by[s].values())
        n = sum(c[1] for c in by[s].values())
        macro = S.mean([c[0] / c[1] for c in by[s].values() if c[1]])
        lo, hi = S.wilson(k, n)

        def macro_stat(sample, s=s):
            return S.mean([by[s][u][0] / by[s][u][1] for u in sample if by[s][u][1]])

        draws = S.cluster_bootstrap(units, macro_stat, N_BOOT)
        blo, bhi = S.bootstrap_interval(draws)
        out.append(dict(system=s, hits=k, n=n, micro=k / n, macro=macro, wilson_lo=lo, wilson_hi=hi, boot_lo=blo, boot_hi=bhi))
        claims.add(f"C-HEAD-{i:02d}", "Headline", f"{s}: micro hit rate over all items", round(k / n, 4), numerator=k, denominator=n,
                   unit="rate", table="headline/headline.csv", query=f"system={s}",
                   caveat="Micro = pooled over items. Counts are one run per cell: no repeatability claim.")
        claims.add(f"C-HEAD-{i:02d}-macro", "Headline", f"{s}: macro hit rate (mean of per-unit rates)", round(macro, 4), unit="rate",
                   table="headline/headline.csv", query=f"system={s}", caveat=f"Mean over {len(units)} units.")
        claims.add(f"C-HEAD-{i:02d}-wilson", "Headline", f"{s}: Wilson 95% interval for the micro rate", f"{lo:.3f} to {hi:.3f}", unit="interval",
                   table="headline/headline.csv", query=f"system={s}", caveat="Assumes independent items; optimistic when items cluster in units.")
        claims.add(f"C-HEAD-{i:02d}-boot", "Headline", f"{s}: cluster-bootstrap 95% interval for the macro rate", f"{blo:.3f} to {bhi:.3f}",
                   unit="interval", table="headline/headline.csv", query=f"system={s}",
                   caveat=f"Resamples {len(units)} units (sizes {sizes[0]} to {sizes[-1]} items), {N_BOOT} draws, seed {S.SEED}; sensitivity to unit choice, not run-to-run variance.")
    # top-rank frequency: how often each system has the highest macro rate across the same bootstrap resamples
    import random
    rng = random.Random(S.SEED + 1)
    wins = {s: 0 for s in systems}
    for _ in range(N_BOOT):
        sample = [units[rng.randrange(len(units))] for _ in units]
        sc = {s: S.mean([by[s][u][0] / by[s][u][1] for u in sample if by[s][u][1]]) for s in systems}
        best = max(sc.values())
        for s in systems:
            if abs(sc[s] - best) < 1e-12:
                wins[s] += 1 / sum(1 for v in sc.values() if abs(v - best) < 1e-12)  # ties share the win
    for j, s in enumerate(systems, 1):
        claims.add(f"C-HEAD-{j:02d}-top", "Headline", f"{s}: share of bootstrap resamples in which it ranks first (ties shared)",
                   round(wins[s] / N_BOOT, 4), numerator=round(wins[s], 2), denominator=N_BOOT, unit="share",
                   table="headline/headline.csv", caveat="Sensitivity to the choice of units, not run-to-run randomness.")
    C.write_csv("headline/headline.csv", out)
    claims.save()


if __name__ == "__main__":
    main()
