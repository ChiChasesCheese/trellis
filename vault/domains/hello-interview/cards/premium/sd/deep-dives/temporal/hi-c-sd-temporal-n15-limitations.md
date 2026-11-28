---
id: hi-c-sd-temporal-n15-limitations
node: sd.deep-dives.temporal.notes
type: qa
step: 10
---
## Q
**Temporal · 它的局限：什么时候别用**｜摘要 · 必会

Temporal 的四个局限是什么？

## A
- **简单后台任务：** 单个独立任务，用 SQS 这样的普通队列简单得多。在题目本身要考察投递与重试机制时，也应该直接用队列自己设计，而不是用 Temporal 一个方框带过。
- **流式处理：** 它不是 Kafka 或其他事件流平台的替代品；以持续处理大量事件流为主的问题，用为此设计的系统。
- **外部副作用仍需幂等：** Activity 可能被重试，对 Stripe 或数据库的调用可能被尝试多次，必须让操作可安全重试。
- **Workflow 代码有约束：** 重放要求确定性，不能把 Workflow 代码当普通应用代码：结果会变的操作（数据库查询、外部 API 调用）一般要放在 Activity 里。
