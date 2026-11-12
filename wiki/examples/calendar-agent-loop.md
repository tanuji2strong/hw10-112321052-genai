# 範例：行事曆 agent 的工具使用循環

## 重要說明

這是 S07 教學文件中的範例，用來說明工具使用循環（tool-use loop）如何運作。本頁是用文字對照來源的程式碼與說明，**不是一次實際執行的紀錄**。這個例子的所有步驟都能在來源中找到依據。

## 範例請求

使用者的請求（第一環，只需要一次工具呼叫）：[S07]
> "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am." [S07]

第二環加入多步驟的情況，例如需要建立多個行程：[S07]
> "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com." [S07]

## 步驟（對照來源）

1. **送出請求。** 請求中同時附上工具定義（tools 陣列）與使用者訊息。[S07]
> "The request sends a `tools` array alongside the user message." [S07]

2. **Claude 決定呼叫工具。** 回應的 stop_reason 是 tool_use，內含工具名稱與參數。[S07]
> "When Claude determines that a tool call is needed, the response comes back with" [S07]

3. **程式執行工具。** 來源的程式碼註解寫道：在真實系統中，這一步會呼叫你的行事曆 API。[S07]
> "Run the tool. In a real system this would call your calendar API." [S07]

4. **把結果送回。** 程式把結果放進 tool_result 區塊，送回給 Claude。[S07]
> "Your code runs the tool, then sends the result back in a `tool_result` block whose `tool_use_id` matches the `id` from the call." [S07]

5. **循環。** 只要 stop_reason 仍是 tool_use，就重複執行工具與送回結果。遇到其他停止原因（例如 end_turn），代表 Claude 已給出最終回答。[S07][S02]
> "keeps running tools and feeding results back until" [S07]

## 這個例子的教學重點

- 模型本身不執行行事曆操作，程式才執行。[S02]
- 多步驟任務需要迴圈，因為模型可能需要連續呼叫多個工具。[S07]

## 相關頁面

- [c04 工具使用循環（tool-use loop）](../concepts/c04-tool-use-loop.md)
- [S07 來源摘要](../sources/s07.md)
