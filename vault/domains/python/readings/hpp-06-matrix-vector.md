---
nodes: [performance.numpy-vectorization]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 6 章 矩阵和向量计算
---
# High Performance Python 2e · 第 6 章 矩阵和向量计算

这一章讲为什么用 NumPy 向量化操作替代 Python 层面的逐元素循环能快一个数量级以上：运算下沉到 C 层的连续内存块上执行，避免了 Python 解释器逐元素调度的开销。

**读时提取：**
- 向量化操作如何把逐元素循环变成一次 C 层批量运算
- NumPy 数组的连续内存布局为什么对缓存友好
- 什么时候纯 Python 循环嵌套 NumPy 调用反而更慢（小数组、频繁调用开销）

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
