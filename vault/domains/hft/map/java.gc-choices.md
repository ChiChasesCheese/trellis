%% trellis:begin %%
# 收集器选择：G1、ZGC、Shenandoah、Epsilon 与 Azul
*低延迟 Java*

G1 的可预测停顿目标、ZGC 与 Shenandoah 的并发回收（停顿亚毫秒）、Epsilon 不回收、Azul Prime 的 C4；吞吐与延迟的取舍。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.gc|垃圾回收与停顿]]

**Unlocks:** [[domains/hft/map/java.tuning|低延迟 JVM 调优]]

## Readings
- [[jep-318-epsilon|JEP 318：Epsilon 无操作收集器]]
- [[oracle-gc-tuning|Java 21 垃圾回收调优指南]]

## Drills
- [[java-gc-tail-spikes|练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰]]

## Cards (5)
1. [[hft-java-gc-choices-g1]]
2. [[hft-java-gc-choices-zgc]]
3. [[hft-java-gc-choices-zgc-cost]]
4. [[hft-java-gc-choices-others]]
5. [[hft-java-gc-choices-gen-zgc]]
%% trellis:end %%

## Notes
