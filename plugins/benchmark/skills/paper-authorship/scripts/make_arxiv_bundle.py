#!/usr/bin/env python3
"""Build the arXiv source bundle: comments stripped, main.bbl, used figures and prompts only; compile it clean; zip it.

  python3 make_arxiv_bundle.py --paper paper/ [--out paper/arxiv-source.zip]

Run after a full latexmk build, so main.bbl is current. Keep main.bbl in the upload even if arXiv's file manager
offers to delete it: arXiv does not run BibTeX, so without it every citation renders as [?]. Then run
guardrail_lint.py --fail-on-comments on the unpacked copy the script prints, and check arXiv's compiled preview.

What goes in: main.tex and every .tex file it reaches through \\input / \\include (comments stripped), main.bbl,
references.bib if present, prompts/ if present, and every file named by \\includegraphics or \\lstinputlisting
(a graphics path without an extension is resolved to .pdf, .png, .jpg or .eps). Exit code 1 if a referenced file is
missing or the clean compile reports errors or undefined references. Needs pdflatex; otherwise standard library only.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
GRAPHIC_EXTS = (".pdf", ".png", ".jpg", ".jpeg", ".eps")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
LISTING_RE = re.compile(r"\\lstinputlisting(?:\[[^\]]*\])?\{([^}]+)\}")


def strip_comments(text):
    """Drop comment-only lines; cut inline comments but keep the '%' so line joining is unchanged.
    A % after an odd number of backslashes is a literal percent sign."""
    out = []
    for line in text.split("\n"):
        cut = None
        for i, ch in enumerate(line):
            if ch == "%":
                j, n = i - 1, 0
                while j >= 0 and line[j] == "\\":
                    n += 1
                    j -= 1
                if n % 2 == 0:
                    cut = i
                    break
        if cut is not None:
            if not line[:cut].strip():
                continue
            line = line[:cut] + "%"
        out.append(line)
    return "\n".join(out) + "\n"


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def tex_closure(paper):
    """main.tex plus every .tex file reachable through \\input / \\include, as paths relative to the paper folder."""
    seen, todo = [], ["main.tex"]
    while todo:
        rel = os.path.normpath(todo.pop(0))
        if rel in seen:
            continue
        path = os.path.join(paper, rel)
        if not os.path.isfile(path):
            sys.exit(f"missing input: {rel}")
        seen.append(rel)
        for ref in INPUT_RE.findall(strip_comments(read(path))):
            todo.append(ref if ref.endswith(".tex") else ref + ".tex")
    return seen


def resolve_graphic(paper, ref):
    if os.path.splitext(ref)[1].lower() in GRAPHIC_EXTS:
        return ref if os.path.isfile(os.path.join(paper, ref)) else None
    for ext in GRAPHIC_EXTS:
        if os.path.isfile(os.path.join(paper, ref + ext)):
            return ref + ext
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", default="paper", help="paper folder with main.tex, main.bbl and the files they use")
    ap.add_argument("--out", help="zip to write (default: <paper>/arxiv-source.zip)")
    a = ap.parse_args()
    paper = os.path.abspath(a.paper)
    out = os.path.abspath(a.out) if a.out else os.path.join(paper, "arxiv-source.zip")
    for need in ("main.tex", "main.bbl"):
        if not os.path.isfile(os.path.join(paper, need)):
            sys.exit(f"{need} missing in {paper}" + (": run a full build (latexmk) first" if need == "main.bbl" else ""))

    bundle = tempfile.mkdtemp(prefix="arxiv-bundle-")
    missing = []

    def put(rel, text=None):
        dst = os.path.join(bundle, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if text is None:
            shutil.copy(os.path.join(paper, rel), dst)
        else:
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(text)

    texs = tex_closure(paper)
    used = set()
    for rel in texs:
        clean = strip_comments(read(os.path.join(paper, rel)))
        put(rel, clean)
        for ref in GRAPHICS_RE.findall(clean):
            hit = resolve_graphic(paper, ref)
            (used.add(hit) if hit else missing.append(ref))
        for ref in LISTING_RE.findall(clean):
            (used.add(ref) if os.path.isfile(os.path.join(paper, ref)) else missing.append(ref))
    put("main.bbl")
    if os.path.isfile(os.path.join(paper, "references.bib")):
        put("references.bib")
    if os.path.isdir(os.path.join(paper, "prompts")):
        shutil.copytree(os.path.join(paper, "prompts"), os.path.join(bundle, "prompts"), dirs_exist_ok=True)
    for rel in sorted(used):
        put(rel)
    if missing:
        print(f"referenced but missing: {sorted(set(missing))}")

    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"], cwd=bundle,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log_path = os.path.join(bundle, "main.log")
    log = open(log_path, encoding="latin-1").read() if os.path.isfile(log_path) else ""
    problems = [l for l in log.splitlines() if l.startswith("!") or "undefined" in l.lower()]
    pages = re.search(r"Output written on main\.pdf \((\d+) pages?", log)
    for f in glob.glob(os.path.join(bundle, "main.*")):
        if not f.endswith((".tex", ".bbl")):
            os.remove(f)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(bundle):
            for f in sorted(files):
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, bundle))
    print(f"bundle: {len(texs)} tex files, {len(used)} graphics/listings, "
          f"{pages.group(1) if pages else '?'} pages, problems: {problems or 'none'} -> {out}")
    print(f"unpacked copy for inspection: {bundle}")
    sys.exit(1 if (problems or missing or not pages) else 0)


if __name__ == "__main__":
    main()
