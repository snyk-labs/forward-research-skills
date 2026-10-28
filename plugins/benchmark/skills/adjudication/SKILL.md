---
name: adjudication
description: "Decide whether findings reported outside a benchmark's reference set are real and new, and report the result without turning it into a miss rate. Use when the user says \"adjudicate the unmatched findings\", \"did the systems find things the reference set missed\", \"are these real or noise\", \"review the consensus clusters\", \"extra findings\", \"reference set gaps\", \"build reproducers for the confirmed items\", \"third-party vs first-party finding\", or has an adjudication queue from the evidence packet. Covers review-set definition, two-pass review, the human verdict CSV, reference-tool checks, novelty rules, boundary analysis, live reproducers, and reporting."
---

# Adjudication: findings outside the reference set

**Inputs:** the consensus-cluster queue and funnel counts from `benchmark:empirical-analysis`, the findings with their evidence, source access to the units, the reference tool's raw outputs. **Outputs:** `adjudication-review.md` (per-item write-ups), `adjudication-verdicts.csv` (the human's final calls and notes), reproducers, new claim IDs emitted by the pipeline from the CSV. **Human checkpoint:** the human makes every final verdict; reviewers only propose. **Hand-off:** `benchmark:narrative-guideline` (report section), `benchmark:release-readiness` (disclosure of what is reported to third parties, if anything).

Why this exists: scoring against a curated reference set measures recall on what was curated. Real findings the curators missed are invisible to it, and calling them false positives is wrong; calling them real without checking is worse. Every system's unmatched findings deserve the same chance of being found real, the reference tool's and the author's own product's included; otherwise adjudication rewards some systems and not others.

## 1. Define the review set before any verdict

Name the question first, because it decides the review set:

- **Which real items does the reference set lack?** (symmetric, the default). Review clusters from every system, prioritised by consensus (for example at least 3 systems from at least 2 families), plus a same-size random sample of each system's single-system findings, so a system with one configuration is not excluded by construction.
- **Which real items does any system find that the reference tool does not?** (one-sided by design). The same clusters minus items the reference tool already reported. Label it as answering only that question; it cannot support a comparison between systems on its own.

Fix the rule before any verdict. Write the rule and the funnel in plain words, per system: all unmatched findings, clustered, meeting the consensus rule, sampled, excluded (and why), remaining in scope. A consensus rule favours families with many configurations, so report each family's share of the queue. Readers misread the funnel unless every step has a number and a reason. Do not change the rule after seeing verdicts.

## 2. First pass: parallel code-tracing reviewers

Spawn parallel reviewers (subagents), one cluster each, with the strict rubric in `assets/review-rubric.md`. Strip system names from the cluster packets, so the real / borderline / noise verdict is made without knowing which systems reported it. They must trace the real code from source to sink (or the equivalent for your domain) and cite file and line. Verdicts: real / borderline / noise. Novelty: yes / partial / no. A reviewer who cannot trace the path says so; no verdict from the finding's own description.

## 3. Second pass: independent sceptic

A second reviewer who has not seen the first verdicts tries to refute each real or novel verdict, then both are compared. Merge conservatively: the weaker verdict wins until resolved. Disagreements go to the human with both traces.

## 4. Check broadly whether the reference tool already reported it (one-sided view only)

In the "reference-set gaps" view, novelty is judged against the reference set alone, the same way for every system. In the "new relative to the reference tool" view, do this check after the blind real / borderline / noise verdict and before any verdict is final, because it decides that view's novelty call and funnel (it needs the reference tool's outputs, so it cannot be blind). Two checks, both required: any rule from the reference tool near the location, and the same finding type anywhere in the same files. A narrow proximity window can miss a report placed at a configuration entry point rather than at the faulty line. A finding the reference tool reported under a different, correct label is "real but not new".

## 5. Human final calls

The human decides each item and writes notes in `adjudication-verdicts.csv` (`assets/adjudication-verdicts.csv`). The pipeline emits claims only from those final calls, never from reviewer drafts.

## 6. Novelty rules, applied consistently

Write the rules down and apply them to every item. The core one: a different manifestation of the same faulty item counts as one item (same root cause, same fix). Shares a source or sink with a reference item but a separate flow: "real, partly new". Needs an unusual precondition: borderline. Item outside the scored categories (for example a type the benchmark does not score): real, labelled out of scope of the scored classes.

## 7. Boundary and third-party analysis

For each confirmed item decide where the defect lives: in a third-party library (a library defect), or in first-party code misusing a sink-by-design API (misuse is a valid first-party finding). Keep two layers separate: the structural layer (what the code does, publishable now) and per-tool attribution (what each tool reported, and why). Attribution waits for confirmation from each attributed tool's owner, offered to all of them on the same terms; until every owner has had that chance, publish the structural layer only, for every tool alike.

## 8. Live reproducers

Build a reproducer for every confirmed item. Run it on a copy of the unit, never inside the benchmark's source or fixture directories; verify fingerprints afterwards so nothing leaked in. Footnote constraints (for example an input-size cap that limits one reproduction). Report "k of n reproduced live".

## 9. Report

Say "at least k real findings outside the reference set", in a section separate from the headline, with the review set's question and its per-system funnel. Compare systems on these counts only if the review set was symmetric. Never present it as a miss rate or adjust the headline. Report reference-set label gaps found along the way (items the set mislabels or omits) as a sensitivity with per-system impact, and let the human decide on a reference-set revision for future runs.

## Do not

Do not send findings to vendors or upstream maintainers without the human's approval; draft the disclosure and wait. When findings go to one system's owner before publication, draft the same disclosure, on the same timeline, for every other affected owner (`benchmark:release-readiness`, post-disclosure protocol). Do not describe unconfirmed clusters as confirmed findings in any outward text.
