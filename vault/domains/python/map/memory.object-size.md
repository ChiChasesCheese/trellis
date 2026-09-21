%% trellis:begin %%
# 对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销
*内存管理与垃圾回收*

掌握一个 Python 对象的头部开销、list 的过量分配策略、dict 的键共享，以及百万级小对象为什么该用 `__slots__`、tuple、array 或 NumPy。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.allocator|pymalloc：arena / pool / block 与为何内存不还给操作系统]]

**Unlocks:** [[domains/python/map/performance.less-ram|省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构]]

## Readings
- [[cpy-dict-notes|dict 的键值分离设计：为什么同一个类的实例能共享一张键表]]
- [[cpyint-03-memory-management|CPython Internals · 内存管理]]
- [[hpp-11-using-less-ram|High Performance Python 2e · 第 11 章 减少内存占用]]
- [[peps-pep412-key-sharing-dict|PEP 412：键共享字典（Key-Sharing Dictionary）]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]
- [[pydocs-sys-module|sys 模块：解释器内部状态入口]]

## Cards (5)
1. [[dict-data-layout-three-parts]]
2. [[dict-key-sharing-saves-memory]]
3. [[dict-sparse-tradeoff]]
4. [[getsizeof-excludes-referents]]
5. [[slots-saves-per-instance-dict]]
%% trellis:end %%

## Notes
