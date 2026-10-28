---
name: narrative-guideline
description: "Write the single governing narrative document for a benchmark or evaluation write-up after the human has chosen the thesis. Use when the user says \"we picked the thesis\", \"write the narrative guideline\", \"frame the paper\", \"what can we claim\", \"claims never to make\", \"set the wording rules\", \"retire the research questions\", or before drafting any paper, blog, deck or social post from benchmark results. The guideline overrides every other write-up document and records DECIDED choices with dates."
---

# Narrative guideline: one document that governs every write-up

**Inputs:** research memo, ranked candidate theses, limitations and confounds, evidence ledger, the human's thesis decision, any reviewer feedback so far. **Output:** one `narrative-guideline.md` in the packet folder, from `assets/narrative-guideline.md`. Date every update. **Human checkpoint:** the human approves the framing, the headline metric convention, each DECIDED option and the "claims never to make" list before anyone drafts from it. **Hand-off:** `benchmark:literature-review` (targeted pass per finding); `benchmark:supplementary-runs` or `benchmark:adjudication` if the guideline names evidence gaps; `benchmark:review-kit`; `benchmark:release-readiness`; `benchmark:paper-authorship`.

Why one document: when a paper, a deck and a social post are each drafted from the memo, the claims drift apart. A single guideline that overrides everything else makes drift a bug with an owner. The guideline's job is to make the wording match the evidence, not to make the evidence persuasive: it governs how strongly each result may be stated, for every system alike.

## Steps

1. **Record the decision.** Name the chosen thesis (lead plus supporting findings) and what was left out and why. If the human chose a thesis ranked below another in `candidate-theses`, record the reason; how a thesis reflects on any system is not a valid one. If the findings cut across the pre-planned research questions, retire the RQ language honestly: say the data did not follow the plan, and mark the old theses document historical with a pointer here.
2. **Frame.** State the question the work answers, a one-sentence answer, and the headline metric convention (which aggregation, which registered metric, what is never mixed).
3. **One section per finding.** For each: the claim IDs it rests on, wording guardrails (strongest allowed verb, required caveat), and the figures that carry it. The guardrails apply to every system the finding mentions: comparable results get the same verb and the same caveat whoever produced them. A finding is a section; a number outside a section's claim IDs is a bug.
4. **Robustness, short.** One section, not a second paper. Point to the sensitivity claims; say what held and what did not.
5. **Required disclosures.** Everything from limitations that a reader needs to interpret the numbers: confounds, single runs, reference-set defects with their impact, version-recording gaps, independence and conflict of interest (see `benchmark:release-readiness`), asymmetries in treatment or pre-publication access, use of AI assistance where the venue asks for it. Paper-authorship turns each item into a lint `require` rule, so write them as a list.
6. **Future work.** Name the open items the packet deferred, so the paper does not imply they are closed.
7. **Claims never to make.** An explicit list: superlatives the data cannot support, causal statements blocked by a confound, rankings across unlike metrics, "significant", repeatability, hallucination language for unmatched findings (in detection-style studies), vendor-internal attributions awaiting confirmation, and wording that states comparable results more strongly or more weakly depending on which system produced them.
8. **Paper structure and appendix specs.** Section list; appendix A corpus (counting bases), appendix B configurations, versions and prompts, data and code availability, and the rules applied from reviewer feedback.
9. **Mark and date.** Every choice the human made is `DECIDED (‹date›): option ‹x›`. Every later change adds a dated line; never silently rewrite a decided item.

## Wording rules to put in the guideline

Read `references/wording-lessons.md` and copy the relevant ones. The load-bearing ones:

- "consistent with" until a control supports a claim; then "supported by a ‹control› (single run)".
- Label exploratory analyses as exploratory.
- Never merge supplementary arms into the headline; keep them in their own labelled section.
- Do not conflate model tier with effort or with harness configuration.
- Structural explanations (a property of a category of problem) can go in now. Vendor-internal attributions wait for the vendor's confirmation.
- Unmatched findings are "outside the reference set" until adjudicated.

## Objectivity and tone

For every study: write as a neutral third party would. Every system, the author's own product included, is described accurately and neither promoted nor downplayed: its strengths and its weaknesses in the same plain words, with the same caveats, and other systems' strengths stated as plainly as their weaknesses. Results unfavourable to the author's product are reported where they belong, not moved to an appendix or a footnote. No marketing language and no superlatives about any system. When the author's employer makes an evaluated system, the conflict of interest is disclosed up front. Titles are questions or plain descriptions, no slogans.

## Do not

Do not introduce a number the ledger does not hold; add it to the pipeline first. Do not leave a section as a template placeholder; delete empty sections.
