---
id: k8s-object-manifest-notes
node: p1.t05.object-manifest-apiversion-kind-metadata-spec-st
type: qa
step: 1
tags: [摘要]
---
## Q
**Object manifest**｜摘要 · 必会

Kubernetes 里的每个对象（Pod、Service、Node……）的 YAML 都由哪几块组成？各块写什么？

## A
**一句话：** 每个对象都是同一个骨架：`apiVersion`、`kind`、`metadata`、`spec`，读出来时多一块 `status`。

```yaml
apiVersion: v1          # 属于哪个 API 组和版本
kind: Pod               # 什么类型的对象
metadata:               # 身份信息
  name: kiada           # 名字（同类型、同命名空间里唯一）
  labels: {app: kiada}  # 标签，用来分组、被选择
spec:                   # 期望状态：你想要它是什么样
  containers:
  - name: kiada
    image: luksa/kiada:0.1
status:                 # 实际状态：由系统写，你不写
  phase: Running
  podIP: 10.244.1.5
```

| 字段 | 谁写 | 作用 |
|---|---|---|
| `apiVersion` | 你 | 对象所在的 API 组/版本，如 `v1`、`apps/v1` |
| `kind` | 你 | 对象类型，首字母大写，如 `Deployment` |
| `metadata` | 你写名字和标签，系统补 `uid`、创建时间等 | 身份 |
| `spec` | 你 | 期望状态 |
| `status` | 系统 | 实际状态 |

- **读任意对象的办法：** `kubectl get node <name> -o yaml`，然后按这五块逐块看；不认识的字段用 `kubectl explain node.spec` 查。
- **例外：** ConfigMap（存放配置键值的对象，第 3 部分细讲）、Secret（存放密码、令牌等敏感配置的对象，第 3 部分细讲） 等少数对象没有 `spec`，直接是 `data` 之类的字段。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §4.1–4.2（Object manifest、用 Node 对象逐字段读）

</details>
