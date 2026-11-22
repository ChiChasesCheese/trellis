---
id: k8s-secret-exam
node: p3.t01.secret
type: qa
step: 2
tags: [考点]
---
## Q
**Secret**｜考点 · 必会

下面四个做法，哪些真的提升了 Secret 的安全？
1. 把密码从 ConfigMap 挪到 Secret，什么都不再改
2. 开启 etcd 的静态加密
3. 把 Secret 以环境变量注入，而不是挂成文件
4. 限制只有部署流水线的账号能 `get secrets`

## A
| # | 效果 | 说明 |
|---|---|---|
| 1 | 几乎没提升 | 只是 Base64 编码，值本身没加密；唯一的好处是可以对 Secret 单独授权 |
| 2 | 有效 | 防止有人拿到 etcd 所在磁盘或备份就直接看到所有 Secret |
| 3 | 无关 | 环境变量和文件都会让应用拿到明文；环境变量还容易被写进日志 |
| 4 | 有效 | 访问由 RBAC 决定，权限过宽是常见的泄露路径 |

- **答题要点：** 区分三层：存储层（etcd 是否加密）、访问层（RBAC）、使用层（应用如何处理）。
- **真正的方案：** 外部密钥管理工具，加上轮换和审计。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §8.3

</details>
