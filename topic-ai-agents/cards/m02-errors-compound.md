# card: m02-errors-compound

- page: `wiki/misconceptions/m02-errors-compound.md`
- title: m02 誤解：每一步都對，最後結果就一定對

## Verbatim quotes (copied from the page)

> "Compound mistakes: an agent often needs to perform multiple steps to accomplish a task, and the overall accuracy decreases as the number of steps increases. If the model’s accuracy is 95% per step, over 10 steps, the accuracy will drop to 60%, and over 100 steps, the accuracy will be only 0.6%." [S06]
> "The autonomous nature of agents means higher costs, and the potential for compounding errors." [S01]

## Claims (copied from the page)

- S06 指出，錯誤會複合：步驟越多，整體準確率下降得越快。它舉的例子是每步 95% 的準確率，十步後降到 60%，一百步後只剩 0.6%。[S06]
- S01 也提到，agent 的自主性會帶來更高成本與累積錯誤的風險，建議在沙盒環境中大量測試並加上防護措施。[S01]
- [m01 agent 是完全自主的](m01-agents-are-fully-autonomous.md)
- [c05 規劃（planning）](../concepts/c05-planning.md)
