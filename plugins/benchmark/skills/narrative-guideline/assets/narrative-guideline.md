# ‹Benchmark name›: narrative guideline

> Governing document. It overrides `research-memo`, `candidate-theses` (now historical) and every earlier draft. Last updated ‹YYYY-MM-DD›. Every number cites a claim ID in `evidence-ledger`.

## 1. The decision

- **DECIDED (‹date›), thesis:** ‹lead finding› with ‹supporting findings›. Option chosen: ‹T-n›. Options not taken: ‹list, why›.
- **Research-question framing:** ‹retired / kept›. ‹If retired: one honest sentence on why, and the old document is marked historical.›

## 2. Framing for the whole paper

- **The question:** ‹…›
- **One-sentence answer:** ‹…›
- **Headline metric convention:** ‹macro or micro, registered metric per system family, what is never mixed›.
- **Objectivity and tone:** ‹written as a neutral third party would; every system, the authors' product included, described accurately, neither promoted nor downplayed; comparable results get the same wording and caveats whoever produced them; results unfavourable to the authors' product stay in the main text; no marketing language; title is a question or description›.

### Paper structure

1. ‹Introduction› 2. ‹Related work› 3. ‹Benchmark and method› 4. ‹Finding 1› 5. ‹Finding 2› 6. ‹Finding 3› 7. ‹Robustness› 8. ‹Threats to validity and disclosures› 9. ‹Future work› 10. ‹Conclusion›. Appendices A to ‹n› below.

## 3. Finding 1 — ‹title›

- **Claim IDs:** ‹…›
- **Wording guardrails:** strongest verb ‹…›; required caveat ‹…›.
- **Figures:** ‹figure ids from `recommended-charts`›.
- **Sub-points:** ‹each with its claim IDs›.

## 4. Finding 2 — ‹title› (same shape)

## 5. Finding 3 — ‹title› (same shape)

## 6. Robustness (short)

What held under the sensitivity suite and what did not: ‹claim IDs›. Exploratory analyses are labelled exploratory.

## 7. Required disclosures

One item per line; paper-authorship turns each into a lint `require` rule.

- Confounds (‹list›)
- Runs per cell (‹single run, or the number of repetitions›)
- Reference-set defects and their impact
- Version-recording gaps
- Independence and conflict of interest (‹link to release-readiness statement›)
- Asymmetries in treatment or pre-publication access (‹who reviewed results or received findings before publication; anything configured or tuned for one system only›)
- Supplementary arms (‹labelled, not in headline›)
- Adjudication scope
- Use of AI assistance (‹if the venue asks›)
- Post-disclosure note (‹if results were shared with a system owner before publication›)

## 8. Future work to name

‹Items deferred in `TODO`, so the paper does not imply they are closed.›

## 9. Claims never to make

- ‹Superlative the data cannot support›
- ‹Causal statement blocked by confound›
- ‹Ranking across unlike metrics›
- "Significant" or "statistically indistinguishable"
- Repeatability or run-to-run variance
- "False positives" or "hallucinations" for unmatched findings (detection-style studies)
- Vendor-internal attributions before confirmation
- Wording that states comparable results more strongly or more weakly depending on which system produced them
- ‹Anything the human added›

## 10. Appendix A — corpus and dataset

Counting bases stated explicitly (after de-duplication, per unit, per category). ‹Table›.

## 11. Appendix B — configurations, versions and prompts

Per system: harness and version, model, effort, tool access, prompt delivery, run date, commit. Gaps stated.

## 12. Data and code availability

‹Public archive, checksum, repository, licence, how to reproduce the tables›. Links resolve before submission.

## 13. Reviewer feedback — rules applied

| Date | From | Rule now applied | Where |
|---|---|---|---|

## Change log

- ‹date›: ‹what changed and why›.
