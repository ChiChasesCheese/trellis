---
id: k8s-scheduling-exam
node: p2.t04.scheduling-cycle-filter-score-bind
type: qa
step: 2
tags: [考点]
---
## Q
**Scheduling cycle**｜考点 · 必会

三台 node，每台 4 个 CPU 核，上面已有的 Pod requests 合计分别是 3.5、3.0、1.0 核，但第 3 台的实际 CPU 使用率几乎是 100%。现在要调度一个 `requests.cpu: 1` 的 Pod。它会落到哪台？如果 requests 是 2 呢？

## A
**requests 是 1 核：** 每台 node 的剩余（按 requests 算）是 0.5、1.0、3.0 核。

| node | 剩余 | 能装下 1 核吗 |
|---|---|---|
| 1 | 0.5 | 否，Filter 淘汰 |
| 2 | 1.0 | 是 |
| 3 | 3.0 | 是 |

node 2 和 3 都通过 Filter，由 Score 决定。**调度器只看 requests，不看实际使用量**，所以 node 3 虽然实际 CPU 已经跑满，仍然可能被选中，除非打分把它排后面。

**requests 是 2 核：** 只有 node 3 通过（3.0 ≥ 2），落到 node 3。

**如果 requests 是 4 核：** 没有 node 能装下，Pod 保持 Pending；`describe` 的 Events 会写 `Insufficient cpu`。

- **推论：** requests 设得比实际用量大太多，会浪费 node 容量；设得太小，node 被塞满后性能会受影响。
- **「node 上已经跑满了，为什么还调度进来」：** 因为调度看的是声明（requests），不是实测。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io Concepts › Resource Management for Pods and Containers（调度依据 requests）；Poulton ch2

</details>
