%% trellis:begin %%
# 线程模型：一核一线程与 SPSC 队列
*tick-to-trade 系统架构*

每个线程绑一个核、线程之间只用单生产者单消费者（SPSC）队列传消息、不共享可写状态。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.event-loop|单线程事件循环与忙轮询（busy-spin）]]

**Unlocks:** [[domains/hft/map/os-network.cpu-isolation|绑核与 CPU 隔离]]

## Readings
- [[lmax-architecture|The LMAX Architecture]]
- [[rigtorp-ringbuffer|Optimizing a ring buffer for throughput]]

## Cards (5)
1. [[hft-architecture-threading-model]]
2. [[hft-architecture-threading-spsc-lock-free]]
3. [[hft-architecture-threading-handoff-cost]]
4. [[hft-architecture-threading-spsc-vs-mpsc]]
5. [[hft-architecture-threading-queue-sizing-and-full]]
%% trellis:end %%

## Notes
