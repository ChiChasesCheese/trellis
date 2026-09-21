---
nodes: [performance.profiling]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 调试与基准测试
---
# CPython Internals · 调试与基准测试

这一部分讲怎么用 GDB 之类的工具调试 CPython 解释器本身（而不只是 Python 代码），以及 `pyperformance` 这类标准基准测试套件如何被用来衡量解释器改动对真实工作负载的影响。

**读时提取：**
- 调试解释器本身（C 层面）和调试 Python 代码用的是完全不同的一套工具链
- 基准测试套件为什么要覆盖一组真实工作负载，而不是单个微基准
- profiler 报告的『自身耗时』和『累计耗时』分别对应什么，容易被搞混

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
