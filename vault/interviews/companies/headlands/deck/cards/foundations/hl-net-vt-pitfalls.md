---
id: hl-net-vt-pitfalls
node: foundations.networking-basics
type: qa
step: 40
---
## Q
JDK 21 虚拟线程有哪四个坑？`synchronized` 里做阻塞 `socket.read()` 会发生什么？

## A
1. **固定（pinning）**：在 `synchronized` 块里或本地方法栈上做阻塞操作，虚拟线程无法卸载，**占着载体线程不放**；载体默认只有核数个，大量固定会耗尽载体，让所有虚拟线程饥饿。解决：用 `ReentrantLock` 代替 `synchronized` 包裹阻塞调用，或避免持锁时做阻塞 I/O。
2. **ThreadLocal**：百万个虚拟线程各带 `ThreadLocal` 耗内存；`ScopedValue`（预览）是替代。
3. **不是更快，是更多**：提高的是并发度，**不降低单个请求的延迟**。
4. **调度抖动**：由 JVM 的 `ForkJoinPool` 调度，时序不确定，不适用微秒级延迟。
