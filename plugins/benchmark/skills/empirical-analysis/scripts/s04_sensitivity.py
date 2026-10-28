#!/usr/bin/env python3
"""Step 04 — sensitivity: scoring-policy matrix with rank stability (Kendall tau), leave-one-unit-out, macro vs micro.

Policy variants come from the `score` column re-thresholded (a stand-in for tolerance sweeps, endpoint rules, matching
variants, credit policies, type-only). Replace POLICIES with your harness's real variants, each a function row -> 0/1.
The registered policy stays the headline; every variant is labelled counterfactual.
"""
import os
import sys
from collections import defaultdict

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import stats as S  # noqa: E402

from scorer_port import decide  # noqa: E402

REGISTERED = "registered"
TOPK = 2  # size of the top set whose stability is reported
POLICIES = {REGISTERED: decide,
            "strict": lambda r: float(r["score"]) >= 0.7,
            "lenient": lambda r: float(r["score"]) >= 0.3}


def rate_by_system(rows, fn, units=None):
    k, n = defaultdict(int), defaultdict(int)
    for r in rows:
        if units is not None and r["unit"] not in units:
            continue
        k[r["system"]] += int(fn(r))
        n[r["system"]] += 1
    return {s: k[s] / n[s] for s in n}


def main():
    claims = C.Claims(__file__)
    rows = C.load_runs()
    systems = sorted({r["system"] for r in rows})
    units = sorted({r["unit"] for r in rows})
    if len(units) < 2:
        sys.exit("leave-one-unit-out needs >= 2 units")
    base = rate_by_system(rows, POLICIES[REGISTERED])
    pol_rows, tau_rows = [], []
    for name, fn in POLICIES.items():
        rates = rate_by_system(rows, fn)
        rk = S.ranks(rates)
        tau = S.kendall_tau_b([base[s] for s in systems], [rates[s] for s in systems])
        for s in systems:
            pol_rows.append(dict(policy=name, system=s, rate=rates[s], rank=rk[s]))
        tau_rows.append(dict(policy=name, kendall_tau_vs_registered=tau))
    C.write_csv("sensitivity/policy_matrix.csv", pol_rows)
    C.write_csv("sensitivity/policy_tau.csv", tau_rows)
    taus = [t["kendall_tau_vs_registered"] for t in tau_rows]
    destroyed = sum(1 for x in taus if x != x)  # NaN: every system tied under the variant
    worst = min((x for x in taus if x == x), default=float("nan"))
    claims.add("C-SENS-04", "Sensitivity", "Policy variants whose ranking is undefined (all systems tied)", destroyed,
               numerator=destroyed, denominator=len(taus), table="sensitivity/policy_tau.csv", caveat="Counts as ranking destroyed, not as agreement.")
    base_top = {s for s, r in S.ranks(base).items() if r <= TOPK}
    changed = sum(1 for n, fn in POLICIES.items() if n != REGISTERED
                  and {s for s, r in S.ranks(rate_by_system(rows, fn)).items() if r <= TOPK} != base_top)
    claims.add("C-SENS-05", "Sensitivity", f"Variants that change the top-{TOPK} set", changed, numerator=changed,
               denominator=len(POLICIES) - 1, table="sensitivity/policy_matrix.csv")
    claims.add("C-SENS-01", "Sensitivity", "Lowest Kendall tau-b between the registered ranking and any policy variant", round(worst, 3),
               unit="tau-b", table="sensitivity/policy_tau.csv", caveat=f"{len(POLICIES) - 1} counterfactual variants; labelled counterfactual, never headlines.")
    loo = []
    for u in units:
        rest = set(units) - {u}
        r = rate_by_system(rows, POLICIES[REGISTERED], rest)
        loo.append(dict(left_out=u, **{s: r[s] for s in systems}, top=sorted(r, key=lambda s: (-r[s], s))[0]))
    C.write_csv("sensitivity/leave_one_unit_out.csv", loo)
    tops = {r["top"] for r in loo}
    claims.add("C-SENS-02", "Sensitivity", "Distinct top-ranked systems across leave-one-unit-out runs", len(tops),
               unit="distinct systems", table="sensitivity/leave_one_unit_out.csv", query=f"{len(units)} runs",
               caveat="Top system per run computed with deterministic tie-break by name.")
    macro = {}
    for s in systems:
        per = defaultdict(lambda: [0, 0])
        for r in rows:
            if r["system"] == s:
                per[r["unit"]][0] += int(POLICIES[REGISTERED](r))
                per[r["unit"]][1] += 1
        macro[s] = S.mean([a / b for a, b in per.values()])
    same = S.ranks(base) == S.ranks(macro)
    claims.add("C-SENS-03", "Sensitivity", "Micro and macro aggregation give the identical ranking", same,
               table="headline/headline.csv", caveat="Ranks compared with ties sharing the best rank.")
    claims.save()


if __name__ == "__main__":
    main()
