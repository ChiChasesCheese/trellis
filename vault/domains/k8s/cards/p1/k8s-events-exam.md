---
id: k8s-events-exam
node: p1.t05.events-kubectl-describe
type: qa
step: 2
tags: [考点]
---
## Q
**排查顺序**｜考点 · 必会

你部署后一小时发现某个 Pod 一直 Pending，`kubectl describe` 的 Events 一栏是空的。这是什么情况？接下来怎么查？

## A
**为什么空：** Event 默认只保留一小时，描述里的 Events 来自 etcd，过期就没了。不是「没有发生过事」。

| 步骤 | 做什么 | 看什么 |
|---|---|---|
| 1 | `kubectl get pod <名> -o yaml` | `status.conditions` 里的 reason 和 message，这是对象自己保存的状态，不会过期 |
| 2 | `kubectl describe pod <名>` 的 Node 一栏 | 空：还没被 scheduler 放置；有：卡在 kubelet |
| 3 | `kubectl get events --field-selector type=Warning` | 近期整个 namespace 的告警 |
| 4 | 必要时触发一次重建，立刻看新 Events | Event 是即时的 |

- **关系：** status 是「现在的状态」（对象里），Event 是「刚发生的事」（独立对象，会过期）。长期告警要靠外部监控记录。
- **字段名怎么知道：** `kubectl explain events` 会列出 `type` 等字段和取值。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §4.3（Event 一小时后删除；`--field-selector type=Warning`；`kubectl explain events`）

</details>
