# Guardrail lint

A scripted pass that catches wording the study's narrative guideline forbids and checks that required disclosures are present. It runs in seconds, so run it after every section and before every review round.

## One source for the rules

The narrative guideline is the single source. Build `paper/guardrail-rules.txt` from it:

- one `forbid` rule per item in its "claims never to make" list;
- one `require` rule per item in its "Required disclosures" list;
- the generic defaults in `assets/guardrail-rules.txt` (statistical overreach, design-honesty wording, marketing language, superlatives, placeholders, the disclosures nearly every paper needs);
- the commented design-dependent and task-dependent rules that apply to this study, uncommented. Delete the rest.

When the guideline's lists change, change the rules file the same day. `benchmark:release-readiness` checks the paper by running this same rules file, so there is one banned-phrase list, not two.

## What it checks

1. **Forbidden phrases** (`forbid`; block, review or nit by rule). Defaults: claims of statistical significance (bare "significant" is a review hit, the statistical phrases block), "statistically indistinguishable", "proves", "pre-registered" or "registered rule" unless literally true, causal verbs (review), marketing language, stock filler (nit).
2. **Task-dependent wording** (off by default). For detection-style studies where an unmatched output is not proven wrong: "false positive", "hallucination", "miss rate", repeatability words for single-run systems. An LLM-eval study that measures hallucination rates leaves these off.
3. **Superlatives** (review): "only", "every", "all", "never", "first", "best", "top N", "unique". Often correct, but they were the most frequent source of factual errors, so each hit is checked against every set the sentence could cover, including supplementary runs.
4. **Placeholders** (block): `‹…›`, `[date]`, `[k]`, `TODO`, `TBD`, `FIXME`, `XXX`, `??`. Pass `prompts/*.txt` and `references.bib` to `--tex` as well: in non-LaTeX files only placeholder rules run, and angle-bracket tokens such as `<date>` are listed for review, because a benchmark prompt may contain them on purpose.
5. **Internal ID leakage** (block): claim IDs in the paper's text. They may sit in LaTeX comments while drafting; comments are stripped from the arXiv bundle.
6. **Required disclosures** (`require`): each pattern must match somewhere outside a section heading, so a heading such as "Data and code availability" does not count as the statement itself. Defaults: conflict of interest, reference-set provenance, data and code availability, licence terms. Design-dependent (uncomment per the guideline): single run per cell, independence of curation, confounds, known reference-set defects, version-recording gaps, supplementary runs kept separate, adjudication scope, AI assistance, post-disclosure note.
7. **Spelling variant** (nit): the other variant's spellings for the paper's chosen English.

## Rules file format

One rule per line, `#` comments allowed. Fields are separated by ` | ` with spaces on both sides, so a bare `|` inside the regex is alternation:

```
<severity> | <kind> | <regex> | <reason>
```

- `severity`: `block`, `review` or `nit`.
- `kind`: `forbid` (must not appear), `require` (must appear at least once), `superlative` (listed for review), `placeholder`.
- `regex`: Python syntax, case-insensitive; use `\b` word boundaries. An invalid regex stops the lint with the line number.

## How text is matched

LaTeX comments are removed first (a `%` after an odd number of backslashes is a literal percent sign, so `50\%` stays text and `\\% note` is a comment). Then the lines of each paragraph are joined with spaces, so a phrase or a disclosure that wraps across source lines still matches, and hits are reported at the line where they start.

Markdown files passed explicitly (a README, release notes, a blog draft) get every rule except `require`, so the same rules file guards public text outside the paper. Other non-LaTeX files (prompts, `.bib`) get placeholder checks only.

## How to run

```
python3 scripts/guardrail_lint.py --rules paper/guardrail-rules.txt --tex paper/sections paper/main.tex paper/prompts/*.txt paper/references.bib
python3 scripts/guardrail_lint.py --rules paper/guardrail-rules.txt --tex arxiv-bundle/ --fail-on-comments
```

Exit code 1 if any `block` rule fires, a required disclosure is missing, a path does not exist or no `.tex` or `.md` file is found; with `--fail-on-comments`, also if any comment carries a claim ID or an internal note. `review` and `nit` hits are listed with file and line. `--check-comments` lists the comments without failing.

## Turning the guideline's lists into rules

For each item: write the shortest pattern that catches the forbidden (or required) wording without catching its legitimate uses; run it on the current draft; read every hit; tighten until the false positives are gone. Keep the rules file in `paper/`, because it belongs to the study, not to the skill.

## What it does not do

It matches phrases, not meaning. A wrong number passes, and so does a sentence that implies causation without a causal verb. Use it with the claim-inventory check and the cross-review loop, never instead of them.
