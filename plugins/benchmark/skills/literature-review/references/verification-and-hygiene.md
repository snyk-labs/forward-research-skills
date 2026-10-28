# Verification tiers and citation hygiene

## Tiers (every entry carries one)

- **VERIFIED:** the arXiv abstract page, its HTML full text, or the publisher's record was opened, and the title, authors, year and the cited claim were read there. Say which page, and whether the full text was read.
- **VERIFIED (index):** only the identifier-to-title pairing was confirmed (arXiv listing, publisher index, DOI resolver). The ID can be quoted; numbers from the paper cannot until it is opened.
- **UNVERIFIED:** the paper appears in a search result or a model's summary and nothing was confirmed against the source. It does not enter the bibliography, and it goes on the verification queue.

## Hard rules

1. **No number from an UNVERIFIED or index-only entry, and no number from a search snippet, goes into the paper.** Snippets misquote, mix versions and attach figures to the wrong paper.
2. **Quote a finding with its scope.** If the paper found an effect in 3 of 12 tests, in one language, on two small models, say so or don't cite it for that point. If a figure is a narrow bar (an acceptance threshold, a subset), quote it as that, not as a general rate.
3. **Check the direction.** A paper is sometimes cited for the consensus it overturns. Read the abstract's conclusion, not only its framing sentence.
4. **Phantom citations exist.** Models produce plausible titles with real authors' names. If a title cannot be found on the venue or arXiv, record it as non-existent in the guide, with the real work it was probably confused with, so it is not re-added later.
5. **Record canonical identifiers** (DOI, arXiv ID, venue and year) once, in the guide's verification log, and copy them into the bibliography from there.
6. **Affiliations are facts to check.** Abstract pages often omit them; confirm from the PDF or the authors' pages before writing "independent" or naming a lab, and record any tie to an evaluated system.
7. **Preprints change.** Record the version read; re-check at submission.

## What a statement about a cited work may say

Only what its abstract says, or its full text if it was read (and the guide says so). "Consistent with [x]" is fine when the result points the same way; "as [x] showed" needs the cited result to be the same claim, on a comparable setting.

## The verification queue

A section in the prior-art guide listing every entry not yet VERIFIED, with what needs checking (title, authors, a specific number, an affiliation). A verification pass clears it item by item and records the outcome: confirmed, corrected (with the fix), downgraded (cite for less), or dropped (with why). The queue is empty before submission.
