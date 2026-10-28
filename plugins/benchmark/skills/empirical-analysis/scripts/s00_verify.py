#!/usr/bin/env python3
"""Step 00 — provenance: verify the authoritative data against its checksum manifest.

Expects BENCH_DATA/SHA256SUMS (lines: "<sha256>  <relative path>"). For a real archive: verify the archive hash first,
extract OUTSIDE the packet folder (scratch dir), then verify per-file hashes here. Audit parent/child lineage separately and never
mix partial parent results into the final data: record in the claims which run set is authoritative.
"""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def main():
    claims = C.Claims(__file__)
    manifest = os.path.join(C.DATA, "SHA256SUMS")
    if not os.path.exists(manifest):
        sys.exit(f"{manifest} missing: provenance cannot be verified")
    ok = bad = 0
    missing = []
    for line in open(manifest, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        digest, rel = line.split(None, 1)
        p = os.path.join(C.DATA, rel.strip().lstrip("*"))
        if not os.path.exists(p):
            missing.append(rel)
        elif C.sha256_file(p) == digest:
            ok += 1
        else:
            bad += 1
    listed = {l.split(None, 1)[1].strip().lstrip("*") for l in open(manifest, encoding="utf-8") if l.strip()}
    for must in ("runs.csv", "systems.csv"):
        if must not in listed:
            sys.exit(f"{must} is not covered by SHA256SUMS")
    C.write_json("provenance/verification.json", {"verified": ok, "mismatched": bad, "missing": missing})
    claims.add("C-PROV-01", "Provenance", "Data files verified against the checksum manifest", ok, numerator=ok,
               denominator=ok + bad + len(missing), table="provenance/verification.json",
               caveat="Replace with archive hash + per-file hashes + lineage audit for a real run.")
    claims.save()
    if bad or missing:
        sys.exit(f"provenance failure: {bad} mismatched, {len(missing)} missing")


if __name__ == "__main__":
    main()
