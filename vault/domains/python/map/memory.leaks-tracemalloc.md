%% trellis:begin %%
# 长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`
*内存管理与垃圾回收*

掌握泄漏的常见来源（全局缓存、`lru_cache`、闭包与回调持有、循环引用加 `__del__`、C 扩展），用 `tracemalloc` 快照比对定位分配点，以及分块处理与定期重启 worker 的工程手段。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]]

## Readings
- [[effective-13-testing-debugging|Effective Python 3e · 第 13 章 测试与调试]]
- [[hpp-02-profiling|High Performance Python 2e · 第 2 章 性能分析]]
- [[pydocs-tracemalloc|tracemalloc：追踪内存分配]]

## Drills
- [[memory-debug-the-growing-worker|Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位]]

## Cards (5)
1. [[leak-sources-cache-closure-cycle-del]]
2. [[tracemalloc-diff-snapshots-finds-leak]]
3. [[tracemalloc-filter-noise-out]]
4. [[tracemalloc-start-early-and-frame-cost]]
5. [[tracemalloc-traceback-pinpoints-allocation-site]]
%% trellis:end %%

## Notes
