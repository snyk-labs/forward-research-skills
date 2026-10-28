#!/usr/bin/env python3
"""Social card script skeleton: 1200x675 cards (saved at 2x) plus manifest.csv mapping each card to its claims.

Copy to <project>/analysis/figures/make_cards.py. Import the paper's figure script for its palette, system colours and
table helpers where it exists, so the cards match the paper; the constants below are neutral stand-ins. Every number on
a card comes from a table or a claim value (claim()); only corpus constants declared below may be typed. Every system
on a card keeps its colour from the paper's figures; none gets a highlight the others don't (references/card-production.md).

Usage:  python3 -B make_cards.py --claims ../tables/claims.csv --out ../../social/cards [--theme dark]
Needs matplotlib.
"""
import argparse
import csv
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# ---- visual system (replace with the paper's figure tokens; keep the figure rules) ----
THEMES = {
    "light": dict(bg="#FFFFFF", ink="#111827", soft="#374151", faint="#6B7280", grid="#E5E7EB", rule="#2563EB"),
    "dark": dict(bg="#0F1115", ink="#F3F4F6", soft="#D1D5DB", faint="#9CA3AF", grid="#2A2F3A", rule="#7AA2F7"),
}
SANS, MONO = "DejaVu Sans", "DejaVu Sans Mono"      # register the project's fonts with matplotlib to use them
SYSTEM_COLOUR = {"‹system 1›": "#0072B2", "‹system 2›": "#E69F00", "‹system 3›": "#009E73"}   # from the paper's figures
FOOTER = "‹Study name› · ‹site›"
N_ITEMS, N_UNITS = 0, 0                               # corpus constants, declared once (values from the registry)

W, H = 12.0, 6.75
CLAIMS, USED = {}, {}
T = THEMES["light"]


def claim(card, cid, field="value"):
    """Return a claim field and record that the card uses the claim."""
    if cid not in CLAIMS:
        raise SystemExit(f"{card}: claim {cid} not in the registry; add a pipeline step that computes it")
    USED.setdefault(card, set()).add(cid)
    return CLAIMS[cid][field]


def nums(s):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


def money(x):
    return f"\\${x:,.2f}"   # escaped: matplotlib reads paired $ signs as mathtext


def frame(eyebrow, headline, sub, caveat):
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(T["bg"])
    fig.add_artist(plt.Line2D([0, 1], [0.994, 0.994], transform=fig.transFigure, color=T["rule"], linewidth=6))
    fig.text(0.055, 0.905, eyebrow.upper(), fontfamily=MONO, fontsize=13, color=T["rule"], va="top")
    fig.text(0.055, 0.845, headline, fontfamily=SANS, fontsize=34, color=T["ink"], va="top", fontweight="semibold")
    fig.text(0.055, 0.745, sub, fontfamily=SANS, fontsize=16, color=T["soft"], va="top", linespacing=1.35)
    fig.text(0.055, 0.085, caveat, fontfamily=MONO, fontsize=10.5, color=T["faint"], va="bottom")   # caveat above footer
    fig.text(0.945, 0.035, FOOTER, fontfamily=MONO, fontsize=11, color=T["soft"], va="bottom", ha="right")
    return fig


def style(ax):
    ax.set_facecolor(T["bg"])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(T["faint"])
    ax.tick_params(colors=T["soft"], labelsize=13, length=0)
    ax.grid(axis="x", color=T["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def hbars(fig, labels, values, fmt, xmax, box=(0.30, 0.20, 0.62, 0.42)):
    """Horizontal bars in a stated order (pass labels already ordered by the paper's rule), each in its system colour,
    with the value at the bar's end. Every bar gets the same label weight."""
    ax = fig.add_axes(box)
    y = list(range(len(labels)))[::-1]
    ax.barh(y, values, color=[SYSTEM_COLOUR[l] for l in labels], height=0.62)
    for yi, v in zip(y, values):
        ax.text(v + xmax * 0.012, yi, fmt(v), va="center", fontfamily=MONO, fontsize=14, color=T["ink"])
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=14, color=T["ink"])
    ax.set_xlim(0, xmax)
    style(ax)
    return ax


# ---- cards: one function per card, returning (stem, fig) ----
def card_example():
    c = "card01-‹slug›"
    labels = ["‹system 1›", "‹system 2›", "‹system 3›"]          # in the paper's stated order
    values = [nums(claim(c, cid))[0] for cid in ("‹C-…›", "‹C-…›", "‹C-…›")]   # parsed from claims, never typed
    fig = frame("‹eyebrow›", "‹headline with the number›", "‹sub-line›",
                "‹Main runs. The caveat that keeps it true.›")
    hbars(fig, labels, values, lambda x: f"{x:g}", max(values) * 1.15)
    return c, fig


CARDS = [card_example]


def main():
    global T
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme", default="light", choices=sorted(THEMES))
    a = ap.parse_args()
    T = THEMES[a.theme]
    CLAIMS.update({r["id"]: r for r in csv.DictReader(open(a.claims, newline="", encoding="utf-8"))})
    os.makedirs(a.out, exist_ok=True)
    for make in CARDS:
        stem, fig = make()
        fig.savefig(os.path.join(a.out, stem + ".png"), dpi=200, facecolor=T["bg"])   # 2400x1350
        plt.close(fig)
    with open(os.path.join(a.out, "manifest.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["card", "claims"])
        for stem in sorted(USED):
            w.writerow([stem, ";".join(sorted(USED[stem]))])
    print(f"{len(CARDS)} cards -> {a.out}")


if __name__ == "__main__":
    main()
