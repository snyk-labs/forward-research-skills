---
name: empirical-analysis
description: "Turn completed benchmark or evaluation run data into a reproducible evidence packet (research memo, ranked candidate theses, limitations, chart plan, generated evidence ledger) and stop before any thesis is chosen. Use whenever the user has finished runs of several systems on a reference set and says \"analyze the benchmark\", \"what do the results say\", \"first-pass analysis\", \"evidence packet\", \"candidate theses\", \"validate the scorer\", \"claims ledger\", \"sensitivity analysis\", \"is the ranking robust\", or wants numbers traceable and reproducible before writing anything. Not for bias sensitivities tied to provenance (use release-readiness). Applies to any system comparison, such as security scanners, LLM evals, data-quality or retrieval studies."
---

# Empirical analysis: raw runs to an evidence packet

**Inputs:** a completed study intake (`assets/study-intake-template.md`: archive and lineage, ordered reading list, study-specific caveats, established questions, output folder), the authoritative run archive and its checksums, the harness repo and scoring docs, the reference set, the run configuration table, and the prior-art guide from `benchmark:literature-review` if one exists (it informs the novelty score). **Outputs (in the project's packet folder):** `research-memo`, `candidate-theses`, `limitations-and-confounds`, `recommended-charts`, `evidence-ledger` (generated), `TODO`, `tables/`, `scripts/`. **Human checkpoint:** the human picks the thesis and rules on every deferred item. Stop at the memo; do not draft publication prose or draw final charts. **Hand-off:** `benchmark:narrative-guideline` once the human has decided.

The point is that a reader can re-derive every number and cannot be misled by a flattering aggregate. Analyse as a neutral third party would (`benchmark:workflow`, "Objectivity comes first"): the same rules for every system, the author's own product included, and every result reported wherever it points. Work in this order; each step protects the next.

## 0. Intake and reading

Fill the study intake with the human first; blanks are asked, not guessed. Read the sources in the intake's order. Treat a prior version's report as context only, never as a template: copying its structure quietly imports its thesis. The packet is internal; anything that later goes public cites only public sources.

## 1. Provenance first

Verify the authoritative archive against its published checksums, then extract it outside the packet folder into a scratch directory. Verify per-file hashes. Audit parent/child lineage (forks, resumes, re-runs): extract the parent only to audit lineage, and never mix partial parent results into the final data. Record which run set is authoritative as a claim. Why: one stale row from a superseded run silently changes a headline.

## 2. Validate the scorer before analysing

Re-implement or port the harness scorer independently from its documented semantics, then reproduce every recorded per-candidate decision and every recorded aggregate exactly. Zero mismatches is the gate. Why: all later numbers inherit its errors, and a port that cannot reproduce recorded scores has a bug in either the port or your understanding. Template: `scripts/scorer_port.py` and `scripts/s01_validate_scorer.py`. In the skeleton `common.load_runs()` derives every hit from the port and aborts if it disagrees with the recorded decision, so no later step can use unvalidated hits.

## 3. Build a deterministic pipeline

Use numbered steps (`s00_…`, `s01_…`) and a `run_all.py`: fixed seeds, `PYTHONHASHSEED=0`, deterministic tie-breaking (sort by key, never rely on dict or set order), no bytecode written into the packet folder (run entry points with `python3 -B`), and a `--verify-determinism` run that proves two runs are byte-identical. Steps write only to `tables/`. Skeleton: `scripts/`. Copy it to the project, extend `STEPS`, and keep the claims contract.

## 4. Claims registry and ledger

Analyse the raw per-run records (every run, every candidate decision), not the harness's configuration aggregates; aggregates hide the denominators and the per-unit spread. Every number gets a claim ID with statement, value, numerator, denominator, table, query, caveat and script (`common.Claims`). `ledger.py` generates `evidence-ledger` and `--check` fails when a document cites an ID that does not exist. Never hand-compute a number into prose: add it to the pipeline and cite the ID. Why: hand-typed numbers drift from the data after the next re-run, and reviewers cannot trace them.

## 5. Reporting conventions

Details and wording in `references/reporting-conventions.md`. In short: raw counts beside percentages; define macro versus micro and say which is the headline; Wilson intervals for rates; a cluster bootstrap over the natural unit with cluster count and sizes stated; exact McNemar with mid-p beside it, described as descriptive and unadjusted; never write "significant" or "statistically indistinguishable".

## 6. Questions, exploration, sensitivity and coverage

Evaluate each established question from the intake and report every answer, including the uninteresting ones. Then work through `references/exploration-checklist.md` (coverage, failure modes, complexity, efficiency frontiers, execution-failure signals) and label what it finds as exploratory. Run: a scoring-policy matrix (tolerance sweep, endpoint rules, matching variants, credit policies, type-only), rank stability by Kendall tau, leave-one-unit-out, and macro versus micro. Then coverage: overlap, union ceiling, unique coverage, a failure taxonomy, and consensus clusters of unmatched findings as an adjudication queue (not verdicts), built from every system's unmatched findings, the reference tool's included. Unmatched findings are "outside the reference set", never "false positives" or "hallucinations". See `references/sensitivity-and-coverage.md`. Counterfactual policies are labelled and never become headlines.

## 7. Confounds register

Record every confound next to the numbers it affects (`scripts/s06_confounds.py` flags system pairs that differ in more than one factor). Two systems that differ in more than one factor, for example effort and tool access, are descriptive only. One run per cell means no repeatability claim. Cost is observed known cost; unavailable is not $0. Attribute a result to the complete harness plus configuration, not just the model. Also record corpus facts with explicit counting bases, and reproducibility facts (per-run tool versions, commits, prompt delivery per system), including the gaps.

## 8. Disconfirmation

Each candidate thesis states its falsifier and is actively tested, with the same rigour whichever system it favours; failures go in a disconfirmation log, and a thesis that fails stays in the memo as "not recommended". Generate theses from the evidence, including readings unfavourable to the author's product; if every strong thesis points the same way, say so and record the strongest opposite reading you tested. Then run two independent checks: (a) a verifier subagent that recomputes the top claims from the raw data without reading your scripts; (b) a sceptical review that hunts superlatives ("only", "every", "top N"), mixed metric sets, causal wording and mislabelled claims. Checklist in `references/disconfirmation.md`. Fix findings in the pipeline, not the prose.

## 9. Write the packet from templates

Copy from `assets/` (files end in `-template.md`; drop the suffix when copying) and fill: `research-memo.md` (with a "Terms used" section written for non-statisticians and a dated "Decisions taken" log), `candidate-theses.md` (3 to 6, ranked by evidence strength, novelty, practical importance and caveat severity, each with a falsifier; how a thesis reflects on any system is never a ranking criterion), `limitations-and-confounds.md`, `recommended-charts.md` (spec table plus chart rules), `todo.md` (each item ends with a "For the paper: disclose…" line). The ledger is generated, never edited.

## 10. Stop

Hand the memo and ranked theses to the human with a short list of decisions needed. Do not write publication prose. Charts stay as specs in `recommended-charts`; rendering them is done in `benchmark:review-kit` (draft figures for reviewers) and later in the paper stage. After the decision, invoke `benchmark:narrative-guideline`.

## Using the shipped scripts

Copy this skill's `scripts/` folder into the project's packet folder first and run it from there with `python3 -B`, never from inside the installed plugin. The input files and column names are in `references/data-contract.md` (including the `arm` column and `findings.csv`). The steps are working skeletons, not finished analyses: `s04_sensitivity.py` re-thresholds a score as a stand-in for your real policy variants, `s05_coverage.py` covers overlap, union and unique coverage but leaves the failure taxonomy and the consensus-cluster queue for you to add, and `scorer_port.py` is a toy scorer to replace. Keep the claims contract (`common.Claims`) and the ledger when you extend them.

## Dry-run the pipeline

`python3 scripts/make_synthetic.py <dir>` builds a 3-system, 2-unit, 12-item dataset with a deliberate confound; then `BENCH_DATA=<dir> BENCH_OUT=<packet> python3 -B scripts/run_all.py --verify-determinism`, then write a short markdown file that cites a few claim IDs from `<packet>/evidence-ledger.md` and run `BENCH_OUT=<packet> python3 -B scripts/ledger.py --check <that file>`. Use it to confirm the skeleton works before adapting it.
