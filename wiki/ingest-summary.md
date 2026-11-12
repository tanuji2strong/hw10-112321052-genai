# Ingest 摘要

日期：2026-11-12。依 AGENTS.md 的流程，一次 ingest 一個來源，每次都記錄於 [log.md](log.md)。

## 來源

| 代號 | 來源 | 摘要頁 | 狀態 |
|---|---|---|---|
| S01 | Building effective agents（Anthropic） | [s01](sources/s01.md) | 已 ingest |
| S02 | How tool use works（Anthropic） | [s02](sources/s02.md) | 已 ingest |
| S03 | LLM Powered Autonomous Agents（Lilian Weng） | [s03](sources/s03.md) | 已 ingest |
| S04 | ReAct（Yao et al.） | [s04](sources/s04.md) | 已 ingest |
| S05 | Function calling（OpenAI） | [s05](sources/s05.md) | 已 ingest |
| S06 | Agents（Chip Huyen） | [s06](sources/s06.md) | 已 ingest |
| S07 | Tutorial: Build a tool-using agent（Anthropic） | [s07](sources/s07.md) | 已 ingest |

## 產出的頁面

- 概念頁：c01 什麼是 agent、c02 增強型 LLM、c03 workflow 與 agent 的差異、c04 工具使用循環、c05 規劃、c06 記憶、c07 ReAct
- 誤解頁：m01 agent 是完全自主的、m02 錯誤會累積、m03 agent 越複雜越好
- 範例頁：行事曆 agent 的工具使用循環（來自 S07，已標示為對照說明，非實際執行紀錄）
- 名詞表、目錄、log、lint 報告

## 衝突與差異

- c01：S01 以「誰控制流程」定義 agent，S03 以元件描述。記為定義角度不同，不矛盾。
- c04：S02 與 S05 的用詞（tool use 與 function calling）與流程描述不同，記為用詞差異。
- c05：S03 的規劃做法與 S06 的「規劃與執行分開」，記為補充，不矛盾。

## 對簡報的涵蓋

- 什麼是 agent、LLM 在核心位置：c01、c02（S01、S03、S06）
- 工具使用與循環：c04（S02、S05、S07），範例頁
- 規劃與記憶：c05、c06（S03，S06 補充）
- ReAct：c07（S04、S06）
- 誤解：m01、m02、m03（S01、S06）

## 限制

- 所有引文都由 lint 逐字比對過 raw/ 檔案，但 S02 與 S05 是 Claude 與 OpenAI 的線上文件，內容可能隨時間更新，抓取日期為 2026-11-12。
- 行事曆範例是 S07 的示範，不是實際執行。
- 名詞表的部分定義（例如 LLM）是縮寫說明，不是來源中的定義段落。

## Lint 結果

見 [lint-report.md](lint-report.md)。
