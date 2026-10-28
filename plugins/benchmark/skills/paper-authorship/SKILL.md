---
name: paper-authorship
description: "Turn a benchmark or empirical study's evidence packet and narrative guideline into a submission-ready paper (LaTeX, figures, claim inventory) plus a pre-publication package: figures first, section-by-section human checkpoints, every number checked against the evidence ledger, repeated independent cross-review rounds, and a scripted guardrail lint. Use whenever the user says \"write the paper\", \"draft the arXiv preprint\", \"turn the evidence packet into a paper\", \"draft the method section\", \"render the paper figures\", \"build the claim inventory\", \"cross-review the draft\", \"lint the paper for forbidden claims\", \"get the paper ready for arXiv\" or \"prepare the sign-off packet for the paper\", even without naming this skill. Any study comparing systems on a curated reference set. Not for producing the evidence (empirical-analysis), choosing the thesis (narrative-guideline), an internal expert review kit before the paper (review-kit), or the data and licence release gate (release-readiness)."
---

# Paper authorship: evidence packet to submission-ready paper

**Inputs** (ask for anything missing rather than guessing):

- a paper brief filled in with the human (`assets/paper-brief-template.md`: purpose and quality bar, prior version, authors, conflict of interest, owners to receive sign-off packets, style, visual system, reading order, template and output);
- the evidence packet from `benchmark:empirical-analysis`: claims registry (`tables/claims.csv`), generated `evidence-ledger`, `tables/`, the chart spec (`recommended-charts`), `limitations-and-confounds`, `todo`, and any supplementary or adjudication results;
- the governing document from `benchmark:narrative-guideline`: thesis, paper structure, per-finding wording guardrails, required disclosures, "claims never to make", applied reviewer rules;
- the provenance, independence, licence and availability text from `benchmark:release-readiness`, if it exists;
- the prior-art guide and the accepted citations and "to our knowledge" statements from `benchmark:literature-review`;
- a prior paper by the same authors, or the ‹venue› template.

**Outputs** (in the project's `paper/` folder): `main.tex` with one file per section, `references.bib`, rendered figures with `figures/manifest.json`, `claim-inventory.md`, `guardrail-rules.txt`, `review-rounds.md`, and `pre-publication-package.md`.

**Human checkpoints** (stop and wait at each): the figure set; each section or agreed group; title, authors, affiliations and conflict-of-interest wording; every placeholder value; every statement about a third party's product; the decision to submit. Nothing is sent, posted, pushed or submitted by this skill; sign-off requests are drafts for the human.

**Hand-off:** `benchmark:release-readiness`, whose pre-submission checklist is the final gate and consumes the pre-publication package (stage 7 hands back to stage 6).

The governing idea: a reader can trace every number in the paper to one ledger row, every figure to one script and one table, and every judgement call to a dated decision, and a reader with no stake in any system would find each system treated the same way. Most of this skill protects those properties while a human reshapes the prose.

**Terms** (as in `benchmark:workflow`): *reference set* = the curated items; *reference tool* = the evaluated system used as the comparison anchor; *unit* = the cluster items belong to.

## Order of work, and why

1. Read the governing documents (§1).
2. Figures, then a checkpoint (§2).
3. Scaffold the LaTeX (§3).
4. Draft section by section with checkpoints (§4), building the claim inventory as you go (§5); lint after every section (§7).
5. Abstract and introduction, once every other section and appendix exists.
6. Cross-review rounds until a round finds nothing new and material (§8); then re-check the abstract and introduction.
7. Pre-publication package (§9), including any post-disclosure re-scan (§10), then hand to release-readiness.

Figures come before prose because the prose describes them; written the other way round, every figure correction becomes a text correction too. The abstract and introduction come last because they summarize wording that only settles after review.

## 1. Read before writing

Fill the paper brief with the human first. Then read in the brief's order: the narrative guideline first (it overrides everything earlier), then the memo, limitations, chart spec, ledger, TODO, the literature-review outputs, and supplementary and adjudication results. Extract: the thesis and order of findings; the headline metric convention (what is primary for which system family, what is never mixed); each finding's strongest allowed verb and required caveat; the required-disclosures list; the "claims never to make" list. The last two become the lint rules (§7). If the guideline and the ledger disagree, the ledger wins for numbers and the guideline for framing; raise it with the human.

## 2. Figures first (checkpoint)

Read `references/figure-rules.md` before rendering anything: it records the corrections review rounds forced, and following it up front avoids most of them.

- One script renders every figure (`assets/figure-script-skeleton.py`; needs matplotlib). Table rows give geometry; every value a figure prints is looked up in the registry, by ID or by the claim's `table` and `query` fields, and recorded in `figures/manifest.json`. A derived value (ratio, difference, per-unit cost) gets a pipeline step and a claim first; the figure script only formats.
- Render to PNG and look at every image yourself. Code that "should" be fine often isn't.
- Propose the figure list mapped to the guideline's sections (body or appendix, one line each), render after agreement, then wait for approval of the rendered set before writing prose. Expect two or three correction rounds; log each correction in `review-rounds.md` so later figures don't repeat it.

## 3. LaTeX from a template

Read `references/latex-layout.md`. Copy `assets/latex/` (or the prior paper), order the section inputs as the guideline's paper structure says, and compile cleanly before drafting. Decide the venue variant now: a double-blind venue needs an anonymized build, which changes how disclosures and links are written.

## 4. Section by section, with checkpoints

Default order, stopping for the human after each section or agreed group: method (defines every term the results use); one results section per finding, in the guideline's order; robustness (short); threats to validity; related work (from the literature-review outputs only: no citation enters `references.bib` unless that review accepted and verified it; grouped by theme, concurrent work engaged by name); future work (the packet's deferred items, so the paper doesn't imply they are closed); conclusion; appendices; data and code availability; statements (`sections/12-statements.tex`). Then the abstract and introduction.

For each section: follow that finding's guardrails, with the same verb strength and caveats for comparable results whichever system produced them; plain language, short declarative sentences, no promotional adjectives; add every number and factual sentence to the inventory as you write it; run both checks (§5, §7); compile; look at the changed pages; present it with a note on anything unsourced, any judgement call, and anything changed elsewhere.

When the human reviews a section: apply the changes, turn each change that could recur into a rule (guideline reviewer-rules table or the review log), sweep earlier sections for the same problem, and record a dated change-log entry. A reviewer's question ("what does this term mean?") usually marks a gap in the text: answer it in the paper, not only in chat.

Statistics: one plain sentence per method; p-values only for comparisons the narrative relies on, described as descriptive; secondary statistics in footnotes; say what each interval represents (resampling of ‹units›, not run-to-run variation).

## 5. Claim inventory

`claim-inventory.md` (from `assets/claim-inventory-template.md`) maps every number and factual sentence to a claim ID, a cited public source, or an author statement with name and date. Fill **Value as stated** with the number exactly as the paper prints it: the check compares it with the registry, so a re-run that changes a value cannot leave stale prose behind. List each ID (no wildcards or ranges: they hide the one that doesn't exist). Never hand-compute a number, even a difference: add it to the pipeline and cite the new ID. Record the counting basis wherever two counts could cover different sets.

```
python3 scripts/check_claims.py --inventory paper/claim-inventory.md --registry ‹packet›/tables/claims.csv \
    --tex paper/sections paper/main.tex --manifest paper/figures/manifest.json --numbers
```

It fails on unknown, wildcard or range IDs (inventory and manifest), claim IDs leaked into the text, values as stated that don't match the registry, a registry that changed since the inventory's `Registry sha256:` stamp, and missing paths. `--numbers` lists numbers in the text with no inventory row; 0–10 are skipped unless `--all-numbers`, so run that once per round, because small hand-computed differences hide there. Claim IDs live in the inventory and in LaTeX comments only.

## 6. When the evidence changes mid-draft

A pipeline re-run (a fix, a new claim, a supplementary arm) changes the registry under the paper. Keep a copy of the previous `claims.csv`, then run `check_claims.py … --diff-registry ‹old claims.csv›`: it lists changed and removed claims, the inventory rows that cite them and the figures that print them. Fix the prose, re-render the listed figures (and get them re-approved if they changed visibly), re-run both checks, then update the stamp (`--print-stamp`). Note the change in the review log.

## 7. Guardrail lint

Read `references/guardrail-lint.md`. Copy `assets/guardrail-rules.txt` to `paper/` and make the guideline its single source: one `forbid` rule per "claim never to make", one `require` rule per required disclosure. Add a `review` rule for the authors' own product name, so every sentence about it gets an even-handedness check against comparable sentences about other systems. Uncomment the design-dependent rules that apply (single run per cell, AI assistance, pre-publication access, post-disclosure note if results were shared with a system owner before publication) and the task-dependent ones (for detection-style studies, "false positive" and "hallucination" for unmatched outputs); leave the rest off, since an LLM-eval paper may measure exactly those.

```
python3 scripts/guardrail_lint.py --rules paper/guardrail-rules.txt --tex paper/sections paper/main.tex paper/prompts/*.txt paper/references.bib
```

Run it after every section and before every review round. Superlatives are listed for manual checking because they were the most frequent source of factual errors. A lint pass is necessary, not sufficient: it catches phrases, not wrong numbers.

## 8. Cross-review loop

The author stops seeing a draft's errors; an independent reviewer that sees the evidence but not the author's reasoning finds them. Follow `references/cross-review-procedure.md`: a fresh read-only reviewer per round (vary the model where possible; a human for the last round if one is available) that also checks even-handedness: wording, caveats, ordering and figure prominence compared across systems; verify every finding against the registry and sources before acting; log each with severity and act, decline or ask-the-human; fix, then re-run the checks and re-read every changed sentence; bring the human only the decisions that are theirs. Stop when a round yields no new verified blocker or should-fix finding, or after about four rounds, when the remainder goes to the human.

## 9. Pre-publication package

Assemble `pre-publication-package.md` from the template:

- **Placeholder inventory:** every unfilled value (for example an archive DOI that only exists at release), where it is, who supplies it and when. Nothing goes out with an open row.
- **Links and citations:** every URL resolves to a merged, default-branch or tagged location; every arXiv ID and DOI matches its bib entry; "to our knowledge" statements re-searched at the checklist walk and again on submission day, because concurrent work can appear days before you submit. When it does, cite it as concurrent work and narrow the claim instead of dropping the citation.
- **Statements:** conflict of interest (also one sentence in the introduction, before the contributions, so a reader meets it before the results), who performed each review or adjudication pass (people or AI agents) and who made the final call, pre-publication access (which system owners reviewed results or received findings, and what they could change), author contributions, funding, use of AI assistance, acknowledgements, ethics where relevant; the venue's anonymization and preprint rules.
- **Sign-offs:** every author approves authors, affiliations and conflict-of-interest wording. The owner of every product the paper characterizes is offered the same packet (`assets/signoff-packet-template.md`) listing every number and sentence about it with its source, on the same timeline; the authors' own employer gets no earlier or wider access. Owners correct facts; they do not change results or wording that applies to every system. If an owner already reviewed an earlier draft, a later round can be the list of high-risk statements that changed since, confirmed by the human, instead of the full packet; offer the same to every owner. Draft only; the human sends it.
- **External-safe sources:** public text cites only public sources; internal notes and chats are a map of what to say, never a source to quote.
- **arXiv bundle:** `scripts/make_arxiv_bundle.py --paper paper/` strips comments, copies `main.bbl`, the figures actually used and `prompts/`, compiles from a clean directory and zips; then `guardrail_lint.py --fail-on-comments` on the unpacked copy. Check the plain-text abstract against the form limit (1,920 characters on arXiv) and write a shorter form version with the same numbers if needed. If arXiv's file manager offers to delete `main.bbl`, keep it: arXiv does not run BibTeX, so without it every citation renders as [?]. Read arXiv's compiled preview (references present, no [?]) before submitting.

## 10. Post-disclosure re-scan

When findings were shared with a system's owner and they shipped changes before publication, follow `references/post-disclosure-rescan.md`: a separate labelled execution and archive, never merged into the main results; an operator prompt from `assets/postfix-rescan-prompt-template.md`; your own verification (checksums, re-scoring against the frozen reference set, detection judged with the paper's own matching rule against each disclosed item's locations); the owner's facts (what was fixed, by when) recorded as author statements; one short paragraph saying what changed and that the main results stay as run.

## Objectivity, tone and title

Write every paper as a neutral third party would; it matters most when an author's employer makes one of the evaluated systems. Report where each system leads and where it trails with the same plainness, the authors' product included; describe every system accurately, neither promoted nor downplayed, never in marketing language; give comparable results the same verbs, caveats and prominence whoever produced them; keep results unfavourable to the authors' product in the main text; show the authors' product explicitly in every comparison, ordered by the same rule as the others. Disclose the relationship in three places (statements, threats and one sentence in the introduction; any role the product played in building the reference set; any prior vendor use of the ‹units›), each with the direction it could bias the results and any sensitivity analysis. If one reference tool stands for a category, say so in threats and name it wherever a number is attached. Titles are a question or a description of what was compared and found, with no slogans, for example "Does ‹factor› Change ‹outcome›? ‹N› ‹systems› on ‹reference set›" or "‹Systems› on ‹reference set›: ‹dimension› and ‹dimension›".

## Working habits that paid off

- Commit every change-set with a dated change-log entry; the trail answers "why does it say that?" a month later.
- When the human corrects a fact, fix it everywhere (paper, inventory, guideline, provenance note), then grep for the old wording.
- Two counts that seem to disagree usually count different sets: name the overlap in the text.
