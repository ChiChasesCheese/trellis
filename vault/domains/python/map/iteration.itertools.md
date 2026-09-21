%% trellis:begin %%
# `itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`
*迭代器、生成器与上下文管理器*

掌握用迭代器工具组合出流水线而不物化中间列表，`groupby` 要求先排序，以及 `tee` 的内存代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]]

## Readings
- [[effective-03-loops-iterators|Effective Python 3e · 第 3 章 循环与迭代器]]
- [[pydocs-functional-howto|函数式编程 HOWTO]]
- [[pydocs-itertools-module|itertools 模块：惰性迭代器工具]]

## Drills
- [[iteration-stream-a-10gb-log|Drill：用生成器管道统计 10 GB 日志的每小时错误数]]

## Cards (6)
1. [[accumulate-default-sum-custom-running-max]]
2. [[chain-concatenates-lazily-yield-from]]
3. [[groupby-group-view-invalidated-on-advance]]
4. [[groupby-requires-presorted-input]]
5. [[islice-advances-by-stop-not-yielded-count]]
6. [[tee-buffers-gap-between-branches]]
%% trellis:end %%

## Notes
