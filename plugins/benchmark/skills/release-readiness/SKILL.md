---
name: release-readiness
description: "Get a benchmark study ready for public release: precise provenance and independence statement, bias sensitivity analyses, licence audit of the whole public repository, authors and conflict-of-interest disclosure, public data and code publication, pre-submission checklist, and the post-disclosure protocol. Use when the user says \"before we publish the benchmark\", \"release checklist\", \"provenance of the reference set\", \"is the benchmark independent of the tools\", \"licence audit\", \"third-party licences\", \"publish the data\", \"conflict of interest wording\", \"pre-submission check\", or \"post-disclosure note\". Applies to any benchmark with a public repository or paper. Not for publishing supplementary run archives (use supplementary-runs) or the sensitivity analysis of scoring choices (use empirical-analysis)."
---

# Release readiness

**Inputs:** the narrative guideline, how the corpus and reference set were created (ask for the facts, do not guess), the harness repository, author list. **Outputs:** `provenance-and-independence.md`, bias sensitivity claims in the ledger, licence files in the repo, data release archive, completed pre-submission checklist, optional post-disclosure note. **Human checkpoints:** the human confirms every provenance fact, the root licence, the author list and disclosure wording, and publication. Nothing is published, pushed or merged without approval; licence analysis is not legal advice. **Hand-off:** `benchmark:paper-authorship` (data and code availability, disclosures); `benchmark:narrative-guideline` (required disclosures).

## 1. Provenance and independence statement (`assets/provenance-and-independence.md`)

Write it as facts a reader can check, with the direction of each bias:

- where the units (applications, repos, datasets, documents) came from and under which licences;
- how the reference set was created, including which AI models seeded it, what humans reviewed, and what was curated by hand;
- whether any evaluated system was used during curation or validation, and how;
- prior vendor use of the units (for example a vendor's demo or training corpus);
- for each of the above: which direction it could bias the results (toward the tool used in curation, toward a tool trained or demoed on the units, toward systems similar to the seeding models) and what is not known.

Do not soften it. A precise, slightly uncomfortable statement is worth more than a vague reassuring one.

## 2. Sensitivity analyses for the likely biases

Turn each bias into a pipeline analysis and claim: for example exclude units with prior vendor use and recompute the headline and ranking; exclude items that any evaluated system helped to seed or validate. Report whether the ranking holds. Add it to `limitations-and-confounds` as a dated section.

## 3. Licence audit (whole public repository, not just the current version)

Read `references/licence-audit.md`. In short: inventory every unit and dependency, check local licence files against upstream, put `LICENSE-UPSTREAM` files outside any fingerprinted directories (so fingerprints do not change), add a root `LICENSE`, a `NOTICE` and `THIRD_PARTY_LICENSES`, check git history and other branches for removed content that is still public, and say plainly that this is not legal advice. Confirm the root licence with the owner. `scripts/licence_inventory.py` lists licence files and flags units without one.

## 4. Authors and disclosure

List every author with affiliation. When any author or their employer or funder owns, sells or is paid by a system included in the study, include a conflict-of-interest disclosure in the paper and repository README. Record pre-publication access too: which system owners reviewed results or received findings, when, and what they could and could not change. Every evaluated system's owner is offered the same access on the same terms; where that did not happen, the paper says so (`assets/provenance-and-independence.md` §4a). External-safe sourcing: public text cites only public sources; internal documents are a map of what to say, never a source of facts to quote.

## 5. Data and code publication

Publish an immutable, checksummed archive of the authoritative run data and the supplementary data, a per-file manifest, a README that says how to verify and reproduce the tables, and the pipeline scripts. Run `benchmark:supplementary-runs`'s `secret_scan.py` over the staging directory first. Links in the paper point to tagged or merged locations, not to branches that may move.

## 6. Pre-submission checklist (`assets/pre-submission-checklist.md`)

This is the final gate before anything is public, and it runs twice: once here at stage 6 for the data and repository release, and again after `benchmark:paper-authorship` (stage 7) hands back its pre-publication package. For the paper it does not repeat that package's checks; it confirms they passed (claims check with values and registry stamp, guardrail lint with the paper's rules file, placeholders, links, statements, sign-offs, arXiv bundle) and adds what only this stage owns: the provenance statement matches the paper's method section, licence files are present, the release archive and secret scan are clean, branches are merged, and documents outside the paper (guideline, README) pass `ledger.py --check`.

## 7. Post-disclosure protocol

Disclose to every affected system's owner on the same terms and timeline; the author's own employer gets no head start. When owners get the results and ship fixes: keep the published benchmark frozen, never re-run and report a new score for any system (contamination), and publish a dated post-disclosure note listing which owners were informed and when, what was reported to each, and what each confirmed or fixed. Draft vendor disclosures for the human to send; do not send.
