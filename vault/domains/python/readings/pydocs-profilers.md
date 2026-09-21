---
nodes:
- performance.profiling
title: Python Profilers：cProfile 与 profile
corpus: python-docs
section: 63-profile
url: https://docs.python.org/3/library/profile.html
tags:
- canonical
---

# Python Profilers：cProfile 与 profile

这是官方剖析器（profiler）参考，cProfile（C 实现，开销较小，推荐日常使用）和 profile（纯 Python 实现，可扩展但开销大得多）提供相同接口。文档讲清了确定性剖析（deterministic profiling）的原理：在每个函数调用和返回时插桩计时，能精确统计每个函数被调用了多少次、自身耗时多少、连同子调用一共耗时多少（Stats 类提供了按不同维度排序输出这些统计的方法），但插桩本身带来的开销会让结果比真实运行慢，需要用校准（calibration）机制扣除测量工具自身引入的系统性偏差。文档也坦承了局限性：C 扩展函数内部的调用不会被逐层统计，多线程程序的剖析结果需要额外小心解读。这是整个程序到底慢在哪个函数这类问题该先用的工具，比 timeit 的适用范围更宏观。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/profile.html)

## Archived copy
![[pydocs-profilers-clip]]
%% trellis:end %%
