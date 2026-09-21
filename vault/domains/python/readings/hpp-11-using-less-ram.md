---
nodes: [memory.object-size, performance.less-ram, memory.allocator]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 11 章 减少内存占用
---
# High Performance Python 2e · 第 11 章 减少内存占用

这一章讲怎么量出一个 Python 对象实际占多少内存（不能只看 `sys.getsizeof` 顶层数字，容器要递归算），以及 `__slots__`、数组类型、更紧凑的数据结构如何显著压缩大规模对象的内存占用。

**读时提取：**
- `sys.getsizeof` 为什么不能直接反映容器的『递归』真实占用
- `__slots__` 如何去掉实例 `__dict__`，换来更小的单实例内存
- 用 `array`/NumPy 定长数值数组替代『一堆装箱的 Python int/float 对象』能省多少结构性开销

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
