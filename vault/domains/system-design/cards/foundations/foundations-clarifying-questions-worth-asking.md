---
id: foundations-clarifying-questions-worth-asking
node: foundations.method
type: qa
---
## Q
Interviewer says "design X" with no details. Which clarifying questions actually change the design (vs filler)?

## A
Questions whose answers select an architecture:

- **Read/write ratio** — decides caching and replication strategy.
- **Scale** (DAU, data size) — one box vs sharded fleet.
- **Consistency vs availability priority** — e.g. can a user briefly see stale data?
- **Latency-sensitive paths** — which operations must be fast vs can be async.

Filler: questions about UI details or features you'd scope out anyway.


## Q zh
面试官说"设计X"但没有细节。哪些澄清问题实际上会改变设计（vs 填充内容）？

## A zh
答案选择架构的问题：

- **读写比** — 决定缓存和复制策略。
- **规模**（DAU、数据大小）— 单机 vs 分片集群。
- **一致性 vs 可用性优先** — 例如用户能否短时间看到陈旧数据？
- **延迟敏感路径** — 哪些操作必须快 vs 可以异步。

填充内容：关于 UI 细节或你反正会排除在范围外的功能的问题。
