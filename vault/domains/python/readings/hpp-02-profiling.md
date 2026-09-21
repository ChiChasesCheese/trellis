---
nodes: [performance.profiling, memory.leaks-tracemalloc]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 2 章 性能分析
---
# High Performance Python 2e · 第 2 章 性能分析

这一章系统讲各种 profiler 的取舍：`cProfile` 这类确定性分析器开销大但精确，统计采样分析器开销小但是近似，`memory_profiler`/`tracemalloc` 则专门定位内存增长点。

**读时提取：**
- 确定性 profiling（如 cProfile）与统计采样 profiling 的开销/精度取舍
- 逐行 profiling 工具如何定位到函数内部具体哪一行慢
- 内存 profiler 如何区分『峰值占用』和『持续增长（疑似泄漏）』

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
