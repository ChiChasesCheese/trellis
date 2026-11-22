---
id: k8s-emptydir-exam
node: p3.t02.volumes-emptydir
type: qa
step: 2
tags: [考点]
---
## Q
**Volumes 与 emptyDir**｜考点 · 必会

一个 Pod 里的 MongoDB 容器把数据写在 emptyDir 卷里。依次发生：
1. MongoDB 容器 OOM 被杀并重启
2. 你执行 `kubectl delete pod`，Deployment 补了一个新 Pod
3. node 宕机，Pod 被调度到另一台 node

每次，数据还在吗？

## A
| 事件 | 数据 | 原因 |
|---|---|---|
| 1 容器重启 | 在 | 卷属于 Pod，Pod 没变 |
| 2 Pod 被删、重建 | **不在** | 新 Pod 是新对象，得到新的空 emptyDir |
| 3 换 node | **不在** | emptyDir 在原来那台 node 上，Pod 换了，卷也没了 |

- **结论：** emptyDir 只适合容器重启后还要的临时数据、缓存，不适合数据库的真正数据。
- **真正要持久化的数据：** 用 PersistentVolumeClaim（Pod 申请持久存储用的对象，下一章细讲），数据在 Pod 之外，Pod 重建后可以再挂回来。
- **判断口诀：** 问「这份数据比这个 Pod 活得久吗？」是，就不能用 emptyDir。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §9.2（emptyDir 的数据在 Pod 存续期间保留）、§10.1

</details>
