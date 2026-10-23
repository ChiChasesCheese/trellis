%% trellis:begin %%
# Java 内存模型、volatile 与 VarHandle
*低延迟 Java*

happens-before、volatile 的可见性与顺序保证、VarHandle 的 plain / opaque / acquire-release / volatile 四种访问模式，以及 lazySet（setRelease）为什么便宜。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/machine.memory-ordering|内存序、x86 TSO 与原子操作的成本]]

**Unlocks:** [[domains/hft/map/java.disruptor|LMAX Disruptor]]

## Readings
- [[jls-memory-model|Java 语言规范第 17 章：线程与锁]]
- [[lea-jdk9-memory-modes|Using JDK 9 Memory Order Modes]]
- [[mechanical-sympathy-barriers|Memory Barriers/Fences]]
- [[preshing-acquire-release|Acquire and Release Semantics]]

## Cards (5)
1. [[hft-java-memory-model-happens-before]]
2. [[hft-java-memory-model-volatile]]
3. [[hft-java-memory-model-varhandle-modes]]
4. [[hft-java-memory-model-lazyset]]
5. [[hft-java-memory-model-publish-bug]]
%% trellis:end %%

## Notes
