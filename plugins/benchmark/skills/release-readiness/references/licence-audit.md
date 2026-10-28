# Licence audit for a public benchmark repository

Not legal advice. Have the owner confirm the root licence and, if anything is unclear, ask counsel.

## Scope: the repository as published, all of it

- the current tree, every branch that will be public, and tags;
- git history: content removed from the tree but still reachable is still public;
- every unit (app, repo, dataset, document) copied or adapted into the corpus;
- vendored dependencies, lockfiles that embed licence-bearing content, fonts, images, sample data;
- the reference set itself (your own work: choose its licence), prompts, scripts and generated tables.

## Steps

1. Inventory: for each unit, record upstream URL, upstream licence (from the upstream repo, not from a copied file), commit copied, local licence file present or not, whether the unit was modified.
2. Compare: local licence file versus upstream. Missing local file, a changed licence upstream, or no licence upstream (all rights reserved by default) are findings.
3. Resolve per finding: add the upstream licence text; replace the unit; get written permission; or remove it and its history if removal is necessary and permitted.
4. Place `LICENSE-UPSTREAM` files outside any directory that is fingerprinted or hashed for run identity, so fingerprints and checksums do not change.
5. Add a root `LICENSE` for your own work (code, reference set, prompts, tables), a `NOTICE` for attributions, and `THIRD_PARTY_LICENSES` listing each unit with upstream licence and URL.
6. Check obligations: attribution, notice retention, copyleft reach (does a copyleft unit force terms on the repository or only on that directory?), patent clauses, any "no benchmark use" terms.
7. Record the result in a provenance-and-licences note and in the paper's data availability statement.
8. Re-run the verification that fingerprints and archive checksums are unchanged.

## Output table

| Unit | Upstream | Upstream licence | Local licence file | Modified | Action | Status |
|---|---|---|---|---|---|---|
