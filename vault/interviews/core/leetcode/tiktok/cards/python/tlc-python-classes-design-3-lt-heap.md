---
id: tlc-python-classes-design-3-lt-heap
node: python.classes-design
type: qa
step: 3
---
## Q
**Python 设计题｜让自己的类能放进堆：`__lt__` 与 `total_ordering`**

`heapq` 只用 `<` 比较。自定义类要怎样才能入堆？`functools.total_ordering` 帮了什么忙？

## A
`heapq` 只调用元素的 `__lt__`。定义了 `__lt__`，类就能入堆、`sorted`、`min`：

```python
import heapq
class Ver:
    def __init__(self, v: int, i: int) -> None:
        self.v, self.i = v, i
    def __lt__(self, other: "Ver") -> bool:
        return (self.v, self.i) < (other.v, other.i)   # 先比值，值相同比序号
h = [Ver(2, 0), Ver(1, 1), Ver(1, 0)]
heapq.heapify(h)
print([(x.v, x.i) for x in (heapq.heappop(h) for _ in range(3))])   # [(1, 0), (1, 1), (2, 0)]
```

- `__lt__` 里写成一个**元组比较**，既清楚又保证平局时有确定顺序。
- 需要 `<=`、`>`、`>=` 时，写 `__eq__` 和 `__lt__`，再用 `@functools.total_ordering` 补全其余的：

```python
from functools import total_ordering
@total_ordering
class P:
    def __init__(self, x: int) -> None: self.x = x
    def __eq__(self, o: object) -> bool: return isinstance(o, P) and self.x == o.x
    def __lt__(self, o: "P") -> bool: return self.x < o.x
print(P(1) <= P(2), P(3) > P(2), max(P(1), P(5)).x)   # True True 5
```

- 最大堆：把 `__lt__` 写成 `self.v > other.v`，不用对字段取负；这在字段是字符串、不能取负时很有用。
- LC 23 合并 K 个链表的做法有两种：给 `ListNode` 加 `ListNode.__lt__ = lambda a, b: a.val < b.val`（猴子补丁，LeetCode 上可行），或入堆 `(val, i, node)`。后者更安全，不依赖修改题目给的类。
- 性能：`__lt__` 是 Python 函数，每次比较的开销比元组比较大；`n` 在 `10^5` 以上时优先用元组。
