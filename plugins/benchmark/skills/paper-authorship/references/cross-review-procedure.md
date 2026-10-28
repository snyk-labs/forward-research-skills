# Cross-review procedure

The author of a draft stops seeing its errors. An independent reviewer that sees the evidence but not the author's reasoning finds them. A first round on a full draft typically finds many issues, some of which would be factually wrong in print. This is the repeatable procedure.

## When to run a round

- After the full draft exists: all sections, figures and appendices.
- After any large change: a new section, a re-run of the pipeline, a rewrite after human review.
- Before the pre-publication package is assembled.
- Repeat until the stop rule in Step 7 is met.

## Severities

- **Blocker:** a factual error, an untraceable number, a missing required disclosure, or a claim the guideline forbids. It would mislead a reader or a reviewer would reject on it.
- **Should-fix:** an overstatement, an inconsistency between sections, a gap a sceptical reviewer would attack, unclear method text. A reader is not misled but trust drops.
- **Nit:** wording, spelling, layout.

"Material" means blocker or should-fix.

## Step 1: prepare the reviewer's inputs

Give the reviewer:

- the paper source (`main.tex`, `sections/`, `references.bib`) and the rendered text (`pdftotext -layout main.pdf`);
- the claims registry and the generated ledger;
- the claim inventory;
- the narrative guideline (framing, disclosures, claims never to make, reviewer rules);
- the limitations and confounds document;
- figure PNG previews.

Do not give it:

- your conclusions, your list of known issues, or the reasons behind your wording choices;
- chat history.

Why: you want it to re-derive, not to agree. A reviewer that knows what you think checks your reasoning rather than the evidence. The guideline states the thesis, which the reviewer needs for the guardrails, so tell it explicitly to test whether the evidence supports the thesis rather than assume it. Where possible use a different model from the one that drafted the paper, and a named human for the last round: reviewers that share the author's model share some of its blind spots.

Tell it which documents are superseded on which points (for example "the limitations file's section on X is out of date: the defect is now fixed in the harness, results still use the frozen set"), so it doesn't report stale contradictions.

## Step 2: the reviewer prompt

Adapt this:

> You are a sceptical expert reviewer (‹domain› + evaluation methodology) doing a pre-submission review. Read-only: do not edit any file. Return a prioritized list of concrete issues.
> Check, in priority order:
> 1. NUMBERS: every number in body, captions, abstract and appendices matches the registry or a named table; flag mismatches, untraceable numbers, and the same quantity stated differently in two places.
> 2. THESIS AND GUARDRAILS: does the evidence support the thesis as the paper states it (do not assume it does)? The guideline's "claims never to make" and required disclosures (list them).
> 3. CITATIONS: any statement about a cited work that goes beyond its abstract (fetch the abstract pages); malformed or uncited bib entries; overreaching novelty claims.
> 4. EVEN-HANDEDNESS: compare how the paper treats each system, especially any system made by an author's employer: verb strength and hedging for comparable results, which caveats are attached to whom, where favourable and unfavourable results appear (main text or appendix), figure ordering and emphasis, and whether any system's owner had access the others did not. Quote the asymmetric pairs.
> 5. METHODOLOGY a sceptical reviewer would attack, where the paper does not already answer it; say which section should.
> 6. CLARITY AND CONSISTENCY: undefined terms, inconsistent names, wrong cross-references, captions that don't match figures, non-‹spelling variant› spelling, promotional wording.
> For each item give: location, short quote, why it is a problem, a concrete fix, and BLOCKER / SHOULD-FIX / NIT. Do not report things that are fine. Be terse.

Run it as a background subagent and wait for the result. Don't predict or summarize it before it arrives.

## Step 3: verify before acting

Reviewers are often right and sometimes confidently wrong. For each item:

- re-read the cited sentence in the current source;
- check the claim against the registry row itself, including its caveat and query columns, not only the value column;
- check the cited work's abstract yourself;
- decide: **act** (and what the fix is), **decline** (and why: for example "the value is in the claim's caveat column"), or **ask the human** (when the fix depends on a fact only they know, or on a judgement that is theirs).

## Step 4: log the round

Use `assets/review-round-log-template.md`. One row per finding: ID, severity, location, issue, decision, fix or reason, and whether it was re-verified. Then add a short summary: counts by severity, what was acted on, what was declined, and what went to the human.

## Step 5: fix, then recheck

- If a fix needs a number that doesn't exist yet, add a pipeline claim and re-run the ledger (then follow the SKILL's "When the evidence changes mid-draft" steps). Never hand-compute.
- After all fixes:
  - re-run `check_claims.py` and `guardrail_lint.py`;
  - recompile;
  - re-extract the text;
  - re-read every changed sentence in context.
- Grep for the old wording. A fact stated in three places is usually fixed in one.
- Check that fixes didn't create new errors. Typical ones:
  - a new number without a claim;
  - a softened sentence that now contradicts a figure;
  - a renamed term used in the old form elsewhere;
  - an overfull line from a longer sentence.
- Update the guideline if a fix changes a rule it states. Otherwise the next draft repeats the error.

## Step 6: bring the human the decisions

List only what needs them, with your recommendation. Examples:

- whether curators could see one system's output;
- whether a branch is merged;
- whether to keep a title;
- whether to publish a supporting document or state its content in the paper.

Record their answer in the log and in the relevant document.

## Step 7: repeat

Start a new round with a fresh reviewer, same inputs, updated files. A fresh reviewer has not seen the log, so it will re-raise some items you already declined: match each finding against the log first, and count only findings that are new and survive verification.

Stop when a round yields no new verified blocker or should-fix finding. If round four still yields some, stop the loop anyway and take the remaining findings, with your recommendation for each, to the human: by then the reviewer and the author are usually arguing about judgement calls that are the human's to make.

## Error classes to check for

| Class | Example (generic) | Check |
|---|---|---|
| Superlatives | "the only model that improved" when a control run also improved | Every "only", "every", "all", "never", "first", "top N", "best": recompute against every set the sentence could cover, including supplementary runs |
| Mixed metric sets | "the best of all ‹N› systems" when two of them are scored with a different metric | Name the set behind every count; state "of the ‹M› systems scored with ‹metric›" |
| Causal or mechanism wording without a control | "the gain came from the larger context window" from two single runs | Replace with "is consistent with"; state the design limit; keep causal verbs only where a control isolates the factor |
| Count drift between sections | 12 in the abstract, 10 in the results | Grep every number that appears more than once; one claim ID per quantity |
| Mislabelled claims | a rate attributed to one model that the registry computes over a whole model family | Read the claim's statement and query, not only its value |
| Absolute claims a qualifier would fix | "no system answered these questions" when one did and was credited under another item | Look for the edge cases the registry records in caveats and notes |
| Figure–text mismatches | the caption describes three panels and the figure has four | After any figure change, re-read its caption and every "Figure n(X)" reference |
| Disclosures stated inconsistently | the number of annotators given as three in one section and "a small team" in another | Grep each disclosure's key terms; state each once in full, refer to it elsewhere |
| Citation overreach | a sentence credits a paper with a finding its abstract doesn't state | Fetch the abstract; restate only what it says |
| Jargon that implies more than happened | "registered rule" when nothing was pre-registered | Plain wording; lint rule |
| Missing required disclosure | a control run's cost and the units it skipped absent from the method | Check the guideline's disclosure list item by item |
| Generalization beyond the sample | "open-weight models" when one was tested | Name the system where a number is attached; add a threats sentence |
| Selection bias in a qualitative filter | a consensus filter that favours the family with more configurations | Disclose it where the counts appear; soften comparative wording |
| Asymmetric framing | the authors' product "detects" while another system "appears to detect" the same kind of item; the authors' product's losses explained at length, others' not | Read every sentence about the authors' product beside the comparable sentence about another system; same verb, same caveat, same placement |
| Asymmetric access | one system's owner reviewed the draft or received findings early and the others did not | Offer the others the same, or disclose it in statements and threats |
| Possible execution failures reported as model behaviour | a configuration whose runs mostly ended after a few turns with empty output | Report run-level signals (turns, exports); say what was and wasn't ruled out |
