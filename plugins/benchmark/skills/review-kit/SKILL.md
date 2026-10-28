---
name: review-kit
description: "Build an internal peer-review kit PDF for a busy domain expert (about 25 to 30 minutes), then triage the reviewer's feedback and draft the messages. Use when the user says \"send this to an expert for review\", \"review kit\", \"get the tool owner to check our findings\", \"expert feedback on our findings\", \"triage the reviewer comments on the benchmark\", \"draft the message to the reviewer\", \"v2 of the review kit\", or needs fairness checks on how a vendor's tool was evaluated before publication. Not for code or pull-request review. Covers kit structure, versioning and correction notes, reproducible charts, rendering checks, the act/decline/future-work triage, and draft-only messaging with transparency notes."
---

# Review kit and reviewer-feedback triage

**Inputs:** the narrative guideline, evidence ledger (claims CSV), figures, the reviewer's profile and what they can sanity-check. **Outputs:** `review-kit-vN.pdf` (+ build script, spec, rendered page images), `reviewer-feedback-‹name›-‹date›.md` (triage), draft messages. **Human checkpoints:** the human reads the kit before it goes out; sends every message; accepts or declines each comment. **Hand-off:** accepted changes go to `benchmark:narrative-guideline` (new rule, dated) and the pipeline (new claims); `benchmark:release-readiness` for sign-off requirements.

## 1. Design for a busy expert (25 to 30 minutes)

Write for a reader who was not in the room, in complete sentences: a kit condensed too far costs the reviewer more time than it saves. Order (`assets/review-kit-outline.md`):

1. A plain abstract: what was studied, what was found, what we need from you. Short but complete sentences.
2. One-page overview.
3. The original plan versus what the data said (shows the work was not bent to a story).
4. The headline chart.
5. One section per thesis, each with its figure and a "why we decided" box (the options, the choice, the reason).
6. Claims never to make.
7. Yes/no reviewer checks pinned in context, next to the claim they test, and repeated on a one-page checklist at the end. Fairness checks come first and cover every evaluated system, not only the reviewer's own: was each configured, run, scored and described as its owner would expect, under the same rules as the others?

## 2. Build it reproducibly

Write the kit as a JSON spec plus a build script (`scripts/build_review_kit.py`): `{C-ID}` placeholders are filled from the claims CSV, so every number comes from the ledger and an unknown ID aborts the build. Generate charts from `tables/` with a script, never by hand. Versioning: a "New in vN" box, visible correction notes when a number or claim changed, and an internal-only footer on every page. Render pages to images and look at them for overflow, clipped tables and unreadable figures before sharing.

## 3. Triage feedback (`assets/feedback-triage.md`)

For each comment decide, with reasons: **act** (change the pipeline or guideline; add a dated rule), **decline** (with the data that supports declining), or **future work**. Apply the same evidence bar whichever system a change would help; note in the triage which system each accepted change favours, so a pattern is visible. Do not accept everything: a comment that conflicts with the registered scoring rule or asks for a rescore after seeing the results is declined with the sensitivity data. Turn good questions into new claims in the pipeline, then answer with the claim. Do not ask the reviewer to re-review unless a finding about their own tool changed. If feedback proposes fixing the evaluated tool and re-scanning, keep the benchmark frozen and report the fixes as a dated post-disclosure note (see `benchmark:release-readiness`).

## 4. Messages

Draft only, never send. When one evaluated system's owner reviews the kit, draft the same offer (a kit covering their system, the same fairness checks, the same deadline) for every other evaluated system's owner, or record why not; the paper discloses who reviewed. Each draft (`assets/message-draft.md`) carries transparency notes: the conflict of interest if the author's company owns a system in the study; that the kit is internal-only; the data caveats (single run, confounded pairs, reference-set defects). Keep asks specific and bounded, with a deadline that respects the reviewer's time. Show the drafts to the human and wait.

## Do not

Do not share the kit outside the named reviewers. Do not include numbers that are not in the ledger. Do not describe any system, the reviewer's or another, in ways you would not publish. Do not let a reviewer's comments change how their own system is scored or described without the same change being applied to comparable systems.
