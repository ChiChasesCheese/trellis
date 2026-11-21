---
id: k8s-api-rest-exam
node: p1.t06.api-rest-api-groups-versions
type: qa
step: 2
tags: [考点]
---
## Q
**API 的形状 · 考点**｜考点 · 必会

写出下面三项的 REST 路径：
1. 命名空间 `shield` 里的所有 Pod
2. 命名空间 `dev` 里的 Deployment `web`
3. 所有 Node

并回答：为什么 Node 的路径里没有命名空间？

## A
| # | 路径 |
|---|---|
| 1 | `GET /api/v1/namespaces/shield/pods/` |
| 2 | `GET /apis/apps/v1/namespaces/dev/deployments/web` |
| 3 | `GET /api/v1/nodes/` |

- **Node 没有命名空间：** Node 是整个集群的资源，不归属任何命名空间，所以路径更短。可以用 `kubectl api-resources` 里 `NAMESPACED` 一列判断（`nodes` 是 `false`，`pods` 是 `true`）。
- **常见错误：** 把 Deployment 写到 `/api/v1/...`（核心组里没有它）。判断方法：看 `apiVersion`，`v1` 走 `/api/v1`，`apps/v1` 走 `/apis/apps/v1`。
- **为什么分组：** 书里的说法，把 API 拆成较小的组，更容易扩展和导航；新资源都进命名组。
- **版本：** 同一个资源可能有多个版本（如 `v1beta1` → `v1`），旧版本会被弃用，写 manifest 时用当前的稳定版本。

**出处：** Poulton ch14「The API」（核心组与命名组的路径表）
