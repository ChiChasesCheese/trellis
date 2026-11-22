---
id: k8s-end-to-end-exam
node: p1.t04.end-to-end-walk-through
type: qa
step: 2
tags: [考点]
---
## Q
**End-to-end walk-through**｜考点 · 必会

`kubectl apply` 一个 Deployment（3 副本）后，你看到：Deployment 存在、ReplicaSet 存在、**没有任何 Pod**。问题出在链路的哪一步？如果是 Pod 存在但 `READY 0/1`、状态是 Pending 且已分配了 node，又出在哪？

## A
**情况一：有 ReplicaSet，没有 Pod。** 卡在 **ReplicaSet controller 创建 Pod 对象**（步骤 3）这一步。可能是 controller manager 没在跑，或创建请求被 API server 拒绝（比如命名空间里的配额不够，会在 ReplicaSet 的 Events 里看到原因）。

**情况二：Pod 已分配 node，但还在 Pending。** 卡在 **node 上**（步骤 5–6）：镜像拉取慢或拉取失败、runtime 出错。

| 现象 | 链路上的位置 | 看什么 |
|---|---|---|
| 没有 Deployment | 步骤 1–2 | kubectl 的报错、认证鉴权 |
| 有 Deployment，没有 ReplicaSet | 步骤 3 前半 | controller manager |
| 有 ReplicaSet，没有 Pod | 步骤 3 后半 | `kubectl describe rs` 的 Events |
| Pod 的 NODE 为空 | 步骤 4：scheduler | `kubectl describe pod` 的 Events |
| NODE 有值，容器起不来 | 步骤 5–6：kubelet / runtime | Pod 的 Events、镜像名、node 状态 |
| 一直 `0/1` 不就绪 | 步骤 7 以后：容器已起，探针没过 | 第 2 部分的 probe |

- **方法：** 沿着「一对象 → 下一个对象」的链路，找最后一个正常存在的环节，下一环就是嫌疑。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §1.2.4、§3.3（Pod 先 Pending 再 Running）；Poulton ch2

</details>
