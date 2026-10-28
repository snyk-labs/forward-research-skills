---
name: supplementary-runs
description: "Close evidence gaps after the main benchmark run with small, additive control runs, planned and pre-specified before any result is seen. Use when the user says \"can we run a control\", \"same-effort arm\", \"neutral prompt arm\", \"repeatability run\", \"add a supplementary arm\", \"easy-lift estimate\", \"pre-register the thresholds\", \"have another agent run the harness\", \"publish the extra runs\", or when a confound in the evidence packet blocks a claim and a cheap run could resolve it. Not for the final public data release (use release-readiness). Covers the cost estimate, locked outcome thresholds, a proxy protocol for agent-operated harnesses, integration with the main data, publication, and the contamination rule."
---

# Supplementary runs: small additive controls after the main run

**Inputs:** the limitations register and narrative guideline (which confound blocks which claim), harness repo and docs, the validated scorer, budget. **Outputs:** `supplementary-runs-plan`, `supplementary-arms-thresholds` (copied from `assets/thresholds-fixed-before-analysis-template.md`, locked before analysis), new execution data, supplementary claims in the ledger, an immutable checksummed archive. **Human checkpoints:** approve the plan and spend before any run; approve the merge of harness changes; approve publication. **Hand-off:** re-run `benchmark:empirical-analysis` pipeline with the loader below; update `benchmark:narrative-guideline` (supplementary arms in their own labelled section).

Why small and additive: the main run is frozen and published. A supplementary arm is a control that makes a hedge ("consistent with") into a supported claim, or shows it does not hold. It must never be able to rewrite the headline. A control is only a control if either outcome is possible and either outcome gets reported.

## 1. Easy-lift estimate (`assets/supplementary-runs-plan-template.md`)

For each candidate arm write: the question and which confound it addresses; what the harness permits (for example a fork may not add configurations, so use a separate execution); cost and time extrapolated from the observed main-run cost per cell; what the paper must say if the result goes against the current reading; which systems the arm could help or hurt; and a recommended bundle. Rank arms by how much the confound they address limits the study's conclusions, not by which claims they could rescue, and include arms that could weaken a claim or narrow a lead the author's product holds. An arm that gives one system an extra chance (a tuned prompt, more effort, extra tools, a re-run) gets a matching arm for the comparable systems, or is labelled as one-sided in every place it is reported. Recommend the smallest bundle that resolves the most limiting confounds, and list the arms considered but not run, with the reason. State caveats that will always be disclosed (single run, separate execution, version drift).

## 2. Lock thresholds before analysing (`assets/thresholds-fixed-before-analysis-template.md`)

Before looking at any supplementary result, write for each arm the outcome rule and the exact wording for each outcome: supported, partial, not supported. Every arm that runs is reported against these rules, whatever the outcome; none is dropped or re-framed because of where it points. Include the scoring policy, the units, the comparison and the numeric thresholds. Commit the file with a timestamp before the runs finish. In public text say "thresholds fixed before analysis", not "pre-registered", unless a public registry holds it. Why: thresholds chosen after seeing a result are a story, not a control.

## 3. Proxy protocol (another agent operates the harness)

Use when you can read the repo and write prompts but another agent runs the commands. Full text in `references/proxy-protocol.md`. Order:

1. Read-only health check first: repo state, pinned toolchain including bundled CLIs, credentials through the harness's own env path, baseline checksums of existing data, a dry run.
2. Branch-only changes; review the diff yourself before any run.
3. Run the cheapest arm first to validate the pipeline end to end.
4. Run long jobs detached (nohup plus polling) because an agent's tool timeout can kill a foreground process.
5. Set any spend cap at the human-approved budget plus headroom, never below the estimate: a cap hit mid-run wastes the money already spent. Raising it again needs the human's approval.
6. On failure, stop and diagnose; retry only the failed items.
7. Re-verify baseline checksums at the end.
8. Keep source and fixture directories clean: no build output, no notes; verify fingerprints.
9. Record tool versions per run; if the harness does not, add that first.

## 4. Integration

Use the `arm` column contract in `empirical-analysis/references/data-contract.md`. Write a loader that verifies identity with the main run (reference set, prompts, fingerprints) and refuses to load on any mismatch. Score with the validated scorer. Label every supplementary row supplementary. Failed items are excluded and disclosed, never imputed. Add the arms to the ledger under their own section and never merge them into the headline.

## 5. Publish

Publish as an immutable, checksummed archive next to the original, with a manifest of per-file hashes. Secret-scan the staging directory or an extracted copy first (compressed archives are reported as skipped, not scanned) with credential-shaped patterns (`scripts/secret_scan.py`), not prose words such as "Bearer" that appear in documentation. After human approval, fast-forward merge the harness branch. Never force-push.

## 6. Contamination rule

Never re-run any evaluated system after changes derived from the benchmark (rule fixes, prompt or configuration tuning on the corpus) and report the result as a score; the benchmark has leaked into the system. This applies to the author's own product first. Report the fixes as a dated post-disclosure note instead (see `benchmark:release-readiness`).
