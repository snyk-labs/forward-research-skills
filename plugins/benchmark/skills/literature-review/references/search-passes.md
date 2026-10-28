# Running the search passes

## Plan

- One pass per finding or paper section in the narrative guideline, plus one verification pass over the queue. Passes are independent, so run them in parallel.
- Build the exclusion list first (`python3 scripts/extract_ids.py prior-art-guide.md paper/references.bib > existing_ids.txt`) so passes don't re-report what is already held.
- Give each pass only what it needs: its section's claims in plain words (no internal claim IDs), the exclusion list, the search scope, and the report template. Don't give it the authors' preferred answer.

## Brief for one search pass (adapt)

> You are doing a targeted literature search for the ‹section› of a paper on ‹study in one sentence›. The section claims: ‹2–4 plain-language claims›. Search arXiv and the main venues of ‹fields› from ‹year› to today, plus anything older that the field treats as foundational.
> Find work that supports, extends, differs from, or threatens these claims. Look as hard for contradicting work as for supporting work, and for concurrent work on the same question.
> Skip everything in the attached exclusion list.
> For each candidate: full citation with identifier; what it shows, with its scope; which claim it touches; relation (agrees / extends / differs / threat); affiliation, including any tie to ‹the evaluated systems›; verification tier (open the abstract page before calling anything VERIFIED; never report a number from a snippet as verified). Rank candidates by how much a reviewer would expect to see them.
> Also report: candidates you considered and rejected, and why; gaps where you found nothing (possible novelty, phrased cautiously).
> Read-only research: do not edit any file except your report. Write the report from the attached template.

## Brief for the verification pass

> For each entry in this queue, open the source (arXiv abstract or HTML, publisher record, DOI resolver) and confirm the title, authors, year, venue, and the specific claim or number listed. Report per item: confirmed / corrected (with the fix) / downgraded (cite for less, and what) / dropped (and why), with the page you checked. Flag any title you cannot find anywhere as possibly non-existent.

## After the passes

- Read every raw report; don't summarise one you haven't read.
- Spot-verify the top candidates yourself before they enter the proposal, especially every number and every "threat".
- Merge duplicates across passes; keep the strongest scope statement.
- A pass that found nothing for a claim is a result: it supports a cautious "to our knowledge", re-searched at submission.
