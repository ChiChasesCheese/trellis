---
id: amz-splitwise-objects-and-jobs
node: amazon.amz-splitwise
type: qa
step: 2
tags: [grown]
---
## Q
在分账设计里应该有哪几个对象？各自只负责一件什么事？

## A
`User`：参与者。`Expense`：一笔支出（付款人、总额、参与者、分法）。`Split` 策略（均分、精确、百分比）：只回答 `compute(amount, users) → {user: 分}`。`Ledger`：记录两两净余额。`ExpenseManager`：门面，先算分摊再更新账本。切分依据：分法会增加，账本结构不变。
