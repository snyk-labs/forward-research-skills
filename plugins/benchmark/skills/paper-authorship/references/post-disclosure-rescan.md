# Post-disclosure re-scan

Use this when findings were shared with a system's owner before publication and the owner shipped changes in response. If more than one owner received findings, offer each the same re-scan on the same terms, or say in the paper why not. Readers will want to know what changed. A careless re-scan can blur the line between the study's results and a vendor's later product, so the procedure keeps them apart.

## Principles

- **The main results stay as run.** A re-scan never replaces or merges into the main tables, unions or rankings. If it entered them, the re-run system would get a second attempt that the others did not.
- **It is its own execution.** Run it as a separate, labelled execution with its own archive, checksums and README. Its role is "post-disclosure re-scan", and the README says it must never be merged. Link it from the data and code availability section.
- **Same inputs, recorded.** Use the same ‹units›, prompts and configuration as the main run. Record the harness commit, the system's version as reported per run (and the release channel, such as a preview build, if that is what was used), and the run date. If the published reference set has changed since the main run (an erratum fix, for example), say so, and score against the frozen reference set for any comparison with the main run.
- **Verify it yourself.** Do not take the operator's summary at face value. Verify the archive checksums, re-score every run with the validated scorer against the frozen reference set, and check that the scorer port agrees with the harness on unchanged ‹units›.
- **Detection uses the paper's rule.** Judge whether each disclosed item is now detected with the same matching rule as the main results, against the item's recorded locations. A nearby finding of another class, or of a different flow, is not a detection. Report the nearby-findings view separately if it helps. When an earlier analysis already counted nearby findings, compute the re-scan's on the same location basis, or name the basis in both. Two claims that count "the same thing" on different bases will look like a contradiction.
- **Facts from the owner are author statements.** How many items received a fix, and by when, come from the system's owner and are recorded as such, with a date. The re-scan shows what the product now detects. It does not show what was fixed.

## Wording

State it in one short paragraph in the section that reports the disclosed findings, with a pointer from the threats section:

> We shared the ‹k› findings with the ‹system› team before publication. By ‹date›, ‹j› of them had received a fix deployed to production (‹owner's statement›). A re-scan of the ‹N› ‹units› on ‹date›, with ‹system› ‹version›, detects ‹d› of the ‹k›, judged with the paper's matching rule; against the frozen reference set it matches ‹M′› items, compared with ‹M› in the main run. These post-disclosure results are reported separately and never merged into the main results, which stay as run.

Fill every count from the registry, whichever way it points; the template does not assume the re-scan detects what was fixed or leaves the main matches unchanged.

Avoid:

- **"Not comparable"** after a comparison. Either compare like-for-like, against the frozen reference set and with the same rule, or don't compare at all.
- **Release-status claims.** Name the version and channel; don't make announcements.
- **Rates built from the disclosed items.** They are a lower-bound count from the items that were reviewed, not a sample.

## Steps

1. Draft the operator prompt from `assets/postfix-rescan-prompt-template.md`. The human runs it, or hands it to whoever operates the harness.
2. When the run is back:
   - add a pipeline step that verifies and extracts the archive;
   - re-score against the frozen reference set;
   - checks each disclosed item under the paper's rule;
   - registers claims for the run facts, the re-scored totals and the per-item detection.
3. Ask the human for the owner's facts (fixes shipped, date), and for any decision on how to describe the version.
4. Fill the paragraph. Add the archive to data availability, add the version to the configuration appendix if relevant, and update the inventory. Then re-run the claims check, the lint and the compile.
5. Nothing is merged or pushed by the skill. The operator publishes on a branch, and the human merges before the paper cites the path on the default branch.
