#!/usr/bin/env python3
"""Figure script skeleton: render every paper (and web) figure from the pipeline's tables.

  python3 -B make_figures.py --tables ‹packet›/tables --registry ‹packet›/tables/claims.csv \\
      --out figures --paper-dir ../paper/figures [--only fig01] [--themes print,light,dark]

Requires matplotlib (the only dependency outside the standard library).

Rules this skeleton enforces (see references/figure-rules.md):
  * reads only CSVs under --tables and the claims registry; no raw data, no typed numbers;
  * table rows give geometry (bar lengths, interval ends); every value a figure PRINTS is looked up in the registry,
    by claim ID (claim()) or by the claim's table + query fields (claim_where()), and the IDs used are merged into
    <paper-dir>/manifest.json for check_claims.py;
  * one colour and one display name per system, from SYSTEMS, in every figure; a colour-blind-safe palette;
  * the reference tool is always drawn explicitly, in a neutral colour that stays visible on every theme;
  * values that do not fit an axis (for example "no recorded cost") go in an off-axis column, never at zero;
  * text is at least 7 pt at final size; paper PDFs carry no in-image notes (captions do that);
  * after rendering, open the PNGs and look at them.
"""
import argparse
import csv
import json
import os
import re
import sys

sys.dont_write_bytecode = True
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

MIN_PT = 7  # smallest text size at final print size

# ---------------------------------------------------------------- identity: one name and colour per system
# key = system id used in the tables; label = display name used everywhere (the text uses the same names).
# Colours: Okabe-Ito (distinguishable with the common colour-vision deficiencies). Families may share a hue only if
# members also differ in marker, hatch or outline, not lightness alone.
SYSTEMS = {
    "‹ref_id›": dict(label="‹Reference tool›", reference=True),
    "‹sys_a›": dict(label="‹System A›", color="#0072B2"),
    "‹sys_b›": dict(label="‹System B›", color="#56B4E9", hatch="//"),
    "‹sys_c›": dict(label="‹System C›", color="#D55E00"),
}
ORDER = list(SYSTEMS)  # one row order for every figure and panel, set by a stated rule (e.g. headline metric), never to feature one system

THEMES = {  # `ref` = reference-tool fill; `interval` contrasts with every fill, including the reference
    "print": dict(bg="#ffffff", ink="#1a1a1a", grid="#e6e6e6", ref="#8c8c8c", interval="#000000", notes=False),
    "light": dict(bg="#ffffff", ink="#1a1a1a", grid="#e6e6e6", ref="#8c8c8c", interval="#000000", notes=True),
    "dark": dict(bg="#0d0d1a", ink="#f2f2f2", grid="#2a2a3a", ref="#b3b3b3", interval="#ffffff", notes=True),
}

USED = {}  # figure name -> claim IDs printed; merged into manifest.json


def color(s, T):
    return T["ref"] if SYSTEMS[s].get("reference") else SYSTEMS[s]["color"]


# ---------------------------------------------------------------- data access
class Data:
    def __init__(self, tables, registry):
        self.tables = tables
        self.claims = {r["id"]: r for r in csv.DictReader(open(registry, newline="", encoding="utf-8"))}

    def rows(self, rel, key="system"):
        rows = {r[key]: r for r in csv.DictReader(open(os.path.join(self.tables, rel), newline="", encoding="utf-8"))}
        unknown = [s for s in ORDER if s not in rows]
        if unknown:
            sys.exit(f"{rel}: no rows for {unknown}; set SYSTEMS keys to the system ids used in the tables")
        return rows

    def _use(self, fig, cid):
        USED.setdefault(fig, []).append(cid)
        return self.claims[cid]

    def claim(self, fig, cid):
        """Registry row for a claim ID; records that the figure prints it."""
        if cid not in self.claims:
            sys.exit(f"{fig}: claim {cid} not in registry; add a pipeline step that computes it")
        return self._use(fig, cid)

    def claim_where(self, fig, table, query, suffix=""):
        """The one claim registered for this table row (its `table` and `query` fields). `suffix` picks a variant
        (e.g. "macro" for C-SEC-01-macro); empty means the unsuffixed claim. Exits unless exactly one matches."""
        def suf(cid):
            m = re.fullmatch(r"C-[A-Z0-9]+-\d+(?:-(.+))?", cid)
            return (m.group(1) or "") if m else None
        hits = [c for c, r in self.claims.items() if r.get("table") == table and r.get("query") == query and suf(c) == suffix]
        if len(hits) != 1:
            sys.exit(f"{fig}: expected one claim for table={table} query={query} suffix={suffix!r}, found {hits}")
        return self._use(fig, hits[0])


def num(r, field="value", pct=False, digits=1):
    """Format a registry value for printing; the figure never computes it."""
    v = float(r[field])
    return f"{100 * v:.{digits}f}%" if pct else f"{v:g}"


def kn(r):
    """'k/n' from a claim's numerator and denominator."""
    return f"{r['numerator']}/{r['denominator']}"


# ---------------------------------------------------------------- helpers
def style(ax, T):
    ax.set_facecolor(T["bg"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=T["ink"], labelsize=MIN_PT)
    ax.grid(axis="x", color=T["grid"], lw=0.6)
    ax.set_axisbelow(True)


def note(fig, text, T):
    """In-image note: web variants only (paper captions carry the explanation)."""
    if T["notes"]:
        fig.text(0.01, 0.01, text, fontsize=MIN_PT, color=T["ink"], va="bottom")


def off_axis_column(fig, ax, width_frac, label, T):
    """A narrow column joined to the left of `ax` for values that have no position on its scale."""
    pa = ax.get_position()
    w = pa.width * width_frac
    col = fig.add_axes([pa.x0 - w, pa.y0, w, pa.height], sharey=ax)
    col.set_xticks([0.5])
    col.set_xticklabels([label], fontsize=MIN_PT, rotation=0)
    col.set_xlim(0, 1)
    col.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    for dx in (-0.004, 0.004):  # break mark at the seam
        fig.add_artist(Line2D([pa.x0 + dx - 0.004, pa.x0 + dx + 0.004], [pa.y0 - 0.01, pa.y0 + 0.01],
                              transform=fig.transFigure, color=T["ink"], lw=0.8))
    return col


# ---------------------------------------------------------------- figures (one function each)
def fig01_headline(D, T):
    """Example: headline rate per system with its interval; reference tool explicit; printed labels from the registry.
    ‹adapt the table, columns and suffixes to the packet; this matches empirical-analysis's headline table›"""
    name = "fig01-headline"
    table = "headline/headline.csv"
    rows = D.rows(table)
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    fig.patch.set_facecolor(T["bg"])
    for y, s in enumerate(reversed(ORDER)):
        r = rows[s]
        v, lo, hi = float(r["macro"]), float(r["boot_lo"]), float(r["boot_hi"])  # geometry from the table
        ax.barh(y, v, color=color(s, T), hatch=SYSTEMS[s].get("hatch"), edgecolor=T["ink"], lw=0.4, height=0.6)
        ax.plot([lo, hi], [y, y], color=T["interval"], lw=1.2, zorder=3, solid_capstyle="butt")
        rate = D.claim_where(name, table, f"system={s}", suffix="macro")   # printed values from the registry
        counts = D.claim_where(name, table, f"system={s}")
        ax.text(hi + 0.01, y, f"{num(rate, pct=True)} ({kn(counts)})", va="center", fontsize=MIN_PT, color=T["ink"])
    ax.set_yticks(range(len(ORDER)))
    ax.set_yticklabels([SYSTEMS[s]["label"] for s in reversed(ORDER)], fontsize=MIN_PT + 0.5)
    ax.set_xlabel("‹metric› (macro rate; ‹items› matched of ‹N›)", fontsize=MIN_PT + 0.5, color=T["ink"])
    style(ax, T)
    note(fig, "Interval: resampling the ‹units› (how much the score depends on which ‹units› are included), not run-to-run variation.", T)
    fig.subplots_adjust(left=0.28, right=0.9, top=0.95, bottom=0.22)
    return name, fig


FIGURES = [fig01_headline]  # append new figure functions here


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", default="figures")
    ap.add_argument("--paper-dir", help="copy print PDFs here and merge their claim IDs into manifest.json")
    ap.add_argument("--only", help="prefix filter, e.g. fig01")
    ap.add_argument("--themes", default="print,light,dark")
    a = ap.parse_args()
    D = Data(a.tables, a.registry)
    selected = [fn for fn in FIGURES if not a.only or fn.__name__.startswith(a.only)]
    if not selected:
        sys.exit(f"--only {a.only}: no figure function matches")
    for theme in a.themes.split(","):
        T = THEMES[theme]
        for fn in selected:
            name, fig = fn(D, T)
            if theme == "print":
                os.makedirs(os.path.join(a.out, "pdf"), exist_ok=True)
                fig.savefig(os.path.join(a.out, "pdf", f"{name}.pdf"), bbox_inches="tight", facecolor=T["bg"])
                if a.paper_dir:
                    os.makedirs(a.paper_dir, exist_ok=True)
                    fig.savefig(os.path.join(a.paper_dir, f"{name}.pdf"), bbox_inches="tight", facecolor=T["bg"])
            for ext in ("png", "svg"):
                d = os.path.join(a.out, ext, theme)
                os.makedirs(d, exist_ok=True)
                fig.savefig(os.path.join(d, f"{name}.{ext}"), dpi=300, bbox_inches="tight", facecolor=T["bg"])
            plt.close(fig)
            print("ok", theme, name)
    if a.paper_dir:
        path = os.path.join(a.paper_dir, "manifest.json")
        man = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
        man.update({k: sorted(set(v)) for k, v in USED.items()})  # merge: --only never drops other figures' entries
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(man, fh, indent=1, sort_keys=True)
            fh.write("\n")
    print("Now open the PNGs and look at every figure (figure-rules.md §9).")


if __name__ == "__main__":
    main()
