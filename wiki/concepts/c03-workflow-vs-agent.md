# c03 workflow 與 agent 的差異

## 白話說明

Workflow 是工程師先寫好步驟順序的系統，LLM 只是在每一步做事。Agent 則由 LLM 自己決定下一步要做什麼、要用哪個工具。兩者都是 agentic systems，差別在於誰控制流程。

## 來源怎麼說

- Workflow 的定義：LLM 與工具依照預先寫好的程式路徑被編排。[S01]
> "Workflows are systems where LLMs and tools are orchestrated through predefined code paths." [S01]
- Agent 的定義：LLM 動態決定自己的流程與工具使用。[S01]
> "Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." [S01]
- 選擇原則：workflow 適合定義清楚的任務，agent 適合需要彈性與模型自行決策的情況。[S01]
> "When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale." [S01]

## 衝突 / 差異

- 無衝突。S01 是唯一直接比較 workflow 與 agent 的來源。

## 相關頁面

- [c01 什麼是 agent](c01-what-is-an-agent.md)
- [m03 先從簡單開始](../misconceptions/m03-more-complexity-is-better.md)
