---
id: k8s-pod-status-exam
node: p2.t02.pod-status-phase-conditions-container-states
type: qa
step: 2
tags: [考点]
---
## Q
**Pod status**｜考点 · 必会

三种 `kubectl get pods` 的输出，各是什么问题？
1. `0/1  Pending`
2. `0/1  Running`，`RESTARTS 0`，一直如此
3. `0/1  CrashLoopBackOff`，`RESTARTS 7`

## A
| 输出 | 状态含义 | 下一步 |
|---|---|---|
| 1 | phase 是 Pending：没分配到 node，或在拉镜像 | `describe pod`：看 NODE 是否为空、Events 里有没有调度失败或镜像拉取失败 |
| 2 | 容器在跑（Running），但 Ready 是 False，没有重启 | 就绪探针没通过：应用还没起来，或探针配错。看 `describe` 的 Conditions 和 Events，应用日志 |
| 3 | 容器反复崩溃，kubelet 在重启，间隔越来越长（退避） | `logs --previous` 看崩溃原因，`describe` 看退出码 |

- **注意：** `CrashLoopBackOff` 不是 phase，是容器 Waiting 状态的 reason。
- **第 2 行的陷阱：** Running 却不接流量，Service 不会把请求送过来。很多「部署了但访问不到」就是这个。
- **所以：** 判断一个 Pod 好不好，看 Ready，不看 Running。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §6.1；KIA2 §6.2（CrashLoopBackOff）

</details>
