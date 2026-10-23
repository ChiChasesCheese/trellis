---
id: hl-hc02-followup-slow-source
node: problems.hc02-merge-k-streams
type: qa
step: 19
---
## Q
追问：合并流里某个 source 很慢或卡死了怎么办？失败的流怎么处理？为什么选虚拟线程加 `StructuredTaskScope` 而不是线程池？

## A
**慢 / 卡死的 source**：先说清语义——有序合并**必须**等每个活着的流的队首，否则可能输出错误顺序。所以：
(a) `tryNext()` 返回 `Pending`，让调用方决定去做别的；
(b) 给 `next` 加超时；
(c) 可接受乱序的场景改成「尽力有序」的窗口合并（水位线 watermark）。
一个 source 永远不给数据，`Pending` 就永不变成 `Ready`，这是确定结果。真实系统可在 source 外套一层超时，超时算作 `Failed`。

**失败的流**：fail-fast（抛 `MergeException(流编号, cause)` 并取消其他）或 skip-and-continue（视为结束并记录错误）。这是产品决策，要问清楚。

**为什么不用线程池**：线程池 + `Future` 不自动取消兄弟，离开作用域线程可能仍在跑；虚拟线程 + 结构化并发代码是直线的，保证离开 `try` 块时所有子任务已结束，`ShutdownOnFailure` 自动取消兄弟。

**还有一个等价问题**：给一个会阻塞的 unsafe client，要求「同时最多读 m 个」的有界并发；这里的 `capacity` 是每流预读深度，作用相近。

**测等待事件**：不要用 `Thread.sleep` 判断「现在应该是 Pending」，睡多久都不保证生产者已跑过；用 `CountDownLatch`，或让慢 source 由测试控制放行。
