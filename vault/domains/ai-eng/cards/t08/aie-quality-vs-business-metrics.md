---
id: aie-quality-vs-business-metrics
node: t08.quality-metrics-business-metrics
type: qa
step: 1
tags: [摘要]
---
## Q
**Quality metrics 与 business metrics · 一起看**｜摘要 · 必会

仪表盘上「回答相关性」从 0.82 升到 0.86，但日活没动，工单转人工率还升了。这是怎么回事，该看哪些指标？

## A
**metrics 不是目的：** 它的用途是发现问题和机会。设计顺序：**先想要抓住哪些 failure mode，再设计对应的指标。**

| 想抓的问题 | 指标 |
|---|---|
| 格式错误（最容易抓） | 输出无效 JSON 的比例；其中多少能轻易修复 |
| 幻觉 | 输出能否从 context 推出（factual consistency），可用 AI judge 算 |
| 安全 | 毒性、敏感信息、guardrail 触发率、拒答率、异常请求 |
| 用户体验 | 中途停止生成的比例、每次对话轮数、重新生成率、点赞率、任务完成率 |
| 长度 | 平均输入、输出 token 数及其分布变化 |
| 工具/检索 | 工具错误率、重试率、检索的 context precision |
| 延迟 | TTFT、TPOT、总延迟，按用户统计 |
| 成本 | 请求数、输入输出 token、缓存命中率、每秒请求数 |

**和 business metrics 并看：** 业务北极星指标如 DAU、会话时长、订阅数。测各 quality metric 与它们的**相关性**：强相关的指标指出怎么提升北极星；毫不相关的说明不必优化它。回到题目：相关性升了、业务没动，说明该指标对用户价值不是瓶颈；转人工率上升说明有别的失败类型没被监控。

**实践要点：**
- 指标可以按用户、版本、prompt 版本、类型、时间拆开看；
- spot check（抽样）和 exhaustive check（每条都评）结合；
- 好的 observability 看三个数：MTTD（发现用时）、MTTR（解决用时）、CFR（变更失败率）；
- 评测指标应能迁移到监控指标，线上发现的问题要回流到评测集。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch10 §Metrics；§Monitoring and Observability；ch4 §Tie evaluation metrics to business metrics

</details>
