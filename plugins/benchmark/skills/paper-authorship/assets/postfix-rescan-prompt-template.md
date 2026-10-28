# Operator prompt: post-disclosure re-scan

Fill the ‹placeholders› and give this to whoever operates the harness. It produces one new labelled execution and a separate published bundle on a branch. It never changes the main results.

```text
Run a post-disclosure re-scan of ‹system› for ‹benchmark›. It is a separate, labelled execution: it never replaces or merges into the authoritative results (‹main execution id›) or any supplementary runs.

Context: after ‹benchmark› reported ‹k› findings to the ‹system› team, they shipped changes. The paper needs to state how many of the ‹k› the updated ‹system› now detects, with its version and the run date.

1. Prepare
   - Check out the default branch and pull. Record the commit.
   - Confirm that no ‹unit›, reference-set or task file is modified. Do not change any of them.
   - Update ‹system› to ‹the version or channel the owner names›. Record its version string, and which binary or endpoint the harness actually invokes.
   - Confirm that credentials point at the same account or organization as the main run. Report the account name, never a secret, and never print, log or commit a secret.

2. Run
   - Dry run first, restricted to ‹system›'s configuration and the main run's tasks. Check that it plans exactly ‹N› runs.
   - Run it. Record the execution id and date. Check that every run record carries the version. Retry a failed run once and report both attempts.

3. Publish (same layout as ‹existing supplementary publication path›)
   - Create a new publication folder with the checksummed bundle, per-file checksums, an index and a README. The README states:
     - the role: post-disclosure re-scan, never merged into the main results;
     - the run date, harness commit and version;
     - the account;
     - which reference set was used, including any changes since the main run.
   - Run the secret scan over the folder. Commit on a new branch and push. Do not merge.

4. Report back
   - execution id, date, commit, version (as reported and as recorded per run), account, branch and commit;
   - succeeded and failed runs, and the harness's totals next to the main run's;
   - for each of the ‹k› items (‹list with their recorded source and sink locations›): every output of ‹system› within ‹the paper's matching tolerance› of those locations, or of the same class in the same ‹unit›, with its identifier, class, location and message. Raw facts only; the paper's authors decide what counts as detected;
   - anything unexpected: changed ‹unit› fingerprints, installation problems, failed runs, output that changed where nothing should have.
```
