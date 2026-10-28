# Pre-submission checklist: ‹benchmark name›

Run top to bottom on the day. Each item gets a date and initials, or a note. For the paper, the checks live in `paper/pre-publication-package.md` (from `benchmark:paper-authorship`); this list confirms they passed and adds what only release readiness owns.

## Numbers
- [ ] Pipeline re-run is byte-identical (`run_all.py --verify-determinism`).
- [ ] Paper: pre-publication package §6 passed (`check_claims.py` with values as stated and a current registry stamp; `--numbers` triaged).
- [ ] Documents outside the paper (guideline, README, release notes): `ledger.py --check` passes.

## Wording
- [ ] Paper: `guardrail_lint.py` with `paper/guardrail-rules.txt` has no blocking hits. That rules file, built from the guideline's "claims never to make" and required-disclosures lists, is the one banned-phrase list; run it on the README and release notes too.

## Disclosures
- [ ] Provenance and independence statement matches the paper's method section.
- [ ] Conflict of interest in the paper (statements and threats) and the README.
- [ ] Every item in the guideline's required-disclosures list present (single run, confounded pairs, reference-set defects, version gaps, as the guideline lists them).
- [ ] Supplementary arms in their own labelled section; wording "thresholds fixed before analysis".
- [ ] Post-disclosure note, if results were shared with a system owner before publication.

## Objectivity
- [ ] Same scoring, adjudication, wording strength and figure treatment for every system, the authors' product included (spot-check every sentence about the authors' product against comparable sentences about other systems).
- [ ] Results unfavourable to the authors' product are in the main text with the same weight as comparable results.
- [ ] Every evaluated system's owner was offered the same pre-publication review and disclosure; any asymmetry is disclosed (`provenance-and-independence.md` §4a).
- [ ] No supplementary arm, sensitivity result or adjudicated finding was dropped because of its outcome.

## Repository and data
- [ ] Licence audit done; root LICENSE, NOTICE, THIRD_PARTY_LICENSES present; fingerprints unchanged.
- [ ] Secret scan clean on the release staging directory.
- [ ] Archive and per-file checksums published; README explains verification and reproduction.
- [ ] Branches merged (fast-forward); tags created; no force-push.
- [ ] Source and fixture directories clean (no build output, notes, caches).

## Links and placeholders
- [ ] Paper: pre-publication package §1 (placeholders) and §2 (links) have no open rows.
- [ ] README and release notes: every link resolves from a logged-out browser; no placeholder (‹…›, TODO, TBD, XXX) left.
- [ ] Figures regenerate from tables; captions carry their caveat labels. Claim IDs stay in the inventory and manifest, never in captions.

## People
- [ ] Sign-offs from every author, and from the owner of every product the paper characterizes (package §4).
- [ ] Author list and affiliations confirmed.
- [ ] Vendor disclosures drafted for the human to send; none sent without approval.

## Approval
- [ ] Human approval to publish: ‹name, date›.
