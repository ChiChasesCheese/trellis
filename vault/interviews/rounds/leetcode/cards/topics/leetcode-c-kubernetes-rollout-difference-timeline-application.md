---
id: leetcode-c-kubernetes-rollout-difference-timeline-application
node: topics.uncategorised
type: qa
anki: 1787361362423
tags: [algorithm::difference-array, algorithm::event-timeline, algorithm::prefix-sum, application, case, case::kubernetes-rollout-difference-timeline, category::developer-infrastructure, chapter::14, leetcode, system::kubernetes-deployment]
---
## Q
如何用差分事件重建 Kubernetes rollout 的 total/available replicas 曲线？

## A
create/delete 分别对 total 做 +1/-1，ready/unready 对 available 做 +1/-1；按版本/时间有序重放并做 prefix sum，即可在每个边界检查 maxSurge 与 maxUnavailable。

**Evidence**

Kubernetes 官方文档定义 RollingUpdate bounds 与 watch 语义；差分重放是对这些状态转移的审计模型。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FKubernetes%20RollingUpdate%EF%BC%9A%E5%AE%B9%E9%87%8F%E4%BA%8B%E4%BB%B6%E5%B7%AE%E5%88%86%E5%AE%A1%E8%AE%A1)
