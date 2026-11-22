---
id: k8s-namespaces-cgroups-exam
node: p1.t02.namespaces-cgroups
type: qa
step: 2
tags: [考点]
---
## Q
**Namespaces 与 cgroups**｜考点 · 必会

下面三个现象，分别是 namespace 还是 cgroup 在起作用？
1. 容器里 `ps aux` 只列出几个进程，主进程的 PID 是 1
2. 给容器设了 `--memory=100m`，进程想用 150MB 内存
3. 两个容器都监听 80 端口，互不冲突

## A
| 现象 | 机制 | 解释 |
|---|---|---|
| 1 | **pid namespace** | 每个 namespace 里的进程号从 1 重新编，只看得到本 namespace 的进程 |
| 2 | **cgroup** | 内核强制执行内存上限，进程超出后会被杀掉（OOM kill） |
| 3 | **net namespace**（每个容器一套） | 端口属于各自 namespace 里的网卡，互不冲突 |

- **一个对比：** CPU 超额不会杀进程，只会被限速（throttle）；内存超额才会被杀。第 2 部分的 limits 一卡会细讲。
- **反例：** 用 `--net=host`，容器就不再有自己的 net namespace，用的是宿主机的网络，两个容器监听同一端口就会冲突。

<details class="pt" markdown="1"><summary>出处</summary>

KIA2 §2.3.1–2.3.2（含 `--net=host` 的例子）

</details>
