---
nodes: [machine.memory-hierarchy, machine.cache-lines, machine.numa, machine.tlb-hugepages]
url: https://people.freebsd.org/~lstewart/articles/cpumemory.pdf
---
# What Every Programmer Should Know About Memory

从 DRAM 物理原理到 CPU 缓存、NUMA、虚拟内存，再到程序员能做什么的长篇经典。

**读的时候提取：**
- 各级缓存的访问延迟与顺序 / 随机访问的差距。
- 预取、缓存行、TLB 对程序布局的要求。

%% trellis:begin %%
## Source
[Open the original ↗](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)

## Archived copy
![[drepper-memory-clip]]
%% trellis:end %%
