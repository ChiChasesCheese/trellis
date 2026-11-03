---
id: craft-hash-map-plus-ordered-structure-3-order-book
node: craft.patterns.hash-map-plus-ordered-structure
type: qa
step: 3
---
## Q
**哈希表 + 有序结构 · 订单簿一侧为什么是价位字典加升序价位列表**｜写法

订单簿的买方要支持：挂单、按单号撤单、取最优价（最高买价）、同价位按先来先成交。怎么组合 `dict` 和有序结构？同价位的先进先出为什么不用 `deque`？

## A
**要点。** 价位 → 该价位的挂单字典（`dict[价位, dict[单号, 订单]]`），外加一张升序的价位列表（`bisect` 维护）。最优价是列表端点；同价位的先后由内层 dict 的插入序天然给出，撤单是 O(1)。`deque` 撤中间一张单是 O(n)。

```python
def add(self, o):
    level = self.levels.get(o.price)
    if level is None:
        level = self.levels[o.price] = {}
        bisect.insort(self.prices, o.price)      # 新价位：保持升序
    level[o.id] = o

def remove(self, o):
    level = self.levels.get(o.price)
    if level is None or level.pop(o.id, None) is None:
        return False                             # O(1) 撤单
    if not level:                                # 价位空了：两边同时删除
        del self.levels[o.price]
        self.prices.pop(bisect.bisect_left(self.prices, o.price))
    return True
```

挂 a(100)、b(101)、c(101)，撤 b，再撤 c；以及撤 300 张中间的单的耗时：

```
最优价 101 排第一的单 b 不变式 True
撤掉 b 后排第一的单 c
价位 101 空了 -> 最优价 100 价位表 [100] 不变式 True
撤 300 张中间的单：dict 11 us，deque 35468 us
```

**不变式。** 价位字典和价位列表的键集合永远相等，空价位必须立刻从两边一起删，否则最优价会指向一个没有挂单的价位。

**代价。** 列表插入新价位是 O(log n) 找位置加 O(n) 移动元素；价位数量有限时可以接受，价位极多时换成平衡树或跳表。
