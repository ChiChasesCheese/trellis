---
id: craft-slots-and-memory-5-scales-memory-budget
node: craft.idioms.slots-and-memory
type: qa
step: 5
---
## Q
**__slots__ 与内存 · 从 LRU 节点到百万键的内存预算**｜写法

LeetCode 的 LRU Cache 用双向链表加字典，节点写成带 `__slots__` 的小类。放到一个要缓存一百万个键的服务里，容量规划为什么必须按「每个条目的实际字节数」来估算，而不是按「键值本身的大小」？

## A
**要点。** 缓存的内存成本 = 条目数 ×（键值数据 + 每个条目的结构开销）。小条目场景里，结构开销（对象头、`__dict__`、指针、字典槽）往往不比数据本身小。所以做容量规划要先量一个实例的实际大小，再乘上条目数；这也解释了为什么高频出现的小对象值得用 slots，而不是靠「大概差不多」。

```python
import tracemalloc

class Plain:
    def __init__(self, key):
        self.key, self.prev, self.next = key, None, None

class Slotted:
    __slots__ = ("key", "prev", "next")
    def __init__(self, key):
        self.key, self.prev, self.next = key, None, None

def mb_for(cls, n: int) -> float:
    tracemalloc.start()
    nodes = [cls(1) for _ in range(n)]              # key 共用一个小整数，只量节点本身
    used, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return used / 1e6

N = 1_000_000
plain, slotted = mb_for(Plain, N), mb_for(Slotted, N)
print(f"{N:,} 个节点  普通类 {plain:.0f} MB  slots {slotted:.0f} MB  差 {plain - slotted:.0f} MB")
```

实际输出（Python 3.14，数字含装节点的列表，约 8 MB）：

```
1,000,000 个节点  普通类 104 MB  slots 64 MB  差 40 MB
```

**变化。** LeetCode 里节点开销不影响通过与否；在服务里，一百万个节点相差几十兆，还没算字典本身、键和值。多实例部署时每个实例都要付一份，所以结论是：先量单个条目的实际大小，再决定缓存容量上限（条数或字节数），而不是只设条数。

**代价。** 更省的选择是不用节点对象：用有序字典（`OrderedDict`）把链表放进 C 实现里，换来更少的 Python 对象；这里讨论的是「手写结构」时 slots 的价值，不是说所有缓存都要手写。
