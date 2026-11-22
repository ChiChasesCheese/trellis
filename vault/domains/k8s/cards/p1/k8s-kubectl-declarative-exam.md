---
id: k8s-kubectl-declarative-exam
node: p1.t03.kubectl-imperative-vs-declarative
type: qa
step: 2
tags: [考点]
---
## Q
**kubectl 与 declarative**｜考点 · 必会

对同一个 `kiada.yaml`，依次执行：
1. `kubectl apply -f kiada.yaml`
2. 再 `kubectl apply -f kiada.yaml`
3. 把文件里 `replicas: 3` 改成 `5`，再 `kubectl apply -f kiada.yaml`
4. 全新环境里把 `apply` 换成 `kubectl create -f kiada.yaml`，连跑两次

每一步 kubectl 会输出什么？

## A
| 步骤 | 输出 | 原因 |
|---|---|---|
| 1 | `deployment.apps/kiada created` | 对象不存在，创建 |
| 2 | `deployment.apps/kiada unchanged` | 文件和现状一致，什么也不做 |
| 3 | `deployment.apps/kiada configured` | 只有 `replicas` 变了，更新这个对象 |
| 4 | 第一次 `created`，第二次报 `AlreadyExists` 错误 | `create` 是「去做创建」，对象已存在就失败 |

- **规律：** declarative 的命令可以放心重复执行（幂等）；imperative 的命令每次都是一个动作。
- **所以脚本和 CI 里用 `apply -f`：** 失败重跑也不怕。
- **注意：** `kubectl scale` 看起来像命令，实质也是修改 Deployment 里的期望副本数，Kubernetes 随后去对齐。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §3.3（`kubectl scale` 只是修改 Deployment 对象）；kubernetes.io 文档 Declarative Management of Kubernetes Objects

</details>
