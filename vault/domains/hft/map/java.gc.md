%% trellis:begin %%
# 垃圾回收与停顿
*低延迟 Java*

分代假设、年轻代回收、stop-the-world 停顿、分配速率（allocation rate）决定回收频率；为什么低延迟系统最怕 GC。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/hft/map/java.gc-choices|收集器选择：G1、ZGC、Shenandoah、Epsilon 与 Azul]], [[domains/hft/map/java.garbage-free|零垃圾（garbage-free）编码]], [[domains/hft/map/java.safepoints|safepoint 与 GC 之外的 JVM 停顿]], [[domains/hft/map/java-at-hft.where-java|Java 在交易公司里用在哪里]], [[domains/hft/map/java-at-hft.why-java|为什么选 Java：生产力、安全与生态]]

## Readings
- [[oracle-gc-tuning|Java 21 垃圾回收调优指南]]
- [[shipilev-jvm-anatomy|JVM Anatomy Quarks]]

## Drills
- [[java-gc-tail-spikes|练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰]]

## Cards (5)
1. [[hft-java-gc-generational]]
2. [[hft-java-gc-stw]]
3. [[hft-java-gc-alloc-rate]]
4. [[hft-java-gc-young-vs-full]]
5. [[hft-java-gc-fear-gc]]
%% trellis:end %%

## Notes
