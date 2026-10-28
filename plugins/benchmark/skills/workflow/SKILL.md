---
name: workflow
description: "Router for an empirical benchmark or evaluation study, from raw run data to a public release. Use whenever the user starts or resumes a benchmark, leaderboard, eval, bake-off, comparative study or \"analyze these runs\" project, asks \"what's the next step in the benchmark\", \"where are we on the study\", \"what order do we do this in\", \"which benchmark skill should I use\", or is about to write up results, run a control, review findings or publish data. Not for software eval harness tooling questions or for skill-creator evals. Explains the stage order, the artifacts handed between stages, the human checkpoints, and when to invoke each benchmark skill."
---

# Benchmark workflow router

This skill does no analysis. It tells you which stage the project is in, which skill to invoke, what must exist before it, and where a human must decide. Check the project folder for the artifacts below to locate the stage, then invoke the matching skill.

## Terms

- **Reference set:** the curated items every system is scored against.
- **Reference tool:** the evaluated system chosen, before results are seen and for a stated reason, as the comparison anchor (often an established baseline), for example when judging whether a finding outside the reference set is new to it. If it is the authors' own product, disclose that and say why it was chosen. Name it explicitly in the project; skills refer to it by this term. Being the anchor gives it no benefit of the doubt: it is scored, adjudicated, worded and drawn under the same rules as every other system.
- **Unit of analysis:** the cluster that items belong to (app, repo, dataset, document); it is what the bootstrap resamples.

## Objectivity comes first

Every stage is run as a neutral third party would run it, because the study is only worth publishing if a reader with no stake in any system would reach the same conclusions from the same data. This matters most when an author's employer makes one of the evaluated systems, and it applies to every study. Each skill applies these rules in its own stage:

1. **Same rules for every system.** Scoring, adjudication, wording strength, caveats, figure treatment and the effort spent configuring each system are the same for all of them, the author's own product and the reference tool included.
2. **Decide before you know.** Scoring policy, outcome thresholds, review-set rules and thesis-ranking criteria are fixed before the results they affect are seen. Later changes are logged as dated deviations, never made silently.
3. **Report against interest.** Every result is reported, including results unfavourable to the author's product and favourable to its competitors. No arm, sensitivity analysis, finding or thesis is dropped or downplayed because of where it points.
4. **Equal access.** If one system's owner reviews results, receives findings or gets time to respond before publication, every other evaluated system's owner is offered the same, on the same terms. Otherwise the paper says who had access.
5. **Disclose what cannot be made symmetric.** When equal treatment is not possible, name the asymmetry, the direction it could bias the results, and any sensitivity analysis, next to the numbers it affects.

## Why a fixed order

Each stage protects the next one from a specific failure: analysing before the scorer is validated produces wrong numbers; choosing a thesis before the evidence packet exists produces a story the data cannot carry; writing before a governing narrative exists produces claims that drift between documents; going public before a provenance and licence check turns a research result into a disclosure problem.

## Stages

| # | Stage | Skill | Needs | Produces | Human checkpoint |
|---|---|---|---|---|---|
| 1 | Evidence packet | `benchmark:empirical-analysis` | Authoritative run data, scorer docs, the harness repo | research memo, candidate theses, limitations, chart plan, generated evidence ledger, TODO | Human picks the thesis and decides every deferred item. The skill stops at the memo. |
| 2 | Governing narrative | `benchmark:narrative-guideline` | Memo, theses, ledger, the human's thesis decision | one guideline document that overrides all other write-up docs | Human approves the framing and the "claims never to make" list |
| 2b | Literature review | `benchmark:literature-review` | Study questions; after stage 2 the guideline's findings; the current bibliography | prior-art guide (before results), raw search reports, a proposal for approval, accepted citations and "to our knowledge" statements | Human approves every correction and addition (what, why, scope) before it is used |
| 3 | Close evidence gaps (optional) | `benchmark:supplementary-runs` | Packet gap list, harness access | plan, locked thresholds, supplementary results, archive | Human approves the plan, the spend, the merge |
| 4 | Findings outside the reference set (optional) | `benchmark:adjudication` | Queue of unmatched clusters from stage 1 | verdict CSV, adjudication report, reproducers | Human makes every final verdict |
| 5 | Internal expert review (optional) | `benchmark:review-kit` | Guideline, ledger, figures | kit PDF, feedback triage, draft messages | Human sends messages and accepts or declines each comment |
| 6 | Release readiness | `benchmark:release-readiness` | Guideline, provenance facts, repo | provenance and independence statement, licence audit, data release, checklist | Human confirms root licence, authors, disclosures, publication |
| 7 | Paper | `benchmark:paper-authorship` | Guideline, evidence packet (registry, ledger, tables, chart spec, limitations, TODO), release text from stage 6 | LaTeX paper, figures and manifest, claim inventory, guardrail rules, review-round log, pre-publication package | Figure set; each section; title, authors, affiliations and conflict-of-interest wording; placeholder values; statements about third-party products; submission |
| 8 | Public social assets | `benchmark:social-packet` (scaffold) | Public paper and repo only, the paper's figure script, guideline guardrails | working doc of asset specs, image pack with copy lines and alt text, copy bank | Asset list, each rendered asset and its copy, every hand-off; release gate after publication |

Figures: `empirical-analysis` only specifies charts; draft figures for reviewers are rendered by a script in `benchmark:review-kit`, and final paper figures belong to `paper-authorship`.

Stage 2b has three passes: a prior-art guide written before the results (during or before stage 1, so its predictions are honest), a targeted pass after stage 2, and a re-check of novelty claims before submission. Stages 3 to 5 are optional and can run in parallel after stage 2. Stage 6 runs before the paper (provenance, licences, data release) and again after it, as the final gate. After any of them changes a number, re-run stage 1's pipeline so the ledger stays the single source, then update the guideline (dated).

## Handoff artifacts

- Stage 1 to 2: `research-memo`, `candidate-theses`, `limitations-and-confounds`, `recommended-charts`, `evidence-ledger` (generated), `todo`.
- Stage 2 to everything else: the guideline. When the guideline and any older document disagree, the guideline wins. Mark superseded documents historical.
- Stages 3 and 4 to 2: new claim IDs from the pipeline, never hand-typed numbers.
- Stage 2b to 1, 2 and 7: the prior-art guide (novelty scores for candidate theses), claims the literature constrains (guideline), approved method notes (pipeline claims), and the accepted citations, verification log and "to our knowledge" statements (paper).
- Stage 7 to 8: the public paper, its figure script and tables, the claim inventory, the guideline's guardrails.
- Stage 6 to 7: the provenance and independence statement, the licence audit result, the data and code availability text.
- Stage 7 back to 6: the pre-publication package. Release readiness runs its pre-submission checklist as the final gate on the paper, confirming the package's checks passed rather than repeating them.

## Rules that hold across stages

0. The objectivity rules above hold at every stage and override convenience, schedule and narrative.
1. Every number in prose cites a claim ID generated by the pipeline. If a number is missing, add it to the pipeline.
2. Never send, publish, merge, or spend without explicit human approval. Draft and wait.
3. Keep analysis outputs and notes out of the benchmark's own source and fixture directories.
4. Date every decision. Record decisions in the memo's "Decisions taken" log and in the guideline, marked DECIDED with the option chosen.
5. Unmatched findings are "outside the reference set". Never "false positives" or "hallucinations" before adjudication.
6. Do not pad. A short stage output is valid; empty sections are removed, not filled.

## What to do when invoked

1. List the project folder and match what exists against the table to name the current stage.
2. Report in three lines: current stage, what is missing before it can finish, next skill to invoke.
3. If the user asks to skip ahead (for example "write the paper now" with no guideline), say what the skipped stage protects against and offer the quickest compliant path; do not refuse silently.
4. Invoke the next skill; do not duplicate its instructions here.
