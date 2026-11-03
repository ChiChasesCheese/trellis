%% trellis:begin %%
# bisect 与有序列表：floor/ceiling、key=、只查邻居
*编码功力（Coding Craft） / 高级写法（Idioms）*

有序列表 + bisect 回答「最后一个 ≤ x」「第一个 ≥ x」；key= 参数省掉并行列表；区间冲突只需检查两个邻居。

**Requires:** [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]], [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[domains/python/map/model.sequences|序列类型：list、tuple、array、memoryview 与切片语义]]

## Cards (6)
1. [[craft-bisect-sorted-lists-1-floor-ceiling]]
2. [[craft-bisect-sorted-lists-2-key-param]]
3. [[craft-bisect-sorted-lists-3-insort-cost]]
4. [[craft-bisect-sorted-lists-4-check-neighbours-only]]
5. [[craft-bisect-sorted-lists-5-across-problems]]
6. [[craft-bisect-sorted-lists-6-scales-temporal-index]]
%% trellis:end %%

## Notes
