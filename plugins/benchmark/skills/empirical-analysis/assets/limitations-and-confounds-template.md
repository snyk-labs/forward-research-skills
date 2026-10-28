# ‹Benchmark name›: limitations and confounds

Register read before any number leaves the team. Each entry: what, which claim IDs it affects, how it must be worded, what disclosure it requires.

## 1. What this packet does not and cannot claim

Repeatability (one run per cell), population-level inference, causal factor effects between multi-factor pairs, ‹others›.

## 2. Reference set

How it was built, known defects (with impact in matched count per system), label gaps, independence from evaluated systems (see `benchmark:release-readiness`). Unmatched findings are outside the reference set; precision is a lower bound.

## 3. Scoring policy

Registered rule and why; sensitivity results; counterfactual variants and where they appear.

## 4. Harness and configuration confounds

Table of system pairs that differ in more than one factor (effort, tool access, prompt policy, model tier, harness version). Mark each "descriptive only". Do not conflate model tier with effort.

### 4a. Version recording

Which tool versions were recorded per run and which were not; what the gap means for reproducibility.

## 5. Corpus composition confounds

Unit size imbalance, category imbalance, language or domain mix, units with prior vendor use or public familiarity (possible contamination).

## 5a. Asymmetries in treatment and access

Where systems were not treated identically: configuration effort, prompts or settings tuned for one system, who reviewed results or received findings before publication, which systems' unmatched findings were adjudicated. For each: direction it could bias the results, and any sensitivity analysis.

## 6. Cost, tokens, time

Observed known cost only; unavailable is not zero; cost per match valid only for systems with known cost.

## 7. Analysis-specific risks

Wilson optimism under clustering; approximate bootstrap with few clusters; multiplicity; mixed metric sets.

## 8. External-use guardrails

What may be quoted publicly, what needs vendor confirmation, which claims need an owner sign-off before release.

## 9. ‹Later additions, dated›

Supplementary arms, adjudication, provenance sensitivity: add one dated section each when they happen.
