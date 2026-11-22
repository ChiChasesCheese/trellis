---
id: k8s-control-plane-down-exam
node: p1.t01.cluster-architecture
type: qa
step: 2
tags: [考点]
---
## Q
**Cluster architecture**｜考点 · 必会

control plane 整个不可用了（比如 etcd 因网络分区进入只读）。已经在 worker 上跑着的应用，会怎样？你还能做什么、不能做什么？

## A
**结论：** 已经在跑的应用继续跑，但集群「失去大脑」，不会再变化。

| 事情 | 能不能 |
|---|---|
| 现有容器继续处理请求 | 能，容器在 worker 上，kubelet 和 runtime 不依赖大脑每秒指挥 |
| `kubectl apply`、`scale`、升级 | 不能，请求要经过 API server 并写进 etcd |
| 某个容器崩了被重启 | 能，kubelet 在本机处理 |
| 某台机器整个宕机后在别处补 Pod | 不能，没有 controller 在跑，也没人调度 |

- **书里的说法：** etcd 进入只读后，「用户应用继续工作，但 Kubernetes 无法扩容或更新它们」。
- **为什么生产要 3 或 5 个 control plane 节点：** etcd 要多数派（quorum）才能写，奇数个副本能避免两边各占一半、谁都不够多数的僵局（split brain）。
- **高可用不是备份：** 多副本不能代替对 etcd 的备份和恢复方案。

<details class="pt" markdown="1"><summary>出处</summary>

Poulton ch2「The cluster store」「Control plane and worker nodes」

</details>
