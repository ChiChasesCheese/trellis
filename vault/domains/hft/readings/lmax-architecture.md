---
nodes: [architecture.event-loop, architecture.sequencer-journal, architecture.threading, java-at-hft.how-fast, reliability.failover]
url: https://martinfowler.com/articles/lmax.html
---
# The LMAX Architecture

一家用 Java 写的零售外汇交易所如何在单线程业务逻辑上每秒处理约 600 万订单：输入定序、事件溯源、内存状态与回放。

**读的时候提取：**
- 业务逻辑处理器为什么是单线程、全内存。
- 输入日志 + 快照如何恢复状态。
- Disruptor 在输入和输出两端的作用。

%% trellis:begin %%
## Source
[Open the original ↗](https://martinfowler.com/articles/lmax.html)

## Archived copy
![[lmax-architecture-clip]]
%% trellis:end %%
