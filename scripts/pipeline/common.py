"""Shared helpers for the topic-slides graph pipeline. Standard library + opencc."""
import glob
import html
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI = os.path.join(ROOT, "wiki")
RAW = os.path.join(ROOT, "raw")
TOPIC = os.path.join(ROOT, "topic-ai-agents")
CARDS = os.path.join(TOPIC, "cards")
DRAFTS = os.path.join(TOPIC, "drafts")
CHECKS = os.path.join(TOPIC, "checks")
OUTPUT = os.path.join(ROOT, "output")

NON_CONTENT = {"index.md", "log.md", "lint-report.md", "ingest-summary.md"}
CONTENT_DIRS = ("sources", "concepts", "misconceptions", "examples")
TERMINAL = "。！？"
QUOTE_RE = re.compile(r'^>\s*"(.+)"\s*\[(S\d{2})\]\s*$')


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def norm(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def wiki_pages(content_only=True):
    """Return wiki page paths (repo-relative, e.g. wiki/concepts/c01-...md)."""
    out = []
    for p in glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True):
        base = os.path.basename(p)
        if content_only:
            if base in NON_CONTENT and os.path.dirname(p) == WIKI:
                continue
            if os.path.relpath(p, WIKI).split(os.sep)[0] not in CONTENT_DIRS + ("glossary.md",):
                if base != "glossary.md":
                    continue
        out.append(rel(p))
    return sorted(out)


def read_rel(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def raw_text(tag):
    n = int(tag[1:])
    matches = glob.glob(os.path.join(RAW, f"{n:02d}_*.md"))
    if len(matches) != 1:
        return None
    with open(matches[0], encoding="utf-8") as f:
        return norm(f.read())


def current_round():
    return int(os.environ.get("ROUND", "1"))


def write_log(name, lines):
    """Write checks/roundN/<name> (N from env ROUND, default 1; run 0 = ROUND=0)."""
    path = os.path.join(CHECKS, f"round{current_round()}", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def today():
    return date.today().isoformat()


def strip_html(s):
    s = re.sub(r"(?s)<[^>]+>", "", s)
    return html.unescape(re.sub(r"[ \t]+", " ", s)).strip()


def simplified_chars(text):
    """Characters whose Taiwan-standard form (opencc s2twp, per character) differs from the input."""
    from opencc import OpenCC
    conv = OpenCC("s2twp")
    bad = []
    for ch in text:
        if ch.strip() and ch not in bad and conv.convert(ch) != ch:
            bad.append(ch)
    return bad
