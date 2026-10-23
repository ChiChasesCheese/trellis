---
nodes: [cpp.spsc-seqlock, architecture.threading, cpp.atomics]
url: https://rigtorp.se/ringbuffer/
---
# Optimizing a ring buffer for throughput

从一个朴素 SPSC 环形队列开始，逐步用对齐和缓存下标把吞吐提高数倍。

**读的时候提取：**
- 读写下标为什么要放在不同的缓存行。
- 缓存对方下标的技巧如何减少核间通信。

%% trellis:begin %%
## Source
[Open the original ↗](https://rigtorp.se/ringbuffer/)

## Archived copy
![[rigtorp-ringbuffer-clip]]
%% trellis:end %%
