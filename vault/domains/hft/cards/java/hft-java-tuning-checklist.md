---
id: hft-java-tuning-checklist
node: java.tuning
type: qa
step: 5
---
## Q
给一台要跑低延迟 Java 交易进程的 Linux 机器，一份典型的 JVM 调优起点是什么？每一项解决什么问题？

## A
一份起点清单（JDK 21，数值仅为示例）：
- `-Xms16g -Xmx16g`：固定堆，避免运行中扩缩；
- `-XX:+AlwaysPreTouch`：启动时分配好物理页，避免运行中缺页；
- `-XX:+UseZGC -XX:+ZGenerational`：分代 ZGC，亚毫秒停顿；
- `-XX:+UseLargePages`（或评估透明大页）：减少 TLB 未命中；
- `-Xlog:gc*,safepoint:file=gc.log`：记录 GC 与 safepoint，事后才能解释尖刺；
- 操作系统一侧：核隔离、线程绑核、预热。

注意：这只是起点，不是答案。每一项都要在自己的负载上测量，并用 p99、p99.9 对比，一次改一处。
