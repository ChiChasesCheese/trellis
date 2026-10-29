---
id: uth-compose-k8s-indexer-5-interview
node: compose.k8s-indexer
type: qa
step: 5
---
## Q
**借到面试题：主表加索引**｜两张互指的表

要求插入、删除、随机取一个元素都是 O(1)，怎样用"主表加索引"的思路搭？

## A
**背景。** `Indexer` 的套路：数据放在一个结构里，另一个结构只记"数据在哪"，每次写入两边一起改。LC 380 要求插入、删除、随机取元素都是 O(1)：数组负责按下标随机取，字典 `值 → 下标` 负责按值定位，就是"主表加索引"。

| Indexer | LC 380 |
|---|---|
| `items` 主表 | `items` 数组 |
| `indices` 索引 | `pos` 字典：值 → 下标 |
| 不变量 | 对每个值 v：`items[pos[v]] == v` |
| 改对象：摘旧、挂新 | 搬末尾元素填坑：改 `pos[last]` |

**为什么。** 数组删中间元素要 O(n)，字典记了下标，就能用末尾元素填坑，把删除变成删末尾。

**坑。** 搬了末尾元素却忘了更新它在 `pos` 里的下标，不变量就断了，之后删除这个元素会删错位置。这和"改对象要同时更新所有索引"是同一类错误。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素（同类：LC 381 允许重复）

`RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回一个现有元素。三个操作平均 O(1)。例：`insert(1)` → `true`，`remove(2)` → `false`，`insert(2)` → `true`，`remove(1)` → `true`，`getRandom()` → `2`。

```python
import random


class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```
