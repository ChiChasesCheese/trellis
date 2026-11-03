---
id: craft-dunder-protocols-that-pay-5-container-semantics-cost
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 5
---
## Q
**特殊方法 · 带过期的缓存里 __len__ 和 __contains__ 为什么要先清理**｜写法

带过期时间的缓存想像 `dict` 一样支持 `len(c)` 和 `k in c`。`dict` 的这两个操作是纯读取、常数时间。缓存里一个条目已经过期但还没被物理删除，`len` 应该怎么回答？这对实现意味着什么？

## A
**要点。** 对使用者来说，过期的条目就不存在：`len` 和 `in` 不应该把它们算进去。所以这两个方法在回答之前先清理过期条目（sweep），不再是无副作用的 O(1)。语义对齐 `dict`，代价是一次 `len()` 可能做清理工作，也需要加锁；这是特殊方法里最容易被忽略的隐藏成本。

```python
class TTL:
    def __init__(self, clock) -> None:
        self._d: dict[str, tuple[float, int]] = {}      # key -> (过期时间, 值)
        self._clock = clock
    def put(self, k: str, v: int, ttl: float) -> None:
        self._d[k] = (self._clock() + ttl, v)
    def _sweep(self) -> None:                           # 先清掉过期的，再回答
        now = self._clock()
        for k in [k for k, (exp, _) in self._d.items() if exp <= now]:
            del self._d[k]
    def __len__(self) -> int:
        self._sweep(); return len(self._d)
    def __contains__(self, k: str) -> bool:
        self._sweep(); return k in self._d

t = [0.0]
c = TTL(lambda: t[0])
c.put("a", 1, 10); c.put("b", 2, 2)
print(len(c), "b" in c)
t[0] = 3
print(len(c), "b" in c, len(c._d))
```

实际输出：

```
2 True
1 False 1
```

**为什么。** 第二行：时间走到 3，`b` 已过期，`len` 是 1，`"b" in c` 为假，内部字典也只剩 1 条（物理删除了）。如果 `__len__` 不先清理，`len(c._d)` 会是 2，使用者看到的数量就是错的。

**代价。** 每次 `len()` 都可能是 O(n)。性能敏感时，用小根堆按过期时间排序，每次只弹出已到期的，让清理的代价正比于过期的条数，而不是总条数。
