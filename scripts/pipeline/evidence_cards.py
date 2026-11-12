"""Node evidence_cards: one card per wiki page. A card contains only text copied from that page:
its path, its title, its verbatim quote lines, and its bullet claims. Output: topic-ai-agents/cards/<stem>.md
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CARDS, QUOTE_RE, read_rel, wiki_pages, write_log  # noqa: E402

os.makedirs(CARDS, exist_ok=True)


def card_id(path):
    return os.path.splitext(os.path.basename(path))[0]


def main():
    pages = wiki_pages()
    made = []
    for p in pages:
        text = read_rel(p)
        lines = text.split("\n")
        title = next((l[2:].strip() for l in lines if l.startswith("# ")), card_id(p))
        quotes = [l.strip() for l in lines if QUOTE_RE.match(l.strip())]
        bullets = [l.strip() for l in lines if l.strip().startswith("- ")]
        body = [
            f"# card: {card_id(p)}",
            "",
            f"- page: `{p}`",
            f"- title: {title}",
            "",
            "## Verbatim quotes (copied from the page)",
            "",
        ]
        body += quotes if quotes else ["(none)"]
        body += ["", "## Claims (copied from the page)", ""]
        body += bullets if bullets else ["(none)"]
        body.append("")
        out = os.path.join(CARDS, card_id(p) + ".md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(body))
        made.append((card_id(p), p, len(quotes), len(bullets)))

    # Self-check: every non-empty card line must appear in its source page (cards copy only).
    problems = []
    for cid, p, _, _ in made:
        page_norm = re.sub(r"\s+", " ", read_rel(p).replace("`", ""))
        with open(os.path.join(CARDS, cid + ".md"), encoding="utf-8") as f:
            for line in f.read().split("\n"):
                s = line.strip()
                if not s or s.startswith("#") or s.startswith("- page:") or s.startswith("- title:") or s in ("(none)",):
                    continue
                s2 = re.sub(r"\s+", " ", s.replace("`", ""))
                if s2.startswith("- "):
                    s2 = s2[2:]
                if s2 not in page_norm:
                    problems.append(f"{cid}: line not found in page: {s2[:60]}")
    log = [
        "evidence_cards",
        f"cards written: {len(made)}",
    ] + [f"  {cid}: quotes={q} claims={b}  <- {p}" for cid, p, q, b in made] + [
        f"self-check problems: {len(problems)}",
    ] + [f"  {x}" for x in problems]
    write_log("evidence_cards.log", log)
    print("\n".join(log[:2]), f"(problems: {len(problems)})")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
