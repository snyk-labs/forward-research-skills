# ‹Benchmark name›: recommended charts

A plan only. Each chart reads tables under `tables/` produced by the pipeline, so it can be regenerated when the data is.

## Rules for every chart

1. Show counts: k/n on or beside every bar and dot.
2. Keep unlike metrics in separate panels; never put a system on an axis it was not registered for, except in a panel labelled counterfactual.
3. Mark counterfactual policies visibly.
4. No run-to-run error bars when there is one run per cell. Cluster-bootstrap intervals are allowed, labelled as such.
5. Label p-values "descriptive (exact McNemar, unadjusted)" with the mid-p in parentheses.
6. Show scoring sensitivity wherever a headline count depends on a scoring choice.
7. Every chart carries its mandatory caveat label in the caption, and its claim IDs in this plan (internal drafts may print them; published captions never do).
8. Colour-blind-safe palette; no 3-D; direct labels over legends where possible.
9. Order systems by a stated rule (the headline metric, or a fixed order kept across charts), and give no system visual emphasis the question does not need: the reference tool and the authors' product get no highlight colour, bolding or prime position.

## Chart plan

| # | Chart | Question it answers | Source table (columns) | Encoding | Mandatory caveat label | Claim IDs | Thesis |
|---|---|---|---|---|---|---|---|
| 1 | Headline dot plot | What share of the reference set does each system find? | `headline/headline.csv` | dot per system with cluster-bootstrap whiskers, k/n labels | "Intervals reflect choice of units, not run-to-run variance" | | all |
| 2 | Overlap and ceiling | Do systems find the same items? | `coverage/overlap.csv` | UpSet or staircase | "Ceiling of this system set, not of the task" | | |
| 3 | Rank-stability heatmap | Is the ranking an artefact of the scorer? | `sensitivity/policy_matrix.csv` | rows = policies, columns = systems, cell = rank, tau column | "Variants are counterfactual" | | |

## Charts to avoid

Ranked bars with no counts, intervals implying run-to-run variance, any chart mixing registered metrics, dual axes, charts whose only message is a causal claim a confound blocks.

## Rendering

Script that regenerates every figure from `tables/`, committed with the packet. Render each figure to an image and check for overflow and legibility at the published size before sharing.
