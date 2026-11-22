---
id: k8s-control-plane-node-exam
node: p1.t04.control-plane-node
type: qa
step: 2
tags: [考点]
---
## Q
**Control plane 与 node 组件**｜考点 · 必会

下面三个现象，哪个组件出了问题？
1. 新建的 Pod 一直 Pending，`kubectl describe pod` 里 NODE 一栏是 `<none>`
2. Pod 已经被分配到 node（NODE 有值），但状态一直停在 ContainerCreating，`kubectl get nodes` 显示这台 node 是 NotReady
3. 所有 `kubectl` 命令都超时，但机器上已经在跑的应用还能访问

## A
| 现象 | 嫌疑 | 推理 |
|---|---|---|
| 1 | **scheduler** | 放到哪台机器是 scheduler 的活，NODE 为空说明还没人分配。可能 scheduler 没在跑，也可能没有合适的 node |
| 2 | **kubelet / runtime** | 已经分配了，卡在本机起容器这一步。node NotReady 说明 kubelet 没向 API server 汇报 |
| 3 | **API server**（或它背后的 etcd） | 所有请求都经它；已在跑的容器只靠 kubelet 和 runtime，不受影响 |

- **排查顺序的思路：** 顺着「一条请求的旅程」找它停在了哪一步（见 end-to-end 一卡）。
- **注意：** 现象 1 的另一种原因是资源不够，所有 node 都装不下。这时 describe 的 Events 里会有 scheduler 写的原因。

<details class="pt" markdown="1"><summary>出处</summary>

Poulton ch2（scheduler 找不到合适节点则标记 pending；kubelet 汇报任务状态）；KIA2 §1.2

</details>
