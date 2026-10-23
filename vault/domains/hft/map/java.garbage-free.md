%% trellis:begin %%
# 零垃圾（garbage-free）编码
*低延迟 Java*

稳态下不分配：对象复用与池化、primitive 代替包装类、避免自动装箱 / 迭代器 / lambda 捕获 / 字符串拼接，以及如何验证分配为零。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.gc|垃圾回收与停顿]]

**Unlocks:** [[domains/hft/map/java.off-heap|堆外内存：DirectByteBuffer、Unsafe、FFM API 与 mmap]], [[domains/hft/map/java-at-hft.how-fast|Java 能做到多快：真实案例]]

## Readings
- [[agrona|Agrona]]
- [[jep-318-epsilon|JEP 318：Epsilon 无操作收集器]]

## Drills
- [[java-gc-tail-spikes|练习：Java 订单簿的 p99.9 每隔几秒冒一簇尖峰]]

## Cards (5)
1. [[hft-java-garbage-free-goal]]
2. [[hft-java-garbage-free-pooling]]
3. [[hft-java-garbage-free-hidden-alloc]]
4. [[hft-java-garbage-free-verify]]
5. [[hft-java-garbage-free-cost]]
%% trellis:end %%

## Notes
