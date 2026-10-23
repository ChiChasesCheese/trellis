%% trellis:begin %%
# 定序器、日志与确定性回放
*tick-to-trade 系统架构*

所有输入先经过定序器（sequencer）编号并写入日志（journal），业务逻辑是纯函数式的状态机，因此可以确定性回放（deterministic replay）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.event-loop|单线程事件循环与忙轮询（busy-spin）]]

**Unlocks:** [[domains/hft/map/architecture.simulation|回放与交易所模拟器]], [[domains/hft/map/java.disruptor|LMAX Disruptor]], [[domains/hft/map/reliability.failover|主备切换与状态恢复]]

## Readings
- [[fowler-event-sourcing|事件溯源（Event Sourcing）]]
- [[lmax-architecture|The LMAX Architecture]]

## Cards (5)
1. [[hft-architecture-sequencer-journal-how-they-fit]]
2. [[hft-architecture-sequencer-journal-why-replay-works]]
3. [[hft-architecture-sequencer-journal-determinism-killers]]
4. [[hft-architecture-sequencer-journal-exchange-vs-client-journal]]
5. [[hft-architecture-sequencer-journal-journal-volume]]
%% trellis:end %%

## Notes
