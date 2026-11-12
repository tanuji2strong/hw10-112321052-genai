# c04 工具使用循環（tool-use loop）

注意：本頁名稱用「循環」指 agent 的重複步驟。

## 白話說明

LLM 本身只會產生文字，它不能直接查天氣或建立行事曆。做法是：模型先「要求」呼叫某個工具，應用程式執行它，再把結果交回模型。模型讀完結果後，可能再要求另一個工具，也可能直接給出最終回答。這一來一往就是工具使用循環。

## 來源怎麼說

- 模型不直接執行任何東西。它發出結構化請求，由你的程式（或 Anthropic 的伺服器）執行，結果再回到對話中。[S02]
> "The model never runs anything on its own." [S02]
> "It emits a structured request, your code (or Anthropic’s servers) runs the operation, and the result flows back into the conversation." [S02]
- Claude 決定何時、如何呼叫工具。[S02]
> "Claude determines when and how to call them." [S02]
- 使用者自訂工具時，Claude 只看得到 schema 與你回傳的結果，看不到你的程式碼。[S02]
> "Claude never receives your implementation; it only receives the schema you provided and the result you returned." [S02]

## 循環的步驟（S02 的描述）

1. 送出請求，附上 tools 陣列與使用者訊息。
2. Claude 回傳 stop_reason 為 tool_use 的回應，內含一或多個 tool_use 區塊。
3. 程式執行每個工具，並把輸出格式化成 tool_result。
4. 把原始訊息、助理回應與 tool_result 一起送出新的請求。
5. 只要 stop_reason 仍是 tool_use，就回到第 2 步。[S02]

## 多步驟的情況

- 一次呼叫不夠時，需要迴圈。S07 的說明是：真實任務常需要多次呼叫。[S07]
> "Ring 1 assumed Claude would call the tool exactly once. Real tasks often need several calls: Claude might create an event, read the confirmation, then create another." [S07]
- 完整的對照範例見 [行事曆 agent 範例](../examples/calendar-agent-loop.md)。

## 衝突 / 差異

- 用詞差異：S02 稱為 tool use（工具使用），S05 稱為 function calling（函式呼叫），並註明「也稱 tool calling」。[S05]
> "Function calling" [S05]
- 兩份文件描述的流程相同：模型請求呼叫，應用程式執行，再把輸出送回模型。S05 把它列為五個高階步驟，S02 把它寫成以 stop_reason 為條件的迴圈。這是描述方式不同，不是衝突。[S02][S05]
> "Make a second request to the model with the tool output" [S05]
> "It emits a structured request, your code (or Anthropic’s servers) runs the operation, and the result flows back into the conversation." [S02]

## 相關頁面

- [c02 增強型 LLM](c02-augmented-llm.md)
- [c01 什麼是 agent](c01-what-is-an-agent.md)
