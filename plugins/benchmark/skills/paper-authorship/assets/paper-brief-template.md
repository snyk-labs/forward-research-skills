# ‹Benchmark name and version› paper: brief

Fill this in with the human before the figures step. It is the paper-specific half of the brief; the method is the rest of this skill. Anything left blank is asked for, not guessed. The narrative guideline still governs framing and wording; this brief only says what the paper is for and how it is produced.

## 1. Purpose and quality bar

- **What the paper is for:** ‹for example a technical research paper for ‹venue›, written for researchers who will check the method›.
- **Quality bar:** a reader with no stake in any evaluated system would trust the method and reach the same conclusions from the same data. Where an author's employer makes an evaluated system, that bar is the reason the paper exists, not a constraint on it.
- **Continuity:** ‹prior version, its citation and link, or "first version"›. If there is a prior version, cite it where relevant and state plainly what this version changes (corpus, reference set, scoring, systems).
- **Downstream uses:** ‹site, blog, social assets›. They are derived from the final paper later (`benchmark:social-packet`); none is produced in this step.

## 2. People

| Field | Value |
|---|---|
| Authors, in order, with affiliations and emails | ‹…› |
| Conflict of interest to declare | ‹employers and the evaluated systems they make, sell or are paid by› |
| Owners of evaluated systems to receive the same sign-off packet | ‹every evaluated system's owner, with contact; or why one cannot be reached› |
| Human approver at each checkpoint | ‹name› |

## 3. Style

- **Register and spelling:** ‹academic; US or UK English›. No marketing language, no stock filler.
- **Brand voice:** applies to downstream blog and social copy, not to the paper's prose.
- **Visual system:** ‹the project's visual system, if any›, applied within `references/figure-rules.md`; readability in print, colour-blind safety and neutral treatment of every system win any conflict.

## 4. Sources, in reading order

1. The narrative guideline (governs everything else).
2. The research memo (findings, "Terms used", decisions taken).
3. Limitations and confounds (everything in it is disclosed).
4. The chart plan.
5. The evidence ledger and claims registry (the only source of numbers).
6. The TODO (deferred work, named as future work).
7. The literature-review outputs: the prior-art guide and the accepted citations and novelty statements (`benchmark:literature-review`).
8. The provenance, independence and licence text (`benchmark:release-readiness`).
9. The LaTeX template and packaging to reuse: ‹prior paper's source, or the venue template›.

Historical documents (candidate theses, earlier briefs) are context only.

## 5. Non-negotiables (copied from the guideline, not restated in new words)

- Headline convention: ‹metric, with k/N beside it, e.g. "‹x›% (‹k› of ‹N›)"›.
- Metric families never mixed: ‹…›.
- Disclosures and errata that must appear: ‹…›.
- Claims never to make: ‹pointer to the guideline section›.
- Internal IDs and question labels never appear in the paper.

## 6. Output

- Paper folder: ‹path›, with `main.tex`, `sections/`, `references.bib`, `figures/`, `prompts/`; it compiles.
- Figure script: ‹path›, producing paper PDFs and any web variants from the pipeline's tables.
- Checkpoints: figures, then each section, then pre-publication; nothing is sent.
