%% trellis:begin %%
# 惰性删除堆：墓碑 + 压实（lazy deletion with tombstones and compaction）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

堆不能删中间元素：作废的条目留在堆里，弹出时发现无效就丢；墓碑过多时一次性压实重建。

**Requires:** [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]]

## Cards (5)
1. [[craft-lazy-deletion-heap-1-tombstone]]
2. [[craft-lazy-deletion-heap-2-validity-test]]
3. [[craft-lazy-deletion-heap-3-compaction]]
4. [[craft-lazy-deletion-heap-4-monotonic-time]]
5. [[craft-lazy-deletion-heap-5-scales-max-stack]]
%% trellis:end %%

## Notes
