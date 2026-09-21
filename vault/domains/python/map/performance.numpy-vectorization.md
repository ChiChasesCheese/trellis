%% trellis:begin %%
# NumPy 向量化与内存布局：ndarray、广播、连续内存与视图
*性能与数据处理*

理解向量化把循环下推到 C、连续内存与缓存友好、切片是视图而非拷贝、广播规则，以及为什么 Python 层 `for` 循环比向量化慢一到两个量级。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]]

**Unlocks:** [[domains/python/map/performance.pandas-at-scale|pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制]]

## Readings
- [[hpp-06-matrix-vector|High Performance Python 2e · 第 6 章 矩阵和向量计算]]

## Drills
- [[performance-aggregate-50m-rows|Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级]]

## Cards (6)
1. [[numpy-vectorization-broadcasting-rule]]
2. [[numpy-vectorization-contiguous-cache]]
3. [[numpy-vectorization-fancy-indexing-copies]]
4. [[numpy-vectorization-order-of-magnitude]]
5. [[numpy-vectorization-push-to-c]]
6. [[numpy-vectorization-slice-is-view]]
%% trellis:end %%

## Notes
