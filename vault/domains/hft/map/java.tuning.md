%% trellis:begin %%
# 低延迟 JVM 调优
*低延迟 Java*

固定堆大小、-XX:+AlwaysPreTouch、大页、线程绑核（Java Thread Affinity 库）、关闭偏向锁等历史选项、用 JFR 观察。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.gc-choices|收集器选择：G1、ZGC、Shenandoah、Epsilon 与 Azul]], [[domains/hft/map/os-network.cpu-isolation|绑核与 CPU 隔离]], [[domains/hft/map/machine.tlb-hugepages|虚拟内存、TLB 与大页（huge pages）]]

## Readings
- [[java-thread-affinity|Java Thread Affinity]]
- [[kernel-hugetlbpage|Linux HugeTLB Pages]]
- [[oracle-gc-tuning|Java 21 垃圾回收调优指南]]

## Drills
- [[java-gc-tail-spikes|练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰]]

## Cards (5)
1. [[hft-java-tuning-heap-pretouch]]
2. [[hft-java-tuning-hugepages]]
3. [[hft-java-tuning-affinity]]
4. [[hft-java-tuning-legacy-flags]]
5. [[hft-java-tuning-checklist]]
%% trellis:end %%

## Notes
