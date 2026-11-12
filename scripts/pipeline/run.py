"""Runner for the topic-slides graph. Each node can be rerun on its own.

  python3 scripts/pipeline/run.py <node> [--round N]

Nodes (deterministic, script-only):
  retrieve_wiki   -> topic-ai-agents/sources.md
  coverage_gate   (stop rule: fewer than 3 relevant pages for a section)
  evidence_cards  -> topic-ai-agents/cards/
  outline_gate    (reads topic-ai-agents/outline.md)
  text_gate       (reads drafts/roundN)
  faithfulness_gate
  render          -> topic-ai-agents/deck.html
  render_gate     (Playwright)
  graph_png       -> topic-ai-agents/graph.png from graph.mmd
  deliver         -> output/presentation.html (only after all gates pass)
  status          -> prints round state and last gate results

Routing is printed after each gate. Draft and ai_review are done by the author/agent (see
.agents/workflows/topic-slides.md), not by this script.
Logs go to topic-ai-agents/checks/roundN/ (round 0 = run 0, the old deck).
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import CHECKS, DRAFTS, OUTPUT, ROOT, TOPIC  # noqa: E402

STATE = os.path.join(TOPIC, "state.json")
MAX_ROUNDS = 3


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE, encoding="utf-8"))
    return {"round": 1, "history": []}


def save_state(s):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)


def node_module(name):
    mod = {
        "retrieve_wiki": "retrieve_wiki",
        "coverage_gate": "coverage_gate",
        "evidence_cards": "evidence_cards",
        "outline_gate": "outline_gate",
        "text_gate": "text_gate",
        "faithfulness_gate": "faithfulness_gate",
        "render": "render",
        "render_gate": "render_gate",
    }
    return mod.get(name)


def call(name, round_no):
    env = dict(os.environ, ROUND=str(round_no))
    mod = node_module(name)
    code = f"import sys; sys.path.insert(0,{HERE!r}); import {mod}; sys.exit({mod}.main())"
    proc = subprocess.run([sys.executable, "-c", code], env=env, cwd=ROOT)
    return proc.returncode


def graph_png():
    script = os.path.join(HERE, "render_graph.py")
    return subprocess.run([sys.executable, script], cwd=ROOT).returncode


def deliver(round_no):
    """Copy deck.html to output/presentation.html only if the last gates passed in this round."""
    needed = ["text_gate.log", "faithfulness_gate.log", "render_gate.log"]
    rdir = os.path.join(CHECKS, f"round{round_no}")
    for n in needed:
        path = os.path.join(rdir, n)
        if not os.path.exists(path) or "result: PASS" not in open(path, encoding="utf-8").read():
            print(f"deliver refused: {n} has not PASSed in round {round_no}")
            return 1
    shutil.copy(os.path.join(TOPIC, "deck.html"), os.path.join(OUTPUT, "presentation.html"))
    print("deliver: copied deck.html to output/presentation.html")
    return 0


def status():
    s = load_state()
    print(f"round: {s['round']} (max {MAX_ROUNDS})")
    for h in s["history"][-10:]:
        print("  ", h)
    if os.path.isdir(CHECKS):
        for r in sorted(os.listdir(CHECKS)):
            p = os.path.join(CHECKS, r)
            if os.path.isdir(p):
                logs = sorted(f for f in os.listdir(p) if f.endswith(".log"))
                print(f"  checks/{r}: {', '.join(logs) if logs else '(none)'}")
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    node = argv[0]
    round_no = None
    if "--round" in argv:
        round_no = int(argv[argv.index("--round") + 1])
    s = load_state()
    round_no = round_no if round_no is not None else s["round"]
    if node == "status":
        return status()
    if round_no > MAX_ROUNDS and node in ("text_gate", "faithfulness_gate", "render", "render_gate", "deliver"):
        print(f"stop rule: round {round_no} exceeds {MAX_ROUNDS}; stop and report")
        return 3
    if node == "graph_png":
        rc = graph_png()
    elif node == "deliver":
        rc = deliver(round_no)
    elif node_module(node):
        rc = call(node, round_no)
    else:
        print(f"unknown node: {node}")
        return 2
    s["history"].append(f"round {round_no}: {node} -> {'PASS' if rc == 0 else 'FAIL'}")
    save_state(s)
    print(f"[{node}] round {round_no}: {'PASS' if rc == 0 else 'FAIL'}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
