%% trellis:begin %%
# 内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect
*性能与数据处理*

能说出 list 头部插入 O(n)、`in` 在 list 与 set 上的差异、dict 查找的常数因子、`deque` 两端 O(1)，以及排序（Timsort）稳定且利用已有序段。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]]

## Readings
- [[cpy-timsort|Timsort：为什么 list.sort() 对“已经有点顺序”的数据特别快]]
- [[effective-12-data-structures-algorithms|Effective Python 3e · 第 12 章 数据结构与算法]]
- [[hpp-03-lists-tuples|High Performance Python 2e · 第 3 章 列表与元组]]
- [[hpp-04-dicts-sets|High Performance Python 2e · 第 4 章 字典与集合]]
- [[pydocs-collections-module|collections 模块：专用容器数据类型]]
- [[pydocs-sorting-howto|排序技巧（Sorting Techniques）]]
- [[pydocs-tutorial-datastructures|Python 教程第 5 章：数据结构]]

## Drills
- [[performance-aggregate-50m-rows|Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级]]
- [[runtime-explain-the-traceback-and-the-import-cycle|Drill：解释一个循环导入报错，再解释一个「异常被吞掉」的 traceback]]

## Cards (6)
1. [[containers-bisect-search-vs-insert]]
2. [[containers-in-list-vs-set]]
3. [[containers-list-head-vs-deque]]
4. [[containers-timsort-merge-order-stability]]
5. [[containers-timsort-minrun]]
6. [[containers-timsort-natural-runs]]
%% trellis:end %%

## Notes
