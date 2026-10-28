#!/usr/bin/env python3
"""Minimal run_all skeleton: run the numbered steps in order, deterministically, then regenerate the ledger.

  BENCH_DATA=data BENCH_OUT=analysis python3 -B scripts/run_all.py [--verify-determinism]

--verify-determinism additionally runs the whole pipeline into a FRESH temporary output dir with a different
PYTHONHASHSEED and fails unless every file under tables/ and the ledger is byte-identical to the main output. A fresh dir
catches stale files and a different hash seed catches dependence on set or dict order.
Claim files from steps no longer listed in STEPS are ignored by the ledger (with a warning), so renamed or removed steps
cannot leave phantom claims behind. Add a step: drop sNN_name.py next to this file and append its stem to STEPS.
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = ["s00_verify", "s01_validate_scorer", "s02_headline", "s03_paired", "s04_sensitivity", "s05_coverage",
         "s06_confounds", "ledger"]  # ledger always last


def run_once(out: str, hashseed: str) -> None:
    steps = ",".join(s for s in STEPS if s != "ledger")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=hashseed, BENCH_OUT=out, BENCH_STEPS=steps)
    for step in STEPS:
        t0 = time.time()
        r = subprocess.run([sys.executable, "-B", os.path.join(HERE, f"{step}.py")], env=env, stdout=subprocess.DEVNULL)
        if r.returncode != 0:
            sys.exit(f"step {step} failed (exit {r.returncode})")
        print(f"  ok  {step:22s} {time.time() - t0:5.1f}s")


def digest(root: str) -> dict:
    out = {}
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(base, f)
            rel = os.path.relpath(p, root)
            if rel.startswith(os.path.join("tables", "claims") + os.sep) and os.path.splitext(f)[0] not in os.environ.get("_LIVE", "").split(","):
                continue  # ignore stale claim files in the main output dir
            out[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def main():
    out = os.environ.get("BENCH_OUT", "analysis")
    run_once(out, "0")
    if "--verify-determinism" in sys.argv:
        os.environ["_LIVE"] = ",".join(s for s in STEPS if s != "ledger")
        tmp = tempfile.mkdtemp(prefix="bench-verify-")
        run_once(tmp, "12345")
        first, second = digest(out), digest(tmp)
        diff = sorted(k for k in set(first) | set(second) if first.get(k) != second.get(k))
        if diff:
            sys.exit(f"NOT deterministic (fresh dir, different hash seed), differing files: {diff}")
        print(f"deterministic: {len(second)} files byte-identical across a fresh run with a different hash seed")
    print("done")


if __name__ == "__main__":
    main()
