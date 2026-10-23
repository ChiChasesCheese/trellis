%% trellis:begin %%
# 单线程事件循环与忙轮询（busy-spin）
*tick-to-trade 系统架构*

一个线程在一个独占核上死循环轮询网卡和队列，不睡眠、不加锁；为什么这比多线程 + 锁更快更稳定。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.pipeline|交易系统的组件流水线]]

**Unlocks:** [[domains/hft/map/architecture.hot-cold-path|快路径与慢路径分离]], [[domains/hft/map/architecture.threading|线程模型：一核一线程与 SPSC 队列]], [[domains/hft/map/architecture.sequencer-journal|定序器、日志与确定性回放]]

## Readings
- [[lmax-architecture|The LMAX Architecture]]

## Cards (5)
1. [[hft-architecture-event-loop-how-it-works]]
2. [[hft-architecture-event-loop-why-not-sleep]]
3. [[hft-architecture-event-loop-single-thread-vs-locks]]
4. [[hft-architecture-event-loop-busy-spin-cost]]
5. [[hft-architecture-event-loop-blocking-call-freezes-loop]]
%% trellis:end %%

## Notes
