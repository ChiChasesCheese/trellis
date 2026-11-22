---
id: k8s-ingress-retirement-beyond
node: p4.t02.ingress-ingress-controller
type: qa
step: 3
tags: [拓展, 时效]
---
## Q
**Ingress 的现状 · 2026 实践**｜拓展 · 2026-03-24

你的集群用着 Ingress NGINX。2026 年它的状况是什么？Ingress API 本身还能用吗？

## A
| 项 | 状态 |
|---|---|
| **Ingress NGINX**（Kubernetes 项目里的 NGINX controller） | **2026-03-24 退役**：之后不再发布新版本、不修 bug、不修安全漏洞。已有部署继续工作，Helm chart 和镜像仍可获取 |
| **Ingress API**（`networking.k8s.io/v1`） | 已 **frozen**：仍是 GA，没有移除计划，但**不再开发**，不会有新字段 |
| 官方建议 | 新项目用 **Gateway API**；非要用 Ingress，换别的 controller |

- **为什么退役：** 灵活性过大带来维护负担，如「snippets」类 annotation 能插入任意 NGINX 配置，后来被视为严重安全隐患；长期只有一两个维护者，利用业余时间开发。
- **自查：** `kubectl get pods --all-namespaces --selector app.kubernetes.io/name=ingress-nginx`（需要集群管理员权限）。
- **迁移要点：** annotation（如 `nginx.ingress.kubernetes.io/...`）是 controller 私有的，换了 controller 就失效；这些能力在 Gateway API 里多半有标准字段（权重、header 匹配、改写）。
- **继续用的风险：** 已知漏洞不会再被修，不要继续把它暴露在公网。

**出处：** kubernetes.io 博客 2025-11-11「Ingress NGINX Retirement: What You Need to Know」；v1.36 发布博客（2026-03-24 已退役）；Concepts › Ingress（API frozen）
