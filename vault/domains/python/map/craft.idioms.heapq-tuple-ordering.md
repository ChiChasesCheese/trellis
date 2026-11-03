%% trellis:begin %%
# heapq 的元组序与 tie-break：计数器、负号、dataclass(order=True)
*编码功力（Coding Craft） / 高级写法（Idioms）*

堆元素是 (主键, 次键, 序号, 载荷)：序号保证稳定与不比较载荷，负号做大顶堆，None 要包一层。

**Requires:** [[domains/python/map/runtime.stdlib-map|标准库地图：`collections`、`heapq`、`bisect`、`datetime`、`pickle`、`logging`]], [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (6)
1. [[craft-heapq-tuple-ordering-1-counter-before-payload]]
2. [[craft-heapq-tuple-ordering-2-max-heap]]
3. [[craft-heapq-tuple-ordering-3-none-sorts-last]]
4. [[craft-heapq-tuple-ordering-4-dataclass-order]]
5. [[craft-heapq-tuple-ordering-5-across-problems]]
6. [[craft-heapq-tuple-ordering-6-scales-delay-queue]]
%% trellis:end %%

## Notes
