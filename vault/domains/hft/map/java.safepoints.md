%% trellis:begin %%
# safepoint 与 GC 之外的 JVM 停顿
*低延迟 Java*

JVM 需要所有线程停在安全点（safepoint）才能做某些操作；到达安全点的时间（time to safepoint）、去优化、类加载等隐藏停顿。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.gc|垃圾回收与停顿]], [[domains/hft/map/java.jit|JIT、分层编译、预热与去优化]]

## Readings
- [[psy-lob-saw-safepoints|Safepoints: Meaning, Side Effects and Overheads]]
- [[shipilev-jvm-anatomy|JVM Anatomy Quarks]]

## Drills
- [[java-gc-tail-spikes|练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰]]

## Cards (5)
1. [[hft-java-safepoints-what]]
2. [[hft-java-safepoints-ttsp]]
3. [[hft-java-safepoints-hidden-pauses]]
4. [[hft-java-safepoints-observe]]
5. [[hft-java-safepoints-diagnose]]
%% trellis:end %%

## Notes
