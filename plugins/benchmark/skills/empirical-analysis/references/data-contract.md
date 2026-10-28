# Data contract for the pipeline skeleton

Put these files in `BENCH_DATA` (read-only, listed in `SHA256SUMS`, which is required). Adapt the loader in `common.py`; keep the column names so the steps keep working.

## runs.csv (required)

One row per (system, unit, item) cell, exactly once.

| column | meaning |
|---|---|
| `system` | evaluated system or configuration id |
| `unit` | unit of analysis (cluster): app, repo, dataset, document |
| `item` | reference-set item id, unique within the unit |
| `score` | whatever the scorer needs (here a match score; in your project the raw evidence) |
| `recorded_hit` | the harness's own recorded decision, 0 or 1; used only to validate your scorer port |
| `arm` | optional; `main` (default) or a supplementary arm label |

`hit` is not read from the file. `common.load_runs()` derives it from `scorer_port.decide()` and aborts if it disagrees with `recorded_hit`, so every number inherits the scorer validation. `load_runs()` also fails on duplicate rows, an incomplete system x item grid, or fewer than 2 units.

## Supplementary arms

Give supplementary rows their own `arm` label. `load_runs()` returns `main` rows only unless you pass `arm=`; the headline steps never see supplementary rows. Supplementary steps call `load_runs(arm="‹label›")`, verify identity with the main run (same reference set, prompts, fingerprints) first, and register their claims under their own section. Failed supplementary items are excluded and disclosed, never imputed: record them in a `failed_items.csv`, not as rows.

## findings.csv (optional; needed for coverage of unmatched findings and adjudication)

One row per finding a system reported, matched or not.

| column | meaning |
|---|---|
| `system`, `family`, `unit` | who reported it and where |
| `location`, `label` | where and what (file/line/type, or document/span/category) |
| `matched_item` | reference item id it was credited to, empty if outside the reference set |

Consensus clusters are built from every system's rows with empty `matched_item`, the reference tool's included: group by (unit, location, label), prioritise groups reported by at least k systems from at least 2 families, and add a same-size random sample of each system's single-system findings. The "not reported by the reference tool" filter is a separate, labelled view (see `sensitivity-and-coverage.md`). The output is an adjudication queue plus funnel counts per system.

## systems.csv (required)

`system` plus one column per factor (family, model, effort, tool_access, prompt). `s06_confounds.py` flags pairs differing in more than one factor.

## recorded_aggregates.csv (strongly recommended)

`system,hits`: the harness's recorded totals. Without it the aggregate-reproduction gate is reported as not checked.
