---
id: k8s-kubectl-declarative-prereq
node: p1.t03.kubectl-imperative-vs-declarative
type: qa
step: 1
tags: [先修]
---
## Q
**kubectl 与 declarative · 先修**｜先修 · 必会

部署同一个应用，可以敲 `kubectl create deployment kiada --image=luksa/kiada:0.1`，也可以写一个 YAML 文件再 `kubectl apply -f kiada.yaml`。kubectl 是什么？这两种做法差在哪？

## A
**kubectl：** Kubernetes 的命令行工具。你敲的每条命令，都被它变成一个 HTTP 请求，发给 control plane 里的 **API server**。集群地址和你的身份，写在本机的 kubeconfig 文件里。

| | Imperative（下命令） | Declarative（交一份想要的样子） |
|---|---|---|
| 例子 | `kubectl create deployment …`、`kubectl scale … --replicas=3` | `kubectl apply -f kiada.yaml` |
| 你说的是 | 「去做这一步」 | 「最后应该是这个样子」 |
| 再跑一次 | `create` 报错：已经存在 | 没变化就什么也不做；文件改了就按文件更新 |
| 适合 | 临时试一下、学习 | 正式环境：YAML 进 git，可审查、可回滚 |

```yaml
# kiada.yaml：一份「想要的样子」
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kiada
spec:
  replicas: 3            # 想要 3 份
  selector:
    matchLabels: {app: kiada}
  template:              # 每一份 Pod 长什么样
    metadata:
      labels: {app: kiada}
    spec:
      containers:
      - name: kiada
        image: luksa/kiada:0.1
```

- **关键：** 不管用哪种，结果都是 API server 里存了一个 Deployment 对象，`spec` 里写着「想要什么」。真正把它变成现实的是 controller（下一章）。

**出处：** KIA2 §3.2–3.3（imperative 部署 Kiada）；Poulton ch2（declarative model）
