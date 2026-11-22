---
id: k8s-cpu-memory-beyond
node: p2.t04.cpu-throttling-oom-kill
type: qa
step: 3
tags: [拓展]
---
## Q
**PSI 与 Memory QoS · 2026 实践**｜拓展 · v1.36 / v1.37

只看「CPU 用了多少」和「内存有没有超 limit」，看不出 node 上的资源是否已经让容器等待。2026 年有什么更直接的信号和更温和的内存保护？

## A
| 特性 | 状态 | 作用 |
|---|---|---|
| **PSI**（Pressure Stall Information，内核报告「任务因为缺资源而被卡住的时间占比」） | **v1.36 GA**（KEP-4205，基于 cgroup v2） | 直接看到 CPU、内存、IO 的压力，比利用率更能反映「是否在等」 |
| **Memory QoS**（cgroup v2 的 `memory.high`、`memory.min`） | v1.36 beta → **v1.37 默认开启**（feature gate `MemoryQoS`，KEP-2570） | 按 Pod 的 request 和 limit 分层保护内存，减少同机负载互相挤占和抖动 |

- **用法：** 先用 PSI 判断是否真的受压，再决定是加 request、调 limit，还是搬 node。
- **v1.37 的默认值：** gate 虽然默认开，但 `memoryThrottlingFactor` 默认改成 null、`memoryReservationPolicy` 默认 `None`，所以升级后不会自动写 `memory.high`、`memory.min`、`memory.low`；要用就在 kubelet 配置里显式设（`TieredReservation` 开分层保护）。
- **前提：** 这两项都依赖 **cgroup v2**；v1.35 起 kubelet 不再支持 cgroup v1。
- **节点驱逐：** PSI 也可用来参与 node 压力判断，具体见 kubelet 文档（本卡不展开）。

<details class="pt" markdown="1"><summary>出处</summary>

kubernetes.io 发布博客 v1.36（Support PSI based on cgroupv2 GA，KEP-4205；Memory QoS with cgroups v2，KEP-2570，列在 Beta 一节）；v1.37 博客 2026-09-14「Memory QoS Graduates to Beta」（默认开启，memoryThrottlingFactor 默认改为 null）

</details>
