---
id: hl-os-scheduling-concepts
node: foundations.os-processes-threads-ipc
type: qa
step: 8
---
## Q
时间片、抢占、自愿 / 非自愿切换、Linux 调度器（CFS、EEVDF）是什么？

## A
- **时间片**（quantum）：线程连续运行的最长时间，毫秒量级；
- **抢占**（preemption）：时钟中断到来时内核把正在跑的线程踢下去换别人，是**非自愿切换**；线程自己阻塞（等 I/O、锁、`park`）是**自愿切换**；
- **CFS**（Completely Fair Scheduler）：Linux 2.6.23 起的主流调度器，用红黑树按「已用 CPU 时间」排队；6.6 版内核起换成 **EEVDF**；
- 实时任务有 `SCHED_FIFO` / `SCHED_RR`。
