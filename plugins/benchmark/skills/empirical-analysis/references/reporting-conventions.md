# Reporting conventions

## Rates and counts

Print k/n beside every rate: "61.3% (49/80)". A bare percentage hides a small denominator.

## Micro versus macro

Micro pools all items and divides hits by items, so a unit with 10 items weighs five times a unit with 2. Macro computes the rate per unit, then averages the unit rates, so every unit weighs the same. Say which the harness registers as the headline, headline that one, and print the other beside it. Report whether the two give the same ranking; if only precision-like metrics change, say so.

## Intervals

- Wilson interval for a rate. It treats items as independent, so call it optimistic when items cluster in units.
- Cluster bootstrap over the natural unit (app, repo, dataset, document). State the cluster count, the cluster sizes (range and median), the number of draws and the seed. With few clusters (around 20 or fewer) say the percentile interval is approximate. It measures sensitivity to the choice of units, not run-to-run randomness.
- "Ranks first in x% of bootstrap draws" is a valid summary of top-rank stability; explain what a draw is in plain words.

## Small and uneven cells

Cross-tabulations (by language, category, structure) usually have cells of a handful of items, and the cells differ in size and mix. Report them descriptively with their counts, name the other factors that differ between cells, and never imply that a pattern holds for the wider population from a small cross-tab.

## Paired tests

On the same items, count discordant items: only A hit (b), only B hit (c). Report b versus c, exact McNemar p, and the mid-p beside it. Name them "descriptive, unadjusted for multiplicity, ignoring clustering". If exact and mid-p fall on different sides of 0.05, say so explicitly. Forbidden wording: "significant", "statistically indistinguishable", "no difference". Allowed: "not separable on this reference set (9 vs 6 discordant, exact p = 0.61, descriptive)".

## Sensitivity wording

Counterfactual policies are labelled as such in every table and chart. The registered policy remains the headline. A sensitivity result either holds ("top two unchanged under k of k variants") or it does not; report how many variants changed which rank, not just the best case.

## Metrics that must not mix

If systems are scored under different registered metrics (for example one family can only localise a finding, another gives endpoint evidence), keep them in separate panels and tables. Never average unlike metrics into one headline. A row scored under another system's metric is labelled counterfactual.

## Unmatched findings

"Outside the reference set." Report counts as a lower bound on what the system found, and name precision as a lower bound with respect to reference-set omissions. Adjudication (skill `benchmark:adjudication`) is what turns a cluster into a verdict.

## Cost and efficiency

Report observed known cost. If a system's cost is unavailable, say unavailable, not zero, and exclude it from cost comparisons. Cost per match is only valid among systems with known cost and the same match definition. Name the costs the study does not measure (licences, subscriptions, infrastructure, human triage time) for every system alike, so a system whose measured per-run cost is zero is not read as free.
