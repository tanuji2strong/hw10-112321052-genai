# card: c05-planning

- page: `wiki/concepts/c05-planning.md`
- title: c05 規劃（planning）

## Verbatim quotes (copied from the page)

> "Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks." [S03]
> "Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results." [S03]
> "LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error." [S03]
> "To avoid fruitless execution, planning should be decoupled from execution. You ask the agent to first generate a plan, and only after this plan is validated is it executed." [S06]

## Claims (copied from the page)

- 規劃的第一部分是「拆解」：把大任務切成可以管理的子目標。[S03]
- 第二部分是「反思」：從過去的行動中學習，改進之後的步驟。[S03]
- 限制：遇到非預期的錯誤時，LLM 不容易調整計畫。[S03]
- 做法差異：S03 描述 agent 自己拆解與反思；S06 建議把規劃與執行分開，先驗證計畫再執行。兩者不矛盾，後者是實作上的補充。[S06]
- [c02 增強型 LLM](c02-augmented-llm.md)
- [c06 記憶（memory）](c06-memory.md)
