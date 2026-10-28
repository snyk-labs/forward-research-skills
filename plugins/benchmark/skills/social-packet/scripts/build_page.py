#!/usr/bin/env python3
"""Build the launch page from a content file, refusing to write it unless every check passes.

  python3 build_page.py --content social/page_content.py --template social/page-template.html \\
      --claims analysis/tables/claims.csv --cards social/cards --out social/page.html [--standalone]

The content file is plain Python (copy assets/page-content-template.py) defining META, STRUCTURAL, CARDS, STAGE, TERMS,
FINDINGS, QUOTES, LINKEDIN, X and GUARDRAILS. Checks:
  1. every claim ID cited exists in the registry;
  2. every card referenced is declared in CARDS and exists as <cards>/<card>.png;
  3. every number in a claim-tagged item equals one of its claims' values, numerators or denominators at the precision
     written (a stored rate may be written as a percent), or is declared in STRUCTURAL with a reason;
  4. every X post fits in 280 characters with the paper link appended, counting each URL as 23 characters, as X does
     (characters X counts double, such as emoji, are not modelled: keep a margin);
  5. every quote attribution says "draft";
  6. every finding declares which systems it reflects well and badly on ("favours" and "against", lists, may be empty),
     and the build prints the balance across the set for the human to judge;
  7. a disclosure line is set, it appears on the page, and at least one post per channel carries it (discloses=True).
--standalone wraps the page in a full HTML document (for a static file); without it the output is a page body for a
host that adds the document skeleton (for example a published Claude artifact). Standard library only.
"""
import argparse
import csv
import json
import os
import re
import runpy
import sys
from collections import Counter

sys.dont_write_bytecode = True
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?!\w)(?!\.\d)")
URL = re.compile(r"(https?://\S+|\b[\w-]+(?:\.[\w-]+)*\.(?:com|io|dev|org|net|ai|app|co)(?:/\S*)?)")


def stated_numbers(text):
    """[(raw, value, decimals, is_percent)] for every number in text (URLs removed first)."""
    t = URL.sub(" ", text)
    out = []
    for m in NUM.finditer(t):
        raw = m.group(1).replace(",", "")
        tail = t[m.end():m.end() + 8].lstrip()
        out.append((m.group(1), float(raw), len(raw.split(".")[1]) if "." in raw else 0,
                    tail.startswith("%") or tail.lower().startswith("percent")))
    return out


def registry_numbers(row):
    vals = []
    for f in ("value", "numerator", "denominator"):
        for m in NUM.finditer(str(row.get(f, "") or "")):
            vals.append(float(m.group(1).replace(",", "")))
    return vals


def matches(x, dec, pct, pool):
    tol = 0.5 * 10 ** -dec + 1e-9
    for r in pool:
        if abs(x - 100 * r) <= tol:
            return True
        if dec == 0 and not pct:
            if abs(r - round(r)) < 1e-9 and abs(x - r) < 1e-9:
                return True
        elif abs(x - r) <= tol:
            return True
    return False


def x_len(text, link_stub):
    return len(URL.sub("x" * 23, text + " " + link_stub))


def standalone(page, title):
    head, sep, body = page.partition("</style>")
    if not sep:
        sys.exit("template has no </style> to split head from body")
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            + head + sep + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n").replace("__TITLE__", title)


def main():
    ap = argparse.ArgumentParser()
    for k in ("content", "template", "claims", "cards", "out"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--standalone", action="store_true")
    a = ap.parse_args()
    for k in ("content", "template", "claims"):
        if not os.path.isfile(getattr(a, k)):
            sys.exit(f"--{k}: file not found: {getattr(a, k)}")
    if not os.path.isdir(a.cards):
        sys.exit(f"--cards: directory not found: {a.cards}")

    C = runpy.run_path(a.content)
    claims = {r["id"]: r for r in csv.DictReader(open(a.claims, newline="", encoding="utf-8"))}
    structural = {str(k) for k in C.get("STRUCTURAL", {})}
    errors = []

    def check_item(label, text, ids, card=None):
        for cid in ids:
            if cid not in claims:
                errors.append(f"{label}: unknown claim {cid}")
        if card is not None:
            if card not in C["CARDS"]:
                errors.append(f"{label}: card {card} not declared in CARDS")
            elif not os.path.isfile(os.path.join(a.cards, card + ".png")):
                errors.append(f"{label}: missing file {card}.png")
        pool = [v for cid in ids if cid in claims for v in registry_numbers(claims[cid])]
        stray = [raw for raw, x, dec, pct in stated_numbers(text)
                 if raw.replace(",", "") not in structural and not matches(x, dec, pct, pool)]
        if stray:
            errors.append(f"{label}: numbers not in its claims {ids} or STRUCTURAL: {stray}")

    S = C["STAGE"]
    check_item("one-liner", S["one_liner"], S.get("one_liner_claims", []))
    for i, (n, t, ids) in enumerate(S["facts"], 1):
        check_item(f"fact {i}", f"{n} {t}", ids)
    for i, (h, p, ids) in enumerate(S["why"], 1):
        check_item(f"why {i}", f"{h} {p}", ids)
    balance = Counter()
    for f in C["FINDINGS"]:
        label = f"finding {f.get('id', '?')}"
        check_item(label, " ".join([f["title"], f["message"], f["caveat"]] + f["proof"]), f["claims"], f["card"])
        if f.get("extra_card"):
            check_item(label + " extra card", "", [], f["extra_card"])
        if not isinstance(f.get("favours"), list) or not isinstance(f.get("against"), list):
            errors.append(f"{label}: declare favours=[...] and against=[...] (empty lists are fine)")
        else:
            balance.update(("favours", s) for s in f["favours"])
            balance.update(("against", s) for s in f["against"])
    for i, q in enumerate(C["QUOTES"], 1):
        check_item(f"quote {i}", q["text"], q["claims"])
        if "draft" not in q["who"].lower():
            errors.append(f"quote {i}: attribution must say draft (needs the person's approval)")
    for chan in ("LINKEDIN", "X"):
        for i, p in enumerate(C[chan], 1):
            check_item(f"{chan} {i}", p["text"], p["claims"], p["card"])
    stub = C["META"]["paper_link_stub"]
    x_counts = [x_len(p["text"], stub) for p in C["X"]]
    for i, n in enumerate(x_counts, 1):
        if n > 280:
            errors.append(f"X {i}: {n} characters with the paper link (limit 280)")
    for i, (q, ans, ids) in enumerate(C["GUARDRAILS"]["questions"], 1):
        check_item(f"question {i}", f"{q} {ans}", ids)
    disclosure = (C["META"].get("disclosure") or "").strip()
    if not disclosure:
        errors.append("META.disclosure is empty: say who ran the study and any tie to an evaluated system")
    for chan in ("LINKEDIN", "X"):
        if C[chan] and not any(p.get("discloses") for p in C[chan]):
            errors.append(f"{chan}: no post carries the disclosure (set discloses=True on at least one)")

    if errors:
        print("Page NOT written. Fix these:\n  " + "\n  ".join(errors))
        sys.exit(1)

    data = dict(meta=C["META"], stage=S, terms=C["TERMS"], findings=C["FINDINGS"], quotes=C["QUOTES"],
                linkedin=C["LINKEDIN"], x=[dict(p, n=n) for p, n in zip(C["X"], x_counts)], guard=C["GUARDRAILS"],
                cards=C["CARDS"])
    tpl = open(a.template, encoding="utf-8").read()
    if "/*__DATA__*/null" not in tpl:
        sys.exit("template has no /*__DATA__*/null slot")
    page = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = standalone(page, C["META"]["title"]) if a.standalone else page.replace("__TITLE__", C["META"]["title"])
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"{a.out} written. X lengths (with paper link): {x_counts}")
    print("Balance across findings (check it reflects the paper's weight, not a preference):")
    systems = sorted({s for _, s in balance})
    for s in systems or ["(no system named)"]:
        print(f"  {s:<28} favours {balance[('favours', s)]:>2}   against {balance[('against', s)]:>2}")


if __name__ == "__main__":
    main()
