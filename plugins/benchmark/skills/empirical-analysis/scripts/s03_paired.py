#!/usr/bin/env python3
"""Step 03 — paired comparisons on the same items: discordant counts, exact McNemar with mid-p beside it.

Descriptive and unadjusted. Never write "significant" or "indistinguishable"; write "b vs c discordant, exact p = …
(mid-p = …), descriptive, unadjusted for multiplicity, ignores clustering".
"""
import itertools
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import stats as S  # noqa: E402


def main():
    claims = C.Claims(__file__)
    rows = C.load_runs()
    systems = sorted({r["system"] for r in rows})
    hit = {(r["system"], r["unit"], r["item"]): r["hit"] for r in rows}
    items = sorted({(r["unit"], r["item"]) for r in rows})
    out = []
    for n_pair, (a, b) in enumerate(itertools.combinations(systems, 2), 1):
        only_a = sum(1 for u, i in items if hit.get((a, u, i), 0) and not hit.get((b, u, i), 0))
        only_b = sum(1 for u, i in items if hit.get((b, u, i), 0) and not hit.get((a, u, i), 0))
        p, pm = S.mcnemar_exact(only_a, only_b), S.mcnemar_midp(only_a, only_b)
        out.append(dict(a=a, b=b, only_a=only_a, only_b=only_b, p_exact=p, p_mid=pm))
        claims.add(f"C-PAIR-{n_pair:02d}", "Paired", f"{a} vs {b}: items hit by only one", f"{only_a} vs {only_b}",
                   numerator=only_a + only_b, unit="discordant items", table="paired/mcnemar.csv", query=f"a={a}, b={b}",
                   caveat="Descriptive, unadjusted for multiplicity, ignores clustering.")
        claims.add(f"C-PAIR-{n_pair:02d}-pexact", "Paired", f"{a} vs {b}: exact McNemar p", round(p, 4), table="paired/mcnemar.csv",
                   query=f"a={a}, b={b}", caveat="Descriptive; do not call it significant.")
        claims.add(f"C-PAIR-{n_pair:02d}-pmid", "Paired", f"{a} vs {b}: mid-p McNemar", round(pm, 4), table="paired/mcnemar.csv",
                   query=f"a={a}, b={b}", caveat="Shown beside the exact p; descriptive.")
    C.write_csv("paired/mcnemar.csv", out)
    claims.save()


if __name__ == "__main__":
    main()
