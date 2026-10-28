#!/usr/bin/env python3
"""Check a paper's claim inventory against the evidence ledger's claims registry.

  python3 check_claims.py --inventory paper/claim-inventory.md --registry analysis/tables/claims.csv \\
      --tex paper/sections paper/main.tex --manifest paper/figures/manifest.json --numbers
  python3 check_claims.py --registry analysis/tables/claims.csv --print-stamp
  python3 check_claims.py --inventory paper/claim-inventory.md --registry analysis/tables/claims.csv \\
      --diff-registry old-claims.csv

Checks (exit 1 on any failure of 1-6):
  1. every claim ID cited in the inventory and the figure manifest exists in the registry;
  2. no wildcard, range or list IDs (C-ABC-*, C-ABC-01..05, C-ABC-01-03, C-ABC-01/02, C-ABC-0x, C-*);
  3. no claim IDs leak into the paper's text (LaTeX comments are ignored; strip them before upload);
  4. every "Value as stated" cell matches its claims' registry value, numerator or denominator, allowing rounding to
     the stated precision and rate <-> percent;
  5. the inventory's "Registry sha256:" stamp matches the registry it is checked against (the evidence did not change
     under the paper unnoticed). A missing stamp is a warning; --print-stamp prints the line to paste;
  6. every path given exists, and --tex finds at least one .tex file.
Reports (never failures):
  --numbers: numbers in the paper text that appear in no inventory row, for triage. 0-10 are skipped unless
             --all-numbers (small counts and differences are exactly the hand-computed numbers to look for).
  --diff-registry OLD: claims added, removed or changed since OLD, and the inventory rows that cite them.

The claim-ID pattern comes from idpattern.py, which imports it from benchmark:empirical-analysis's ledger.py, so this
check, the ledger's --check and the pipeline's registration guard all use one pattern. Standard library only.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idpattern import ID_RE, SOURCE as ID_SOURCE, strip_comments, tex_files  # noqa: E402

_SEC = r"C-[A-Z0-9]+-"
WILDCARD_RE = re.compile(
    r"\bC-\*"                                            # C-*
    rf"|\b{_SEC}(?:\*|\d*[xX]+\b)"                       # C-ABC-*, C-ABC-xx, C-ABC-0x
    rf"|\b{_SEC}\d+-\*"                                  # C-ABC-01-*
    rf"|\b{_SEC}\d+(?:\.\.|–|—|/|-)\d+\b"                # C-ABC-01..05, 01–05, 01/02, 01-03 (digit tails are ranges)
    rf"|\b{_SEC}\d+\s*(?:\.\.|–|—|-|to)\s*{_SEC}\d+"     # C-ABC-01 – C-ABC-05
    rf"|\b{_SEC}\d+\.\.\w*")
LOOSE_ID_RE = re.compile(r"\b[cC]-[A-Za-z0-9]+-\d+[A-Za-z0-9+.-]*")
NUM_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?!\w)(?!\.\d)")  # a sentence-final full stop ends a number
STAMP_RE = re.compile(r"registry sha256:\s*`?([0-9a-f]{64})", re.I)
VALUE_FIELDS = ("value", "numerator", "denominator")


def load_registry(path):
    """Return {id: row}. Accepts tables/claims.csv or the tables/claims/ directory of per-script JSON files."""
    rows = {}
    if os.path.isdir(path):
        for p in sorted(glob.glob(os.path.join(path, "*.json"))):
            for c in json.load(open(p, encoding="utf-8")):
                rows[c["id"]] = {k: "" if v is None else str(v) for k, v in c.items()}
    elif os.path.isfile(path):
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row.get("id"):
                    rows[row["id"].strip()] = row
    else:
        sys.exit(f"registry not found: {path}")
    if not rows:
        sys.exit(f"registry {path} has no claim ids")
    return rows


def registry_hash(path):
    h = hashlib.sha256()
    files = sorted(glob.glob(os.path.join(path, "*.json"))) if os.path.isdir(path) else [path]
    for p in files:
        h.update(os.path.basename(p).encode())
        h.update(open(p, "rb").read())
    return h.hexdigest()


def numbers_in(s):
    """[(value, decimals, is_percent)] for every number in s."""
    out = []
    for m in NUM_RE.finditer(s or ""):
        raw = m.group(1).replace(",", "")
        dec = len(raw.split(".")[1]) if "." in raw else 0
        tail = s[m.end():m.end() + 9].lstrip("\\ ")
        out.append((float(raw), dec, tail.startswith("%") or tail.lower().startswith("percent")))
    return out


def value_matches(x, dec, pct, reg_vals):
    """True if stated x equals a registry number at the stated precision. A plain integer must equal an integer
    registry field exactly (counts are not rounded), or be a rounded percentage of a stored rate."""
    tol = 0.5 * 10 ** -dec + 1e-9
    for r in reg_vals:
        if abs(x - 100 * r) <= tol:  # a stored rate stated as a percent
            return True
        if dec == 0 and not pct:
            if abs(r - round(r)) < 1e-9 and abs(x - r) < 1e-9:
                return True
        elif abs(x - r) <= tol:
            return True
    return False


def inventory_tables(text):
    """Yield (line_no, {header: cell}) for every data row of every markdown table."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            head = [c.strip().lower() for c in lines[i].strip().strip("|").split("|")]
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                yield j + 1, dict(zip(head, cells))
                j += 1
            i = j
        else:
            i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory")
    ap.add_argument("--registry", required=True, help="tables/claims.csv or the tables/claims/ directory")
    ap.add_argument("--tex", nargs="+", default=[])
    ap.add_argument("--manifest", help="figure manifest written by the figure script")
    ap.add_argument("--numbers", action="store_true", help="report numbers in the paper with no inventory row")
    ap.add_argument("--all-numbers", action="store_true", help="with --numbers, also report 0-10")
    ap.add_argument("--print-stamp", action="store_true", help="print the registry stamp line for the inventory header")
    ap.add_argument("--diff-registry", metavar="OLD", help="report claims changed since an earlier claims.csv")
    a = ap.parse_args()

    reg = load_registry(a.registry)
    stamp = registry_hash(a.registry)
    if a.print_stamp:
        print(f"Registry sha256: {stamp}")
        return
    if not a.inventory:
        sys.exit("--inventory is required (except with --print-stamp)")
    if not os.path.isfile(a.inventory):
        sys.exit(f"inventory not found: {a.inventory}")
    inv = open(a.inventory, encoding="utf-8").read()
    known = set(reg)
    fail = False

    # 5. registry stamp
    m = STAMP_RE.search(inv)
    if not m:
        print(f"WARNING: the inventory has no registry stamp. Add this line to its header:\n  Registry sha256: {stamp}")
    elif m.group(1) != stamp:
        fail = True
        print(f"REGISTRY CHANGED since the inventory was stamped ({m.group(1)[:12]}… → {stamp[:12]}…). "
              "Run --diff-registry <previous claims.csv>, re-verify the affected rows and figures, then update the stamp.")

    # 2. wildcards and ranges
    wild = sorted(set(x.group(0) for x in WILDCARD_RE.finditer(inv)))
    if wild:
        fail = True
        print("WILDCARD, range or list claim IDs in the inventory (list each ID):", wild)
    loose = sorted(set(x.group(0) for x in LOOSE_ID_RE.finditer(inv) if not ID_RE.fullmatch(x.group(0))
                       and not WILDCARD_RE.match(x.group(0)) and not ID_RE.match(x.group(0))))
    if loose:
        print("WARNING: ID-like tokens that are not valid claim IDs (case or suffix?):", loose)

    # 1. existence
    cited = sorted(set(x.group(0) for x in ID_RE.finditer(inv)))
    missing = [i for i in cited if i not in known]
    if missing:
        fail = True
        print(f"UNKNOWN claim IDs in the inventory ({len(missing)}):", missing)

    if a.manifest:
        if not os.path.isfile(a.manifest):
            sys.exit(f"figure manifest not found: {a.manifest}")
        man = json.load(open(a.manifest, encoding="utf-8"))
        for fig, ids in sorted(man.items()):
            bad = [i for i in ids if i not in known or not ID_RE.fullmatch(i)]
            if bad:
                fail = True
                print(f"UNKNOWN claim IDs in figure manifest [{fig}]:", bad)

    # 4. values as stated
    unchecked = 0
    for ln, row in inventory_tables(inv):
        id_cells = " ".join(v for k, v in row.items() if "claim" in k)
        ids = [i for i in ID_RE.findall(id_cells) if i in known]
        stated = next((v for k, v in row.items() if "value as stated" in k), None)
        if not ids:
            continue
        if not stated:
            unchecked += 1
            continue
        regvals = [x for i in ids for f in VALUE_FIELDS for x, _, _ in numbers_in(reg[i].get(f, ""))]
        bad = [s for s in numbers_in(stated) if not value_matches(s[0], s[1], s[2], regvals)]
        if bad:
            fail = True
            shown = "; ".join(f"{i}: value {reg[i].get('value')}, k/n {reg[i].get('numerator')}/{reg[i].get('denominator')}" for i in ids)
            print(f"VALUE MISMATCH {a.inventory}:{ln}: stated '{stated}' has {[b[0] for b in bad]} not in the registry ({shown})")
    if unchecked:
        print(f"note: {unchecked} inventory rows cite claims but have no 'Value as stated' entry; their numbers are not checked")

    # 3 and 6. paper text
    texs = tex_files(a.tex) if a.tex else []
    if a.tex and not any(f.endswith(".tex") for f in texs):
        sys.exit(f"--tex {a.tex}: no .tex files found")
    leaks, numbers = [], {}
    for f in texs:
        body = strip_comments(open(f, encoding="utf-8").read())
        for ln, line in enumerate(body.splitlines(), 1):
            for x in ID_RE.finditer(line):
                leaks.append(f"{os.path.relpath(f)}:{ln} {x.group(0)}")
            if a.numbers:
                clean = re.sub(r"\\(ref|eqref|label|cite[pt]?|includegraphics|input|path|url|href|texttt)\{[^}]*\}", " ", line)
                clean = re.sub(r"\[[^\]]*\]", " ", clean)
                for n in NUM_RE.finditer(clean):
                    numbers.setdefault(n.group(1), []).append(f"{os.path.relpath(f)}:{ln}")
    if leaks:
        fail = True
        print(f"CLAIM IDs in paper text ({len(leaks)}); they belong in the inventory only:")
        for x in leaks:
            print("  ", x)

    if a.numbers:
        inv_no_ids = LOOSE_ID_RE.sub(" ", ID_RE.sub(" ", inv))
        inv_nums = {n.replace(",", "") for n in NUM_RE.findall(inv_no_ids)}
        trivial = set() if a.all_numbers else {str(i) for i in range(0, 11)}
        orphan = {n: locs for n, locs in numbers.items() if n.replace(",", "") not in inv_nums and n not in trivial}
        print(f"\nNumbers in the paper with no inventory row ({len(orphan)}; triage by hand, not a failure"
              f"{'' if a.all_numbers else '; 0-10 skipped, use --all-numbers'}):")
        for n, locs in sorted(orphan.items(), key=lambda kv: kv[1][0]):
            print(f"  {n:>10}  {', '.join(locs[:4])}{' …' if len(locs) > 4 else ''}")

    if a.diff_registry:
        old = load_registry(a.diff_registry)
        fields = ("statement", "value", "numerator", "denominator", "unit", "table", "query", "caveat")
        added = sorted(set(reg) - set(old))
        removed = sorted(set(old) - set(reg))
        changed = sorted(i for i in set(reg) & set(old) if any((reg[i].get(f) or "") != (old[i].get(f) or "") for f in fields))
        print(f"\nRegistry diff vs {a.diff_registry}: {len(added)} added, {len(removed)} removed, {len(changed)} changed")
        for i in changed:
            diffs = [f"{f}: {old[i].get(f)!r} → {reg[i].get(f)!r}" for f in fields if (reg[i].get(f) or "") != (old[i].get(f) or "")]
            print(f"  changed {i}: " + "; ".join(diffs))
        for i in removed:
            print(f"  removed {i}")
        touched = set(changed) | set(removed)
        rows = [f"{a.inventory}:{n}" for n, line in enumerate(inv.splitlines(), 1) if touched & set(ID_RE.findall(line))]
        if rows:
            print("  inventory rows to re-verify:", ", ".join(rows))
        if a.manifest and os.path.isfile(a.manifest):
            figs = sorted(f for f, ids in json.load(open(a.manifest, encoding="utf-8")).items() if touched & set(ids))
            if figs:
                print("  figures to re-render and re-approve:", ", ".join(figs))

    print(f"\n{len(cited)} claim IDs cited, {len(known)} in registry, {len(texs)} tex files scanned (ID pattern: {ID_SOURCE}).")
    if fail:
        sys.exit(1)
    print("claims check passed")


if __name__ == "__main__":
    main()
