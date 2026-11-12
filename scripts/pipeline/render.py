"""Node render: build a single-file deck.html from drafts/roundN/slide-NN.json (topic-ai-agents/deck.html).
Design: bright, large text for projectors, keyboard navigation (arrows, PageUp/PageDown, Space, Home, End),
slide numbers, one source chip per bullet that links to the wiki page it cites.
"""
import glob
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DRAFTS, TOPIC, current_round  # noqa: E402

CSS = """
:root{--ink:#1e293b;--muted:#475569;--brand:#0f4c81;--accent:#2f6fb2;--ok:#2e9e6b;--warn:#d0554a;--bg:#f7f9fc;--card:#ffffff;--chip:#eef4fa}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{font-family:'Noto Sans TC','PingFang TC','Microsoft JhengHei',sans-serif;background:var(--bg);color:var(--ink)}
.slide{display:none;height:100vh;padding:7vh 8vw 9vh;background:var(--card);flex-direction:column;justify-content:center;gap:3vh;overflow:hidden;position:relative}
.slide.active{display:flex}
.kind{position:absolute;top:4vh;right:6vw;font-size:1rem;padding:.35em 1.1em;border-radius:2em;background:var(--chip);color:var(--brand)}
h1{font-size:3.2rem;color:var(--brand);line-height:1.25}
h2{font-size:2.4rem;color:var(--brand);line-height:1.25}
ul{list-style:none}
li{font-size:1.6rem;line-height:1.7;margin-bottom:1.6vh;padding-left:1.4em;position:relative}
li::before{content:'';position:absolute;left:0;top:.62em;width:.5em;height:.5em;border-radius:50%;background:var(--accent)}
.quote{display:block;margin-top:.3em;font-size:1.05rem;color:var(--muted);font-style:italic}
.src{display:inline-block;margin-left:.4em;font-size:.85rem;padding:.1em .7em;border-radius:1em;background:var(--chip);color:var(--brand);text-decoration:none;white-space:nowrap}
.src:hover{background:#dbe8f5}
.sub{font-size:1.4rem;color:var(--muted)}
.pagenum{position:absolute;bottom:3vh;right:5vw;color:#94a3b8;font-size:1rem}
.nav{position:fixed;bottom:2.5vh;left:6vw;font-size:.95rem;color:#94a3b8}
.cover{text-align:center;align-items:center;background:linear-gradient(135deg,#eaf3fb,#f7f9fc)}
"""

JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var i=0;
  function show(n){
    if(n<0)n=0; if(n>slides.length-1)n=slides.length-1; i=n;
    slides.forEach(function(s,k){s.classList.toggle('active',k===i)});
    history.replaceState(null,'','#'+(i+1));
  }
  document.addEventListener('keydown',function(e){
    if(['ArrowRight','PageDown',' ','ArrowDown'].indexOf(e.key)>=0){show(i+1);e.preventDefault();}
    else if(['ArrowLeft','PageUp','ArrowUp'].indexOf(e.key)>=0){show(i-1);e.preventDefault();}
    else if(e.key==='Home'){show(0);} else if(e.key==='End'){show(slides.length-1);}
  });
  var start=parseInt((location.hash||'#1').slice(1),10);
  show(isNaN(start)?0:start-1);
  window.deckSlides=slides; window.deckShow=show;
})();
"""


def esc(s):
    return html.escape(s, quote=True)


def main():
    directory = os.path.join(DRAFTS, f"round{current_round()}")
    files = sorted(glob.glob(os.path.join(directory, "slide-*.json")))
    if not files:
        print(f"render: no drafts in {directory}")
        return 1
    slides = [json.load(open(f, encoding="utf-8")) for f in files]
    total = len(slides)
    parts = []
    for s in slides:
        n = int(s["n"])
        kind_label = s.get("kind_label", s.get("kind", ""))
        cls = "slide cover" if s.get("kind") == "cover" else "slide"
        body = [f'<section class="{cls}" id="s{n}" data-slide="{n}">']
        body.append(f'<span class="kind">{esc(kind_label)}</span>')
        if s.get("kind") == "cover":
            body.append(f"<h1>{esc(s['title'])}</h1>")
            if s.get("subtitle"):
                body.append(f'<p class="sub">{esc(s["subtitle"])}</p>')
        else:
            body.append(f"<h2>{esc(s['title'])}</h2>")
        if s.get("bullets"):
            body.append("<ul>")
            for b in s["bullets"]:
                item = [esc(b["text"])]
                if b.get("quote"):
                    item.append(f'<span class="quote">&ldquo;{esc(b["quote"])}&rdquo;</span>')
                if b.get("cite"):
                    href = "../" + b["cite"]
                    label = os.path.basename(b["cite"]).replace(".md", "")
                    item.append(f'<a class="src" href="{esc(href)}">{esc(label)}</a>')
                body.append("<li>" + "".join(item) + "</li>")
            body.append("</ul>")
        body.append(f'<div class="pagenum">{n} / {total}</div>')
        body.append("</section>")
        parts.append("\n".join(body))
    doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Agents 入門教學簡報</title>
<style>{CSS}</style>
</head>
<body>
{chr(10).join(parts)}
<div class="nav">← → 切換投影片　Home / End 跳到首尾</div>
<script>{JS}</script>
</body>
</html>
"""
    out = os.path.join(TOPIC, "deck.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"render: wrote {os.path.relpath(out)} with {total} slide(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
