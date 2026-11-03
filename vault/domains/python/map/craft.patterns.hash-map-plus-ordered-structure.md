%% trellis:begin %%
# 哈希表 + 有序结构：O(1) 定位，O(log n) 或 O(1) 取序
*编码功力（Coding Craft） / 跨题模式（Patterns）*

dict 管「按 key 找到」，另一个结构（链表、堆、有序列表、dict 插入序）管「按顺序取下一个」，两者同步增删。

**Requires:** [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]], [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]]

## Cards (5)
1. [[craft-hash-map-plus-ordered-structure-1-lru-two-structures]]
2. [[craft-hash-map-plus-ordered-structure-2-dict-order-gotcha]]
3. [[craft-hash-map-plus-ordered-structure-3-order-book]]
4. [[craft-hash-map-plus-ordered-structure-4-across-problems]]
5. [[craft-hash-map-plus-ordered-structure-5-scales-sampled-lru]]
%% trellis:end %%

## Notes
