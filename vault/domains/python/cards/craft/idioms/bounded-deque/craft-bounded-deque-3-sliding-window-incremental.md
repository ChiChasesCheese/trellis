---
id: craft-bounded-deque-3-sliding-window-incremental
node: craft.idioms.bounded-deque
type: qa
step: 3
---
## Q
**有界 deque · 熔断器的滑动窗口为什么要增量维护失败数**｜写法

熔断器看最近 N 次调用，失败率超过阈值就断开。用 `deque(maxlen=N)` 存每次的成败，每次判断都 `sum(...)` 重算一遍是 O(N)。怎样把它变成 O(1)？这里有什么容易算错的地方？

## A
**要点。** 窗口里的内容只在两端变化：右边进一个，满了左边出一个。所以失败数可以增量维护：进来的是失败就加一，被挤出去的是失败就减一。关键是在 `append` 之前先看清哪个元素会被挤出，因为追加之后它已经不见了。

```python
from collections import deque

class Window:
    """最近 n 次调用的成功/失败；失败率超过阈值就熔断。"""
    def __init__(self, n: int, threshold: float) -> None:
        self.w: deque[bool] = deque(maxlen=n)
        self.failures = 0                          # 增量维护，避免每次 sum(w)
        self.threshold = threshold
    def record(self, ok: bool) -> None:
        if len(self.w) == self.w.maxlen and not self.w[0]:
            self.failures -= 1                     # 被挤掉的那个是失败，要扣回来
        self.w.append(ok)
        if not ok:
            self.failures += 1
    def tripped(self) -> bool:
        return len(self.w) == self.w.maxlen and self.failures / len(self.w) >= self.threshold

w = Window(4, 0.5)
for ok in [False, False, True, True]:
    w.record(ok)
print(w.tripped(), w.failures)        # 4 个里 2 个失败 = 0.5
for ok in [True, True]:
    w.record(ok)                      # 最早的两个失败被挤出窗口
print(w.tripped(), w.failures, list(w.w))
assert w.failures == sum(not x for x in w.w)       # 增量值必须和重算一致
```

实际输出：

```
True 2
False 0 [True, True, True, True]
```

**为什么。** 第二行失败数从 2 回落到 0：被挤出的两个失败都被扣回来了，熔断器因此恢复。如果漏了「扣回」，失败数只增不减，熔断器会永远断开。最后一行的 `assert` 就是测试这类增量状态的办法：随时能用笨办法重算，两者必须相等。

**信号。** 一个窗口上的聚合值（总数、和、失败数），窗口只在两端变化，就可以增量维护；需要最大值或最小值时增量不行，要用单调队列。
