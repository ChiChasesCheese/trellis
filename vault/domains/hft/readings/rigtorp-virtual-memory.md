---
nodes: [machine.tlb-hugepages, os-network.page-faults]
url: https://rigtorp.se/virtual-memory/
---
# Virtual memory for low latency applications

虚拟内存在低延迟应用里的坑：缺页、TLB miss、透明大页、mlock 与预触。

**读的时候提取：**
- 如何让进程启动后不再缺页。
- 大页减少 TLB miss 的原理。

%% trellis:begin %%
## Source
[Open the original ↗](https://rigtorp.se/virtual-memory/)

## Archived copy
![[rigtorp-virtual-memory-clip]]
%% trellis:end %%
