---
id: tlc-python-classes-design-1-lru
node: python.classes-design
type: qa
step: 1
---
## Q
**Python 设计题｜用 `OrderedDict` 写 LRU 缓存**

LC 146 要求 `get` 和 `put` 都是 `O(1)`。用 `OrderedDict` 的完整类怎么写？`put` 里「已存在」「已满」两个分支的顺序要注意什么？

## A
哈希表负责 `O(1)` 查找，双向链表负责 `O(1)` 调整顺序；`OrderedDict` 把两者合在一起：末尾是最近使用，队首是最久未使用。

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.od: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)             # 刚用过：移到末尾
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        if key in self.od:
            self.od.move_to_end(key)         # 更新也算使用
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)      # 超容量：淘汰队首（最久未用）

c = LRUCache(2)
c.put(1, 1); c.put(2, 2)
print(c.get(1))        # 1
c.put(3, 3)
print(c.get(2))        # -1：2 被淘汰
c.put(4, 4)
print(c.get(1), c.get(3), c.get(4))   # -1 3 4
```

- 先判断「已存在」，只更新值和顺序，**不触发淘汰**；新键插入之后再判断容量，淘汰的才是旧的最久未用项。
- 所有操作 `O(1)`，空间 `O(capacity)`。
- 面试官常追问手写：自己建 `Node(key, val, prev, next)`，用哑头 / 哑尾节点避免空判断；`dict[int, Node]` 做索引；节点里必须存 `key`，淘汰时才能从字典里删掉对应项。
- LFU（LC 460）是进阶：每个访问频次一条链表，再记最小频次。
