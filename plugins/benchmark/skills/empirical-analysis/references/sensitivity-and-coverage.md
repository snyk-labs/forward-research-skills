# Sensitivity suite and coverage analysis

## Scoring-policy matrix

Re-score the recorded outputs (never re-run the systems) under every defensible alternative to the registered rule. Typical axes, each generic:

- tolerance sweep on any location or numeric matching (0, 1, 2, 3, 5, 10, 20, coarse level such as file or document);
- endpoint or evidence rules (any location, both ends, either end);
- matching variants (greedy versus optimal assignment; with versus without alias or synonym tables);
- credit policies (one-to-one versus many-to-one);
- type-only matching, as an upper bound.

For each variant store per-system hit counts and ranks. Compute Kendall tau-b between the registered ranking and each variant. Report: the number of variants that change the top-k set, the number that swap order inside the top k, and the lowest tau.

## Other robustness checks

- Leave-one-unit-out: drop each unit in turn and recompute the headline and the top system.
- Macro versus micro: same ranking or not.
- Bootstrap top-rank frequency for the leading system.
- Subgroup splits (by language, by category, by structural property) with the confounds between subgroups named. Control for the likely confounder (stratify by category, unit, length) before interpreting a raw split; a raw gap often shrinks or reverses under control, and that is itself a finding.

## Coverage

- Overlap matrix: which items each system found.
- Union and ceiling: items found by at least one system; the ceiling of this system set, not of the task.
- Unique coverage: items found only by one system.
- Shared blind spots: items nobody found. Inspect them for reference-set defects before calling them hard.
- Greedy cover staircase: how many items are reached by adding systems in order of marginal gain.
- Failure taxonomy: classify each miss with a small fixed set of causes (not reported at all, reported but wrong location, reported under a different label, dropped by a harness policy, excluded by a pipeline stage). Counts per system.
- Reference-set audit: items that no scoring variant can ever match (duplicated or mislabelled reference entries). Report as a sensitivity: the impact in matched count per system if corrected. Do not silently fix the reference set mid-analysis; the registered numbers remain the reported numbers unless the human decides otherwise.

## Consensus clusters of unmatched findings

Cluster findings that match no reference item by location and label, from every system, the reference tool included. Choose k and the rule before looking at the clusters. Then build two views, because they answer different questions:

- **Reference-set gaps (symmetric):** clusters from any system, prioritised by consensus (at least k systems from at least 2 families), plus a same-size random sample of each system's single-system findings, so a system with one configuration is not excluded by construction. This view can change every system's precision and recall picture.
- **New relative to the reference tool (one-sided, by design):** the same clusters minus items the reference tool already reported. Label it as answering only that question, and never use it alone to compare systems.

A consensus rule favours families with many configurations; report each family's contribution to the queue. Output is an adjudication queue with funnel counts per view and per system (all unmatched, clustered, meeting the rule, sampled, in scope). It is not a verdict list. Hand to `benchmark:adjudication`.
