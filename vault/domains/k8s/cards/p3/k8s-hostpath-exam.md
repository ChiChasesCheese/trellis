---
id: k8s-hostpath-exam
node: p3.t02.hostpath-image-volume-volume-types
type: qa
step: 2
tags: [考点]
---
## Q
**hostPath 的危险 · 考点**｜考点 · 必会

安全评审时发现某个 namespace 里有一个 Pod 配了 `hostPath: {path: /}`。这意味着什么？又有人想用 hostPath 存 MongoDB 的数据，有什么问题？

## A
| 情形 | 后果 |
|---|---|
| `hostPath: /` 挂到容器 `/host` | 容器里能读写 node 整个文件系统，等于拿到 node 上的 root 权限 |
| 挂 Docker socket（`/var/run/docker.sock`） | 容器里再用 Docker 客户端，以 root 在 node 上跑任意命令 |
| 数据库存 hostPath | Pod 重新调度到别的 node，看到的是另一个 node 的目录，**数据对不上**（原 node 上的数据还在，但这个 Pod 访问不到） |

- **所以：** hostPath 通常只留给 privileged 的系统 Pod，用准入策略限制（第 6 部分），普通用户不能使用。
- **要 node 本地存储：** 用 **local PersistentVolume**，带 node affinity，scheduler 会保证 Pod 一直调度到有这块盘的 node；而且 PV 由管理员创建，普通用户没法借它访问任意路径。
- **查一下：** `kubectl get pods -A -o json` 里搜 `hostPath`，把所有用的 Pod 过一遍。

**出处：** KIA2 §9.4.1–9.4.2（hostPath 危险性）、§10.3.1（local PV 优于 hostPath）
