---
id: aid-limits-probe
node: t01.capability-boundaries
type: qa
step: 2
tags: [考点]
---
## Q
**能力边界 · 该不该交**｜考点 · 追问

三个任务：(a) 把 30 个服务的 HTTP 客户端从旧库迁到新库，各服务有测试；(b) "优化一下支付流程"，没有指标；(c) 给一个老模块补测试，不改行为。哪个最不适合直接交给 agent？

## A
**(b) 最不适合。** 三条判据逐一过：

| 任务 | 信息在仓库里？ | 有可运行检查？ | 范围明确？ |
|---|---|---|---|
| (a) 迁移 | 是 | 是（各服务测试） | 是 |
| (b) 优化支付 | 否（"优化"的含义只在你脑子里） | 否（无指标） | 否 |
| (c) 补测试 | 是 | 是（测试本身，加变异检查更好） | 是 |

**对 (b) 的做法：** 先把它变成可检验的目标："p95 延迟从 X 降到 Y，不改变对账结果"，再让 agent 写基准和回归测试，最后才动代码。官方文档的建议是先让 agent 访谈你，直到能写出规格。

**出处：** Claude Code docs《Best practices》（Brainstorm with Claude first；Tell Claude what it can't see）
