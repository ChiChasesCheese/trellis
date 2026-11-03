---
id: craft-slots-and-memory-1-what-slots-removes
node: craft.idioms.slots-and-memory
type: qa
step: 1
---
## Q
**__slots__ 与内存 · slots 去掉了什么，省多少**｜写法

LRU 缓存的链表节点只有三个字段：key、prev、next。缓存里有几十万个节点。普通类的每个实例都带着一个 `__dict__`，写成 `__slots__` 之后到底去掉了什么？省的量级是多少，在什么条件下才值得？

## A
**要点。** 普通实例把属性存在自己的 `__dict__`（一个哈希表）里，任何属性都可以随时增减，代价是每个实例多一份字典的开销。声明 `__slots__` 之后，字段被固定下来，直接存在对象内部的固定位置，实例没有 `__dict__`。省下的是「每个实例一份」的固定开销，所以实例越多越值得；实例只有几十个时，省的内存可以忽略。

```python
import sys, tracemalloc

class Plain:
    def __init__(self, key, prev, nxt):
        self.key, self.prev, self.next = key, prev, nxt

class Slotted:
    __slots__ = ("key", "prev", "next")
    def __init__(self, key, prev, nxt):
        self.key, self.prev, self.next = key, prev, nxt

def per_instance(cls, n=100_000) -> float:
    tracemalloc.start()
    before = tracemalloc.get_traced_memory()[0]
    objs = [cls(1, None, None) for _ in range(n)]     # key 共用一个小整数，只量对象本身
    used = tracemalloc.get_traced_memory()[0] - before
    tracemalloc.stop()
    return (used - sys.getsizeof(objs)) / n           # 扣掉装它们的列表

p, s = per_instance(Plain), per_instance(Slotted)
print(f"普通类 {p:.0f} 字节/个  slots {s:.0f} 字节/个  省 {1 - s / p:.0%}")
print(hasattr(Plain(1, None, None), "__dict__"), hasattr(Slotted(1, None, None), "__dict__"))
```

实际输出（Python 3.14；3.11 和 3.12 上普通类的数字略有不同，slots 都是 56）：

```
普通类 96 字节/个  slots 56 字节/个  省 42%
True False
```

**为什么。** 3.11 起普通对象的属性字典是延迟创建的，空间已经比老版本紧凑，所以今天的收益是「几十个字节/个」而不是几倍；但乘上百万个实例就是几十兆。

**易错。** 不要只凭这个数字就给每个类都加 slots。收益 = 实例数 × 每个实例省的字节，实例数小时可忽略，却要付出下面几张卡片里的限制。
