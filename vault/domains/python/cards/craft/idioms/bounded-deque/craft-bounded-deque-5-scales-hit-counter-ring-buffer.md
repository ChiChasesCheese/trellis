---
id: craft-bounded-deque-5-scales-hit-counter-ring-buffer
node: craft.idioms.bounded-deque
type: qa
step: 5
---
## Q
**有界 deque · 从 Hit Counter 到环形缓冲区和日志保留**｜写法

LeetCode 的 Hit Counter 要统计最近 300 秒的点击数；通知服务保留最近 N 条历史；Kafka 主题只保留最近 7 天或 N 字节的日志。它们都是「有界缓冲」，约束的维度分别是什么？在 deque 里怎么表达，什么时候要两个边界一起用？

## A
**要点。** 有界缓冲有两种界：个数界（最近 N 条）和时间界（最近 T 秒）。个数界用 `deque(maxlen=N)` 一行搞定；时间界要手写：每次读或写时，从左边弹出已过期的，每个元素最多进出一次，摊还 O(1)。时间界的缺陷是洪峰时个数无上限，所以生产里常两个界同时用。

```python
from collections import deque

class HitCounter:
    """LeetCode 362：过去 300 秒内的点击数。时间界，不是个数界。"""
    def __init__(self, window: int = 300) -> None:
        self.window = window
        self.hits: deque[int] = deque()            # 时间戳，单调不减
    def hit(self, t: int) -> None:
        self.hits.append(t)
    def count(self, t: int) -> int:
        while self.hits and self.hits[0] <= t - self.window:
            self.hits.popleft()                    # 每个时间戳最多进出一次：摊还 O(1)
        return len(self.hits)

h = HitCounter()
for t in [1, 2, 3, 300]:
    h.hit(t)
print(h.count(300), h.count(301), h.count(600))
big = HitCounter()
for t in range(1000):
    big.hit(t // 100)                              # 洪峰：同一秒大量点击
print(len(big.hits), "条时间戳在内存里")

class Capped(HitCounter):                          # 加一个个数上限兜底
    def __init__(self, window: int = 300, cap: int = 500) -> None:
        super().__init__(window)
        self.hits = deque(maxlen=cap)
c = Capped()
for t in range(1000):
    c.hit(t // 100)
print(len(c.hits), "条（上限兜底；超出的最旧点击不再计入）")
```

实际输出：

```
4 3 0
1000 条时间戳在内存里
500 条（上限兜底；超出的最旧点击不再计入）
```

**变化。** 第一行说明时间界：300 秒的窗口随时间滑动，旧点击自动离开。第二行说明洪峰下它无上限。第三行是加上个数界：内存有保证，代价是洪峰时统计偏低（这是明确的取舍）。到系统级，Kafka 的保留策略同时有时间与大小两个限制，哪个先到就删旧段：思路相同，只是单位从元素变成了日志段，删除也按整段进行。

**信号。** 看到「最近 N 个 / 最近 T 秒」的聚合、历史、窗口，先想有界 deque；问自己约束哪个维度，洪峰时谁来兜底。
