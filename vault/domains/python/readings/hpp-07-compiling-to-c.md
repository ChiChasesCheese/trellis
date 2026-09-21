---
nodes: [performance.compiling]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 7 章 编译为 C
---
# High Performance Python 2e · 第 7 章 编译为 C

这一章比较 Cython、Numba 等把热路径编译成机器码的工具：给关键函数加类型标注、让编译器脱离 Python 对象模型直接操作原生数值，换来数量级的加速。

**读时提取：**
- Cython 的类型标注如何让循环变量脱离 Python 对象的装箱开销
- Numba 的 JIT 装饰器适合什么样的数值密集型函数
- 编译到 C 这条路的代价：构建复杂度、调试难度上升

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
