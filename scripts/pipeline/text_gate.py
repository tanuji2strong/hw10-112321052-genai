"""Gate text_gate (script). Every bullet must:
  - be a complete sentence (ends with 。！？), or a short phrase of at most 12 characters
  - not be truncated
  - have no leading list marker ("- ", "• ")
  - have no outline or placeholder wording
  - have no file paths or wiki paths in the text
  - have no simplified characters (opencc s2twp is the reference)
  - have no [補充] or outside-source tag
  - have a source tag (cite)
Input: a deck HTML file (run 0) or a draft directory (slide-NN.json). Default: drafts/round<ROUND>.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DRAFTS, TERMINAL, current_round, simplified_chars, write_log  # noqa: E402
import slides_io  # noqa: E402

PLACEHOLDER = re.compile(
    r"TODO|TBD|待補|placeholder|一句話複習|用.{0,8}例子走一遍|大綱|（此處|\(此處|請補充|lorem", re.I)
PATHLIKE = re.compile(r"[\w\-]+\.(md|html|py|json|txt|mmd)\b|\bwiki/|\.\./|concepts/|misconceptions/|examples/|sources/")
OUTSIDE = re.compile(r"補充|非原始資料|outside")
MARKER = re.compile(r"^\s*[-•－·]\s*")
SHORT_MAX = 12


def check_bullet(b):
    problems = []
    t = b["text"].strip()
    if not t:
        problems.append("empty bullet")
    if MARKER.match(t):
        problems.append("leading list marker")
    if t and t[-1] not in TERMINAL and len(t) > SHORT_MAX:
        problems.append("not a complete sentence (no 。！？ and not a short phrase)")
    if PLACEHOLDER.search(t):
        problems.append("outline/placeholder wording")
    if PATHLIKE.search(t):
        problems.append("file or wiki path in text")
    bad = simplified_chars(t)
    if bad:
        problems.append("simplified characters: " + "".join(bad))
    if OUTSIDE.search(t) or OUTSIDE.search(b["cite"] or ""):
        problems.append("[補充] / outside-source tag")
    if not (b["cite"] or "").strip():
        problems.append("no source tag")
    return problems


def main(target=None):
    target = target or os.path.join(DRAFTS, f"round{current_round()}")
    bullets = slides_io.load(target)
    total_slides = slides_io.slide_count(target)
    lines = [f"text_gate: input={os.path.relpath(target)} slides={total_slides} bullets={len(bullets)}"]
    failing_slides = {}
    fails = 0
    for i, b in enumerate(bullets, 1):
        probs = check_bullet(b)
        if probs:
            fails += len(probs)
            failing_slides.setdefault(b["slide"], []).extend(probs)
            lines.append(f"  FAIL slide {b['slide']:02d} bullet {i:03d}: {'; '.join(probs)}")
            lines.append(f"       text: {b['text'][:90]}")
    lines.append(f"result: {'FAIL' if fails else 'PASS'} ({fails} problem(s))")
    if failing_slides:
        lines.append("route: redo draft only for slides " + ", ".join(f"{s:02d}" for s in sorted(failing_slides)))
    write_log("text_gate.log", lines)
    print("\n".join(lines))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
