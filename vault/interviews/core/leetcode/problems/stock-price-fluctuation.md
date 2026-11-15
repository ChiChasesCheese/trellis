---
slug: stock-price-fluctuation
---
## Q
**LC 2034 股票价格波动**｜Medium

价格记录流乱序到来，`update(timestamp, price)` 可能更正之前同一时间戳的价格。设计 `StockPrice`：`current()` 返回最新时间戳的价格，`maximum()`、`minimum()` 返回所有记录中的最高、最低价格。

## A
**一句话。** 哈希表存每个时间戳的最新价格，两个堆（大顶、小顶）存历史记录；查询时若堆顶价格与哈希表里的最新价格不符，就是被更正过的旧值，弹掉。

```python
class StockPrice:
    def __init__(self):
        self.price = {}                # 时间 -> 当前价格
        self.latest = 0
        self.hi, self.lo = [], []      # 大顶堆、小顶堆（惰性删除）

    def update(self, timestamp, price):
        self.price[timestamp] = price
        self.latest = max(self.latest, timestamp)
        heappush(self.hi, (-price, timestamp))
        heappush(self.lo, (price, timestamp))

    def current(self):
        return self.price[self.latest]

    def maximum(self):
        while -self.hi[0][0] != self.price[self.hi[0][1]]:
            heappop(self.hi)           # 已被更正的旧价格
        return -self.hi[0][0]

    def minimum(self):
        while self.lo[0][0] != self.price[self.lo[0][1]]:
            heappop(self.lo)
        return self.lo[0][0]
```

**复杂度。** 时间 `update` 为 `O(log n)`，`maximum`、`minimum` 均摊 `O(log n)`，空间 `O(n)`。

**易错点。**
- 更正时去堆里删旧价格：堆不支持任意删除，用惰性删除，到堆顶再校验。
- 堆元素只存价格：校验时需要时间戳去查最新价，所以要存 `(价格, 时间戳)`。
- `current` 用最后一次 `update` 的时间戳：乱序到来，要取最大的时间戳。

**追问。**
- 不用堆有别的做法吗？：`SortedList`（有序多重集）存价格，更正时删旧加新，最大最小直接取两端。
- 为什么惰性删除均摊正确？：每条记录最多入堆一次、出堆一次。

**同模式。** LC 295 数据流的中位数、LC 981 基于时间的键值存储、LC 2349 设计数字容器系统
