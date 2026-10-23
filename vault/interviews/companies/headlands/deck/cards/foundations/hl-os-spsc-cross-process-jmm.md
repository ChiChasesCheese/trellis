---
id: hl-os-spsc-cross-process-jmm
node: foundations.os-processes-threads-ipc
type: qa
step: 27
---
## Q
两个 JVM 进程通过共享内存用 `VarHandle` release / acquire 通信，Java 内存模型（JMM）保证它正确吗？为什么实践上可行？

## A
JMM 形式上只定义**同一 JVM 里线程间**的 happens-before，两个 JVM 进程通过共享内存通信**不在 JMM 覆盖范围**。

实践可行：`VarHandle` 的 release / acquire 会编译成真正的 CPU 屏障指令，缓存一致性硬件对不同进程的核一视同仁（Aeron、Chronicle Queue 都这样做）。但它依赖的是**硬件内存模型加 JIT 实现**，不是 JMM 的形式保证。
