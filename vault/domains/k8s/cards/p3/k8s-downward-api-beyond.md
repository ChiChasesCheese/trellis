---
id: k8s-downward-api-beyond
node: p3.t01.downward-api
type: qa
step: 3
tags: [拓展]
---
## Q
**Node 拓扑标签进 Pod · 2026 实践**｜拓展 · v1.35 beta

应用想知道自己跑在哪个 zone、哪个 region，以前要给 ServiceAccount 开 RBAC 去查 Node 对象，或者加一个 sidecar。2026 年有更简单的办法吗？

## A
| 项 | 内容 |
|---|---|
| 特性 | kubelet 把 node 的标准拓扑 label（如 `topology.kubernetes.io/zone`、`topology.kubernetes.io/region`）直接注入 Pod，作为环境变量或 projected 卷里的文件，通过 Downward API 读取 |
| 状态 | **v1.35 beta**（默认开启，KEP #4742） |
| 好处 | 应用不用调 API server，也不用给自己开读 Node 的权限，最小权限 |
| 注意 | 升级到 v1.35 后，每个 Pod 上会多出几个拓扑相关的 label，这是预期行为 |

- **配合：** topology spread 解决「Pod 放哪」，第 4 部分的就近路由解决「流量往哪」，这里解决「应用自己知道在哪」，例如选择同 zone 的缓存节点。
- **仍是 beta：** 在 v1.35 中默认开启，但不要假设所有集群都已升级。

**出处：** kubernetes.io 发布博客 v1.35（Expose node topology labels via Downward API，beta，KEP #4742）
