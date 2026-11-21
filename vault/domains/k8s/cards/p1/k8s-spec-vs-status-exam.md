---
id: k8s-spec-vs-status-exam
node: p1.t05.spec-vs-status-conditions
type: qa
step: 2
tags: [考点]
---
## Q
**spec vs status 与 conditions · 考点**｜考点 · 必会

一台 node 的 conditions 显示 `Ready: Unknown`，另一台显示 `Ready: False`。两者含义差在哪？还有：你手工 `kubectl edit` 把 Deployment 的 `status.readyReplicas` 改成 3，会怎样？

## A
| | Ready: False | Ready: Unknown |
|---|---|---|
| 意思 | node 汇报了「我不健康」 | 控制面很久没收到 node 的汇报，不知道 |
| 常见原因 | 磁盘、网络、kubelet 自己发现问题 | node 宕机、断网、kubelet 停了 |
| reason / message | 有具体原因 | 一般表示失联 |

- **关键区别：** False 是 node 自己说话了，Unknown 是 node 没说话。这就是为什么 conditions 用三态，而不是布尔值。
- **改 `status`：** 没有意义。`status` 由系统维护，每个 controller 下一轮会把它写回真实值（`status` 是观察结果，不是你可以下的命令）。你该改的永远是 `spec`。
- **排查时读哪里：** `kubectl describe` 把 `Conditions` 单独列出来，先看 `Reason` 和 `Message`。

**出处：** KIA2 §4.2.3；Poulton ch2（kubelet 汇报状态给 API server）
