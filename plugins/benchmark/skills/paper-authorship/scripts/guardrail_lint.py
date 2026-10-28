#!/usr/bin/env python3
"""Lint a LaTeX paper against a rules file built from the narrative guideline.

  python3 guardrail_lint.py --rules paper/guardrail-rules.txt --tex paper/sections paper/main.tex \\
      [paper/prompts/*.txt paper/references.bib] [--check-comments | --fail-on-comments]

Rules file: one rule per line, '#' for comments; fields separated by ' | ' (spaces required, so '|' inside a regex is alternation):
  <severity> | <kind> | <regex> | <reason>
  severity: block | review | nit
  kind:     forbid | require | superlative | placeholder
Regexes are Python syntax, matched case-insensitively.

How text is matched
  * .tex files: LaTeX comments are removed (a % after an odd number of backslashes is a literal percent sign), then the
    lines of each paragraph are joined with spaces, so a phrase or a disclosure that wraps across lines still matches.
    `require` rules ignore section headings: a heading such as "Data and code availability" does not count as the
    disclosure itself.
  * .md files passed explicitly (README, release notes, a blog draft): every rule except `require` (those are
    paper-level), paragraphs joined the same way, no comment stripping.
  * Any other file passed explicitly (prompts, .bib): only `placeholder` rules, plus angle-bracket tokens such as
    <date> reported for review (prompts sometimes contain them on purpose).
--check-comments reports claim IDs and notes inside LaTeX comments (they ship in an arXiv source bundle);
--fail-on-comments does the same and exits 1 if there are any (use it on the stripped arXiv bundle).
Exit code 1 if any 'block' rule fires (a forbid/placeholder hit, or a require rule with no match). Standard library only.
"""
import argparse
import bisect
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idpattern import ID_RE, split_comment, tex_files  # noqa: E402  (shared with check_claims and the ledger)

HEADING_RE = re.compile(r"\\(?:(?:sub)*section|paragraph|chapter|title)\*?\s*(?:\[[^\]]*\])?\{[^{}]*\}")
ANGLE_RE = re.compile(r"<[A-Za-z][^<>\n]{0,60}>")
COMMENT_NOTE_RE = re.compile(r"TODO|FIXME|internal|ledger|inventory", re.I)


def load_rules(path):
    rules = []
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"\s+\|\s+", line)
        if len(parts) < 4:
            sys.exit(f"{path}:{n}: expected 'severity | kind | regex | reason' with spaces around the separators")
        sev, kind, rx, reason = parts[0], parts[1], " | ".join(parts[2:-1]), parts[-1]
        if sev not in ("block", "review", "nit") or kind not in ("forbid", "require", "superlative", "placeholder"):
            sys.exit(f"{path}:{n}: unknown severity or kind")
        try:
            rules.append((sev, kind, re.compile(rx, re.I), reason, n))
        except re.error as e:
            sys.exit(f"{path}:{n}: invalid regex ({e})")
    return rules


def joined_tex(path, latex=True):
    """(text, line_of(pos), comments): comment-free text with each paragraph on one line."""
    parts, offsets, lines, comments = [], [], [], []
    pos = 0
    for ln, raw in enumerate(open(path, encoding="utf-8"), 1):
        text, comment = split_comment(raw.rstrip("\n")) if latex else (raw.rstrip("\n"), "")
        if comment:
            comments.append((ln, comment))
        s = text.strip()
        if not s:
            if parts and parts[-1] != "\n":
                parts.append("\n")
                pos += 1
            continue
        if parts and parts[-1] != "\n":
            parts.append(" ")
            pos += 1
        offsets.append(pos)
        lines.append(ln)
        parts.append(s)
        pos += len(s)
    text = "".join(parts)

    def line_of(p):
        i = bisect.bisect_right(offsets, p) - 1
        return lines[i] if i >= 0 else 1
    return text, line_of, comments


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", required=True)
    ap.add_argument("--tex", nargs="+", required=True)
    ap.add_argument("--check-comments", action="store_true")
    ap.add_argument("--fail-on-comments", action="store_true")
    a = ap.parse_args()
    rules = load_rules(a.rules)
    files = tex_files(a.tex)
    if not any(f.endswith((".tex", ".md")) for f in files):
        sys.exit(f"--tex {a.tex}: no .tex or .md files found")
    hits = {"block": [], "review": [], "nit": []}
    found_require = {i: False for i, r in enumerate(rules) if r[1] == "require"}
    comment_hits = []

    for f in files:
        rel = os.path.relpath(f)
        is_tex, is_md = f.endswith(".tex"), f.endswith(".md")
        if not (is_tex or is_md):
            raw = open(f, encoding="utf-8").read()
            for sev, kind, rx, reason, rn in rules:
                if kind == "placeholder":
                    for m in rx.finditer(raw):
                        hits[sev].append(f"{rel}:{raw.count(chr(10), 0, m.start()) + 1}  [placeholder] '{m.group(0)}' — {reason}")
            for m in ANGLE_RE.finditer(raw):
                hits["review"].append(f"{rel}:{raw.count(chr(10), 0, m.start()) + 1}  [placeholder?] '{m.group(0)}' — angle-bracket token; fill it unless the prompt uses it on purpose")
            continue
        text, line_of, comments = joined_tex(f, latex=is_tex)
        for ln, comment in comments:
            if ID_RE.search(comment) or COMMENT_NOTE_RE.search(comment):
                comment_hits.append(f"{rel}:{ln} {comment.strip()[:100]}")
        for m in ID_RE.finditer(text):
            hits["block"].append(f"{rel}:{line_of(m.start())}  internal claim ID in text: {m.group(0)}")
        text_for_require = HEADING_RE.sub(" ", text)
        for i, (sev, kind, rx, reason, rn) in enumerate(rules):
            if kind == "require":
                if is_tex and not found_require[i] and rx.search(text_for_require):
                    found_require[i] = True
                continue
            for m in rx.finditer(text):
                ctx = text[max(0, m.start() - 40):m.end() + 40].strip()
                hits[sev].append(f"{rel}:{line_of(m.start())}  [{kind}] '{m.group(0)}' — {reason}  …{ctx}…")

    any_tex = any(f.endswith(".tex") for f in files)  # require rules are paper-level: skip them for a README-only run
    for i, ok in found_require.items():
        if any_tex and not ok:
            sev, kind, rx, reason, rn = rules[i]
            hits[sev].append(f"(rule line {rn}) required disclosure not found: {reason}")

    for sev in ("block", "review", "nit"):
        if hits[sev]:
            print(f"\n== {sev.upper()} ({len(hits[sev])})")
            for h in hits[sev]:
                print("  " + h)
    if (a.check_comments or a.fail_on_comments) and comment_hits:
        print(f"\n== COMMENTS that would ship in an arXiv source bundle ({len(comment_hits)})")
        for h in comment_hits:
            print("  " + h)
    print(f"\n{len(files)} files, {len(rules)} rules.")
    if hits["block"] or (a.fail_on_comments and comment_hits):
        sys.exit(1)
    print("no blocking guardrail hits")


if __name__ == "__main__":
    main()
