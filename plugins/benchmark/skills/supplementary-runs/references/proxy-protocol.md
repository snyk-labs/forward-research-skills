# Proxy protocol: another agent runs the harness, you write the prompts

You can read the repo and write prompts; a second agent session executes. The risks are an unverified environment, a change you did not review, a run that dies silently, and a baseline that quietly changed.

## Prompt 1: read-only health check (no edits, no spend)

Ask the operator agent to report, without changing anything:

- git state: branch, HEAD, clean or dirty tree, remotes;
- pinned toolchain: runtime versions, lockfile honoured, and every bundled or global CLI the harness shells out to, with versions;
- credentials: confirm they are present through the harness's own env mechanism (names only, never values);
- baseline checksums: SHA-256 of every existing result archive and the reference-set files, to compare at the end;
- a dry run (the harness's own `--dry-run`) with the manifest it would execute: item counts per arm.

Review the report yourself. Fix environment gaps before any run.

## Prompt 2: branch and code changes

Changes only on a new branch. Ask for the diff and read it. Typical needs: a way to add an arm without altering existing configurations, per-run tool-version capture, a config for the new arm. Reject unrelated edits.

## Prompt 3: cheapest arm first

Run the smallest, cheapest arm end to end (run, score, load, ledger) to validate the pipeline. Only then launch the expensive arms.

## Prompt 4+: long runs

- Start detached: `nohup … > run.log 2>&1 &`, record the PID, poll the status command and log; a foreground command can be killed by the agent's tool timeout.
- Set any spend cap at the approved budget plus headroom, never below the estimate: a cap reached mid-run wastes everything already spent and leaves a partial arm. Raising it needs the human's approval.
- On failure: stop, read the log, diagnose, then retry only the failed items through the harness's resume command. Do not rerun successes.

## Prompt N: close-out

- Re-verify the baseline checksums from the health check; they must be unchanged.
- Verify source and fixture directories: `git status` clean, fingerprints equal to the main run's manifest. No build output, no notes written there.
- Confirm tool versions are recorded per run.
- Report arm statuses: completed, failed, excluded.

## Reviewing the operator's claims

Treat "done" as a claim. Ask for the status command's output and the checksum diff, not a summary.
