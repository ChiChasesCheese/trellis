---
id: k8s-namespaces-cgroups-beyond
node: p1.t02.namespaces-cgroups
type: qa
step: 3
tags: [拓展]
---
## Q
**Namespaces 与 cgroups · 2026 实践**｜拓展 · v1.35 / v1.36

升级到 v1.35 以后，一台还在用 cgroup v1 的老节点上，kubelet 会怎样？v1.36 的 user namespaces 又改善了什么？

## A
**cgroup v1：** v1.35 起 Kubernetes 不再支持 cgroup v1，在这样的节点上 **kubelet 起不来**。节点需要用 cgroup v2（较新的 Linux 发行版默认是 v2）。

**user namespaces：** v1.36 GA。上一张表里的 `user` namespace 让容器里的 root（用户 ID 0）映射成宿主机上一个没有特权的用户。

| | 没有 user namespace | 有 user namespace |
|---|---|---|
| 容器里的 root | 就是宿主机的 root（ID 0） | 在宿主机上只是普通用户 |
| 容器被攻破后逃逸 | 拿到 root 权限 | 权限小很多 |

- **升级前要做：** 先确认节点用的是 cgroup v2，再升到 v1.35 以上。
- **版本：** cgroup v1 移除 v1.35；user namespaces beta v1.33 → GA v1.36。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.35、v1.36（cgroup v1 removal；user namespaces，KEP-127）；KIA2 §2.3.1 说明 user namespace

</details>
