---
id: hft-java-tuning-legacy-flags
node: java.tuning
type: qa
step: 4
---
## Q
老文章建议的“关闭偏向锁”今天还需要吗？为什么要警惕抄来的一串 `-XX` 参数？

## A
偏向锁（biased locking）是早期 JVM 对无竞争锁的优化，但撤销偏向需要 safepoint 停顿，对低延迟有害，所以老文章建议加 `-XX:-UseBiasedLocking`。JDK 15 起偏向锁默认关闭，JDK 18 起已被移除，这个参数在新版本里已经没有意义。

这说明 JVM 参数有强烈的版本依赖：不同版本默认值和行为变化很大，从网上抄来的参数清单常常过时、无效，甚至互相冲突。正确的做法是：先建基线，用 `-Xlog:gc`、JFR 观察，每次只改一个变量并对比分布。

JFR（Java Flight Recorder）是 JVM 内置的事件记录器，开销约 1%，可以在生产常开，用来记录 GC 暂停、分配、锁竞争、编译和 safepoint 事件。
