---
id: k8s-reconcile-loop-exam
node: p1.t04.declarative-model-reconcile-loop
type: qa
step: 2
tags: [考点]
---
## Q
**Reconcile loop · 考点**｜考点 · 必会

ReplicaSet controller 所在的进程重启了，停了 10 分钟。这期间有人删了 2 个 Pod（期望 3 个）。它恢复后，如果 controller 靠「事件」工作，会丢什么？Kubernetes 实际怎么避免？

## A
| | Edge-triggered（靠事件） | Level-triggered（看当前状态） |
|---|---|---|
| 依据 | 「刚发生了删除事件」 | 「期望 3，现在 1」 |
| 停机 10 分钟 | 事件已经错过，永远不知道少了 2 个 | 起来后重新对比，立刻补 2 个 |
| 事件重复或乱序 | 可能多补或少补 | 不影响，每轮都重新数 |

- **Kubernetes 的选择：** controller 启动后先 **list** 一遍当前对象，再 **watch** 后续变化；每一轮 reconcile 只问「现在和 spec 差多少」。
- **设计原则：** 把「要什么」存成状态，而不是把「做什么」存成事件。状态可以反复对比、反复修复，事件错过就没了。
- **同理：** 你手工多建了 1 个带同样标签的 Pod，也会被发现多了 1 个并删掉一个，而不是「没人通知所以不管」。

**出处：** Poulton ch2；kubernetes.io Concepts › Controllers（controller 通过 API server 观察并驱动状态向期望靠拢）
