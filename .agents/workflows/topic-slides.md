# Workflow: topic-slides（wiki → 教學簡報的 graph pipeline）

規則（引用格式、語言、衝突處理）見 [AGENTS.md](../../AGENTS.md)。本檔描述 graph 的節點、閘門、輸入輸出，以及失敗時的路由。圖見 [topic-ai-agents/graph.mmd](../../topic-ai-agents/graph.mmd)（PNG：[graph.png](../../topic-ai-agents/graph.png)）。

每個節點都可以單獨重跑：

    .venv/bin/python scripts/pipeline/run.py <node> [--round N]

`run.py status` 顯示目前 round 與各 round 的 check log。Log 寫在 `topic-ai-agents/checks/roundN/`，round 0 是舊版（run 0）。

## 節點與檔案

| 節點 | 類型 | 輸入 | 輸出 |
|---|---|---|---|
| retrieve_wiki | script | sections.json、wiki/ | sources.md |
| coverage_gate | script 閘門 | sources.md | checks/roundN/coverage_gate.log |
| evidence_cards | script | wiki/ 每一頁 | cards/*.md（每頁一張） |
| outline | agent（寫 outline.md） | sources.md、cards/ | outline.md |
| outline_gate | script 閘門 | outline.md、cards/ | checks/roundN/outline_gate.log |
| 人工檢查點 | 使用者核准 | outline.md | 核准或修改要求 |
| draft | agent（每張投影片一個 JSON） | 該張投影片對應的 cards | drafts/roundN/slide-NN.json |
| text_gate | script 閘門 | drafts/roundN/ | checks/roundN/text_gate.log |
| faithfulness_gate | script 閘門 | drafts/roundN/、wiki/ | checks/roundN/faithfulness_gate.log |
| render | script | drafts/roundN/ | deck.html |
| render_gate | script（Playwright） | deck.html | checks/roundN/render_gate.log、checks/roundN/render/*.png |
| ai_review | 新的 subagent（只看 deck.html 與被引用的 wiki 頁） | deck.html、wiki/ | checks/roundN/ai_review.md |
| graph_png | script | graph.mmd | graph.png |
| deliver | script（需所有閘門 PASS） | deck.html | output/presentation.html |

## 閘門規則

- **coverage_gate**：每個規劃章節至少要有 3 個相關 wiki 頁面（或 cards）。不足時停止並回報，不用 wiki 以外的內容補。
- **outline_gate**：投影片數量 8 到 15；每張投影片至少對應 1 張 card；card 必須存在。
- **text_gate**：每個 bullet 必須是完整句（以 。！？ 結尾），或是 12 字以內的短語；不得截斷；不得有 "- " 開頭；不得有大綱或佔位文字；不得有檔案路徑或 wiki 路徑；不得有簡體字（以 opencc s2twp 為準）；不得有 [補充] 或外部來源標籤；每個 bullet 都要有來源標籤。
- **faithfulness_gate**：來源標籤必須指向存在的 wiki 頁面；引文必須逐字出現在該頁；bullet 中的數字必須出現在該頁。
- **render_gate**：投影片數 8 到 15；每張截圖；overflow（scrollHeight > clientHeight）即失敗；壞連結即失敗；鍵盤 ArrowRight 必須切換投影片。

## 路由（失敗時回到造成錯誤的節點）

- coverage 失敗 → 停止，回報使用者
- outline_gate 失敗 → outline
- 人工檢查點要求修改 → outline
- text_gate 或 faithfulness_gate 在第 k 張失敗 → 只重寫第 k 張的 draft，其他投影片不變
- card 內容錯誤 → 重建該 card（evidence_cards）
- render_gate overflow 在第 k 張 → 回到第 k 張的 draft 縮短內容（不可縮小字體來隱藏）
- ai_review 發現缺少主題 → retrieve_wiki
- ai_review 發現 card 內容錯誤 → evidence_cards
- ai_review 發現忠實度問題在第 k 張 → 第 k 張的 draft

## 停止規則

- 所有閘門 PASS → deliver
- 3 整輪（rounds）後仍未 PASS → 停止並回報
- 任一章節的相關頁面少於 3 個 → 停止並回報

`run.py` 會在 `topic-ai-agents/state.json` 記錄 round 與歷史；超過 3 輪時拒絕執行 draft 之後的閘門。

## 每個節點的 draft 規則（agent 節點）

- draft 只能使用該張投影片 outline 中列出的 cards。
- 每個 bullet 的 cite 必須是 wiki 頁面路徑（例如 `wiki/concepts/c01-what-is-an-agent.md`），quote 若有，必須是該頁中的逐字文字。
- 數字只能出現在被引用的頁面中。
- 每張投影片最多 2 輪重寫。
