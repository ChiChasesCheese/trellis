---
id: k8s-api-pipeline-exam
node: p1.t06.api-server-request-pipeline-authentication-autho
type: qa
step: 2
tags: [考点]
---
## Q
**API server request pipeline**｜考点 · 必会

三条报错，各是哪一关拒绝的？
1. `error: You must be logged in to the server (Unauthorized)`
2. `Error from server (Forbidden): pods is forbidden: User "alice" cannot list resource "pods" in namespace "prod"`
3. `Error from server: admission webhook "policy.example.com" denied the request: …`

## A
| 报错 | 关卡 | 含义 | 去哪里改 |
|---|---|---|---|
| 1 Unauthorized（401） | Authentication | API server 不认识你：证书过期、令牌错 | 检查 kubeconfig 里的凭据 |
| 2 Forbidden（403） | Authorization | 认得你是 alice，但没有权限 | 给 alice 加 Role / RoleBinding |
| 3 admission webhook denied | Admission（validating 或 mutating） | 身份和权限都通过，被策略拒绝 | 看策略写了什么，改你的 manifest |

- **记法：** 401 是「你是谁」，403 是「你能不能」，准入是「你做的这件事合不合规」。
- **顺序的推论：** 只要看到准入层的报错，说明认证和鉴权已经通过了。
- **admission webhook：** 准入阶段可以调用外部服务做检查，故障时会拖慢或拒绝所有相关请求（第 8 部分的内容）。

<details class="pt" markdown="1"><summary>出处</summary>

Poulton ch13（authentication、authorization、admission control）；kubernetes.io Reference › Controlling Access to the Kubernetes API

</details>
