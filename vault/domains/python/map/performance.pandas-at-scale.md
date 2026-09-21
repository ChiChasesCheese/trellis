%% trellis:begin %%
# pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制
*性能与数据处理*

掌握 `read_csv(chunksize=, usecols=, dtype=)` 控制内存、分块聚合再合并的 map-reduce 形态、`merge_asof` 做时间对齐、`validate=` 抓重复键，以及 2.x 写时复制（Copy-on-Write）对 `SettingWithCopy` 的影响。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/performance.numpy-vectorization|NumPy 向量化与内存布局：ndarray、广播、连续内存与视图]], [[domains/python/map/concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]]

## Readings
- [[hpp-12-lessons-from-the-field|High Performance Python 2e · 第 12 章 实战经验]]

## Drills
- [[performance-aggregate-50m-rows|Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级]]

## Cards (6)
1. [[pandas-category-dtype-groupby]]
2. [[pandas-chunking-map-reduce]]
3. [[pandas-copy-on-write-chained-assignment]]
4. [[pandas-dtype-usecols-at-read-time]]
5. [[pandas-merge-asof-time-alignment]]
6. [[pandas-when-to-move-to-polars-duckdb]]
%% trellis:end %%

## Notes
