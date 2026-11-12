# AGENTS.md: LLM Wiki 規則（AI Agents 入門）

## 專案目的
用 LLM Wiki 製作一份給完全初學者的「AI Agents」教學 HTML 簡報。
wiki/ 是簡報唯一的知識來源。簡報中的每個事實都必須能追溯到 wiki 頁面，且 wiki 頁面必須能追溯到 raw/ 原始來源。

## 資料夾
- raw/：原始來源（唯讀，不可修改）。每個檔案開頭記錄標題、作者、網址、日期。
- wiki/index.md：所有頁面與來源的目錄。
- wiki/log.md：每次 ingest 與 lint 的紀錄（只能追加，不可刪改）。
- wiki/sources/：每個原始來源一頁摘要，檔名 sNN.md。
- wiki/concepts/：概念頁，檔名 cNN-英文slug.md。
- wiki/misconceptions/：常見誤解頁，檔名 mNN-英文slug.md。
- wiki/examples/：範例頁。
- wiki/glossary.md：名詞表。
- wiki/ingest-summary.md：ingest 摘要。
- wiki/lint-report.md：最近一次 lint 的結果（由 scripts/wiki_lint.py 產生）。
- scripts/wiki_lint.py：lint 腳本，只使用 Python 標準函式庫。

## 語言與文字規則
- 內容使用繁體中文（台灣用語）。技術名詞保留英文，英文寫在括號內，例如「工具使用（tool use）」。
- 不使用簡體字。不使用 em dash（——）。
- 引文保留原文英文，不翻譯引文本身。中文說明寫在引文之外。

## 引用規則（每個主張都要有來源）
- 概念頁、誤解頁、範例頁、名詞表、來源摘要頁中的每個主張，都要以 [Sxx] 標註來源（xx 為兩位數字，對應 raw/ 檔案前綴）。
- 關鍵主張必須附一段逐字引文，且整行格式必須如下（引文用英文雙引號，行尾是來源標籤）：
  > "逐字引文" [S03]
- 引文必須與 raw/ 對應檔案中的文字完全相同（空白與標點視為相同，lint 會檢查）。
- 來源沒有說的內容不能寫進 wiki。如果需要示範，必須明確標示「（示範，非來源內容）」，且不可作為概念結論的依據。

## 來源代號（見 wiki/index.md 來源表）
S01 至 S07 各自對應 raw/ 下前綴相同的檔案（例如 S03 = raw/03_*.md）。

## 衝突處理
- 來源說法不同時，寫在頁面的「衝突 / 差異」段落。同時列出雙方與引文，不替任何一方選邊。
- 只有用詞不同（例如 tool use 與 function calling）時，記為「用詞差異」，不算衝突。

## Ingest 流程（一次只處理一個來源）
1. 完整讀取 raw/ 中該來源的檔案。
2. 建立 wiki/sources/sNN.md（摘要與引文）。
3. 建立或更新相關的概念、誤解、範例、名詞表頁面，每個新主張都附來源與引文。
4. 更新 wiki/index.md 的頁面清單。
5. 在 wiki/log.md 末尾追加一筆紀錄（日期、來源代號、新增與修改的頁面、引文數）。
6. 執行 `python3 scripts/wiki_lint.py`，修正所有錯誤直到通過。lint 報告會寫入 wiki/lint-report.md。

## Lint 檢查項目
- 壞連結（broken links）：所有相對連結都必須指向存在的檔案。
- 缺少來源（missing citations）：概念、誤解、範例、名詞表、來源頁中必須至少有一個 [Sxx] 標籤。
- 引文驗證（quote verification）：每一段引文都必須在對應 raw/ 檔案中逐字出現。
- 孤立頁面（orphan pages）：每個頁面都必須被 wiki/index.md 連結。

## 禁止事項
- 不修改 raw/。
- 不刪改 wiki/log.md 既有紀錄。
- 不把 outside knowledge 寫成事實。
- 簡報（Phase 2 起）只能使用 wiki 內容，不得補充 wiki 以外的內容。

## 後續階段
Phase 2 的簡報流程（graph pipeline）規格見 .agents/workflows/topic-slides.md，在 Phase 2 才會建立。
