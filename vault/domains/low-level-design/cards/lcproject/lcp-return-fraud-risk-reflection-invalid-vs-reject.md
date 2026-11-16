---
id: lcp-return-fraud-risk-reflection-invalid-vs-reject
node: lcproject.lcp-return-fraud-risk
type: qa
step: 5
tags: [作答]
---
## Q
在 ReturnGuard 的监控里，“无效输入”和“策略拒绝”都表现为请求没通过。说明指标怎样区分这两者，为什么不能混在一起，批量里又怎么计。

## A
**评分点**
- 说出两种信号不同：无效输入是 `invalid_input`（400）错误、没有分数；策略拒绝是一次成功的评估，`decision` 是 reject、有分数和分项
- 说出指标分开：错误计数器按错误码打标签，决定计数器按 `decision`（approve、manual_review、reject）打标签
- 说出批量里 `error` 不为空的项计入无效输入，`result` 里 reject 的项计入拒绝，两类互不重叠
- 说出为什么不能混：无效输入上升多半是上游缺陷或攻击，拒绝率上升是业务或策略变化，告警对象和处理方式不同
- 说出标签只用有限枚举（错误码、决定），不放用户编号或原始数值，避免指标基数爆炸

<details class="pt"><summary>参考答案</summary>

无效输入没有分数，返回 400 与 `invalid_input`，计入错误计数器；策略拒绝是成功的评估，`decision` 为 reject，计入按决定分类的计数器。批量里 `error` 非空的项算无效输入，`result.decision` 为 reject 的项算拒绝。两类要分开告警：前者指向上游或攻击，后者指向业务与策略变化。标签只用错误码与决定这样的有限枚举。

</details>

**知识点：** 接口的错误契约（Error Contract）、错误类型体系（Error Taxonomy）、缺陷与预期失败（Bugs vs Failures）
