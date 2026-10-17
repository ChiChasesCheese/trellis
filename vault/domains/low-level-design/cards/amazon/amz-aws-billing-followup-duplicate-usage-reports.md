---
id: amz-aws-billing-followup-duplicate-usage-reports
node: amazon.amz-aws-billing
type: qa
step: 6
tags: [grown]
---
## Q
在 AWS 账单服务里，面试官追问「用量记录会重复上报」。该怎么办，改哪里？

## A
队列保证至少一次投递，同一条用量可能来多遍。新增 `UsageLedger`：用字典 `usage_id → 记录`，入账时去重，计费代码一行不改。三个分支：新记录入账；内容相同的重复返回 `False` 并计数，账单上 `duplicates_ignored` 可见；同编号但内容不同抛 `InvalidUsage`，不悄悄覆盖。例：`u1` 数量 10 上报两遍，账单只算 10；再来 `u1` 数量 11，报错。
