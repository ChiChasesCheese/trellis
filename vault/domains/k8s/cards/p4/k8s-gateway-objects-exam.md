---
id: k8s-gateway-objects-exam
node: p4.t03.gatewayclass-gateway-httproute
type: qa
step: 2
tags: [考点]
---
## Q
**Gateway 与 HTTPRoute · 考点**｜考点 · 必会

你创建了 Gateway 和 HTTPRoute，但访问不通。`kubectl get gateway` 的 `PROGRAMMED` 是 `False`；另一种情况是 Gateway 正常，但 HTTPRoute 的 status 里 `ResolvedRefs: False`。分别该往哪查？

## A
| 现象 | 条件含义 | 去哪查 |
|---|---|---|
| Gateway `Accepted: False` | 控制器没接受这个 Gateway | GatewayClass 是否存在、名字对不对、控制器是否在跑；`reason` 里有原因（如端口不可用） |
| Gateway `Programmed: False` | 配置没能下发到负载均衡器 | 看 `reason`（如无效配置）和控制器日志 |
| HTTPRoute `Accepted: False` | 没有被它的父 Gateway 接受 | `parentRefs` 的名字、命名空间，Gateway 是否允许这个命名空间的路由 |
| HTTPRoute `ResolvedRefs: False` | `backendRefs` 里的引用解析不了 | 后端 Service 名字、端口是否存在；跨命名空间引用有没有授权 |

```bash
kubectl get gateway
kubectl describe httproute kiada      # 看 Status 里每个 parent 的 Conditions
```

- **读法：** 和第 1 部分的 conditions 一样，看 `type`、`status`、`reason`、`message`。
- **顺序：** 先看 GatewayClass 和 Gateway 是否 Accepted、Programmed，再看路由。

**出处：** KIA2 §13（Gateway 与 HTTPRoute 的 status conditions：Accepted、Programmed、ResolvedRefs）
