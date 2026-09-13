---
id: leetcode-c-kubernetes-scheduler-queues-application
node: topics.uncategorised
type: qa
anki: 1787359912693
tags: [algorithm::event-driven-requeue, algorithm::exponential-backoff, algorithm::heap, algorithm::priority-queue, application, case, case::kubernetes-scheduler-queues, category::developer-infrastructure, leetcode, system::kubernetes-scheduler]
---
## Q
Kubernetes Scheduler 为什么不能只用一个 priority heap？activeQ、backoffQ 和 unschedulable 集合分别解决什么？

## A
activeQ 的 heap 负责选下一个最高优先级 Pod；backoffQ 按重试到期时间隔离持续失败的 Pod，避免 hot loop；unschedulable 集合等待可能改变可行性的 cluster event，再由 queueing hint 选择性 requeue。

**Evidence**

Kubernetes 官方 scheduler queue 源码使用 backend/heap，并实现 activeQ、backoffQ、unschedulable entities 与 event-driven queueing hints。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FKubernetes%20Scheduler%EF%BC%9A%E4%BC%98%E5%85%88%E9%98%9F%E5%88%97%E3%80%81%E9%80%80%E9%81%BF%E4%B8%8E%E4%BA%8B%E4%BB%B6%E9%87%8D%E6%8E%92%E9%98%9F)
