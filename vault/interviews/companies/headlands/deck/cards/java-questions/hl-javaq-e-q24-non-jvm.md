---
id: hl-javaq-e-q24-non-jvm
node: java-questions.e-jit-gc
type: qa
step: 26
---
## Q
不产生垃圾的负载也会看到毫秒级的间隔，怎么解释？生产里怎么压住这类抖动？怎么区分 GC 停顿和 OS 调度延迟？
How would you tell a GC pause from an OS scheduling delay?

## A
- 数据：完全不产生垃圾的负载，两次独立运行的最大间隔分别是 0.02 ms 和 2.26 ms，另一次带 `-Xlog:safepoint` 的跑出过 12 ms。
- **结论**：在没有 CPU 隔离的笔记本上分不清是 JVM 还是 OS 的抖动；生产用**独占核**（隔离核 + 绑核）才能压住 OS 抖动。
- 其他成因：新堆页首次触碰要内核清零（`AlwaysPreTouch`）；透明大页（THP）压缩可能引起停顿；交换（swap）是灾难。
- **区分**：GC 在日志 / JFR 里有记录；OS 调度延迟看 `perf sched`、`runqlat`、`vmstat` 的 `r` 和 `cs` 列。
