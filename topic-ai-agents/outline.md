# outline.md（outline 節點輸出，待人工審核）

- 版本：round 1
- 結構：hook → 概念（依相依順序）→ 範例 → 誤解 → 總結
- 規則：每張投影片只能使用下列 cards 的內容；cards 只能包含其對應 wiki 頁面的文字。

## Slide 01 | cover | AI Agents：給零基礎初學者的入門課
- purpose: 開場，說明這堂課要學什麼。
- cards: c01-what-is-an-agent

## Slide 02 | hook | 從聊天到會做事：為什麼需要 agent？
- purpose: 用「只會回答」與「會自己做事」的差別引起動機。
- cards: s06, c01-what-is-an-agent

## Slide 03 | concept | 什麼是 agent？
- purpose: 建立 agent 的定義，並說明「誰決定流程」。
- cards: c01-what-is-an-agent, s01

## Slide 04 | concept | LLM 是核心，加上工具、檢索與記憶
- purpose: 介紹增強型 LLM 這個基本積木。
- cards: c02-augmented-llm, s03

## Slide 05 | concept | workflow 與 agent 的差別
- purpose: 依相依順序，先講固定流程，再講由模型決定的 agent。
- cards: c03-workflow-vs-agent

## Slide 06 | concept | 工具使用：模型請求，程式執行
- purpose: 說明模型不直接執行任何東西，由應用程式執行工具。
- cards: c04-tool-use-loop, s02

## Slide 07 | concept | 工具使用循環：一來一往直到完成
- purpose: 說明循環的步驟，以及何時停止。
- cards: c04-tool-use-loop, s05

## Slide 08 | example | 範例：行事曆 agent 怎麼工作
- purpose: 用官方教學的行事曆範例，走一遍單次與多步驟的情況。
- cards: calendar-agent-loop, s07

## Slide 09 | concept | 規劃：拆解任務，並從錯誤中反思
- purpose: 說明規劃的兩個部分，以及規劃與執行分開的做法。
- cards: c05-planning, s03

## Slide 10 | concept | 記憶：短期記憶與長期記憶
- purpose: 區分上下文中的短期記憶與外部資料庫的長期記憶。
- cards: c06-memory

## Slide 11 | concept | ReAct：推理與行動交錯
- purpose: 介紹 ReAct 的做法，以及它為什麼有效。
- cards: c07-react, s04

## Slide 12 | misconception | 誤解一與二：agent 是完全自主的？錯誤會累積
- purpose: 修正「完全自主」與「每一步都對，結果就對」兩個誤解。
- cards: m01-agents-are-fully-autonomous, m02-errors-compound

## Slide 13 | misconception | 誤解三：agent 越複雜越好？
- purpose: 修正「越複雜越好」的誤解，建議先從簡單開始。
- cards: m03-more-complexity-is-better, s01

## Slide 14 | summary | 總結與下一步
- purpose: 用名詞表整理核心概念，並給出下一步的學習方向。
- cards: glossary, c01-what-is-an-agent
