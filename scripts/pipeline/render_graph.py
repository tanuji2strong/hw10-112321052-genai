"""Render topic-ai-agents/graph.mmd to topic-ai-agents/graph.png with Mermaid (loaded from jsDelivr) in headless Chromium."""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MMD = os.path.join(ROOT, "topic-ai-agents", "graph.mmd")
PNG = os.path.join(ROOT, "topic-ai-agents", "graph.png")
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.0/dist/mermaid.min.js"


def main():
    code = open(MMD, encoding="utf-8").read()
    code = "\n".join(l for l in code.split("\n") if not l.startswith("%%"))
    page_html = f"""<!doctype html><html><head><meta charset="utf-8">
<style>body{{margin:0;background:#fff;font-family:'Noto Sans TC','PingFang TC',sans-serif}}
#wrap{{display:inline-block;padding:24px;background:#fff}}</style></head>
<body><div id="wrap"><pre class="mermaid">{code}</pre></div>
<script src="{MERMAID}"></script>
<script>mermaid.initialize({{startOnLoad:false,theme:'base',flowchart:{{htmlLabels:true,curve:'basis'}},
themeVariables:{{fontSize:'16px',primaryColor:'#eaf3fb',primaryBorderColor:'#2f6fb2',lineColor:'#475569'}}}});
mermaid.run({{querySelector:'.mermaid'}}).then(()=>{{document.body.setAttribute('data-done','1')}});</script>
</body></html>"""
    tmp = os.path.join(ROOT, "topic-ai-agents", "_graph_render.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page_html)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1400, "height": 1000}, device_scale_factor=2)
            pg.goto("file://" + tmp)
            pg.wait_for_selector("body[data-done='1']", timeout=60000)
            pg.locator("#wrap").screenshot(path=PNG)
            b.close()
    finally:
        os.remove(tmp)
    print(f"graph_png: wrote {os.path.relpath(PNG, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
