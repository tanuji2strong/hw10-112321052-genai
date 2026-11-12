"""Gate coverage_gate: every planned section must have >= 3 relevant wiki pages (from sources.md).
Fail -> stop and report to the user; do not pad with outside knowledge.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import TOPIC, write_log, current_round  # noqa: E402

MIN_PAGES = 3


def main(round_no=None):
    round_no = round_no or current_round()
    text = open(os.path.join(TOPIC, "sources.md"), encoding="utf-8").read()
    secs = re.findall(r"## (sec-\d+) (.+)\n- keywords: .*\n- relevant pages: (\d+)", text)
    lines = [f"coverage_gate (round {round_no}): need >= {MIN_PAGES} relevant pages per section"]
    failed = []
    for sid, title, n in secs:
        ok = int(n) >= MIN_PAGES
        lines.append(f"  {'PASS' if ok else 'FAIL'}  {sid}  {int(n):2d} page(s)  {title}")
        if not ok:
            failed.append(sid)
    lines.append(f"result: {'PASS' if not failed else 'FAIL'} ({len(secs) - len(failed)}/{len(secs)} sections covered)")
    if failed:
        lines.append("stop rule: fewer than 3 relevant pages for " + ", ".join(failed) + " -> stop and report")
    write_log("coverage_gate.log", lines)
    print("\n".join(lines))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
