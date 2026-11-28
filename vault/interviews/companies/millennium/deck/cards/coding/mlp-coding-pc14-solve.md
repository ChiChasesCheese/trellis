---
id: mlp-coding-pc14-solve
node: coding.pc14
step: 1
type: qa
---
## Q
**流式报价缓冲：题与解**｜编程轮

行情（市场上不断到来的报价）一条条流进来。设计一个缓冲：每个代码（symbol）只保留最近 N 条报价；`add(symbol, price)` 写入，`latest` 返回最新价，`average` 返回窗口内的平均价，`high` / `low` 返回窗口内的最高和最低价；行情线程写入、别的线程查询。

## A
**一句话思路。** 每个 symbol 用一个 `deque` 保存窗口内的报价，满了就从左边挤掉最老的一条；窗口总和随进出增减，平均价 O(1)。最高、最低价各用一个单调队列（monotonic deque，队内的价格单向递增或递减）：新价进来时，把队尾比它小的全部弹掉，因为它们比新价早到、过期更早，永远不会成为最大值，队首就是当前窗口的最大值；最小值对称。

```python
from collections import deque
from decimal import Decimal
from threading import Lock

class QuoteBuffer:
    """每个代码保留最近 n 条报价；latest / average / high / low 都是 O(1)。"""
    def __init__(self, n):
        self.n = n
        self.q = {}                              # symbol -> deque[(序号, 价格)]
        self.mx, self.mn = {}, {}                # 单调队列：队首是窗口内最大 / 最小
        self.total, self.seq = {}, {}
        self.lock = Lock()                       # 行情线程写、查询线程读

    def add(self, sym, price):
        price = Decimal(price)
        with self.lock:
            if sym not in self.q:
                self.q[sym], self.mx[sym], self.mn[sym] = deque(), deque(), deque()
                self.total[sym], self.seq[sym] = Decimal(0), 0
            i = self.seq[sym] = self.seq[sym] + 1
            q, mx, mn = self.q[sym], self.mx[sym], self.mn[sym]
            q.append((i, price))
            self.total[sym] += price
            while mx and mx[-1][1] <= price: mx.pop()    # 比新价小的永远当不了最大值，丢掉
            mx.append((i, price))
            while mn and mn[-1][1] >= price: mn.pop()
            mn.append((i, price))
            if len(q) > self.n:                  # 满了：挤掉最老的一条
                old_i, old_p = q.popleft()
                self.total[sym] -= old_p
                if mx[0][0] == old_i: mx.popleft()   # 被挤掉的正好是当前最大/最小，一并出队
                if mn[0][0] == old_i: mn.popleft()

    def latest(self, sym):
        with self.lock:
            return self.q[sym][-1][1]
    def average(self, sym):
        with self.lock:
            return self.total[sym] / len(self.q[sym])
    def high(self, sym):
        with self.lock:
            return self.mx[sym][0][1]
    def low(self, sym):
        with self.lock:
            return self.mn[sym][0][1]

b = QuoteBuffer(3)
for p in ["10", "12", "9", "11"]:
    b.add("X", p)                                # 窗口是 [12, 9, 11]
assert b.latest("X") == 11 and b.high("X") == 12 and b.low("X") == 9
assert b.average("X") == Decimal(32) / 3
b.add("X", "8")                                  # 12 被挤掉
assert b.high("X") == 11 and b.low("X") == 8
```

**复杂度。** `add` 均摊 O(1)（每条报价进出各队列至多一次）；四个查询都是 O(1)；空间 O(N × symbol 数)。

**边写边讲。**
- "A **deque with a size cap** gives me the last N quotes; eviction is O(1) from the left."
- "For high and low I keep a **monotonic deque**, so each quote is pushed and popped at most once."
- "Writes and reads come from different threads, so every method takes a **lock**."
