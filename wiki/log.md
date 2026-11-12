# Wiki log

只追加，不刪改。每次 ingest 一筆，每次 lint 一筆。

## 2026-11-12 ingest 1/7 | S01 Building effective agents

- 來源：raw/01_anthropic_building_effective_agents.md（Anthropic，2024-12-19）
- 新增：wiki/sources/s01.md；wiki/concepts/c01-what-is-an-agent.md；wiki/concepts/c02-augmented-llm.md；wiki/concepts/c03-workflow-vs-agent.md；wiki/misconceptions/m03-more-complexity-is-better.md；wiki/index.md
- 引文：15 段（逐字驗證通過）
- 衝突記錄：c01 記錄 S01 與（待 S03 ingest 的）定義角度差異
- lint：PASS（0 錯誤，15 段引文驗證，8 個頁面）

## 2026-11-12 ingest 2/7 | S02 How tool use works

- 來源：raw/02_anthropic_how_tool_use_works.md（Anthropic，Claude 文件，抓取 2026-11-12）
- 新增：wiki/sources/s02.md；wiki/concepts/c04-tool-use-loop.md；wiki/index.md（來源表與概念頁）
- 衝突記錄：c04 記錄 tool use 與 function calling 的用詞差異（待 S05 補引文）
- lint：第一次失敗（1 段引文含反斜線與反引號，與原文不符），已刪除該引文並改為轉述；再次執行 PASS（0 錯誤，24 段引文驗證，10 個頁面）

## 2026-11-12 ingest 3/7 | S03 LLM Powered Autonomous Agents

- 來源：raw/03_weng_llm_powered_autonomous_agents.md（Lilian Weng，2023-06-23）
- 新增：wiki/sources/s03.md；wiki/concepts/c05-planning.md；wiki/concepts/c06-memory.md
- 修改：wiki/concepts/c01-what-is-an-agent.md（加入 S03 的定義角度）；wiki/index.md
- 衝突記錄：c01 記錄 S01 與 S03 的切入點差異（不矛盾）
- lint：PASS（0 錯誤，43 段引文驗證，13 個頁面）

## 2026-11-12 ingest 4/7 | S04 ReAct

- 來源：raw/04_react_arxiv_2210.03629.md（Yao et al.，arXiv:2210.03629）
- 新增：wiki/sources/s04.md；wiki/concepts/c07-react.md
- 修改：wiki/index.md
- lint：PASS（0 錯誤，51 段引文驗證，15 個頁面）

## 2026-11-12 ingest 5/7 | S05 Function calling (OpenAI)

- 來源：raw/05_openai_function_calling.md（OpenAI API 文件，抓取 2026-11-12）
- 新增：wiki/sources/s05.md
- 修改：wiki/concepts/c04-tool-use-loop.md（用詞差異與流程描述的比較，附 S02 與 S05 引文）；wiki/index.md
- 衝突記錄：c04 記錄 S02 與 S05 的用詞與流程描述差異（判定為描述方式不同，非衝突）
- lint：PASS（0 錯誤，60 段引文驗證，16 個頁面）

## 2026-11-12 ingest 6/7 | S06 Agents (Chip Huyen)

- 來源：raw/06_huyen_agents.md（Chip Huyen，2025-01-07）
- 新增：wiki/sources/s06.md；wiki/misconceptions/m01-agents-are-fully-autonomous.md；wiki/misconceptions/m02-errors-compound.md
- 修改：wiki/concepts/c01-what-is-an-agent.md（外部工具補充）；wiki/concepts/c05-planning.md（規劃與執行分開）；wiki/concepts/c07-react.md（ReAct 作為常見模式）；wiki/index.md
- 衝突記錄：c05 記錄 S03 與 S06 的做法差異（判定為補充，不矛盾）
- lint：PASS（0 錯誤，73 段引文驗證，19 個頁面）

## 2026-11-12 ingest 7/7 | S07 Tutorial: Build a tool-using agent

- 來源：raw/07_anthropic_tool_agent_tutorial.md（Anthropic，Claude 文件，抓取 2026-11-12）
- 新增：wiki/sources/s07.md；wiki/examples/calendar-agent-loop.md（示範，非實際執行紀錄）；wiki/glossary.md；wiki/ingest-summary.md
- 修改：wiki/concepts/c04-tool-use-loop.md（多步驟情況）；wiki/index.md（來源表全部改為已 ingest，新增範例、名詞表、摘要、lint 報告連結）
- 第一次 lint 失敗 4 項：1 段引文含反斜線（已刪除並改寫）；3 個頁面未列入 index（已加入）。修正後 PASS。
- lint：PASS（0 錯誤，87 段引文驗證，23 個頁面）

