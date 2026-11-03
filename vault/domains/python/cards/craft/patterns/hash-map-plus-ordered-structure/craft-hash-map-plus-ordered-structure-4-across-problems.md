---
id: craft-hash-map-plus-ordered-structure-4-across-problems
node: craft.patterns.hash-map-plus-ordered-structure
type: qa
step: 4
---
## Q
**哈希表 + 有序结构 · 缓存、订单簿、定时器里怎么选配搭**｜模式

LRU 缓存、TTL 缓存、订单簿、图像前缀缓存都是「dict 加一个有序的东西」，但有序的东西各不相同：链表、堆、升序列表、OrderedDict。选择的依据是什么？

## A
**要点。** 三个问题决定搭配：（1）要按什么顺序取（最久未用 / 最早到期 / 最优价）；（2）要不要删中间的元素；（3）取序的代价能不能摊还。

```python
# lru-cache：最久未用，频繁删中间 → 双向链表，哨兵头尾，O(1) 摘除
class _DoublyLinkedList: ...   # append/remove/move_to_end/pop_front 都是 O(1)

# ttl-cache：最早到期，删中间少 → 小顶堆 + 惰性删除（墓碑）
class ExpiryIndex: ...         # 改期 / 撤销靠标记，压实摊还 O(1)

# stock-brokerage.BookSide：最优价 + 同价位 FIFO → dict + bisect 升序列表
self._levels: dict[int, dict[str, Order]] = {}
self._prices: list[int] = []   # 键集合永远与 _levels 相等
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

| 需要 | 结构 |
|---|---|
| 取最久未用，常删中间 | dict + 双向链表（或 OrderedDict） |
| 取最早到期，偶尔删中间 | dict + 堆 + 墓碑 |
| 取最优价，按价位分组 | dict + 升序列表 |

**不变。** 两份结构在同一把锁内同步增删，不变式写在注释里（`_levels` 与 `_prices` 键集合相等；缓存的 policy 键集合等于 store 键集合）。**变化。** 有序结构的类型，由取序的方式决定。

**见于。** lru-cache、ttl-cache、stock-brokerage、image-transform-pipeline、amz-closest-store、amz-configurable-cache。

**信号。** 需求里同时出现「按 key 找」和「按某个顺序取第一个」。
