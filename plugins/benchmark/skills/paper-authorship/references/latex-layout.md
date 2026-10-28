# LaTeX layout that held up in review

Start from the authors' prior paper or the ‹venue› template; `assets/latex/` is a generic skeleton with this layout.

## Files

- `main.tex` holds packages, title, authors and metadata, and `\input`s one file per section from `sections/`. Separate files keep review diffs small and let a reviewer be pointed at one section. Order the `\input` lines as the narrative guideline's paper structure says; the skeleton's order is only a default.
- `sections/12-statements.tex` holds the formal statements most venues ask for: conflict of interest, author contributions, use of AI assistance, acknowledgements. State each once there; the bias discussion stays in Threats.
- `references.bib` holds only entries whose metadata was checked against the arXiv abstract page or the publisher record. Keep the verification log in the claim inventory, not in `note` fields, because notes print in the reference list.
- `prompts/` holds the benchmark's own prompts and configuration files, included verbatim with `\lstinputlisting`. If the ledger records a hash of a prompt, the file must hash to it; watch for a trailing newline. Third-party built-in prompts are paraphrased with their version, not reproduced.
- Tables of more than a few rows (corpus, per-unit lookups) are generated from the pipeline's CSVs by a small script, not typed. Check that totals reconcile with the ledger.

## Layout

- Pin floats near first mention (`float` with `[H]`, or `placeins` per section), so a float page never splits a paragraph.
- Wrap code listings so they cannot break across pages.
- Start each appendix on a new page.
- Use `xurl` or `\path` for long paths, and `hyperref` with PDF title metadata.
- Panel letters in captions match the letters printed in the figures.

## Build

- Compile cleanly: no undefined references or citations, no overfull boxes worth seeing.
- Build artefacts (`*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`, `*.out`, `*.blg`, temporary files) are ignored by version control (`assets/latex/.gitignore`). Keep `main.bbl`, because arXiv needs it.
- After every compile that changed a page, render that page to an image and look at it.

## Venue variants

- **arXiv / camera-ready:** the default layout, with authors, statements and repository links.
- **Double-blind review:** a separate build with authors, affiliations, acknowledgements and the conflict-of-interest declaration held back, repository links pointed at an anonymized mirror, and self-citations written in the third person. The conflict-of-interest wording is not deleted, only deferred, so the camera-ready version restores it unchanged. Check the venue's preprint policy before posting the arXiv version during review.
