"""Read slides into one bullet record format, from either:
  - a single HTML deck (run 0 legacy output), or
  - a draft directory with slide-NN.json files (new pipeline).

Bullet record: {"slide": int, "text": str, "cite": str, "quote": str|None}
"""
import glob
import json
import os
import re

from common import strip_html

LI_RE = re.compile(r"(?s)<li[^>]*>(.*?)</li>")
SRC_SPAN_RE = re.compile(r'(?s)<span class="src">(.*?)</span>')


def from_html(path):
    text = open(path, encoding="utf-8").read()
    parts = re.split(r'(?=<section class="slide)', text)
    out = []
    slide_no = 0
    for part in parts:
        if not part.startswith("<section"):
            continue
        slide_no += 1
        for li in LI_RE.findall(part):
            cite_m = SRC_SPAN_RE.search(li)
            cite = strip_html(cite_m.group(1)) if cite_m else ""
            body = SRC_SPAN_RE.sub("", li)
            out.append({"slide": slide_no, "text": strip_html(body), "cite": cite, "quote": None})
    return out


def from_drafts(directory):
    out = []
    files = sorted(glob.glob(os.path.join(directory, "slide-*.json")))
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        for b in data.get("bullets", []):
            out.append({
                "slide": int(data["n"]),
                "text": b.get("text", ""),
                "cite": b.get("cite", ""),
                "quote": b.get("quote"),
            })
    return out


def load(path):
    if os.path.isdir(path):
        return from_drafts(path)
    return from_html(path)


def slide_count(path):
    if os.path.isdir(path):
        return len(glob.glob(os.path.join(path, "slide-*.json")))
    return open(path, encoding="utf-8").read().count('<section class="slide')
