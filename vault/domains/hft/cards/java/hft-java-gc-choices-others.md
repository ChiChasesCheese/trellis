---
id: hft-java-gc-choices-others
node: java.gc-choices
type: qa
step: 4
---
## Q
Shenandoah、Epsilon 和 Azul Prime 的 C4 收集器各是什么思路？各适合什么场景？

## A
- **Shenandoah**：OpenJDK 里的并发整理收集器，和 ZGC 同类，靠屏障让搬对象与应用并发，停顿很短且基本与堆大小无关，是 ZGC 之外的另一个低停顿选择。
- **Epsilon**：只分配、不回收，堆用完进程就退出。适合短命进程、基准测试，或者能保证一个交易日内分配量不会超过堆大小的“零分配”系统。
- **Azul Prime 的 C4**（Continuously Concurrent Compacting Collector）：商业 JVM，并发整理，是最早“花钱买低停顿”的方案，现在 ZGC 把这种能力带进了免费的 OpenJDK。

共同点是都在拿吞吐、内存或成本换尾延迟。
