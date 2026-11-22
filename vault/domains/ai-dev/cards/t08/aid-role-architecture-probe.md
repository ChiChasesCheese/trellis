---
id: aid-role-architecture-probe
node: t08.architecture-judgment
type: qa
step: 2
tags: [考点]
---
## Q
**Architecture · 哪些决定不能交出去**｜考点 · 追问

agent 给出一个方案：为了让订单服务的新功能"更快做完"，让它直接读取库存服务的数据库表。你批准吗？

## A
**不批准。** 局部看它可行、测试能过，但打破了服务边界。

| 代价 | 说明 |
|---|---|
| 隐性耦合 | 库存团队改表结构，订单服务悄悄坏掉 |
| 一致性 | 绕过了库存服务的业务规则 |
| 难回头 | 一旦多个调用点这样做，改回成本很高 |

**你要做的判断：** 这类"改动容易做、撤回难做"的决定归人；把它们写进 CLAUDE.md（"服务之间只通过 API 通信"），并用架构测试强制。

**做：** 让 agent 提供替代方案：调库存服务的接口，或事件订阅；你选。
**别做：** 因为"能跑、更快"就接受。

**出处：** Claude Code docs《Best practices》（Keep CLAUDE.md short：Decisions that aren't in the repo）
