# Exploration checklist: findings beyond the planned questions

Run through this after the established questions. Each item is generic; add the study's own runner- or domain-specific signals in the intake. A finding from this list goes into the memo with the same claim, control and caveat discipline as a planned one, and is labelled exploratory.

## Coverage

- **Item-level overlap and unique coverage:** which items each system found, which only one system found, which none found.
- **Union ceiling ("oracle union"):** items found by at least one system; the ceiling of this system set, not of the task.
- **Marginal coverage of pairs:** which pair of systems adds the most beyond the best single one; greedy cover order.
- **Stable shared blind spots:** items no system finds; check them for reference-set defects before calling them hard.

## Why systems miss

- **Failure taxonomy:** not reported at all, reported with the right label but the wrong location, reported under another label, dropped by a harness policy, excluded by a pipeline stage.
- **Detection-only versus localized performance:** right label anywhere versus right label at the right place; the gap says whether a system fails to find or fails to point.
- **Partial-evidence asymmetries:** for multi-part items (for example source and sink, question and evidence span), which part systems get right, by system, category and subgroup.
- **Complexity effects:** item size, number of files or documents involved, chain length, number of acceptable alternatives; same-unit versus cross-unit structure.

## Robustness

- **Per-unit difficulty:** which units drive the headline; leave-one-unit-out ranking.
- **Macro versus micro:** same ranking or not.
- **Scoring-policy rank reversals:** which defensible scoring variants change the order (see `sensitivity-and-coverage.md`).

## Efficiency

- **Pareto frontiers:** recall, precision, wall time, tokens and cost; which systems are dominated.
- **Cost-quality inversions:** more expensive and less effective, among systems with known cost only.

## Execution and harness behaviour

- **Self-reported exclusions:** coverage a system says it skipped or deferred (scope limits, file caps, policy exclusions).
- **Execution-failure signals:** empty exports, early stops, very few turns or very short runs, partial outputs. Distinguish "the system could not" from "the run did not", and report which was ruled out.

## Outside the reference set

- **Categories of unmatched outputs worth adjudication**, from every system, the reference tool included (see `sensitivity-and-coverage.md`, consensus clusters).
