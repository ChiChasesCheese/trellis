---
id: infra-requests-limits-noisy-neighbor
node: infra.containers
type: qa
---
## Q
On a shared Kubernetes node, what do resource *requests* vs *limits* actually do — and why do CPU and memory overruns fail differently?

## A
- **Requests** = what the scheduler reserves when bin-packing pods onto nodes; your guaranteed share under contention. **Limits** = a hard runtime cap.
- **CPU is compressible**: hitting the limit means **throttling** — no crash, just mysterious p99 latency spikes.
- **Memory is incompressible**: hitting the limit is an **OOM-kill**.
- Noisy neighbors appear when pods set requests below real usage: the scheduler overcommits the node and co-tenants steal cycles or trigger evictions. For latency-critical pods, set requests = limits (Guaranteed QoS) to opt out of the fight.

## Q zh
在共享 Kubernetes 节点，资源**请求** vs **限制**实际上做什么——以及为什么 CPU 和内存超限失败不同？

## A zh
- **请求** = 调度器在把 pod 装箱到节点时保留什么；在竞争时你的保证份额。**限制** = 一个硬运行时上限。
- **CPU 是可压缩的**：命中限制意味着**限流**——无崩溃，只是神秘的 p99 延迟尖刺。
- **内存是不可压缩的**：命中限制是一个 **OOM-kill**。
- 吵闹邻居出现当 pod 设置请求低于真实使用：调度器超承诺节点，共租赁偷取周期或触发驱逐。对于延迟关键 pod，设置请求 = 限制（保证 QoS）来退出战斗。
