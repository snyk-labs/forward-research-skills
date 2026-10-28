# Copy review

Run a fresh reviewer over the finished copy before the human sees it, and again after any large change. The build's number check catches a typed number with no source; it cannot catch a true number on the wrong basis, a superlative that one subset breaks, or wording looser than the paper's.

## Reviewer prompt (adapt)

> You are a sceptical reader with the paper and its claims registry open. You could work for the team behind any of the evaluated systems. Read-only. Review the content file (every finding, quote, post, card headline and caveat, term and guardrail) against `claims.csv`, the paper, and the guideline's "claims never to make". Find any sentence you could quote back as misleading or as unfair to any system. Check, in order:
> 1. NUMBERS: each matches its claim value. Is it on the basis the sentence implies (which systems, metric, runs)?
> 2. SUPERLATIVES: does every "most / only / every / none / first / all" hold on every set a reader would assume?
> 3. CEILING: any causal, repeatability or significance wording beyond the paper's?
> 4. TIME AND RUN WORDING: are dates, intervals and run counts described exactly?
> 5. ATTRIBUTION: are quotes marked as drafts? Are roles and process claims only what the paper or the working doc states?
> 6. EVEN-HANDEDNESS: do comparable results get the same verbs, caveats and prominence whichever system produced them? Is any system singled out by colour, order or annotation?
> 7. BALANCE: does the set of findings reflect the paper's weight, including findings unfavourable to the authors' product?
> For each issue give: item, quote, why it is a problem, the fix, and BLOCKER / SHOULD-FIX / NIT. Do not report things that are fine.

Give the reviewer the content file, the registry, the paper and the guideline, but not your reasoning. Verify each finding against the registry before acting, log it, fix it, and rebuild.

## Error classes to check for

| Class | Example (generic) | Fix |
|---|---|---|
| Favourable basis passed off as the general one | "found by no other system", when the count left out systems scored on a different metric | Name the basis: "missed by all ‹n› systems scored the same way" |
| Interval drift | "three runs, a week apart" when it was one run and two repeats later | Say exactly what happened, as the paper does |
| Causal leap | "so the gap comes from the settings, not the model" | Use the paper's wording ("is consistent with"), and give the scope |
| Invented effect | "the stricter rule changed the ranking the most", with no claim behind it | Replace it with a registered number, or cut it |
| Loose overlap wording | "everyone's results overlapped" | Say exactly what the claim counts |
| Unverified role | a job title typed from memory into a quote attribution | Leave it out, or take it from the working doc |
| Invented process claim in a quote | "every finding went straight to the engineers" | Keep only what the paper states |
| Uneven treatment | one system's result "found", another's comparable result "appears to find" | Same verb, same caveat, same placement |
| Missing counterweight | a set of findings that leaves out the ones unfavourable to the authors' product | Add them in proportion to their weight in the paper |
| Unmeasured shown as an advantage | a system with no measured per-run cost read as "free" | Say what the study did not measure, on the card and in the guardrails |

## Log

Record each round in the working doc with these columns: ID, severity, item, issue, decision (act / decline / ask the human), fix, rebuilt (yes or no).
