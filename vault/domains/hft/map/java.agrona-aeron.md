%% trellis:begin %%
# Agrona 与 Aeron
*低延迟 Java*

Agrona 提供无垃圾集合、堆外缓冲区和环形缓冲区；Aeron 是基于 UDP / IPC 的低延迟消息传输，带 Archive（录制回放）和 Cluster（Raft 复制状态机）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.off-heap|堆外内存：DirectByteBuffer、Unsafe、FFM API 与 mmap]], [[domains/hft/map/java.disruptor|LMAX Disruptor]]

## Readings
- [[aeron-docs|Aeron 文档]]
- [[agrona|Agrona]]

## Cards (5)
1. [[hft-java-agrona-aeron-agrona]]
2. [[hft-java-agrona-aeron-aeron]]
3. [[hft-java-agrona-aeron-archive]]
4. [[hft-java-agrona-aeron-cluster]]
5. [[hft-java-agrona-aeron-backpressure]]
%% trellis:end %%

## Notes
