---
id: hft-measurement-profiling-pmu-ipc
node: measurement.profiling
type: qa
step: 2
---
## Q
CPU 的硬件性能计数器（PMU）能告诉我们什么？怎么用 IPC（每周期指令数）判断一段代码是“算得慢”还是“等内存”？

## A
**PMU**（performance monitoring unit，性能监控单元）是 CPU 内部的一组计数器，可以数出**硬件事件**：执行了多少条指令、花了多少个周期、缓存未命中多少次、分支预测失败多少次等。用 `perf stat -e instructions,cycles,cache-misses,branch-misses ./prog` 就能读到，几乎不增加开销。

**IPC** = instructions ÷ cycles，即平均每个周期完成几条指令。
- 现代 x86 核心每周期最多能完成 4 条以上，计算密集且数据都在缓存里的代码，IPC 可以到 2–4；
- 如果 IPC **远低于 1**，说明 CPU 大部分周期都在**空等**，通常是在等内存（缓存未命中）或在分支预测失败后重新取指。

例：某段订单簿代码 IPC 只有 0.4，缓存未命中率很高，说明瓶颈是数据布局，应该去改内存访问方式，而不是优化算术。反过来，IPC 3 但仍然慢，说明指令本身太多，要减少工作量。

火焰图告诉你**哪里**花时间，PMU 计数器告诉你**为什么**。
