---
id: lcp-return-fraud-risk-contract-rules
node: lcproject.lcp-return-fraud-risk
type: qa
step: 1
tags: [作答]
---
## Q
在退货风险评分服务（ReturnGuard）里，要修复一个评分引擎：`evaluate(rating, value_cents, account_age_days)` 返回总分、决定和三个分项，`evaluate_many(records)` 批量处理。现有代码能跑，但在阈值边界上给出前后不一致的决定。开工前你会先定下哪几条规则？

## A
**评分点**
- 说出校验先于计算：评分是 1 到 5 的整数，金额和账龄是非负整数，`True`、浮点、字符串、`None` 都无效，错误统一是 `ServiceError(400, "invalid_input")`
- 说出每一段的下界都含在这一段里：金额 10000 与 50000、账龄 30 与 180、总分 30 与 60 恰好落在边界时归更高的一档
- 说出总分就是三个分项之和，不取整、不截断、不归一；返回恰好三个键 `score`、`decision`、`components`
- 说出批量规则：每条一个 `{result, error}`，坏记录的 `error` 是 "invalid_input" 而不是 `None`，保持顺序，坏记录不影响后面，空输入返回 `[]`
- 说出输入迭代器只遍历一次，它自己抛出的异常不能被吞掉
- 说出引擎无状态：每次新建返回的嵌套字典，不修改传入的记录

<details class="pt"><summary>参考答案</summary>

先把合同写成六条再动手：校验在计算之前，`bool` 也算无效；每个下界都含（金额 10000 与 50000、账龄 30 与 180、总分 30 与 60）；总分是三项的原样之和；批量每条一个 `{result, error}`，坏记录给 "invalid_input"；输入只遍历一次、迭代器异常照常抛；返回值每次新建、不改输入。每条配一个带数字的测试：`(1, 50000, 10)` 必须是 95 分、reject。

</details>

**知识点：** 边界校验（Validate at the Boundary）、接口的错误契约（Error Contract）、验证输出（Verification）
