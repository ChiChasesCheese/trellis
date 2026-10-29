---
id: uth-compose-caffeine-1-needs
node: compose.caffeine
type: qa
step: 1
---
## Q
**缓存要什么，单个结构为什么不够**｜Caffeine · 3.3.1

内存缓存要快读、快写，满了要踢掉「最没用」的一条，还要按时间过期。只用一个哈希表，或只用 LRU（最近最少使用）链表，各缺什么？

## A
**背景。** 缓存是放在内存里的一小份热数据，容量有限，放满就得踢一条。需求写成表：

| 操作 | 要求 |
|---|---|
| `get` / `put` | O(1)，很多线程同时调用 |
| 淘汰 | 满了踢最没用的一条，O(1) |
| 过期 | 写入 N 秒后失效，不能每次扫全表 |

**结构。** 每个结构只擅长一件事：

- 哈希表（hash map）：按 key 秒查，但条目没有顺序，找「最没用」要扫全表。
- 哈希表 + 双向链表（LRU）：每次访问把条目挪到链尾，链头就是最久没用的，O(1)。可它只看「最近一次」：一次性扫过一百万个只用一次的 key，会把真正的热数据冲光。
- 给每个 key 记访问次数（LFU）：能保住热数据，但每个 key 都要存计数，曾经的大户永远不降温。

**为什么。** 「最近用过」和「经常用」是两个维度，一个结构只能排一个维度，所以 Caffeine 把几个结构拼在一起。

**例题：** LC 146 LRU 缓存（只有「最近」这一个维度）

设计固定容量的缓存：`get(key)` 命中返回值，否则返回 -1；`put(key, value)` 写入，超出容量时淘汰最久未使用的键，两个操作都要 O(1)。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` → 1，`put(3,3)` 淘汰键 2，`get(2)` → -1。

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)  # 右端恒为最近使用
        return self.store[key]

    def put(self, key: int, value: int) -> None:
        if key in self.store:
            self.store.move_to_end(key)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```
