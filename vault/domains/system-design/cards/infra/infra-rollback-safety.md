---
id: infra-rollback-safety
node: infra.delivery
type: qa
---
## Q
When is a deployment "rollback safe" (AWS's definition), and why must an automated test prove that version N-1 can read what version N wrote *before* N ever ships?

## A
- **Definition**: a deploy is rollback safe when reverting to the previous version is guaranteed to work — specifically, **version N-1 can correctly read every piece of data, message, or wire format that version N may have written**.
- **Why it matters**: rollback is the *first* response to a bad deploy — it must be a reflex that never makes things worse. If N introduced a new serialization format (a new field, a new enum value, a changed encoding) and wrote it to a store or queue, rolling back leaves N-1 facing data it cannot parse: it crashes, or worse, silently drops the new fields — turning a quick revert into a second, deeper outage. Debugging *forward* under pressure is exactly what rollback exists to avoid.
- **The same constraint appears without any rollback**: rolling and canary deploys run N-1 and N side by side against shared stores and queues, so adjacent versions must be mutually compatible anyway.
- **Enforcement**: automated **upgrade/downgrade testing** in the pipeline — deploy N, write, roll back to N-1, verify reads — as a gate, not a code-review convention.

## Q zh
什么时候一次部署是 "rollback safe"（AWS 的定义）？为什么必须在版本 N 发布*之前*，就用自动化测试证明版本 N-1 能读懂 N 写下的东西？

## A zh
- **定义**：当回退到上一版本被保证可行时，部署才是 rollback safe — 具体地说，**版本 N-1 能正确读取版本 N 可能写下的每一份数据、消息或线上格式（wire format）**。
- **为什么重要**：回滚是坏部署的*第一*响应 — 它必须是一个绝不会让事情更糟的反射动作。如果 N 引入了新的序列化格式（新字段、新枚举值、变更的编码）并写进了存储或队列，回滚后 N-1 面对的是它无法解析的数据：它会崩溃，或者更糟 — 静默丢弃新字段 — 把一次快速回退变成第二次更深的故障。在压力下向前调试（roll forward），正是回滚要避免的东西。
- **没有回滚也有同样的约束**：滚动部署和金丝雀部署让 N-1 与 N 并肩运行，共享存储和队列，所以相邻版本本来就必须互相兼容。
- **如何强制**：流水线里的自动化 **upgrade/downgrade 测试** — 部署 N、写入、回退到 N-1、验证读取 — 作为关卡（gate），而不是 code review 里的口头约定。
