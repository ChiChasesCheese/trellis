---
nodes:
- memory.leaks-tracemalloc
title: tracemalloc：追踪内存分配
corpus: python-docs
section: 43-tracemalloc
url: https://docs.python.org/3/library/tracemalloc.html
tags:
- canonical
---

# tracemalloc：追踪内存分配

tracemalloc 是定位内存泄漏的标准工具：开启后它会记录每一次内存分配发生的调用栈（traceback），之后可以拍摄快照（take_snapshot()）并用 compare_to() 对比两次快照之间的差异，直接看出哪几行代码新分配了最多内存且没有释放，比盲目猜测精确得多。文档给出的完整示例展示了典型排查流程：在程序运行一段时间后拍第一次快照，触发怀疑有泄漏的操作，再拍第二次快照，然后打印按内存增量排序的差异统计（Statistic/StatisticDiff 对象）。文档还提供了 Pretty top 示例，演示如何格式化输出让人一眼看出问题代码位置。相比 gc 模块告诉你有循环引用没被回收，tracemalloc 回答的是更实际的问题，内存到底被谁分配掉了，两者结合是排查生产环境内存问题的标准组合拳。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/tracemalloc.html)

## Archived copy
![[pydocs-tracemalloc-clip]]
%% trellis:end %%
