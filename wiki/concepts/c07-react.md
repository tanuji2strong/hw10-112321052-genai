# c07 ReAct（推理與行動交錯）

## 白話說明

ReAct 是一種讓 agent「邊想邊做」的方式：模型先寫下它的推理，然後採取一個行動（例如查詢資料），看到結果後再推理下一步。推理幫助它規劃與修正，行動讓它取得外部資訊。

## 來源怎麼說

- 研究的出發點：推理與行動過去被分開研究。[S04]
> "have primarily been studied as separate topics." [S04]
- ReAct 的核心做法是交錯產生推理與行動。[S04]
> "we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner" [S04]
- 推理負責規劃、追蹤與處理例外；行動負責取得外部資訊。[S04]
> "reasoning traces help the model induce, track, and update action plans as well as handle exceptions" [S04]
> "while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information." [S04]

## 衝突 / 差異

- 無衝突。S04 是研究論文。S06 指出這個做法已成為 agent 的常見模式。[S06]
> "First proposed by ReAct (Yao et al., 2022), interleaving reasoning and action has become a common pattern for agents." [S06]

## 相關頁面

- [c04 工具使用循環（tool-use loop）](c04-tool-use-loop.md)
- [c05 規劃（planning）](c05-planning.md)
