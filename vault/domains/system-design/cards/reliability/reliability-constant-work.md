---
id: reliability-constant-work
node: reliability.resilience.containment
type: qa
---
## Q
The constant-work pattern says a reliable system should do the *same amount of work* whether everything is calm or everything is failing — e.g. Route 53 pushes the full health-check result file every few seconds instead of sending deltas on change. What does this buy?

## A
- **Failure mode = normal mode.** A delta-based system does almost nothing when calm and a flood of work when many things change at once — so its busiest, least-tested mode coincides with the outage. A constant-work system has one mode, rehearsed every few seconds forever.
- **No recovery surge.** After a partition or crash there is no backlog of missed updates to replay; the next full push simply overwrites state. Recovery costs the same as steady state.
- **Self-healing by replacement.** Pushing the whole file and replacing state is idempotent — a corrupted or dropped update is fully corrected by the next cycle, with no dependency on every delta arriving exactly once, in order.
- **Trivially provisioned.** Capacity is sized for the known constant load; the control plane physically cannot generate a bigger spike than normal.
- The price is deliberate waste — always doing the maximum work — which is why it fits small-payload, high-stakes planes (health checks, configuration) rather than data planes.

## Q zh
Constant-work 模式说：可靠的系统无论风平浪静还是全面故障都应做*同样多的工作* — 例如 Route 53 每隔几秒推送完整的健康检查结果文件，而不是在变化时发送 delta。这换来了什么？

## A zh
- **故障模式 = 正常模式。** 基于 delta 的系统平静时几乎不做事，大量东西同时变化时却涌来洪水般的工作 — 它最忙、最少被测试的模式恰好与故障重合。constant-work 系统只有一种模式，每几秒排练一次，永不间断。
- **没有恢复洪峰。** 分区或崩溃之后没有积压的错过更新需要重放；下一次全量推送直接覆盖状态。恢复的成本与稳态相同。
- **以替换实现自愈。** 推整个文件并替换状态是幂等的 — 损坏或丢失的更新会被下一个周期完全纠正，不依赖每个 delta 恰好一次、按序到达。
- **容量规划变平凡。** 按已知的恒定负载配容量；控制面物理上不可能产生比平时更大的尖峰。
- 代价是刻意的浪费 — 永远做最大量的工作 — 所以它适合小载荷、高风险的平面（健康检查、配置），而不是数据面。
