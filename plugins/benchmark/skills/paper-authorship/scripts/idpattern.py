"""Helpers shared by check_claims.py and guardrail_lint.py: the claim-ID pattern and LaTeX comment handling.

ID_RE is imported from benchmark:empirical-analysis's ledger.py when it can be found (plugin layout, or a project copy
of the pipeline named by BENCH_LEDGER_DIR), so the paper checks agree with the ledger's own --check and with the
registration guard in common.Claims.add(). The fallback is a copy of that pattern for standalone use; keep them identical.
"""
import os
import re
import sys

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [os.environ.get("BENCH_LEDGER_DIR", ""), os.path.join(_HERE, "..", "..", "empirical-analysis", "scripts")]
FALLBACK = re.compile(r"\bC-[A-Z0-9]+-[0-9]+(?:-[A-Za-z][A-Za-z0-9+.]*)?\b")
ID_RE = None
SOURCE = "fallback copy"
for _d in _CANDIDATES:
    if _d and os.path.exists(os.path.join(_d, "ledger.py")):
        sys.path.insert(0, os.path.abspath(_d))
        try:
            from ledger import ID_RE  # noqa: E402
            SOURCE = os.path.join(os.path.abspath(_d), "ledger.py")
            break
        except Exception:
            ID_RE = None
        finally:
            sys.path.pop(0)
if ID_RE is None:
    ID_RE = FALLBACK


def split_comment(line):
    """Split a LaTeX line into (text, comment). A % starts a comment unless an odd number of backslashes precede it,
    so `50\\%` is text but `\\\\% note` (a line break followed by a comment) is a comment."""
    i = 0
    while True:
        i = line.find("%", i)
        if i < 0:
            return line, ""
        j = i
        while j > 0 and line[j - 1] == "\\":
            j -= 1
        if (i - j) % 2 == 0:
            return line[:i], line[i:]
        i += 1


def strip_comments(text):
    return "\n".join(split_comment(line)[0] for line in text.splitlines())


def tex_files(paths, exts=(".tex",)):
    """Expand files and directories. Exits non-zero on a missing path, so a typo cannot turn a check into a silent pass."""
    out, missing = [], []
    for p in paths:
        if os.path.isdir(p):
            for e in exts:
                out += sorted(os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs if f.endswith(e))
        elif os.path.isfile(p):
            out.append(p)
        else:
            missing.append(p)
    if missing:
        sys.exit(f"path(s) not found: {missing}")
    return sorted(dict.fromkeys(out))
