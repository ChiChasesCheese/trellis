---
id: hl-j19-real-other
node: java21.j19-runtime-zgc-jit
type: qa
step: 33
---
## Q
`LongTickerMap`、`OffHeapTickerMap`、`RecursiveSum.measureDepth` 各体现了哪条运行时考量？

## A
- `LongTickerMap`：「没有 `Long` 装箱，`add()` 在稳态下一个字节都不分配」，与基于 `HashMap<String, Long>` 的朴素 `TickerMap` 对照；
- `OffHeapTickerMap`：类注释「GC 完全看不见它：不管表有多大，GC 扫描/整理的工作量都不变」，低延迟系统避免 GC 抖动的常见手段；
- `RecursiveSum.measureDepth`：新线程里递归到 `StackOverflowError`，演示线程栈大小（`Thread` 构造器第四个参数），是 JVM 运行时的另一个可调维度（`-Xss`）。

测试命令统一 `java --enable-preview -XX:+UseZGC -XX:+ZGenerational ...`，所以参考解都跑在分代 ZGC 上。
