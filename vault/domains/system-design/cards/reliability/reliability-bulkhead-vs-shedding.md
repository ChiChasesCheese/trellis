---
id: reliability-bulkhead-vs-shedding
node: reliability.resilience.containment
type: qa
---
## Q
Bulkheads vs load shedding — which failure does each contain, and when do you need both?

## A
- **Bulkheads** partition resources (connection pools, thread pools, instances) per dependency or tenant, so one slow dependency exhausts only its own pool — contains **cross-contamination**.
- **Load shedding** rejects excess work (by priority, early, cheaply — e.g. 429 at the front door) so the work you do accept finishes within SLO — contains **overload**.

You need both when a multi-tenant service faces both noisy neighbors and traffic spikes: bulkheads isolate who hurts, shedding caps how much total hurt is accepted.

## Q zh
Bulkhead vs load shedding ——每个遏制什么故障，什么时候两者都需要？

## A zh
- **Bulkhead** 按依赖或租户分割资源（连接池、线程池、实例），所以一个慢依赖只会耗尽自己的池——遏制**跨污染**。
- **Load shedding** 拒绝过度工作（按优先级、提前、便宜地——例如在前门返回 429），所以你接受的工作能在 SLO 内完成——遏制**过载**。

当多租户服务面临既有嘈杂邻居又有流量峰值时需要两者：bulkhead 隔离谁造成伤害，shedding 限制接受多少伤害。
