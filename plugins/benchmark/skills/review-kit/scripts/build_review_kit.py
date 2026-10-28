#!/usr/bin/env python3
"""Skeleton builder for an internal review-kit PDF (reportlab). Reproducible: same inputs, same pages.

  python3 build_review_kit.py --spec kit.json --claims tables/claims.csv --out review-kit-v1.pdf [--render-dir pages/]

kit.json: {"title", "version", "new_in": ["…"], "corrections": ["…"], "footer": "Internal review draft, not for distribution",
           "sections": [{"heading", "body": ["paragraph with {C-ID} placeholders"], "box": {"title", "text"},
                         "image": "figure.png", "checks": ["yes/no question"]}]}
Every {C-ID} placeholder is replaced by the claim's value from the claims CSV, so numbers cannot drift from the ledger.
An unknown claim ID aborts the build. Every section's "checks" are repeated on a one-page checklist at the end. Requires
`pip install reportlab`. --render-dir also renders each page to PNG (needs poppler's pdftoppm, skipped with a warning if absent) so you can check overflow
and readability before sharing. Charts: generate them from tables/ with a script, never by hand.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def load_claims(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["id"]: r for r in csv.DictReader(fh)}


def fill(text, claims):
    def sub(m):
        cid = m.group(1)
        if cid not in claims:
            sys.exit(f"unknown claim id in kit spec: {cid}")
        r = claims[cid]
        kn = f" ({r['numerator']}/{r['denominator']})" if r.get("numerator") and r.get("denominator") else ""
        try:
            val = f"{float(r['value']):.4g}"
        except ValueError:
            val = r["value"]
        return f"{val}{kn} [{cid}]"
    return re.sub(r"\{(C-[A-Z0-9]+-[0-9]+(?:-[A-Za-z][A-Za-z0-9+.]*)?)\}", sub, text)  # same shape as common.ID_RE


def box(title, text, styles, fill_color):
    t = Table([[Paragraph(f"<b>{title}</b><br/>{text}", styles["BodyText"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fill_color), ("BOX", (0, 0), (-1, -1), 0.6, colors.grey),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--claims", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--render-dir")
    a = ap.parse_args()
    spec, claims = json.load(open(a.spec)), load_claims(a.claims)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("Check", parent=styles["BodyText"], leftIndent=12))
    footer = spec.get("footer", "Internal review draft, not for distribution")

    def on_page(c, d):
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(20 * mm, 10 * mm, f"{footer} · v{spec['version']}")
        c.drawRightString(190 * mm, 10 * mm, f"Page {d.page}")

    doc = SimpleDocTemplate(a.out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title=spec["title"], author="", invariant=True)
    flow = [Paragraph(spec["title"], styles["Title"]), Paragraph(f"Version {spec['version']}", styles["Normal"]), Spacer(1, 6)]
    if spec.get("new_in"):
        flow.append(box(f"New in v{spec['version']}", "<br/>".join(f"• {fill(x, claims)}" for x in spec["new_in"]), styles, colors.HexColor("#eef6ff")))
    for c in spec.get("corrections", []):
        flow += [Spacer(1, 4), box("Correction", fill(c, claims), styles, colors.HexColor("#fff4e5"))]
    all_checks = []
    for s in spec["sections"]:
        part = [Spacer(1, 8), Paragraph(s["heading"], styles["Heading2"])]
        part += [Paragraph(fill(p, claims), styles["BodyText"]) for p in s.get("body", [])]
        if s.get("box"):
            part += [Spacer(1, 4), box(s["box"]["title"], fill(s["box"]["text"], claims), styles, colors.HexColor("#f3f3f3"))]
        if s.get("image"):
            part.append(Image(s["image"], width=165 * mm, height=95 * mm, kind="proportional"))
        for q in s.get("checks", []):
            part.append(Paragraph(f"[ ] {fill(q, claims)}  (yes / no)", styles["Check"]))
            all_checks.append((s["heading"], fill(q, claims)))
        flow.append(KeepTogether(part) if len(part) < 8 else part[0])
        if len(part) >= 8:
            flow += part[1:]
    if all_checks:
        flow += [PageBreak(), Paragraph("Reviewer checklist (one page)", styles["Heading2"])]
        flow.append(Table([["Section", "Check", "Yes", "No", "Comment"]] + [[Paragraph(h, styles["BodyText"]), Paragraph(q, styles["BodyText"]), "", "", ""] for h, q in all_checks],
                          colWidths=[30 * mm, 80 * mm, 12 * mm, 12 * mm, 36 * mm], repeatRows=1,
                          style=TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee"))])))
    doc.build(flow, onFirstPage=on_page, onLaterPages=on_page)
    if a.render_dir:
        os.makedirs(a.render_dir, exist_ok=True)
        try:
            subprocess.run(["pdftoppm", "-r", "60", "-png", a.out, os.path.join(a.render_dir, "page")], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("WARNING: pdftoppm unavailable or failed; pages not rendered. Install poppler and re-run before sharing.", file=sys.stderr)
    print(f"built {a.out}")


if __name__ == "__main__":
    main()
