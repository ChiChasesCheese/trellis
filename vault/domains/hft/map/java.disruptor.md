%% trellis:begin %%
# LMAX Disruptor
*低延迟 Java*

预分配的环形缓冲区 + 序列号（sequence）+ 等待策略（wait strategy），无锁、无垃圾、批处理；LMAX 交易所用它在单线程上处理每秒数百万事件。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/java.memory-model|Java 内存模型、volatile 与 VarHandle]], [[domains/hft/map/machine.false-sharing|伪共享（false sharing）]], [[domains/hft/map/architecture.sequencer-journal|定序器、日志与确定性回放]]

**Unlocks:** [[domains/hft/map/java.agrona-aeron|Agrona 与 Aeron]], [[domains/hft/map/java-at-hft.how-fast|Java 能做到多快：真实案例]]

## Readings
- [[lmax-disruptor-paper|LMAX Disruptor 技术论文]]

## Cards (5)
1. [[hft-java-disruptor-what]]
2. [[hft-java-disruptor-wait-strategy]]
3. [[hft-java-disruptor-padding]]
4. [[hft-java-disruptor-batching]]
5. [[hft-java-disruptor-vs-abq]]
%% trellis:end %%

## Notes
