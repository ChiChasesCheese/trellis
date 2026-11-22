---
id: k8s-containers-vs-vms-exam
node: p1.t02.containers-vs-vms
type: qa
step: 2
tags: [考点]
---
## Q
**Containers vs VMs**｜考点 · 必会

三种场景，该用容器还是 VM，为什么？
A. 同一台 Linux 机器上并排跑 20 个自己团队写的无状态服务
B. 要在 Linux 机器上跑一个只能在 Windows 上运行的程序
C. 一个平台要让互不信任的外部客户上传代码并运行

## A
| 场景 | 选择 | 理由 |
|---|---|---|
| A | 容器 | 开销小、启动快；服务彼此信任，共享内核的隔离强度够用 |
| B | VM（或 Windows 节点） | 容器共用宿主内核，Linux 内核上跑不了 Windows 程序。Kubernetes 里需要 Windows 容器时，要有 Windows worker node |
| C | 需要比普通容器更强的隔离 | 容器间共用同一个内核，恶意进程发起的系统调用可能影响整台机器 |

- **C 的做法：** 先用 seccomp（限制进程能发哪些系统调用）、capabilities（把 root 的权力拆成小块，只留需要的）收紧容器（第 6 部分），仍不够时用 VM 级的隔离。
- **反过来看：** 隔离更强就要更多开销，所以大多数「自己人的服务」选容器。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §2.1.1、§2.3.4（Strengthening isolation between containers）；Poulton ch2（Windows worker node）

</details>
