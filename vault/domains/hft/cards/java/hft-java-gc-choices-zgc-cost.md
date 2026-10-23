---
id: hft-java-gc-choices-zgc-cost
node: java.gc-choices
type: qa
step: 3
---
## Q
相比 G1，ZGC 为换取亚毫秒停顿付出了哪些代价？

## A
低停顿不是白送的，主要有四项代价：
- **吞吐略低**：每次读引用都多一段加载屏障；
- **需要额外堆空间**（headroom）：并发回收期间应用还在分配，如果新分配快过回收，就发生 allocation stall，分配线程被迫等待，成了新的延迟来源；
- **占 CPU**：并发的 GC 线程要和应用线程抢核；
- **不使用压缩指针**（compressed oops），同样的对象图占用更多内存。

所以堆设得太紧、分配又太快的负载，ZGC 反而可能不如 G1。要在自己的负载上用 GC 日志和 JFR 实测，而不是照搬别人的结论。
