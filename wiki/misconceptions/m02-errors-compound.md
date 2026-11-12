# m02 誤解：每一步都對，最後結果就一定對

## 常見誤解

初學者常以為只要模型在每一步都表現不錯，多步驟的 agent 就會得到可靠的結果。

## 來源怎麼說

- S06 指出，錯誤會複合：步驟越多，整體準確率下降得越快。它舉的例子是每步 95% 的準確率，十步後降到 60%，一百步後只剩 0.6%。[S06]
> "Compound mistakes: an agent often needs to perform multiple steps to accomplish a task, and the overall accuracy decreases as the number of steps increases. If the model’s accuracy is 95% per step, over 10 steps, the accuracy will drop to 60%, and over 100 steps, the accuracy will be only 0.6%." [S06]
- S01 也提到，agent 的自主性會帶來更高成本與累積錯誤的風險，建議在沙盒環境中大量測試並加上防護措施。[S01]
> "The autonomous nature of agents means higher costs, and the potential for compounding errors." [S01]

## 正確理解

Agent 的可靠度不只取決於單一步驟，還取決於步驟數量。因此設計時應減少不必要的步驟、加入檢查點，並在高風險動作前測試。[S01][S06]

## 相關頁面

- [m01 agent 是完全自主的](m01-agents-are-fully-autonomous.md)
- [c05 規劃（planning）](../concepts/c05-planning.md)
