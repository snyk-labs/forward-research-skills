#!/usr/bin/env python3
"""Extract citation identifiers (arXiv IDs and DOIs) from markdown, BibTeX or LaTeX files.

  python3 extract_ids.py prior-art-guide.md paper/references.bib > existing_ids.txt   # exclusion list for search passes
  python3 extract_ids.py paper/references.bib --against accepted_ids.txt              # bib entries not accepted by the review

arXiv IDs are taken only where they are marked as such (arXiv:2401.01234, arxiv.org/abs/..., eprint = {...}), so other
dotted numbers (costs, versions) are not mistaken for IDs. Versions (v2) are dropped. DOIs are lower-cased.
--against: print the identifiers found in the inputs that are missing from the given list, and exit 1 if any are.
Standard library only.
"""
import argparse
import re
import sys

ARXIV_RE = re.compile(r"(?:arxiv:\s*|arxiv\.org/(?:abs|pdf|html)/|eprint\s*=\s*[{\"]\s*)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>{}|\]\[`]+)", re.I)


def extract(text):
    ids = {f"arXiv:{m.group(1)}" for m in ARXIV_RE.finditer(text)}
    for m in DOI_RE.finditer(text):
        doi = m.group(1).rstrip(".,;:)*_'")
        ids.add(f"doi:{doi.lower()}")
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--against", help="file listing accepted identifiers (any format this script can read)")
    a = ap.parse_args()
    found = set()
    for f in a.files:
        try:
            found |= extract(open(f, encoding="utf-8").read())
        except OSError as e:
            sys.exit(f"cannot read {f}: {e}")
    if a.against:
        accepted = extract(open(a.against, encoding="utf-8").read())
        missing = sorted(found - accepted)
        for i in missing:
            print(i)
        print(f"{len(missing)} of {len(found)} identifiers are not in {a.against}", file=sys.stderr)
        sys.exit(1 if missing else 0)
    for i in sorted(found):
        print(i)
    print(f"{len(found)} identifiers", file=sys.stderr)


if __name__ == "__main__":
    main()
