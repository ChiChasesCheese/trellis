---
id: k8s-preemption-beyond
node: p2.t04.priorityclass-preemption-poddisruptionbudget
type: qa
step: 3
tags: [拓展]
---
## Q
**异步 preemption · 2026 实践**｜拓展 · v1.33 beta

高优先级 Pod 触发 preemption 时，scheduler 要先发一批「删除 Pod」的 API 调用，这段时间里其他 Pod 的调度会被拖慢吗？

## A
| 版本 | 状态 | 变化 |
|---|---|---|
| v1.32 | alpha | 引入 asynchronous preemption |
| **v1.33** | **beta** | 删除受害者 Pod 的 API 调用**并行**处理，scheduler 可以继续调度别的 Pod（KEP-4832） |

- **以前：** 驱逐 Pod 这类重操作串在调度循环里，Pod 频繁变动或调度频繁失败的集群里，别的 Pod 也被拖慢。
- **不变的：** 受害者仍有完整的 graceful termination 宽限期；被抢位置的 Pod 在 status 里记 `nominatedNodeName`，这只是「预留意向」，最终放不放这台 node 还要重新判断。
- **注意：** preemption 尽力而为，并不保证成功；也不保证 PDB 一定被遵守（文档说明 preemption 对 PDB 只是尽力而为）。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.33（Asynchronous preemption in the Kubernetes Scheduler，KEP-4832）；Concepts › Pod Priority and Preemption（nominatedNodeName、graceful termination）

</details>
