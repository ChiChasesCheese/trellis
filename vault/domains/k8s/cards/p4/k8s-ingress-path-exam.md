---
id: k8s-ingress-path-exam
node: p4.t02.tls-annotations-ingressclass-backend
type: qa
step: 2
tags: [考点]
---
## Q
**路径与主机匹配 · 考点**｜考点 · 必会

一条规则：host `api.example.com`，两个路径：`/quote`（`Exact`）转 quote 服务，`/questions`（`Prefix`）转 quiz 服务。请求 `/quote/today`、`/questions/random`、`/questions`、`/QUOTE` 各去哪里？另外，host 写成 `*.example.com` 能匹配 `a.b.example.com` 吗？

## A
| 请求路径 | 结果 | 原因 |
|---|---|---|
| `/quote` | quote | Exact 完全相等 |
| `/quote/today` | **不匹配**（404 或 default backend） | Exact 不接受多出来的部分 |
| `/questions/random` | quiz | Prefix 按 `/` 分段匹配 `questions` 这一段 |
| `/questions` | quiz | 同上 |
| `/QUOTE` | 不匹配 | 匹配**区分大小写** |

| host 规则 | 请求 host | 匹配吗 |
|---|---|---|
| `*.example.com` | `api.example.com` | 是 |
| `*.example.com` | `a.b.example.com` | **否**，通配符只覆盖**一段**域名标签 |
| `*.example.com` | `example.com` | 否 |

- **同时命中多条路径：** `Exact` 优先。
- **没有改写：** 转给后端的路径和请求一样，后端要自己认 `/quote`；要改写得用 controller 的私有 annotation。
- **规则都不命中：** 用 default backend 或返回 404。

**出处：** KIA2 §12.2.2（pathType 表 12.1，`Exact` 优先，不做 URL 改写）、表 12.4（通配符）；kubernetes.io Concepts › Ingress（区分大小写、通配符只覆盖单个 DNS 标签）
