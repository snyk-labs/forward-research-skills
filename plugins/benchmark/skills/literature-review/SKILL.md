---
name: literature-review
description: "Run the literature review for a benchmark or empirical study: a prior-art guide written before the results (anchor set, novelty threats, predictions from prior work), a targeted pass per finding after the thesis is chosen, a verification pass that clears every unchecked citation, a proposal the human approves before anything enters the paper plan, and a re-check of novelty claims at submission. Use whenever the user says \"literature review\", \"related work\", \"prior art\", \"is this novel\", \"what has been published on this\", \"find papers that support or contradict\", \"check our citations\", \"verify the references\", \"concurrent work\", \"to our knowledge\", or before drafting a related-work section. Any study comparing systems on a curated reference set. Not for writing the related-work prose itself (paper-authorship) or for choosing the thesis (narrative-guideline)."
---

# Literature review: prior art, verified, approved before use

**Inputs:** the study's questions or thesis context; once chosen, the narrative guideline (its findings and sections); the current prior-art guide and bibliography, if any; the list of citation IDs already held (the exclusion list). **Outputs** (in the project folder): `prior-art-guide.md` (living), one raw report per search pass in a dated `lit-review-‹date›/` folder, `lit-review-proposal-‹date›.md`, and the guide's "accepted additions" section after approval. **Human checkpoint:** nothing new enters the guideline, the paper plan or the bibliography until the human approves what it is, why it is cited and in what scope; corrections to existing citations are proposed too. **Hand-off:** `benchmark:empirical-analysis` (novelty scores for candidate theses; method notes that become pipeline claims), `benchmark:narrative-guideline` (claims the literature constrains), `benchmark:paper-authorship` (accepted citations, verification log, "to our knowledge" statements).

Why it exists: a benchmark paper is judged against work the authors may not have read. A citation that says something the cited paper does not, or a novelty claim someone else already made, costs more credibility than the whole related-work section earns. And the review is where a study most easily drifts into collecting only the papers that agree with it.

## Objectivity in the review

The plugin's rules (`benchmark:workflow`, "Objectivity comes first") apply here as follows:

- Search for counter-evidence as hard as for support. Every candidate gets a relation label (agrees / extends / differs / threat), and a threat that constrains a claim is top priority, never left out.
- When a paper weakens a claim, narrow the claim; don't drop the paper.
- Cite work by the vendors of the evaluated systems, competitors and the authors' own organisation on the same terms. Record each cited paper's affiliation with any evaluated system, the authors' own employer included, and keep self-citations to what the paper needs.
- A paper evaluating its authors' own system gets that caveat beside every number taken from it.

## Pass 1: prior-art guide, before the results (`assets/prior-art-guide-template.md`)

Write it while the runs execute, or before. It holds:

- the anchor set (the study's own lineage);
- a novelty threat board: the few papers close enough that a reviewer will read the study against them;
- an annotated bibliography against the study's questions;
- the methodology a reviewer attacks first, with the citation for each practice adopted;
- the claims the study must not make unqualified;
- dated predictions that prior work implies for this study's outcome.

Predictions written after the data are not predictions; the paper later says which were confirmed and which contradicted.

## Pass 2: targeted review after the thesis (`references/search-passes.md`)

1. **Plan the passes.** One search pass per finding or paper section in the guideline, plus one verification pass that clears every entry not yet verified. Give each pass the exclusion list (`scripts/extract_ids.py` builds it from the guide and bib), its section's claims, and the instruction to look for contradicting work too.
2. **Run them in parallel** as subagents with web access. Each writes a raw report from `assets/search-report-template.md`: ranked candidates with full citation, what the paper shows, which claim it touches, relation label, affiliation, verification tier; then the candidates considered and rejected, with reasons, and the gaps found (possible novelty).
3. **Verify before proposing.** Apply the tiers and hard rules in `references/verification-and-hygiene.md`. A number from a search snippet or an unopened page never reaches the proposal as a fact.
4. **Consolidate into one proposal** (`assets/proposal-template.md`):
   - A: corrections to citations already held (wrong title, inverted finding, figure out of scope);
   - B: promotions of listed but unread papers;
   - C: new citations by section, each with priority (P1 a sentence or more, P2 grouped mention, P3 optional) and relation;
   - D: novelty claims the search supports, phrased "to our knowledge";
   - E: method notes that change the analysis (approved separately; they become pipeline claims, never prose numbers);
   - F: research-community outreach (drafted only after the paper is final);
   - decisions needed, each with a recommendation.
5. **Stop for the human.** Apply only what was approved: corrections inline, accepted additions to the guide's "accepted additions" section by paper section, method notes through `benchmark:empirical-analysis`. Mark the proposal DECIDED with the date and what was dropped.

## Pass 3: at submission

- Re-search every "to our knowledge" statement and narrow it if needed.
- Re-open the abstract page of every preprint cited, for new versions.
- Check whether concurrent work has appeared since the last pass.
- Log anything found after the review date in the guide's "later additions" section, with its tier, and propose it the same way.

## Do not

Do not add a citation to the bibliography from a search summary. Do not attribute a finding to a paper beyond what its abstract (or full text, if read, and say which) states. Do not send outreach; draft it after the paper is final, and offer concurrent-work authors the same courtesy note whatever their affiliation.
