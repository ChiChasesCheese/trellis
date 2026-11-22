---
id: k8s-scheduling-constraints-beyond
node: p2.t04.affinity-taints-tolerations-topology-spread
type: qa
step: 3
tags: [拓展]
---
## Q
**调度约束的新字段 · 2026 实践**｜拓展 · v1.33 / v1.35

滚动更新时，新旧版本的 Pod 的 anti-affinity 和 topology spread 总是把彼此算进去，导致放不下。以及 taint 能不能表达「SLA 等级」这种数字？

## A
| 特性 | 状态 | 解决什么 |
|---|---|---|
| Pod affinity 的 `matchLabelKeys`、`mismatchLabelKeys` | **v1.33 稳定**（KEP-3633） | 按「同一批」Pod（比如同一 `pod-template-hash`）划范围，滚动更新时新旧版本互不干扰 |
| topology spread 的 `nodeAffinityPolicy`、`nodeTaintsPolicy` | v1.33 发布博客列入稳定 | 计算 skew 时是否考虑 node affinity 和 taint；默认 `Honor` / `Ignore`，避免因为算了不可用的 node 而一直 Pending |
| toleration 的数字比较运算符（如 `Gt`、`Lt`） | **v1.35 alpha**（KEP #5471） | 用数字型 taint 表达 SLA 或容错域质量，让关键负载挑高 SLA 的 node |

```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector: {matchLabels: {app: web}}
  matchLabelKeys: [pod-template-hash]   # 只和同一批 Pod 比
  nodeTaintsPolicy: Honor               # 算 skew 时考虑 node 的 taint
```

- **alpha 默认关闭：** 数字 toleration 不要用在生产，先在测试集群试。
- **升级前：** 看一下你的 spread 约束有没有因为 taint 被排除的 zone。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.33（KEP-3633；PodTopologySpread nodeAffinityPolicy/nodeTaintsPolicy 一节）、v1.35（Extended toleration operators，KEP #5471）

</details>
