---
id: k8s-image-volume-beyond
node: p3.t02.hostpath-image-volume-volume-types
type: qa
step: 3
tags: [拓展]
---
## Q
**OCI 制品作 volume · 2026 实践**｜拓展 · v1.36 GA

要给推理服务的 Pod 挂几十 GB 的模型权重，又不想塞进主镜像、也不想靠 init 容器下载。2026 年标准做法是什么？

## A
| 时间 | 状态 |
|---|---|
| v1.31 | 加入 `image` volume 类型 |
| v1.33 | beta |
| v1.35 | beta，默认开启（需要兼容的 runtime，如 containerd v2.1 及以上） |
| **v1.36** | **GA**（OCI volume source，KEP-4639） |

- **做法：** 把模型或静态资源打成 OCI 制品推到 registry，Pod 的 `image` volume 直接引用；kubelet 从 registry 拉取并只读挂载，版本管理和镜像一样。
- **好处：** 数据与应用分开发版本；少一个 init 容器；复用 registry 的权限和缓存。
- **限制：** 只读；要 runtime 支持。
- **同期清理：** `gitRepo` 卷（v1.11 起弃用）在 **v1.36 被移除**，需要从 git 取内容的，改用 init 容器或 image volume。

**出处：** kubernetes.io 发布博客 v1.35（image volume beta 默认开启，需 containerd v2.1+）、v1.36（OCI volume source Stable；gitRepo 移除，KEP-5040）
