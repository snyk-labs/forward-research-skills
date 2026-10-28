#!/usr/bin/env python3
"""List licence files per unit directory and flag units without one.

  python3 licence_inventory.py REPO_ROOT [--units-glob 'units/*'] [--out inventory.csv]

Read-only. Looks for LICENSE*/COPYING* up to two levels inside each unit, and for a sibling file named
LICENSE-UPSTREAM or LICENSE-UPSTREAM-<unit-dir-name> in the unit's parent folder. A NOTICE file alone does not count as a
licence. Exits 1 when any unit has none.
It does not decide licences: it finds gaps for a human to resolve against upstream. Not legal advice.
"""
import csv
import glob
import os
import sys

sys.dont_write_bytecode = True
NAMES = ("license", "licence", "copying")


def find(unit: str):
    hits = []
    for base, dirs, files in os.walk(unit):
        depth = base[len(unit):].count(os.sep)
        if depth > 2:
            dirs[:] = []
            continue
        dirs[:] = [d for d in dirs if d not in (".git", "vendor", "third_party")]
        for f in sorted(files):
            if f.lower().startswith(NAMES):
                hits.append(os.path.relpath(os.path.join(base, f), unit))
    return hits


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = os.path.normpath(sys.argv[1])
    pat = sys.argv[sys.argv.index("--units-glob") + 1] if "--units-glob" in sys.argv else "*"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    rows = []
    for unit in sorted(glob.glob(os.path.join(root, pat))):
        if not os.path.isdir(unit):
            continue
        local = find(unit)
        parent, name = os.path.dirname(os.path.normpath(unit)), os.path.basename(os.path.normpath(unit))
        upstream = [f for f in os.listdir(parent) if f.upper() in ("LICENSE-UPSTREAM", f"LICENSE-UPSTREAM-{name}".upper())] if parent != root else []
        rows.append(dict(unit=os.path.relpath(unit, root), local_licence_files=";".join(local), upstream_file=";".join(upstream),
                         flag="" if (local or upstream) else "NO LICENCE FILE"))
    w = csv.DictWriter(open(out, "w", newline="") if out else sys.stdout, fieldnames=["unit", "local_licence_files", "upstream_file", "flag"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    gaps = sum(1 for r in rows if r["flag"])
    print(f"{len(rows)} units, {gaps} without a licence file", file=sys.stderr)
    sys.exit(1 if gaps else 0)


if __name__ == "__main__":
    main()
