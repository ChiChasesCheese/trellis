---
id: k8s-gateway-vs-ingress-exam
node: p4.t03.gateway-api-ingress
type: qa
step: 2
tags: [考点]
---
## Q
**Gateway API vs Ingress**｜考点 · 必会

你的团队用 Ingress NGINX，靠 annotation 做金丝雀（10% 流量给新版本）。下面三件事，各会对你的选型产生什么影响？
1. 2026 年 3 月，Ingress NGINX 停止发布和安全修复
2. 想换到另一个 Ingress 控制器
3. 平台团队想让各业务团队自己管路由，但不能让他们动负载均衡器

## A
| # | 影响 | 说明 |
|---|---|---|
| 1 | 要迁移 | Ingress NGINX 于 **2026-03-24 退役**，之后没有新版本、没有安全修复。已有部署还能跑，但不该长期依赖 |
| 2 | annotation 不通用 | 金丝雀这类能力是控制器私有的 annotation，换控制器要重写。Gateway API 把权重切分写进标准字段，可移植 |
| 3 | Gateway API 的角色拆分正好适用 | 运维管 Gateway（负载均衡器），开发者只写自己的 HTTPRoute，谁也不用碰对方的对象 |

```yaml
# HTTPRoute 里的权重切分：标准字段，不靠 annotation
rules:
- backendRefs:
  - {name: kiada-v1, port: 8080, weight: 90}
  - {name: kiada-v2, port: 8080, weight: 10}
```

- **版本：** Gateway API v1.0 于 2023-10-31 GA，Gateway、GatewayClass、HTTPRoute 为 v1。
- **迁移时：** 可以先让 Ingress 和 Gateway 并存，按服务逐个切换。

<details class="pt" markdown="1"><summary>出处</summary>

Ingress NGINX 退役见 kubernetes.io 博客 2025-11-11 与 v1.36 发布博客；Gateway API v1.0 GA 见 kubernetes.io 博客 2023-10-31；Poulton ch8；KIA2 ch13（HTTPRoute 的 weight）

</details>
