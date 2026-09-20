---
nodes: [problems.commerce.stock-exchange]
url: https://lmax-exchange.github.io/disruptor/disruptor.html
---
# LMAX Disruptor: High Performance Alternative to Bounded Queues

值得读：Disruptor 官方技术文档，披露了环形缓冲区（ring buffer）+ 单写者原则如何消除锁
竞争，以及相对传统阻塞队列的实测对比——三阶段流水线下平均延迟 52 纳秒对比阻塞队列的
32,757 纳秒，现代硬件上吞吐可达每秒过亿次操作。本题「瓶颈、故障与演进」的 10 倍演进部分
用这组数字说明序列化层本身的吞吐远非瓶颈；需要注意这组基准是通用无锁队列场景的测量，不是
专门针对股票交易系统的实测，本文引用时保留了这个限定。

%% trellis:begin %%
## Source
[Open the original ↗](https://lmax-exchange.github.io/disruptor/disruptor.html)

## Archived copy
![[src-lmax-disruptor-stock-exchange-clip]]
%% trellis:end %%
