%% trellis:begin %%
# 低延迟 Java

JVM 怎样执行和回收、怎样写出不产生垃圾的 Java，以及 Disruptor、Agrona、Aeron、Chronicle 这些让 Java 做到微秒级的工具。

## Topics
- [[domains/hft/map/java.jit|JIT、分层编译、预热与去优化]]
- [[domains/hft/map/java.gc|垃圾回收与停顿]]
- [[domains/hft/map/java.gc-choices|收集器选择：G1、ZGC、Shenandoah、Epsilon 与 Azul]]
- [[domains/hft/map/java.garbage-free|零垃圾（garbage-free）编码]]
- [[domains/hft/map/java.object-layout|对象布局与机械同理心（mechanical sympathy）]]
- [[domains/hft/map/java.off-heap|堆外内存：DirectByteBuffer、Unsafe、FFM API 与 mmap]]
- [[domains/hft/map/java.flyweight-sbe|flyweight 编解码与 SBE]]
- [[domains/hft/map/java.memory-model|Java 内存模型、volatile 与 VarHandle]]
- [[domains/hft/map/java.disruptor|LMAX Disruptor]]
- [[domains/hft/map/java.agrona-aeron|Agrona 与 Aeron]]
- [[domains/hft/map/java.chronicle|Chronicle Queue 与 Chronicle Map]]
- [[domains/hft/map/java.safepoints|safepoint 与 GC 之外的 JVM 停顿]]
- [[domains/hft/map/java.tuning|低延迟 JVM 调优]]
- [[domains/hft/map/java.modern|现代 Java 特性与低延迟]]
%% trellis:end %%

## Notes
