# pc09 · Price Data Store：练的是"用有序结构 + 二分代替只 append 的 list"

> [!tldr]
> - 这题考的是：时间序列存储不能假设"插入顺序 = 时间顺序"，写入必须乱序容忍，查询要用二分
> - 三步套路：先想清楚"按 ts 排序的列表 + 二分"这个模型 → 跑通 upsert/latest/as_of → 区间聚合复用同一个有序列表切片
> - 最值得带走的一个模式：**任何"写入乱序到达、按时间查询"的存储题，先维护一个始终有序的 key 列表（`bisect.insort`），查询全部变成二分/切片**

## 1. 题目在说什么（人话版）

写一个价格数据存储：不断写入 `(symbol, ts, price)`，随时能查"某个 symbol 现在的最新价"、"某个 symbol 在某个历史时刻的价格是多少"（as-of 查询）、"某段时间区间的开高低收和成交量加权均价"，最后再加一层"这个价格是外币计价的，换算成统一的基础货币"。

```
upsert("AAPL", 100, "150.00")
upsert("AAPL", 105, "151.25")
upsert("AAPL", 102, "150.75")   # 写入顺序和时间顺序不一致
latest("AAPL")     -> 151.25    # ts 最大的那条，不是"最后写入"的那条
as_of("AAPL", 103) -> 150.75    # ts <= 103 里最新的一条
```

写入乱序到达是这题的核心陷阱：现实里行情、订单回报经常网络延迟导致后到达的消息反而时间戳更早。

## 2. 读题：把文字变成模型

- **实体**：多个 symbol，每个 symbol 是一条独立的价格时间序列。
- **输入长什么样**：`(symbol, ts, price, volume)` 四元组，`ts` 不保证递增到达。
- **输出要什么**：单点查询（`latest`/`as_of`）返回一个价格；区间查询（`ohlc`/`vwap`）返回聚合结果；第三层是把价格换算成另一种货币。
- **状态**：每个 symbol 需要记住"目前为止所有 `(ts, price, volume)`"，但只需要**按 ts 排序**这一种视角——没有别的查询模式。
- **一句话建模**：这是一个"按 key 分组、组内按时间排序、支持 as-of 点查和区间切片"的问题——本质上是给每个 symbol 一份"始终有序的数组"。

> [!note] 为什么选"排序列表 + 二分"而不是"dict-of-list + append"
> `append` 只保证插入顺序；写入一旦乱序，`latest`（想要 ts 最大）和 `as_of`（想要 ts <= 查询值里最新的）全部找错。`bisect.insort` 把"插入"变成"插入到该在的排序位置"，之后的所有查询都能用二分，且对递增到达的正常场景，插入退化成 O(1) 摊还的末尾追加——正确性没有额外代价。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`PriceStore.__init__` 建两层结构：`ts_list: dict[symbol, list[ts]]` + `price_map: dict[symbol, dict[ts, price]]`。先让 `upsert`/`latest` 跑起来，立刻用题面样例自测。
2. **Part 1 最小可用**：`upsert` 里 `if ts not in price_map[symbol]: bisect.insort(ts_list[symbol], ts)`，再无条件覆盖 `price_map[symbol][ts] = price`（这一行同时处理了"首次写入"和"覆盖写入"两种情况）。`as_of` 用 `bisect_right(ts_list, ts) - 1` 拿下标。
3. **Part 2 叠加**：`ohlc`/`vwap` 用 `bisect_left`/`bisect_right` 切出区间对应的下标范围，`open`/`close` 是切片首尾，`high`/`low` 是切片里的 max/min，`vwap` 是切片里 `Σ(price·volume)/Σ(volume)`。这一步不需要碰 Part 1 的任何代码，只是多读了同一个排序列表。
4. **Part 3 叠加**：另开一个 `FXTable`，其实就是把 `PriceStore.as_of` 的查找逻辑抽出来复用——"symbol" 换成"货币对"，"price" 换成"汇率"。`price_in_base` 先查正向货币对再查反向货币对（除法代替乘法）。
5. **收尾**：舍入规则只写一次（展示层 `quantize` 到 4 位小数，`ROUND_HALF_UP`），内部计算全程用精确 `Decimal`，不要在中间步骤舍入。

## 4. 代码怎么组织

```
_check_symbol / _check_ts / _to_decimal   # 输入校验 + float 拒绝，集中一处
_as_of_lookup(ts_list, value_map, ts)     # 二分核心，PriceStore.as_of 和 FXTable.rate_as_of 共用
PriceStore.upsert/latest/as_of/ohlc/vwap  # Part 1 + Part 2
FXTable.upsert/rate_as_of                 # Part 3，复用 _as_of_lookup
price_in_base(store, fx, ...)             # Part 3：正向/反向货币对 + 同币种短路
_fmt(x)                                    # 四舍五入只在这里发生一次
process_operations(lines) / part1..part3 / main
```

`_as_of_lookup` 被抽出来是这题唯一值得强调的复用点：写完 `PriceStore.as_of` 之后，`FXTable.rate_as_of` 不是重新写一遍二分，而是调用同一个函数——面试官会注意到"这人看出了这是同一个问题的第二个实例"。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def _as_of_lookup(ts_list, value_map, ts):
    i = bisect.bisect_right(ts_list, ts) - 1   # 最后一个 <= ts 的下标
    if i < 0:
        raise LookupError(f"no value at or before ts={ts}")
    return value_map[ts_list[i]]

class PriceStore:
    def upsert(self, symbol, ts, price, volume=0):
        price_d, vol_d = _to_decimal(price, "price"), _to_decimal(volume, "volume")
        if symbol not in self._ts:
            self._ts[symbol], self._px[symbol], self._vol[symbol] = [], {}, {}
        if ts not in self._px[symbol]:
            bisect.insort(self._ts[symbol], ts)   # 只在首次出现该 ts 时插入排序列表
        self._px[symbol][ts] = price_d             # 覆盖：后写的赢
        self._vol[symbol][ts] = vol_d

    def ohlc(self, symbol, t0, t1):
        arr = self._ts[symbol]
        window = arr[bisect.bisect_left(arr, t0):bisect.bisect_right(arr, t1)]
        prices = [self._px[symbol][t] for t in window]
        return prices[0], max(prices), min(prices), prices[-1]   # open, high, low, close
```

## 6. Talking through it in the interview

- Before starting: "Since writes can arrive out of order, I want to key each symbol's history on a list I keep sorted by timestamp with `bisect.insort`, so every query — latest, as-of, or a range — is a binary search or a slice instead of a linear scan."
- Writing Part 1: "latest isn't 'the last upsert call', it's the price at the *largest recorded timestamp* — those two only coincide when writes happen to arrive in order."
- Writing Part 3: "I'm reusing the exact same as-of binary search for the FX table — a rate table is just a price store where the symbol is a currency pair."
- On delivery: "The worked examples pass; if there's time I'd add persistence — right now everything is in-memory, a real system would snapshot the sorted arrays to columnar storage and replay a WAL on restart."

## 7. 常见跑偏（方法层面，3 条）

- 一上来就用 `dict[symbol] = []` 然后 `.append()`：能过"递增写入"的样例，但一遇到乱序写入的隐藏测试就全错——这题的隐藏测试专门构造了乱序输入。
- 把舍入散落在多个地方（比如 `vwap` 内部先 `round()` 再返回）：一旦后续还要拿这个值去乘汇率（Part 3），提前舍入的误差会被放大；舍入只应该在最终展示的那一刻做一次。
- `as_of` 查询不到数据时返回 `None` 或者 `0` 而不是抛异常：调用方很容易忘记判断 `None`，把"没有数据"和"价格恰好是 0"混为一谈；显式抛 `LookupError` 更安全。

## 8. 同族题 / 延伸

- 本 kit `pc08_lru_ttl_median`：同样是"设计一个带查询接口的数据结构"，那道题的 TTL 淘汰和这题的"始终有序 + 二分"是两种不同的"维护结构不变量"手法。
- `../../snowflake/loop/rounds/03_phone_coding/pc03_recent_event_stream`：同一种"类 + 批处理封装函数 + main() 命令流"骨架，那道题维护的是滑动窗口而不是全历史。
- 系统设计版：本 kit 第二轮 `sd01`（market/price data service）是这题的分布式/持久化版本，值得对照复习。
- 练习命令：`python3 loop/mock.py start pc09`
