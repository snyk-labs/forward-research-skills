# ‹Benchmark name and version›: research memo

> Internal evidence packet: findings, not publication prose. Every number carries a claim ID that resolves in `evidence-ledger`. The memo stops before a thesis is chosen; options are ranked in `candidate-theses`. Read `limitations-and-confounds` before any number leaves the team. All p-values are exact McNemar on discordant items with the mid-p beside them; descriptive, unadjusted, not clustered.

**Configuration labels.** Each label names the complete ‹harness› plus configuration, never the bare model.

- ‹label›: ‹what it is: tool, version, model, effort, tool access, prompt›.

### Terms used (written for non-statisticians)

- **Micro rate (k/n).** Pool all ‹items›; count how many a system matched. Every item weighs the same, so a ‹unit› with many items counts more.
- **Macro rate (the headline when the harness registers it).** Compute the rate within each ‹unit of analysis›, then average. Every unit weighs the same. State which is the registered headline and print k/n beside it.
- **Cluster bootstrap and its 95% interval.** A resampling check of how much a score depends on which ‹units› are in the corpus. One replicate is a pretend benchmark made by drawing ‹N› units at random with replacement; the score is recomputed on each replicate, ‹B› times. The interval is the middle 95% of those scores. It measures sensitivity to the choice of units, not run-to-run randomness.
- **Discordant items / paired comparison.** Both systems are scored on the same items. Items both hit or both missed carry no information on which is better; items hit by one and missed by the other do. "9 vs 2" means 9 only A, 2 only B. McNemar asks how surprising that split would be if they were equally good.
- **Counterfactual policy.** Re-scoring recorded outputs under a rule other than the registered one, to test sensitivity. Never a headline.
- **Outside the reference set.** A reported finding that matched no reference item. Not the same as wrong.

## 1. What was analysed, and how far it can be trusted

Authoritative run set, archive checksum, per-file verification, parent/child lineage, scorer-port reproduction result (claim IDs). Corpus facts with explicit counting bases (for example "N items across M units, counted after de-duplication"). Reproducibility facts: tool versions per run, commits, prompt delivery per system, and the gaps.

## 2. Headline landscape (registered metrics only)

Table: system, k/n, micro, macro, intervals. Separate panels for systems with different registered metrics.

## 3.–N. Findings by question

One section per question or finding. Each: the result with claim IDs, the control that was run, the caveat that applies.

## N+1. Beyond the planned questions

Coverage and union ceiling, failure taxonomy, shared blind spots, efficiency and cost, fixture difficulty, unmatched-findings queue, reference-set defects.

## N+2. Disconfirmation log

| Candidate narrative | Test | Outcome |
|---|---|---|

## N+3. Decisions taken (‹YYYY-MM-DD›)

Dated, numbered, with the human's name. Example form: "1. Reference-set defect: not fixed or rescored for this publication; disclosed. Impact: ‹claim ID›." Deferred work lives in `TODO`.
