"""Your independent port of the benchmark's scorer. REPLACE the body of `decide` for a real project.

Rules for a real port: re-implement from the harness's documented semantics, keep every tie-break identical, and make
`decide` return the SAME per-candidate decision the harness recorded. s01_validate_scorer.py compares them row by row and
fails on any difference. Do not analyse anything until it reports zero mismatches.
"""


def decide(row: dict) -> int:
    """Example scorer: a candidate counts as a hit when its match score reaches the registered threshold."""
    return int(float(row["score"]) >= 0.5)
