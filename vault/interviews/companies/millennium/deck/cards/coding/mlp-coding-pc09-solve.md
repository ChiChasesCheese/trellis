---
id: mlp-coding-pc09-solve
node: coding.pc09
step: 1
type: qa
---
## Q
**价格数据存储：题与解**｜编程轮

设计一个存股票价格的内存结构：`upsert(symbol, ts, price, volume)` 写入一笔行情（tick，某时刻的一次报价），同一个 `(symbol, ts)` 再写就覆盖；`latest(symbol)` 返回最新价；`as_of(symbol, ts)` 返回时间不晚于 `ts` 的最后一笔价格；`ohlc` 返回一段时间的开盘、最高、最低、收盘价；`vwap` 返回成交量加权平均价。写入顺序不保证按时间递增。

## A
**一句话思路。** 每个 symbol 维护一个始终按时间排序的时间戳列表（`bisect.insort` 插入），再配一个 `ts -> 价格` 的字典；所有查询都是对排序列表的二分查找或切片。不能直接 `append`：乱序到达时列表不再有序，二分就全错。金额一律用 `Decimal`，不用浮点数。

```python
import bisect
from decimal import Decimal

class PriceStore:
    def __init__(self):
        self.ts = {}      # symbol -> 排序后的时间戳列表
        self.px = {}      # symbol -> {ts: 价格}
        self.vol = {}     # symbol -> {ts: 成交量}

    def upsert(self, symbol, ts, price, volume=0):
        if isinstance(price, float) or isinstance(volume, float):
            raise ValueError("use str, int or Decimal for money")
        if symbol not in self.ts:
            self.ts[symbol], self.px[symbol], self.vol[symbol] = [], {}, {}
        if ts not in self.px[symbol]:
            bisect.insort(self.ts[symbol], ts)     # 乱序到达也插在正确位置
        self.px[symbol][ts] = Decimal(price)        # 同一个 ts 再写：后写的覆盖
        self.vol[symbol][ts] = Decimal(volume)

    def latest(self, symbol):
        arr = self.ts[symbol]                       # 未知 symbol 抛 KeyError
        return self.px[symbol][arr[-1]]             # 取最大 ts，不是最后一次 upsert 的那条

    def as_of(self, symbol, ts):
        arr = self.ts[symbol]
        i = bisect.bisect_right(arr, ts) - 1        # 最后一个 <= ts 的位置
        if i < 0:
            raise LookupError(f"no price at or before {ts}")   # key 存在，但那个时刻没数据
        return self.px[symbol][arr[i]]

    def _window(self, symbol, t0, t1):
        if t0 > t1:
            raise ValueError("t0 must be <= t1")
        arr = self.ts[symbol]
        w = arr[bisect.bisect_left(arr, t0):bisect.bisect_right(arr, t1)]   # 闭区间 [t0, t1]
        if not w:
            raise LookupError("no data in range")
        return w

    def ohlc(self, symbol, t0, t1):
        prices = [self.px[symbol][t] for t in self._window(symbol, t0, t1)]
        return prices[0], max(prices), min(prices), prices[-1]   # 开收盘按时间顺序，不按插入顺序

    def vwap(self, symbol, t0, t1):
        w = self._window(symbol, t0, t1)
        den = sum((self.vol[symbol][t] for t in w), Decimal(0))
        if den == 0:
            raise ValueError("zero volume")         # 除零，和"没数据"是两种失败
        return sum((self.px[symbol][t] * self.vol[symbol][t] for t in w), Decimal(0)) / den

s = PriceStore()
for ts, p in [(100, "150.00"), (105, "151.25"), (102, "150.75")]:
    s.upsert("AAPL", ts, p)
print(s.latest("AAPL"), s.as_of("AAPL", 103))   # 151.25 150.75
m = PriceStore()
for ts, p, v in [(1, "300", "10"), (2, "305", "5"), (3, "295", "20"), (4, "310", "5")]:
    m.upsert("MSFT", ts, p, v)
print(m.ohlc("MSFT", 1, 4), m.vwap("MSFT", 1, 4))   # (300, 310, 295, 310) 299.375
```

**复杂度。** `latest` 和 `as_of` 是 O(log n)；`ohlc`、`vwap` 是 O(log n + 区间内笔数)。`insort` 单次插入最坏 O(n)，但实盘行情基本递增，新时间戳几乎总插在末尾，摊还接近 O(1)。

**边写边讲。**
- "Writes can arrive **out of order**, so I keep a list sorted by timestamp and use `bisect`."
- "`latest` is the price at the **largest timestamp**, not the last upsert call."
- "I use **Decimal**, and I'd round only at display time, never inside storage or calculations."
