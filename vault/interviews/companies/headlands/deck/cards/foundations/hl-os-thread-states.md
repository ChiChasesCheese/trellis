---
id: hl-os-thread-states
node: foundations.os-processes-threads-ipc
type: qa
step: 7
---
## Q
调度器（scheduler）管理的线程有哪几种状态，状态之间怎么转换？和 Java 的 `Thread.State` 怎么对应？

## A
- 就绪 → 运行中：被调度器选中；
- 运行中 → 就绪：时间片用完，或被更高优先级抢占；
- 运行中 → 阻塞：等待 I/O、等锁、`park`、`sleep`；
- 阻塞 → 就绪：I/O 完成、锁被释放、被 `unpark`、`sleep` 到期。

Java 的 `Thread.State`（`RUNNABLE`、`BLOCKED`、`WAITING`、`TIMED_WAITING`）大致对应：`RUNNABLE` 包括「运行中」和「就绪」，以及在内核里阻塞读 socket 的线程。
