---
id: k8s-first-deployment-exam
node: p1.t03.first-deployment
type: qa
step: 2
tags: [考点]
---
## Q
**First deployment**｜考点 · 必会

kiada 现在有 3 个 Pod。你执行 `kubectl delete pod kiada-5d9c8-p449x`。几秒后 `kubectl get pods` 会看到什么？为什么？如果你用 `kubectl delete deployment kiada` 呢？

## A
**删一个 Pod：** 仍然是 3 个 Pod，但其中一个名字变了（比如 `kiada-5d9c8-x7k2q`）。

- **原因：** Deployment 要 3 份，ReplicaSet 发现只剩 2 个，就新建一个。新 Pod 是新对象，名字、IP 都是新的。
- **Service 不受影响：** 它的地址不变，只是后端换了一个 Pod。

**删 Deployment：** 它的 ReplicaSet 和 3 个 Pod 一起被清理，不会再有新的补出来。Service 还在，但后面没有 Pod 可转发。

| 你删了 | 结果 |
|---|---|
| 一个 Pod | 被补回，总数仍为 3 |
| 整个 Deployment | Pod 全部消失，没人再补 |
| 只删 Service | Pod 照常跑，只是失去固定入口 |

- **逻辑：** 有人在看着「期望 3 个」。你删的是现实，不是期望。要少一个，得改期望（`scale`）。
- **这件事是谁做的：** 下一部分讲的 controller。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §3.3（"Kubernetes ensures that the actual number of pods always matches the desired number"）

</details>
