---
id: k8s-object-manifest-exam
node: p1.t05.object-manifest-apiversion-kind-metadata-spec-st
type: qa
step: 2
tags: [考点]
---
## Q
**Object manifest · 考点**｜考点 · 必会

下面的 YAML 执行 `kubectl apply` 会报错。错在哪？如何修？

```yaml
apiVersion: v1
kind: deployment
metadata:
  name: kiada
spec:
  replicas: 3
  selector:
    matchLabels: {app: kiada}
  template:
    metadata:
      labels: {app: kiada}
    spec:
      containers:
      - name: kiada
        image: luksa/kiada:0.1
```

## A
**两处错误：**

| 错误 | 原因 | 修正 |
|---|---|---|
| `kind: deployment` | `kind` 区分大小写，类型名首字母大写 | `kind: Deployment` |
| `apiVersion: v1` | Deployment 不在核心组，而在 `apps` 组 | `apiVersion: apps/v1` |

- **怎么知道该写什么：** `kubectl api-resources` 列出每种资源的 `APIVERSION` 和 `KIND`（例如 `deployments  deploy  apps/v1  true  Deployment`）。
- **`kubectl explain deployment`：** 显示该类型的字段说明。
- **核心组的对象只写版本：** Pod、Service、Node、Namespace 是 `v1`；其余是 `组/版本`。

**出处：** KIA2 §4.2；Poulton ch14「Inspecting the API」（`kubectl api-resources` 输出）
