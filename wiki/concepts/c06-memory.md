# c06 記憶（memory）

## 白話說明

LLM 本身不會記住之前的對話。Agent 的記憶分兩種：一種是放在目前上下文視窗（context window）裡的短期記憶；另一種是存在外部資料庫、需要時再取回的長期記憶。

## 來源怎麼說

- 短期記憶：上下文中的 in-context learning 可以視為短期記憶，但它很有限，受 Transformer 的上下文視窗長度限制。[S03]
> "Short-term memory: I would consider all the in-context learning (See Prompt Engineering) as utilizing short-term memory of the model to learn." [S03]
> "It is short and finite, as it is restricted by the finite context window length of Transformer." [S03]
- 長期記憶：外部向量資料庫，讓 agent 在查詢時取回資訊。[S03]
> "Long-term memory: This provides the agent with the capability to retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval." [S03]
> "Long-term memory as the external vector store that the agent can attend to at query time, accessible via fast retrieval." [S03]

## 衝突 / 差異

- 無衝突。S01 把「記憶」列為增強型 LLM 的增強能力之一，見 [c02](c02-augmented-llm.md)。

## 相關頁面

- [c02 增強型 LLM](c02-augmented-llm.md)
- [c05 規劃（planning）](c05-planning.md)
