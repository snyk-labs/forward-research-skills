# Disconfirmation protocol

## Per thesis

For every candidate thesis write: the claim, the claim IDs behind it, the falsifier (the result that would break it), the test run, and the outcome. Keep failures in a log in the memo (table: narrative, test, outcome). A thesis that fails stays listed as "not recommended" with its composite score, so nobody rediscovers it later.

Typical falsifiers: a control (stratify, balance, uniform rule) reverses the raw split; the gap disappears under many-to-one credit; the effect lives in one category; the top-two order flips under a plausible scoring variant; the result depends on one unit.

## Independent verifier subagent

Spawn a subagent with only the raw data, the scorer documentation and a list of the top claims (statement plus ID). It must recompute each from scratch without reading your scripts, and report any mismatch with its own derivation. Do not hand it your conclusion; hand it the question. Treat any mismatch as a pipeline bug until proven otherwise.

## Sceptical review checklist

Run it on the memo, theses and charts plan before handing over.

1. Superlatives: "only", "every", "all", "never", "top N", "best". Each needs a claim ID that literally supports it, including its denominator.
2. Mixed metric sets: any sentence or chart comparing systems scored under different registered metrics.
3. Causal wording: "because", "due to", "drives", "improves". Replace with "associated with" or "consistent with" unless a control isolates the factor.
4. Mislabelled claims: a counterfactual row presented as a headline, a micro rate called macro, an upper bound called a result.
5. Confounded pairs described as a factor comparison.
6. Hidden defaults: counts quoted from memory of an earlier run; "the six rules" style counts that drift.
7. Claim IDs that exist but whose statement differs from the sentence citing them.
8. Interval and p-value wording: no "significant"; exact and mid-p both shown.
9. Every limitation in `limitations-and-confounds` reflected where the affected number is used.
10. Even-handedness: theses and results favourable to the author's product were tested at least as hard as those unfavourable to it; comparable results for different systems carry the same wording and caveats; nothing unfavourable to any system was left out of the memo.

Record what the review changed and what it left, with dates.
