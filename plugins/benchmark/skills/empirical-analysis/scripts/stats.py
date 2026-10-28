"""Descriptive statistics for benchmark analysis. Standard library only, deterministic.

Everything here is descriptive: no function claims population-level inference. Report raw counts beside every rate.
"""
from __future__ import annotations

import math
import random

SEED = 20260101  # change per project, record it in the memo, never change it after the first publication


def wilson(k: int, n: int, z: float = 1.959963984540054):
    """Wilson score interval for k successes out of n. Treats items as independent, so it is optimistic when items cluster."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar p on discordant counts: b = only A succeeded, c = only B succeeded."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def mcnemar_midp(b: int, c: int) -> float:
    """Two-sided mid-p McNemar = 2*(P(X<k) + P(X=k)/2) with k = min(b, c), capped at 1 (Fagerland et al. convention).
    Equals exact p minus P(X=k) when b != c, and 1 when b == c. Report it beside the exact p."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    point = math.comb(n, k) / (2 ** n)
    if b == c:
        return 1.0  # symmetric split: 2*(P(X<k) + P(X=k)/2) = 1 exactly
    return min(1.0, mcnemar_exact(b, c) - point)


def percentile(xs, q: float) -> float:
    xs = sorted(xs)
    if not xs:
        return float("nan")
    pos = (len(xs) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def cluster_bootstrap(clusters: list, stat_fn, n_boot: int = 2000, seed: int = SEED) -> list:
    """Resample whole clusters (the natural unit: app, repo, dataset, document) with replacement.

    `clusters` must be a sorted list of cluster ids so the draw is reproducible. `stat_fn(sample_ids)` returns a number.
    Report the cluster count and sizes next to any interval; with few clusters the percentile interval is approximate.
    """
    rng = random.Random(seed)
    out = []
    for _ in range(n_boot):
        sample = [clusters[rng.randrange(len(clusters))] for _ in clusters]
        out.append(stat_fn(sample))
    return out


def bootstrap_interval(draws: list, level: float = 0.95):
    a = (1 - level) / 2
    return percentile(draws, a), percentile(draws, 1 - a)


def ranks(values: dict, higher_better: bool = True) -> dict:
    """Competition ranks (1 = best). Ties share the best rank; the sort key is deterministic."""
    items = sorted(values.items(), key=lambda kv: ((-kv[1] if higher_better else kv[1]), str(kv[0])))
    out, prev, prev_rank = {}, None, 0
    for i, (k, v) in enumerate(items, 1):
        if prev is None or abs(v - prev) > 1e-12:
            prev_rank = i
        out[k] = prev_rank
        prev = v
    return out


def kendall_tau_b(x: list, y: list) -> float:
    """Kendall tau-b between two equal-length score lists. Use it to compare system rankings across scoring variants."""
    n = len(x)
    conc = disc = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                tx += 1
            elif dy == 0:
                ty += 1
            elif dx * dy > 0:
                conc += 1
            else:
                disc += 1
    den = math.sqrt((conc + disc + tx) * (conc + disc + ty))
    return (conc - disc) / den if den else float("nan")


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def top(counter, n=None):
    """Deterministic most_common: ties broken by key, so output does not depend on PYTHONHASHSEED."""
    items = sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))
    return items[:n] if n else items
