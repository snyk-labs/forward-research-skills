# Wording lessons

| Situation | Weak | Use instead |
|---|---|---|
| A control has not been run | "X causes Y" | "Y is consistent with X; no control isolates it" |
| A control has been run (single run) | "X improves Y" | "supported by a ‹control› (single run)" |
| Two systems close on the headline | "A beats B" / "indistinguishable" | "not separable on this reference set (b vs c discordant, exact p = …, descriptive)" |
| Pair differs in several factors | "effort helps" | "the two configurations differ in effort, tool access and prompt; the comparison is descriptive" |
| Unmatched findings | "false positives", "hallucinations" | "outside the reference set; adjudicated: k real and new" |
| Adjudicated real findings | "the tool missed k" or "miss rate" | "at least k real findings outside the reference set"; separate from the headline |
| Exploratory subgroup split | "category X is hard" | "exploratory: within-category recall k/n, not pre-planned" |
| Supplementary arm | blended into the leaderboard | own labelled section, own table, one run |
| Model tier vs effort | "the bigger model" | name the complete configuration: harness, model, effort, tool access |
| Mechanism you believe | "because the vendor designed…" | structural property now ("this category needs cross-component reasoning"); attribution to a vendor's internals only after confirmation |
| Ranking under alternatives | "robust" | "top two unchanged under k of m variants; order swaps under ‹variant›" |
| Comparable results from different systems | the authors' product "finds", another system "appears to find" | the same verb and the same caveat for both |
| A result unfavourable to the authors' product | moved to an appendix, or given a longer explanation than other systems' results get | stated in the main text with the same weight as comparable results |

## Other rules

- Superlatives need a claim ID whose denominator literally supports them. "Only" and "every" are the common failures.
- Mixed metric sets never share a sentence unless the sentence says they are different.
- When a number is corrected after a review, add a visible correction note in the review artefact and update the claim in the pipeline; do not just change the prose.
- Counts that drift ("the six rules") are quoted only when something depends on the exact value, and the dependent is named.
- Do not write "pre-registered" in public text unless a public registry exists; write "thresholds fixed before analysis".
