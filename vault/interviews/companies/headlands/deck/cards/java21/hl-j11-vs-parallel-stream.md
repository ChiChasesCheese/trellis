---
id: hl-j11-vs-parallel-stream
node: java21.j11-structured-concurrency
type: qa
step: 21
---
## Q
结构化并发与并行流（parallel stream）有什么区别？为什么说它要和虚拟线程配套理解？

## A
- **并行流**：**数据并行**，集合分块计算，CPU 密集，用公共 `ForkJoinPool`。
- **结构化并发**：**任务并行**，几个不同的、通常阻塞的调用（行情、风控、参考数据），一般搭虚拟线程。它不是并行流的替代品。

配套：`fork` 默认就是虚拟线程，「每个子任务一个线程」不贵；换成平台线程工厂就回到 J10 的线程成本问题。
