---
nodes: [java.disruptor, machine.false-sharing, cpp.spsc-seqlock]
url: https://lmax-exchange.github.io/disruptor/disruptor.html
---
# LMAX Disruptor 技术论文

为什么队列是并发系统的瓶颈，以及环形缓冲区 + 序列号的设计如何消除锁、伪共享和垃圾。

**读的时候提取：**
- 锁和 CAS 的实测成本对比。
- 缓存行填充为什么必要。
- 批处理效应如何在负载高时降低延迟。

%% trellis:begin %%
## Source
[Open the original ↗](https://lmax-exchange.github.io/disruptor/disruptor.html)

## Archived copy
![[lmax-disruptor-paper-clip]]
%% trellis:end %%
