# c05 規劃（planning）

## 白話說明

面對複雜任務，agent 不會一次就把答案寫完。它先把大問題拆成小步驟（子目標），逐步執行，並在做完後檢查結果，必要時修正計畫。

## 來源怎麼說

- 規劃的第一部分是「拆解」：把大任務切成可以管理的子目標。[S03]
> "Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks." [S03]
- 第二部分是「反思」：從過去的行動中學習，改進之後的步驟。[S03]
> "Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results." [S03]
- 限制：遇到非預期的錯誤時，LLM 不容易調整計畫。[S03]
> "LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error." [S03]

## 衝突 / 差異

- 做法差異：S03 描述 agent 自己拆解與反思；S06 建議把規劃與執行分開，先驗證計畫再執行。兩者不矛盾，後者是實作上的補充。[S06]
> "To avoid fruitless execution, planning should be decoupled from execution. You ask the agent to first generate a plan, and only after this plan is validated is it executed." [S06]

## 相關頁面

- [c02 增強型 LLM](c02-augmented-llm.md)
- [c06 記憶（memory）](c06-memory.md)
