"""Node retrieve_wiki: list wiki pages relevant to each planned section -> topic-ai-agents/sources.md"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TOPIC, load_json, read_rel, wiki_pages, today  # noqa: E402

SECTIONS = os.path.join(TOPIC, "sections.json")
OUT = os.path.join(TOPIC, "sources.md")


def main():
    plan = load_json(SECTIONS)["sections"]
    pages = wiki_pages()
    texts = {p: read_rel(p) for p in pages}
    lines = [
        "# sources.md（retrieve_wiki 輸出）",
        "",
        f"- Date: {today()}",
        f"- Wiki pages scanned: {len(pages)}",
        "- Rule: a page is relevant to a section if any keyword occurs in the page (case-insensitive).",
        "",
    ]
    result = {}
    for sec in plan:
        hits = []
        for p in pages:
            low = texts[p].lower()
            matched = [k for k in sec["keywords"] if k.lower() in low]
            if matched:
                hits.append((p, matched))
        result[sec["id"]] = hits
        lines.append(f"## {sec['id']} {sec['title']}")
        lines.append(f"- keywords: {', '.join(sec['keywords'])}")
        lines.append(f"- relevant pages: {len(hits)}")
        for p, m in hits:
            lines.append(f"  - `{p}` (matched: {', '.join(m)})")
        lines.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"retrieve_wiki: wrote {os.path.relpath(OUT)} ({len(plan)} sections, {len(pages)} pages)")
    for sec in plan:
        print(f"  {sec['id']} {len(result[sec['id']])} page(s)  {sec['title']}")


if __name__ == "__main__":
    main()
