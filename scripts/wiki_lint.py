#!/usr/bin/env python3
"""Lint the LLM Wiki. Standard library only.

Checks:
  1. broken links: relative markdown links must resolve to existing files
  2. missing citations: content pages must contain at least one [Sxx] tag
  3. quote verification: every quote line `> "..." [Sxx]` must appear
     verbatim (whitespace-normalized) in the raw file for that source
  4. orphan pages: every page must be linked from wiki/index.md

Writes wiki/lint-report.md and exits 1 if any check fails.
"""
import glob
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
RAW = os.path.join(ROOT, "raw")
REPORT = os.path.join(WIKI, "lint-report.md")
INDEX = os.path.join(WIKI, "index.md")
EXCLUDE = {"lint-report.md", "ingest-summary.md", "log.md", "index.md"}
CITE_REQUIRED_DIRS = ("sources", "concepts", "misconceptions", "examples")
CITE_REQUIRED_FILES = ("glossary.md",)

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
TAG_RE = re.compile(r"\[S\d{2}\]")
QUOTE_RE = re.compile(r'^>\s*"(.+)"\s*\[(S\d{2})\]\s*$')
QUOTE_START_RE = re.compile(r'^>\s*"')


def norm(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def wiki_pages():
    pages = []
    for path in glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True):
        pages.append(path)
    return sorted(pages)


def raw_text_for(tag):
    n = int(tag[1:])
    matches = glob.glob(os.path.join(RAW, f"{n:02d}_*.md"))
    if len(matches) != 1:
        return None
    with open(matches[0], encoding="utf-8") as f:
        return norm(f.read())


def requires_citation(path):
    rel = os.path.relpath(path, WIKI)
    parts = rel.split(os.sep)
    if parts[0] in CITE_REQUIRED_DIRS:
        return True
    return rel in CITE_REQUIRED_FILES


def main():
    errors = []
    notes = []
    pages = wiki_pages()
    index_links = set()

    with open(INDEX, encoding="utf-8") as f:
        for target in LINK_RE.findall(f.read()):
            if target.startswith(("http://", "https://", "#")):
                continue
            index_links.add(os.path.normpath(os.path.join(WIKI, target.split("#")[0])))

    checked_quotes = 0
    for page in pages:
        rel = os.path.relpath(page, ROOT)
        with open(page, encoding="utf-8") as f:
            lines = f.read().split("\n")
        text = "\n".join(lines)

        # 1. broken links
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(page), clean))
            if not os.path.exists(resolved):
                errors.append(f"[broken-link] {rel}: '{target}' does not exist")

        # 2. missing citations
        if requires_citation(page) and not TAG_RE.search(text):
            errors.append(f"[missing-citation] {rel}: no [Sxx] source tag")

        # 3. quote verification
        for i, line in enumerate(lines, 1):
            if not QUOTE_START_RE.match(line):
                continue
            m = QUOTE_RE.match(line)
            if not m:
                errors.append(f"[quote-format] {rel}:{i}: quote line must end with [Sxx]")
                continue
            quote, tag = m.group(1), m.group(2)
            raw = raw_text_for(tag)
            if raw is None:
                errors.append(f"[quote-source] {rel}:{i}: no unique raw file for {tag}")
                continue
            checked_quotes += 1
            if norm(quote) not in raw:
                errors.append(f"[quote-mismatch] {rel}:{i}: not found verbatim in {tag}: {quote[:70]}...")

    # 4. orphan pages
    for page in pages:
        base = os.path.basename(page)
        rel = os.path.relpath(page, ROOT)
        if base in EXCLUDE and os.path.dirname(page) == WIKI:
            continue
        if os.path.normpath(page) not in index_links:
            errors.append(f"[orphan] {rel}: not linked from wiki/index.md")

    today = date.today().isoformat()
    status = "PASS" if not errors else "FAIL"
    body = [
        "# Lint report",
        "",
        f"- Date: {today}",
        f"- Pages checked: {len(pages)}",
        f"- Quotes verified: {checked_quotes}",
        f"- Result: **{status}**",
        f"- Errors: {len(errors)}",
        "",
        "## Errors",
        "",
    ]
    body += [f"- {e}" for e in errors] if errors else ["None."]
    body += ["", "## Checks", "",
             "1. broken links (relative markdown links resolve)",
             "2. missing citations (content pages contain [Sxx] tags)",
             "3. quote verification (each quote line appears verbatim in its raw file)",
             "4. orphan pages (each page is linked from wiki/index.md)", ""]
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(body))
    print(f"lint {status}: {len(errors)} error(s), {checked_quotes} quote(s) verified, {len(pages)} page(s)")
    for e in errors:
        print("  " + e)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
