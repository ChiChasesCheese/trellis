%% trellis:begin %%
# 前缀和 + 二分：把「某一时刻/某一站的累计值」变成 O(log n)/O(1)
*编码功力（Coding Craft） / 跨题模式（Patterns）*

事件只追加，所以累计值数组也只追加；查询用 bisect 找位置，再读前缀。

**Requires:** [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]], [[domains/python/map/iteration.itertools|`itertools` 与迭代器组合：`chain`、`groupby`、`islice`、`accumulate`]]

## Cards (5)
1. [[craft-prefix-sum-bisect-timeline-1-events-and-running-total]]
2. [[craft-prefix-sum-bisect-timeline-2-range-max-baseline]]
3. [[craft-prefix-sum-bisect-timeline-3-cross-check-with-sql]]
4. [[craft-prefix-sum-bisect-timeline-4-prefix-sum-for-positions]]
5. [[craft-prefix-sum-bisect-timeline-5-across-problems-and-scales]]
%% trellis:end %%

## Notes
