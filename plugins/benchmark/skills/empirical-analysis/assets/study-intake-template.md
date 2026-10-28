# ‹Benchmark name and version›: study intake

Fill this in with the human before any analysis. It is the study-specific half of the brief; the method is the rest of this skill and does not change between studies. Anything left blank is asked for, not guessed.

## 1. What and where

| Field | Value |
|---|---|
| Benchmark name and version | ‹…› |
| Harness repository (connected, read-only unless agreed) | ‹path› |
| Project context note (purpose, prior questions, thesis context) | ‹path› |
| Authoritative run archive | ‹archive id, checksum file› |
| Parent / fork / resumed runs (provenance audit only, never mixed in) | ‹ids, or "none"› |
| Corpus size, with counting basis | ‹N items across M units, counted after ‹de-duplication rule›› |
| Output folder for the evidence packet | ‹path, outside the harness's source and fixture directories› |

## 2. Reading list, in order

Same shape for every study; replace the paths:

1. the harness's agent or contributor guide;
2. the run hand-off note (what ran, what failed, what was re-run);
3. the publication or archive README and its index or manifest;
4. the scoring semantics and aggregation docs (matching rules, metric families, fork or resume semantics);
5. the benchmark-management docs (how items and units are defined);
6. the study's research questions or thesis context;
7. the prior version's report, for context only: it must not become a template that constrains this version's thesis.

## 3. Study-specific caveats (stated before analysis)

| Caveat | Value | Consequence for the analysis |
|---|---|---|
| Runs per cell | ‹1 / n› | ‹1: no repeatability analysis› |
| Metric families that must stay separate | ‹system X scored by ‹metric A›, others by ‹metric B›› | ‹never ranked or unioned together› |
| Known confounds between configurations | ‹pairs differing in more than one factor› | ‹descriptive only, no causal claim› |
| Observed known cost | ‹amount, scope› | ‹cost comparisons only among systems with known cost› |
| Unavailable data | ‹what is missing for which system› | ‹stated as unavailable, never as zero› |
| Attribution unit | ‹complete harness plus configuration› | ‹never attribute to the bare model› |
| Pre-publication access or curation involvement of any system | ‹…› | ‹asymmetry register entry› |

## 4. Established questions

‹RQ list, if any. Each is evaluated and reported, including the ones whose answer is uninteresting or unfavourable to any system.›

## 5. Exploration beyond the questions

The generic list in `references/exploration-checklist.md`, plus these study-specific items: ‹runner- or domain-specific signals worth checking›.

## 6. Invariants (do not edit)

Analyse raw per-run records, not configuration aggregates · every number traced to a script, query, output and denominator · raw counts beside percentages · unmatched outputs are "outside the reference set" · no causal claims across confounded configurations · results attributed to the complete harness plus configuration · actively try to disprove each candidate narrative · cautious descriptive statistics on small or uneven cells · same rules for every system · stop at the research memo.
