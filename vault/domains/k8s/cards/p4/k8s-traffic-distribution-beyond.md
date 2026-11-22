---
id: k8s-traffic-distribution-beyond
node: p4.t01.internaltrafficpolicy-topology-aware-routing
type: qa
step: 3
tags: [拓展]
---
## Q
**trafficDistribution · 2026 实践**｜拓展 · v1.33 / v1.34 / v1.35

老文档里让你用 `service.kubernetes.io/topology-aware-hints` 注解，也有人写 `trafficDistribution: PreferClose`。2026 年写新 Service 该怎么写？

## A
| 版本 | 变化 |
|---|---|
| v1.33 | topology-aware routing 和 `trafficDistribution: PreferClose` **GA**（KEP-4444、KEP-2433） |
| v1.34 | `PreferClose` **弃用**，新增 `PreferSameZone`（等同 `PreferClose` 的别名）和 `PreferSameNode`；两者先 beta（KEP-3015） |
| **v1.35** | `PreferSameNode` **GA**；`PreferClose` 改名为 `PreferSameZone`，旧名保留作兼容 |

```yaml
spec:
  trafficDistribution: PreferSameZone   # 或 PreferSameNode
```

- **用哪个：** 想省跨 zone 流量用 `PreferSameZone`；想让流量优先落在本机（如本机缓存、本机代理）用 `PreferSameNode`。都是**偏好**，本地没有健康后端就回退，不会失败。
- **和 `internalTrafficPolicy: Local` 分开：** 后者是硬规则。
- **迁移：** 全文搜 `PreferClose`、`topology-aware-hints`，换成新写法。字段没设置时由实现使用默认策略。
- **相关：** 同一版本里 `Endpoints` API 已弃用（v1.33），要读 EndpointSlice。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.33（topology aware routing，trafficDistribution）、v1.34（PreferClose deprecated，KEP-3015）、v1.35（PreferSameNode stable，PreferClose 改名 PreferSameZone）；Concepts › Service

</details>
