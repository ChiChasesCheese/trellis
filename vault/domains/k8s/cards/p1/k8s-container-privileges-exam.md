---
id: k8s-container-privileges-exam
node: p1.t02.oci-container-runtime-seccomp-capabilities
type: qa
step: 2
tags: [考点]
---
## Q
**Capabilities 与 seccomp**｜考点 · 必会

一个非 root 运行的 Web 应用要监听 80 端口，启动失败（没有权限）。图省事把容器改成 privileged 能解决，为什么不该这么做？该怎么办？

## A
| 手段 | 做什么 | 这里怎么用 |
|---|---|---|
| **privileged** | 容器里的进程不受限，可以执行任何 system call | 能跑起来，但被攻破就等于拿到宿主机，不要用 |
| **capabilities** | 内核把 root 权限拆成很多单项，可以单独加或去掉 | 只加 `CAP_NET_BIND_SERVICE`（绑定小于 1024 的端口） |
| **seccomp** | 用 JSON 档案列出容器**允许调用**的 system call，其余拒绝 | 进一步收紧 |
| **AppArmor / SELinux** | 强制访问控制，限制进程能碰哪些文件和资源 | 额外一层 |

- **默认值：** Docker 和 Kubernetes 默认去掉大部分 capabilities，只保留典型应用需要的。
- **最小权限：** 只加需要的那一项；更常见的做法是干脆让应用监听 8080，再用 Service 映射到 80，什么特权都不用加。
- **优先级：** 能不用就不用 privileged。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §2.3.4「Using capabilities…」「Using seccomp profiles…」「AppArmor and SELinux」

</details>
