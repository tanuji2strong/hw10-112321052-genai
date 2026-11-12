# card: glossary

- page: `wiki/glossary.md`
- title: 名詞表（Glossary）

## Verbatim quotes (copied from the page)

(none)

## Claims (copied from the page)

- **Agent（代理）**：以 LLM 為核心，能自己決定下一步、使用工具並朝目標前進的系統。見 [c01](concepts/c01-what-is-an-agent.md)。[S01][S03]
- **LLM（大型語言模型）**：文件中使用的縮寫，指 large language model。[S01]
- **增強型 LLM（augmented LLM）**：加上檢索、工具與記憶的 LLM，是 agent 系統的基本積木。見 [c02](concepts/c02-augmented-llm.md)。[S01]
- **Workflow（工作流程）**：LLM 與工具依照預先寫好的程式路徑被編排。見 [c03](concepts/c03-workflow-vs-agent.md)。[S01]
- **Tool use（工具使用）**：模型發出結構化請求，由應用程式執行工具，再把結果送回模型。見 [c04](concepts/c04-tool-use-loop.md)。[S02]
- **Function calling（函式呼叫）**：OpenAI 文件對工具使用的稱呼，也稱 tool calling。[S05]
- **Tool call（工具呼叫）**：模型在檢視提示後，判斷需要使用工具時回傳的特殊回應。[S05]
- **stop_reason（停止原因）**：Claude 回應結束的原因。值為 tool_use 時，表示 Claude 要求執行工具。[S02][S07]
- **Tool-use loop（工具使用循環）**：重複「模型要求工具、程式執行、結果送回」直到模型給出最終回答的流程。見 [c04](concepts/c04-tool-use-loop.md)。[S02][S07]
- **規劃（planning）**：把大任務拆成子目標，並對過去行動做反思。見 [c05](concepts/c05-planning.md)。[S03]
- **記憶（memory）**：短期記憶是上下文中的 in-context learning；長期記憶是外部向量資料庫。見 [c06](concepts/c06-memory.md)。[S03]
- **上下文視窗（context window）**：模型一次能處理的文字長度上限。短期記憶受它限制。見 [c06](concepts/c06-memory.md)。[S03]
- **向量資料庫（vector store）**：存放嵌入表示（embedding）、支援快速檢索的外部記憶。見 [c06](concepts/c06-memory.md)。[S03]
- **ReAct**：讓 LLM 交錯產生推理與行動的方法。見 [c07](concepts/c07-react.md)。[S04][S06]
- **累積錯誤（compounding errors）**：多步驟任務中，每一步的錯誤會疊加，使整體準確率下降。見 [m02](misconceptions/m02-errors-compound.md)。[S06]
