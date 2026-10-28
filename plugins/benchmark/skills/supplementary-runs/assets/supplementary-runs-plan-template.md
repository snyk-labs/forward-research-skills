# ‹Benchmark name›: supplementary runs, what is an easy lift

> Draft for human approval. No run starts until the plan and spend are approved. Thresholds are in `supplementary-arms-thresholds` (from `thresholds-fixed-before-analysis-template.md`), committed before results.

## What the harness allows

‹For example: a fork or resume cannot add configurations, so each arm runs as a separate execution; the scorer, reference set and prompts are identical to the main run; tool versions are/aren't recorded per run.›

## Gaps the packet found

| Gap | Blocked claim | Confound |
|---|---|---|

## Candidate arms

| Arm | Question | Confound addressed | Cells (systems × units × reps) | Cost estimate | Time | If the result goes against the current reading | Systems it could help or hurt | Matching arm for comparable systems |
|---|---|---|---|---|---|---|---|---|
| A | ‹e.g. does the effect survive at equal effort?› | ‹…› | | ‹observed cost per cell × cells› | | ‹what the paper must then say› | ‹…› | ‹arm id, or "one-sided: labelled"› |

Cost and time are extrapolated from the observed main run: ‹cost per cell, wall time per cell, source claim IDs›.

## Recommended bundle

‹Arms, order (cheapest first), total estimated cost, which confounds it resolves. Ranked by how much each confound limits the conclusions, not by which claims an arm could rescue.›

## Considered but not run

‹Arm, reason (cost, harness limit, out of scope). An arm is never left out because its likely result is unwelcome.›

## Caveats always disclosed

Single run per arm; separate execution; version drift since the main run; ‹others›.

## Approval

- [ ] Plan and spend approved by ‹name› on ‹date›.
