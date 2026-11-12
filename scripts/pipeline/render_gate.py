"""Gate render_gate (Playwright, Chromium headless).
- slide count must be 8..15
- every slide is screenshotted at 1280x720 to checks/roundN/render/slide-NN.png
- fail on overflow: scrollHeight > clientHeight (fix by shortening the draft, never by shrinking fonts)
- fail on broken links (relative href must exist on disk)
- keyboard navigation must move to the next slide on ArrowRight
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CHECKS, TOPIC, current_round, write_log  # noqa: E402

from playwright.sync_api import sync_playwright  # noqa: E402


def main(deck=None):
    deck = deck or os.path.join(TOPIC, "deck.html")
    shots = os.path.join(CHECKS, f"round{current_round()}", "render")
    os.makedirs(shots, exist_ok=True)
    lines = [f"render_gate: deck={os.path.relpath(deck)} viewport=1280x720"]
    failed = False
    deck_dir = os.path.dirname(os.path.abspath(deck))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("file://" + os.path.abspath(deck))
        page.wait_for_load_state()
        count = page.evaluate("document.querySelectorAll('.slide').length")
        ok_count = 8 <= count <= 15
        lines.append(f"slide count: {count} (need 8..15) {'PASS' if ok_count else 'FAIL'}")
        failed |= not ok_count

        # keyboard navigation: ArrowRight must move from slide 1 to slide 2
        page.evaluate("document.querySelectorAll('.slide').forEach(s=>s.classList.remove('active'));"
                      "document.querySelector('.slide').classList.add('active')")
        page.keyboard.press("ArrowRight")
        active = page.evaluate("[...document.querySelectorAll('.slide')].findIndex(s=>s.classList.contains('active'))")
        nav_ok = active == 1
        lines.append(f"keyboard ArrowRight from slide 1 -> index {active} {'PASS' if nav_ok else 'FAIL'}")
        failed |= not nav_ok

        for i in range(count):
            page.evaluate("(n)=>window.deckShow(n)", i)
            page.wait_for_timeout(60)
            m = page.evaluate("""(n)=>{const s=document.querySelectorAll('.slide')[n];
                const r=s.getBoundingClientRect();
                return {sh:s.scrollHeight, ch:s.clientHeight, title:(s.querySelector('h1,h2')||{}).textContent||''}}""", i)
            over = m["sh"] > m["ch"] + 1
            failed |= over
            page.locator(".slide.active").screenshot(path=os.path.join(shots, f"slide-{i + 1:02d}.png"))
            lines.append(f"  slide {i + 1:02d} overflow {'FAIL' if over else 'ok'} "
                         f"(scrollHeight {m['sh']} / clientHeight {m['ch']}) {m['title'][:30]}")

        hrefs = page.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
        broken = []
        for h in hrefs:
            if h.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = os.path.normpath(os.path.join(deck_dir, h.split("#")[0]))
            if not os.path.exists(target):
                broken.append(h)
        lines.append(f"links checked: {len(hrefs)}; broken: {len(broken)}")
        for b in broken:
            lines.append(f"  BROKEN {b}")
        failed |= bool(broken)
        browser.close()
    lines.append(f"result: {'FAIL' if failed else 'PASS'}")
    write_log("render_gate.log", lines)
    print("\n".join(lines))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
