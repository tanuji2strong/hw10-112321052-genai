# card: calendar-agent-loop

- page: `wiki/examples/calendar-agent-loop.md`
- title: 範例：行事曆 agent 的工具使用循環

## Verbatim quotes (copied from the page)

> "Schedule a 30-minute sync with alice@example.com and bob@example.com on Monday, March 30, 2026 at 10am." [S07]
> "Schedule a weekly team standup every Monday at 9am for the next 4 weeks, starting Monday, March 30, 2026. Invite the whole team: alice@example.com, bob@example.com, carol@example.com." [S07]
> "The request sends a `tools` array alongside the user message." [S07]
> "When Claude determines that a tool call is needed, the response comes back with" [S07]
> "Run the tool. In a real system this would call your calendar API." [S07]
> "Your code runs the tool, then sends the result back in a `tool_result` block whose `tool_use_id` matches the `id` from the call." [S07]
> "keeps running tools and feeding results back until" [S07]

## Claims (copied from the page)

- 模型本身不執行行事曆操作，程式才執行。[S02]
- 多步驟任務需要迴圈，因為模型可能需要連續呼叫多個工具。[S07]
- [c04 工具使用循環（tool-use loop）](../concepts/c04-tool-use-loop.md)
- [S07 來源摘要](../sources/s07.md)
