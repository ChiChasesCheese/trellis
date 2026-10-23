%% trellis:begin %%
# 回放与交易所模拟器
*tick-to-trade 系统架构*

用历史行情驱动同一套生产代码，交易所模拟器模拟排队与延迟；回测结果和实盘差异的来源。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.sequencer-journal|定序器、日志与确定性回放]]

## Readings
- [[fowler-event-sourcing|事件溯源（Event Sourcing）]]

## Cards (5)
1. [[hft-architecture-simulation-replay-mechanism]]
2. [[hft-architecture-simulation-queue-position]]
3. [[hft-architecture-simulation-backtest-live-gap]]
4. [[hft-architecture-simulation-same-code-vs-two-codebases]]
5. [[hft-architecture-simulation-other-uses]]
%% trellis:end %%

## Notes
