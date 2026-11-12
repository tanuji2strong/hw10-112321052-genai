"""Gate outline_gate (script): slide count 8..15, every slide maps to >= 1 existing card, no slide without cards.
outline.md format (one block per slide):

## Slide 01 | hook | 標題
- cards: c01-what-is-an-agent, s03
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CARDS, TOPIC, write_log  # noqa: E402

MIN_SLIDES, MAX_SLIDES = 8, 15
HEAD = re.compile(r"^## Slide (\d{2}) \| (\S+) \| (.+)$")


def main():
    path = os.path.join(TOPIC, "outline.md")
    if not os.path.exists(path):
        write_log("outline_gate.log", ["outline_gate: FAIL (outline.md missing)"])
        print("outline.md missing")
        return 1
    lines = open(path, encoding="utf-8").read().split("\n")
    slides, current = [], None
    for line in lines:
        m = HEAD.match(line.strip())
        if m:
            current = {"n": int(m.group(1)), "kind": m.group(2), "title": m.group(3), "cards": None}
            slides.append(current)
        elif current is not None and line.strip().startswith("- cards:"):
            current["cards"] = [c.strip() for c in line.split(":", 1)[1].split(",") if c.strip()]
    cards = {os.path.splitext(f)[0] for f in os.listdir(CARDS) if f.endswith(".md")}
    report, failed = [], False
    n = len(slides)
    ok_count = MIN_SLIDES <= n <= MAX_SLIDES
    report.append(f"slide count: {n} (need {MIN_SLIDES}..{MAX_SLIDES}) {'PASS' if ok_count else 'FAIL'}")
    failed |= not ok_count
    expected = list(range(1, n + 1))
    nums_ok = [s["n"] for s in slides] == expected
    report.append(f"slide numbers sequential: {'PASS' if nums_ok else 'FAIL'}")
    failed |= not nums_ok
    for s in slides:
        problems = []
        if not s["cards"]:
            problems.append("no cards")
        else:
            missing = [c for c in s["cards"] if c not in cards]
            if missing:
                problems.append("unknown card(s): " + ", ".join(missing))
        status = "PASS" if not problems else "FAIL"
        failed |= bool(problems)
        cards_txt = ", ".join(s["cards"] or [])
        report.append(f"  {status}  slide {s['n']:02d} [{s['kind']}] {s['title']}  cards: {cards_txt}"
                      + (f"  <- {'; '.join(problems)}" if problems else ""))
    report.append(f"result: {'FAIL' if failed else 'PASS'}")
    write_log("outline_gate.log", ["outline_gate"] + report)
    print("\n".join(["outline_gate"] + report))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
