---
nodes: [machine.memory-ordering, java.memory-model]
url: https://mechanical-sympathy.blogspot.com/2011/07/memory-barriersfences.html
---
# Memory Barriers/Fences

CPU 为什么重排内存操作、各类屏障做什么、Java 的 volatile 在 x86 上对应什么。

**读的时候提取：**
- store buffer 与 load/store 屏障。
- lazySet 为什么比 volatile 写便宜。

%% trellis:begin %%
## Source
[Open the original ↗](https://mechanical-sympathy.blogspot.com/2011/07/memory-barriersfences.html)

## Archived copy
![[mechanical-sympathy-barriers-clip]]
%% trellis:end %%
