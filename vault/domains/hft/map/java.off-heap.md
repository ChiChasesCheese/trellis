%% trellis:begin %%
# 堆外内存：DirectByteBuffer、Unsafe、FFM API 与 mmap
*低延迟 Java*

把数据放在 GC 管不到的内存里：直接缓冲区、sun.misc.Unsafe、Java 22 正式发布的 Foreign Function & Memory API、内存映射文件。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.garbage-free|零垃圾（garbage-free）编码]]

**Unlocks:** [[domains/hft/map/java.flyweight-sbe|flyweight 编解码与 SBE]], [[domains/hft/map/java.agrona-aeron|Agrona 与 Aeron]], [[domains/hft/map/java.chronicle|Chronicle Queue 与 Chronicle Map]], [[domains/hft/map/java.modern|现代 Java 特性与低延迟]], [[domains/hft/map/java-at-hft.interop|Java 与 C++ 系统的协作]]

## Readings
- [[agrona|Agrona]]
- [[jep-454-ffm|JEP 454：Foreign Function & Memory API]]

## Cards (5)
1. [[hft-java-off-heap-tradeoff]]
2. [[hft-java-off-heap-four-tools]]
3. [[hft-java-off-heap-directbuf-pitfalls]]
4. [[hft-java-off-heap-ffm-arena]]
5. [[hft-java-off-heap-mmap]]
%% trellis:end %%

## Notes
