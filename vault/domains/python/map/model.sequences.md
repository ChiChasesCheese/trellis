%% trellis:begin %%
# 序列类型：list、tuple、array、memoryview 与切片语义
*对象模型：名字、对象与数据模型（data model）*

区分容器序列与扁平序列、可变与不可变序列，掌握切片对象与 `__getitem__` 的交互、`+=` 的就地语义、`array`/`memoryview` 的零拷贝场景。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.mutability|可变与不可变对象：list vs tuple、可变默认参数、别名（aliasing）]]

**Unlocks:** [[domains/python/map/performance.numpy-vectorization|NumPy 向量化与内存布局：ndarray、广播、连续内存与视图]]

## Readings
- [[effective-02-strings-slicing|Effective Python 3e · 第 2 章 字符串与切片]]
- [[fluent-02-sequences|Fluent Python 2e · 第 2 章 序列构成的数组]]
- [[fluent-12-special-methods-sequences|Fluent Python 2e · 第 12 章 序列的特殊方法]]
- [[hpp-03-lists-tuples|High Performance Python 2e · 第 3 章 列表与元组]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]
- [[pydocs-array-module|array 模块：紧凑数值数组]]
- [[pydocs-builtin-types|内建类型（Built-in Types）完整参考]]
- [[pydocs-tutorial-datastructures|Python 教程第 5 章：数据结构]]

## Cards (6)
1. [[array-typecode-compact-storage]]
2. [[builtin-immutable-vs-mutable-sequence-types]]
3. [[choose-list-array-memoryview]]
4. [[memoryview-slice-assign-inplace-no-resize]]
5. [[memoryview-zero-copy-buffer-protocol]]
6. [[sequence-negative-index-and-slice]]
%% trellis:end %%

## Notes
