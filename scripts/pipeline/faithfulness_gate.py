"""Gate faithfulness_gate (script).
For every bullet:
  - the cite must resolve to an existing wiki page (wiki/...md)
  - every quote must appear verbatim (whitespace and quote-mark normalized) in the cited wiki page
  - every number in the bullet text must appear in the cited wiki page
Input: deck HTML (run 0) or draft directory (slide-NN.json). Default: drafts/round<ROUND>.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DRAFTS, ROOT, current_round, norm, read_rel, write_log  # noqa: E402
import slides_io  # noqa: E402

WIKI_PATH = re.compile(r"wiki/[\w\-./]+\.md")
NUMBER = re.compile(r"\d+(?:\.\d+)?%?")


def resolve_cite(cite):
    m = WIKI_PATH.search(cite or "")
    if not m:
        return None, "cite is not a wiki page path"
    p = m.group(0)
    if not os.path.exists(os.path.join(ROOT, p)):
        return None, f"cited wiki page does not exist: {p}"
    return p, None


def main(target=None):
    target = target or os.path.join(DRAFTS, f"round{current_round()}")
    bullets = slides_io.load(target)
    lines = [f"faithfulness_gate: input={os.path.relpath(target)} bullets={len(bullets)}"]
    fails, failing_slides = 0, {}
    checked_quotes = checked_numbers = 0
    for i, b in enumerate(bullets, 1):
        probs = []
        page, err = resolve_cite(b["cite"])
        if err:
            probs.append(err)
        if page:
            page_text = norm(read_rel(page))
            if b.get("quote"):
                checked_quotes += 1
                if norm(b["quote"]) not in page_text:
                    probs.append(f"quote not verbatim in {page}: {b['quote'][:60]}")
            for num in NUMBER.findall(b["text"]):
                checked_numbers += 1
                if num not in page_text:
                    probs.append(f"number {num} not found in {page}")
        if probs:
            fails += len(probs)
            failing_slides.setdefault(b["slide"], []).extend(probs)
            lines.append(f"  FAIL slide {b['slide']:02d} bullet {i:03d}: {'; '.join(probs)}")
            lines.append(f"       text: {b['text'][:90]}")
    lines.append(f"quotes checked: {checked_quotes}; numbers checked: {checked_numbers}")
    lines.append(f"result: {'FAIL' if fails else 'PASS'} ({fails} problem(s))")
    if failing_slides:
        lines.append("route: redo draft only for slides " + ", ".join(f"{s:02d}" for s in sorted(failing_slides))
                     + " (other slides unchanged)")
    write_log("faithfulness_gate.log", lines)
    print("\n".join(lines))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
