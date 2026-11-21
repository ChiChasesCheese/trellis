---
id: k8s-endpointslice-beyond
node: p4.t01.endpoints-endpointslice-readiness-probe
type: qa
step: 3
tags: [拓展]
---
## Q
**Service 相关弃用与新特性 · 2026 实践**｜拓展 · v1.33 / v1.36

你手上的老 YAML、老脚本里还在读 `Endpoints`、给 Service 设 `externalIPs`。2026 年这些要怎么处理？

## A
| 项 | 状态 | 怎么办 |
|---|---|---|
| `Endpoints` API | **v1.33 弃用** | 改读 **EndpointSlice** |
| Service `.spec.externalIPs` | **v1.36 弃用**，计划 v1.43 移除 | 改用 LoadBalancer 或 Gateway API（新一代的集群流量入口 API，本部分后面细讲） |
| 多个 Service CIDR | **v1.33 GA** | 集群的 Service IP 段用完时可以追加新的段 |

```bash
# 以前
kubectl get endpoints kiada
# 现在
kubectl get endpointslices -l kubernetes.io/service-name=kiada
```

- **为什么 EndpointSlice 更好：** 大 Service 拆成多片，变动时只更新一小片。
- **externalIPs 的问题：** 它让任何有权创建 Service 的人声明任意外部 IP，是已知的安全隐患。
- **升级前：** 全文搜索 `kind: Endpoints`、`externalIPs`，列出还在用的地方。

**出处：** kubernetes.io 发布博客 v1.33（Endpoints 弃用、多 Service CIDR GA，KEP-1880）、v1.36（externalIPs 弃用，计划 v1.43 移除）
