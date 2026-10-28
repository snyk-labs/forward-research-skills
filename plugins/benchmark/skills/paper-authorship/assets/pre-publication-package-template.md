# ‹Benchmark name› paper: pre-publication package

Input to `benchmark:release-readiness`, whose pre-submission checklist is the final gate and points at the sections below rather than repeating them. Nothing here is sent; sign-off requests are drafts for the human.

## 1. Placeholder inventory

| Placeholder | Location | What fills it | Who supplies it | Expected |
|---|---|---|---|---|

The paper does not go out with an open row.

## 2. Links, identifiers and citations

- [ ] Every URL resolves from a logged-out browser and points at a default-branch, merged or tagged location (not a working branch).
- [ ] Every arXiv ID and DOI matches the title and authors in `references.bib`; preprint versions re-checked on ‹date›.
- [ ] Every statement about a cited work matches its abstract (inventory "Citations" table).
- [ ] "To our knowledge" statements re-searched on ‹date› (checklist walk) and again on submission day ‹date›; concurrent work cited, claims narrowed where needed.
- [ ] Repository paths named in the paper exist on the default branch.

## 3. Statements

- [ ] Conflict of interest: each author's employer and its relationship to every evaluated system; funding.
- [ ] Pre-publication access: which system owners were offered and took a review or received findings, when, on what terms; the same offer went to every evaluated system's owner, or the asymmetry is stated.
- [ ] Who performed each review or adjudication pass (people or AI agents, which), and who made the final call.
- [ ] Conflict of interest also stated in one sentence in the introduction.
- [ ] Any threshold said to be fixed before analysis: what had already been seen at that point.
- [ ] Author contributions.
- [ ] Use of AI assistance: which tools, for what (analysis code, drafting, review rounds), and that the authors checked every statement and number.
- [ ] Acknowledgements, with permission from the people named.
- [ ] Ethics or responsible-disclosure statement, where the venue or the study needs one.

## 4. Sign-offs

- [ ] Each author: author list, order, affiliations, emails, conflict-of-interest wording.
- [ ] Owner of every product the paper characterizes: the same packet from `signoff-packet-template.md`, on the same timeline (draft; the human sends it). Owners correct facts; corrections that change how a system is treated are applied to every comparable system or declined.
- [ ] Any person quoted or credited.

## 5. External-safe source check

- [ ] Every number and fact traces to the public paper, the public repository or a public citation.
- [ ] No internal documents, chats, codenames, unreleased product details, customer names or financials.
- [ ] Facts supplied by authors are stated as the study's own description (method), not as quotes from internal material.

## 6. Guardrails and claims

- [ ] `check_claims.py` passes with `--manifest`, every "Value as stated" filled, and the registry stamp current; `--numbers` and one `--all-numbers` report triaged.
- [ ] `guardrail_lint.py` with the paper's rules file (built from the guideline) has no blocking hits; review hits checked.
- [ ] Last cross-review round met the stop rule (no new verified blocker or should-fix), or the remaining findings were decided by the human.
- [ ] Required disclosures present and stated consistently (each grepped).
- [ ] Even-handedness: every sentence about the authors' product read beside the comparable sentence about another system (same verb, caveat, placement); results unfavourable to the authors' product are in the main text; figure order follows the stated rule.
- [ ] Figures regenerated from the final registry; manifest current; alt text written.

## 7. Post-disclosure (only if findings were shared with a system owner)

- [ ] Re-scan run as a separate labelled execution and archive, published on a branch and merged before the paper cites it (`references/post-disclosure-rescan.md`).
- [ ] Archive verified and re-scored against the frozen reference set; per-item detection judged with the paper's rule; claims registered.
- [ ] Owner's facts (fixes shipped, by when) recorded as author statements with a date.
- [ ] Paragraph says what changed and that the main results stay as run.

## 8. Venue

- [ ] Venue rules checked: page limit, template, anonymization, preprint policy, artifact or data requirements.
- [ ] Double-blind: anonymized build (authors, affiliations, acknowledgements and conflict-of-interest declaration held back for camera-ready; repository links to an anonymized mirror; self-citations in the third person). The camera-ready version restores the held-back text unchanged.

## 9. arXiv bundle

- [ ] `scripts/make_arxiv_bundle.py --paper paper/` (comments stripped, used figures only, clean compile, zip), then `guardrail_lint.py --tex ‹unpacked copy› --fail-on-comments` passes.
- [ ] Include `main.bbl`, every figure actually used, `prompts/`; exclude build files, unused figures, scratch and temporary files.
- [ ] Compile the bundle from scratch; zero undefined references; read the PDF once more.
- [ ] Metadata: title, authors, abstract (plain text, within the form limit: 1,920 characters on arXiv; write a shorter form version with the same numbers if needed), categories, licence, comments field.
- [ ] On upload, keep `main.bbl` even if the file manager suggests deleting it; check the compiled preview shows the references and no [?].
