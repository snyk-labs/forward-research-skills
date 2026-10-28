#!/usr/bin/env python3
"""Scan a directory (an archive staging dir) for credential-shaped strings before publication.

  python3 secret_scan.py DIR [--allow REGEX]

Uses credential SHAPES (key prefixes, JWTs, private key blocks, long hex/base64 after an assignment), not prose words:
"Bearer" or "token" appear in harmless documentation and would bury real hits. Exit 1 when anything matches.
Extend PATTERNS with the vendors you actually use. Binary files are skipped. Output shows file, line and the pattern name only,
never the matched secret.
Scan a STAGING DIRECTORY or an extracted copy: compressed archives are reported as skipped, not scanned. Files that are not
valid UTF-8 are read leniently so a stray byte cannot hide a credential; NUL-containing (binary) files are listed as skipped.
Exit 1 on any hit, and also on skipped binary or compressed files unless --allow-skipped is given.
"""
import os
import re
import sys

sys.dont_write_bytecode = True

PATTERNS = {
    "private-key-block": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----",
    "aws-access-key-id": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
    "github-token": r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",
    "api-key-sk-prefix": r"\bsk-[A-Za-z0-9_-]{20,}\b",
    "slack-token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b",
    "jwt": r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b",
    "assignment-with-long-secret": r"(?i)(?:api[_-]?key|secret|token|passwd|password)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9/+_=-]{24,}",
    "authorization-header-with-value": r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._~+/=-]{20,}",
}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    allow = re.compile(sys.argv[sys.argv.index("--allow") + 1]) if "--allow" in sys.argv else None
    hits = 0
    skipped = []
    for base, _, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(base, f)
            try:
                raw = open(p, "rb").read()
            except OSError:
                skipped.append(os.path.relpath(p, root))
                continue
            if b"\0" in raw or f.lower().endswith((".gz", ".tgz", ".zip", ".bz2", ".xz", ".zst", ".tar")):
                skipped.append(os.path.relpath(p, root))
                continue
            text = raw.decode("utf-8", errors="replace")
            for n, line in enumerate(text.splitlines(), 1):
                for name, pat in PATTERNS.items():
                    m = re.search(pat, line)
                    if m and not (allow and allow.search(m.group(0))):
                        hits += 1
                        print(f"{os.path.relpath(p, root)}:{n}: {name}")
    for s in skipped:
        print(f"SKIPPED (binary or compressed, not scanned): {s}")
    print(f"{hits} potential secret(s), {len(skipped)} skipped file(s)")
    sys.exit(1 if hits or (skipped and "--allow-skipped" not in sys.argv) else 0)


if __name__ == "__main__":
    main()
