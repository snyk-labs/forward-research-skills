"""Shared helpers: paths, deterministic CSV/JSON writers, the claims registry, loaders.

Layout (all env-overridable, all outside the source data):
  BENCH_DATA  read-only input dir with runs.csv, systems.csv, SHA256SUMS (required), optional recorded_aggregates.csv, findings.csv
  BENCH_OUT   packet dir; tables/ and claims/ are written below it (the project's analysis folder)
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True  # never write __pycache__ into the packet folder (also run entry points with python3 -B)

# The one claim-ID pattern. Every checker (ledger --check, paper-authorship, review-kit) uses this, and Claims.add()
# refuses an ID that does not match it in full, so no claim can exist that the checkers cannot see.
#   C-<SECTION>-<NN>[-<suffix>]   SECTION: capitals/digits; NN: digits; suffix starts with a letter (C-HEAD-01-macro).
# A digit-led tail (C-HEAD-01-03) is not a suffix: it reads as a range, and the checkers reject ranges.
ID_RE = re.compile(r"\bC-[A-Z0-9]+-[0-9]+(?:-[A-Za-z][A-Za-z0-9+.]*)?\b")

DATA = os.environ.get("BENCH_DATA", "data")
OUT = os.environ.get("BENCH_OUT", "analysis")
TABLES = os.path.join(OUT, "tables")
CLAIMS_DIR = os.path.join(TABLES, "claims")


def tpath(rel: str) -> str:
    p = os.path.join(TABLES, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


def fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return ""
        s = f"{v:.6f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ";".join(str(x) for x in v)
    return v


def write_csv(rel: str, rows: list, fields: list | None = None) -> str:
    p = tpath(rel)
    if fields is None:
        fields = []
        for r in rows:
            for k in r:
                if k not in fields:
                    fields.append(k)
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k)) for k in fields})
    return p


def write_json(rel: str, obj) -> str:
    p = tpath(rel)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, default=str)
        fh.write("\n")
    return p


def read_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_table(rel: str) -> list:
    return read_csv(os.path.join(TABLES, rel))


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pct(k, n, digits=1):
    return "n/a" if not n else f"{100.0 * k / n:.{digits}f}%"


class Claims:
    """Claims registry. One instance per script; saved to tables/claims/<script>.json; merged by ledger.py.

    Every number that appears in prose must be added here (with numerator/denominator when it is a rate) and cited by id.
    Never compute a number by hand into a document: add a claim to the pipeline and cite its id.
    """

    def __init__(self, script: str):
        self.script = os.path.basename(script)
        self.items = []

    def add(self, cid: str, section: str, statement: str, value, *, numerator=None, denominator=None, unit: str = "",
            table: str = "", query: str = "", caveat: str = ""):
        if not ID_RE.fullmatch(cid):
            sys.exit(f"{self.script}: claim id {cid!r} does not match the claim-ID pattern C-<SECTION>-<NN>[-<letter suffix>]")
        self.items.append(dict(id=cid, section=section, statement=statement, value=value, numerator=numerator,
                               denominator=denominator, unit=unit, table=table, query=query, caveat=caveat,
                               script=f"scripts/{self.script}"))

    def save(self):
        write_json(f"claims/{os.path.splitext(self.script)[0]}.json", self.items)


def check_grid(rows: list) -> None:
    """Fail loudly unless every (system x unit x item) cell exists exactly once and there are >= 2 units."""
    keys = [(r["system"], r["unit"], r["item"]) for r in rows]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        sys.exit(f"duplicate rows (would be double-counted): {dup[:5]}")
    systems = sorted({r["system"] for r in rows})
    items = sorted({(r["unit"], r["item"]) for r in rows})
    missing = [(s, u, i) for s in systems for (u, i) in items if (s, u, i) not in set(keys)]
    if missing:
        sys.exit(f"incomplete grid: {len(missing)} missing system x item cells, e.g. {missing[:3]}")
    if len({u for u, _ in items}) < 2:
        sys.exit("need at least 2 units for cluster bootstrap and leave-one-unit-out")


def load_runs(arm: str = "main") -> list:
    """runs.csv: one row per (system, unit, item), plus optional `arm` column (main | supplementary labels).

    `hit` is DERIVED here from the validated scorer port (scorer_port.decide) and must equal the harness's recorded_hit
    when that column exists, so every downstream number inherits the scorer validation. Supplementary arms are never
    mixed into the headline: pass arm= explicitly to load them. See references/data-contract.md.
    """
    from scorer_port import decide
    rows = [r for r in read_csv(os.path.join(DATA, "runs.csv")) if r.get("arm", "main") == arm]
    for r in rows:
        r["hit"] = decide(r)
        if "recorded_hit" in r and int(r["recorded_hit"]) != r["hit"]:
            sys.exit(f"scorer port disagrees with recorded_hit on {r['system']}/{r['unit']}/{r['item']}; run s01 and fix the port")
    check_grid(rows)
    return rows
