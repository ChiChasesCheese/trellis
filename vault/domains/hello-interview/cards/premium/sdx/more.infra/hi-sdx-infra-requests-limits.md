---
id: hi-sdx-infra-requests-limits
node: more.infra
type: qa
step: 6
---
## Q
**Kubernetes 的 requests 和 limits**｜补充 · 平台基础设施：容器、服务网格、发布 · 追问

面试官：「共享的 Kubernetes 节点上，requests 和 limits 分别起什么作用？为什么 CPU 超了和内存超了，后果不一样？」

## A
**结论。** requests 是调度器装箱时为 Pod 预留的量，也是资源紧张时保证拿到的份额；limits 是运行时的硬上限。CPU 可压缩，超限只会被限流，不崩溃，表现为说不清的 p99 延迟尖刺；内存不可压缩，超限就被 OOM 杀掉。

**要点。**
- **requests 低于真实用量：** 调度器会把节点超卖，邻居抢 CPU，或者触发驱逐，这就是吵闹的邻居。
- **CPU 限流：** 达到 limit 后进程被暂停到下一个调度周期，不报错，只表现为延迟变高。
- **QoS 等级：** 每个容器的 CPU 和内存都设成 requests 等于 limits，Pod 才是 Guaranteed；节点压力下 BestEffort 最先被驱逐，Burstable 其次，Guaranteed 最后。
- **延迟敏感的服务：** 让 requests 等于 limits，不参与抢占；也有团队只设 CPU requests 而不设 CPU limit，避免被限流。
- **2026 亮点：** requests/limits 现在可以原地调整（K8s 1.35 GA）：通过 resize 子资源改运行中 Pod 的 CPU 和内存，不用重建 Pod；resizePolicy 默认 NotRequired，内存可配成 RestartContainer，适合启动慢、预热重的服务。限制是 QoS 类不能变，缩小内存 limit 只是尽力而为、仍可能 OOM，所以突发流量仍靠 HPA 加副本。

**面试里这样说。** 「内存我设 limit 并盯 OOM，CPU 的 requests 按真实用量设；延迟敏感的服务用 Guaranteed，避免被邻居抢占，也避免 CPU 限流造成的 p99 抖动。」

**易错。**
- **requests 随便填很小：** 调度器以为节点很空，塞满之后全体变慢。
- **把 CPU 限流当成性能问题去调代码：** 其实是 limit 太低，看限流指标才能发现。
