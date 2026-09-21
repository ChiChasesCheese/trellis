---
nodes: [performance.profiling, performance.compiling, runtime.compile-bytecode]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 11 章 性能
---
# Effective Python 3e · 第 11 章 性能

这一章讲『先测量再优化』的纪律：用 `cProfile` 找到真正的热点而不是凭直觉优化，并简单介绍字节码编译和即时编译工具能在哪些场景把纯 Python 热路径提速。

**读时提取：**
- 为什么『猜哪里慢』通常是错的，profiler 给出的热点往往出人意料
- `cProfile`/`pstats` 的基本使用方式和如何读懂输出的调用时间
- 什么样的热路径适合用编译型工具（Cython 之类）而不是继续调 Python 代码

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
