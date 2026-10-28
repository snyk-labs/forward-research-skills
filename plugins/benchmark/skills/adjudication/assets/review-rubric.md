# Reviewer rubric (give this to every first-pass and second-pass reviewer)

You review one cluster of findings that no reference item matched. Work from the real code, not from the finding's description. You are not told which systems reported it; do not try to infer it, and apply the same bar to every cluster.

## Required output per cluster

1. **Location trace:** entry point (source) with file:line, each hop, the sink with file:line. For non-code domains: the evidence that supports the claim, with a pointer to the original item.
2. **Reachability:** can the relevant actor (end user, adversary, upstream data source) control the input without a precondition that the benchmark's own rules would exclude? List preconditions.
3. **Verdict:** `real` (traced end to end, no unusual precondition), `borderline` (real flow, the outcome depends on a precondition you name), `noise` (path does not exist, input is not controllable, or the finding describes behaviour that is safe).
4. **Novelty:** `yes` (no reference item shares its root cause), `partial` (shares a source or a sink with a reference item but is a separate flow), `no` (same root cause as a reference item; name it). In the "new relative to the reference tool" view only, an item the reference tool already reported is also `no`.
5. **Reference-tool check** ("new relative to the reference tool" view only; done after the verdict in item 3, with the reference tool's outputs): did the reference tool report any rule near this location, or the same type anywhere in these files? Quote the evidence.
6. **Boundary:** defect in third-party code, or first-party misuse of a sink-by-design API?
7. **Confidence and what would change your mind.**

## Rules

- No verdict without a traced path. If you cannot trace it, write `cannot-trace` and why.
- Be strict: borderline is the default when a precondition exists.
- A different manifestation of the same faulty item is the same item.
- Do not read other reviewers' verdicts before writing yours.
- Do not run anything inside the benchmark's source or fixture directories.
