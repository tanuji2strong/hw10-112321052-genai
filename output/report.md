# AI Agents 教學簡報 — Graph Workflow 執行報告
日期：2026-11-12｜執行者：Graph DAG runner (`scripts/build_presentation.py`)

## 1. 目標
將 26 頁 Wiki 知識庫，透過可退回的 Graph 流程，自動產出 13 頁、明亮簡潔風的單檔 HTML 教學簡報（零基礎初學者取向），並以檢查器驅動 Loop 修正。

## 2. Graph 架構設計（節點 / 邊 / 狀態）
```text
plan → slide_writer → assemble → check ──(pass 或達 3 輪上限)──→ finalize
                                   │
                                   └──(fail 且輪次 < 3)──→ fixer ──┐
                                     ▲                             │
                                     └────────────(退回)───────────┘
```