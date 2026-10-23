---
id: hft-java-safepoints-observe
node: java.safepoints
type: qa
step: 4
---
## Q
怎样观察并缓解 safepoint 造成的延迟？

## A
**观察**：
- 打开 `-Xlog:safepoint`（统一日志），每次 safepoint 会记录原因、到达时间（Reaching safepoint）和停顿时间（At safepoint）；
- JFR 中也有 safepoint 相关事件，可以和 GC 日志、应用的延迟尖刺对齐时间戳。

**缓解**：
- 热路径预热后不再出现去优化，避免线上执行 `jstack`、`jmap` 这类需要 safepoint 的命令；
- 避免长时间不含轮询点的大循环，必要时把大循环拆成小块；
- 少用耗时很长的本地调用；
- 使用 ZGC 这类并发收集器，让 GC 自己的停顿缩到极短；
- 把 JIT 编译线程、GC 线程与热线程放在不同的核上。

要先测量再动手，一次只改一处。
