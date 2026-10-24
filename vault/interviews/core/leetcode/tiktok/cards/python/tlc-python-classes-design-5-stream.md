---
id: tlc-python-classes-design-5-stream
node: python.classes-design
type: qa
step: 5
---
## Q
**Python 设计题｜数据流类：移动平均与最后 K 个数的乘积**

「每次调用都要 `O(1)`」的数据流设计题，状态应该怎样放进 `__init__`？LC 1352 最后 K 个数的乘积遇到 0 怎么办？

## A
设计题的套路：先想**每个操作需要什么汇总量**，把它作为实例变量维护，让每次调用只做增量更新。

```python
from collections import deque
class MovingAverage:
    def __init__(self, size: int) -> None:
        self.q: deque[int] = deque(maxlen=size)
        self.total = 0                          # 窗口内元素之和，增量维护
    def next(self, val: int) -> float:
        if len(self.q) == self.q.maxlen:
            self.total -= self.q[0]             # 即将被挤出的元素
        self.q.append(val)
        self.total += val
        return self.total / len(self.q)
m = MovingAverage(3)
print([m.next(v) for v in (1, 10, 3, 5)])   # [1.0, 5.5, 4.666666666666667, 6.0]
```

**LC 1352**：存前缀乘积 `pre`，最后 `k` 个数的积 = `pre[-1] // pre[-1-k]`。遇到 `0`，前缀积全变 0 且不能做除法，所以**把 `pre` 重置为 `[1]`**；之后若 `k` 超过现有长度，说明区间内含 0，答案为 0。

```python
class ProductOfNumbers:
    def __init__(self) -> None:
        self.pre = [1]
    def add(self, num: int) -> None:
        if num == 0:
            self.pre = [1]                  # 零之前的前缀对之后都没用了
        else:
            self.pre.append(self.pre[-1] * num)
    def getProduct(self, k: int) -> int:
        if k >= len(self.pre):              # 窗口里包含最近一次 0
            return 0
        return self.pre[-1] // self.pre[-1 - k]
p = ProductOfNumbers()
for x in (3, 0, 2, 5, 4): p.add(x)
print(p.getProduct(2), p.getProduct(3), p.getProduct(4))   # 20 40 0
p.add(8); print(p.getProduct(2))                           # 32
```

- 乘积用整数除法是精确的（前缀积是后者的倍数）；Python 整数不溢出，无需取模。
- 所有操作 `O(1)`，空间 `O(n)`。
