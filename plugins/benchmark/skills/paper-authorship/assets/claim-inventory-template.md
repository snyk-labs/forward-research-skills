# ‹Benchmark name› paper: claim inventory

Registry sha256: ‹paste the line printed by `check_claims.py --registry ‹packet›/tables/claims.csv --print-stamp`›

Every number and factual sentence in the paper maps to a row here: a claim ID from the registry (`‹packet›/tables/claims.csv`), a cited public source, or a recorded author statement. List each ID; no wildcards or ranges. Fill "Value as stated" with every number exactly as the paper prints it (for example `16 of 24 (66.7%)`); the check compares it with the registry's value, numerator and denominator, allowing rounding to the printed precision and rate↔percent. Check with:

```
python3 scripts/check_claims.py --inventory paper/claim-inventory.md --registry ‹packet›/tables/claims.csv \
    --tex paper/sections paper/main.tex --manifest paper/figures/manifest.json --numbers
```

When the registry changes, keep the previous `claims.csv`, run the same command with `--diff-registry ‹old claims.csv›`, re-verify the rows and figures it lists, then update the stamp above.

"Own-system" marks statements about a system made by the authors' employer; those go into the owner's sign-off packet.

## Abstract

| Statement | Value as stated | Claim / source | Basis (set, metric, subset) | Own-system |
|---|---|---|---|---|
| ‹short paraphrase of the sentence› | ‹number(s) as printed› | ‹C-SEC-01› | ‹all ‹M› systems scored with ‹metric›› | ‹yes/blank› |

## ‹Section n: title›

| Statement | Value as stated | Claim / source | Basis | Own-system |
|---|---|---|---|---|

## Figures

| Figure | Printed values | Claim IDs | Alt text |
|---|---|---|---|
| ‹fig id› | ‹what it prints› | ‹IDs, each listed› | ‹takeaway and key values in one or two sentences› |

## Author statements (facts only the authors can supply)

| Statement | Who | Date | Where in paper |
|---|---|---|---|

## Citations (statements about other work)

| Statement | Work (key) | Checked against | Date |
|---|---|---|---|

## Bibliography verification log

| Key | Identifier | Checked against (abstract page / publisher record) | Date |
|---|---|---|---|

## Novelty statements (re-search at submission)

| Statement | Searched | Date | Result |
|---|---|---|---|
