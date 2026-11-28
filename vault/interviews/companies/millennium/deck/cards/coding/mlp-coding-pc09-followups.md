---
id: mlp-coding-pc09-followups
node: coding.pc09
step: 2
type: qa
---
## Q
**价格数据存储：追问与变体**｜编程轮

价格存储写完后，面试官会往哪些方向追问？

## A
- **多币种换算：** 汇率表就是另一个按时间取"不晚于"的存储，键是货币对（如 `GBPUSD`，1 英镑等于多少美元）。先找正向货币对，价格乘汇率；找不到再找反向货币对，价格除以汇率，因为报价方未必两个方向都发布；两个方向都没有就抛 `LookupError`；币种相同则直接返回，不查表。同一套二分，换一层皮。

```python
def price_in_base(store, fx, symbol, ts, ccy, base):
    price = store.as_of(symbol, ts)
    if ccy == base:
        return price                           # 同币种，不查汇率
    try:
        return price * fx.rate_as_of(ccy + base, ts)    # 正向：GBP -> USD
    except KeyError:
        return price / fx.rate_as_of(base + ccy, ts)    # 反向货币对：除以汇率
```

- **为什么不用 `append`：** 乱序到达时列表不再有序，`as_of`、`ohlc`、`vwap` 的二分和切片全部失效。这是本题的核心。
- **迟到数据：** 很旧的记录很晚才到（回填历史），`insort` 仍把它插到正确位置，只是这一次插入是 O(n)；和乱序写入是同一个问题。
- **为什么 `latest` 不存一个变量：** 乱序写入可能写进一条更早的时间戳，这时最后一次 upsert 的不是最大 ts 的那条；这里选正确性，取排序列表的末尾。
- **内存：** 百万级 tick 要考虑按时间分桶、冷数据落盘。
- **持久化：** 真实系统写预写日志（WAL，先记日志再改数据，重启时重放），或把有序数据定期快照到按 `(symbol, 日期)` 分区的列式存储。
- **舍入：** 只在展示那一刻舍入一次；`vwap` 里提前舍入，误差会在后面乘汇率时放大。
- **查不到时为什么抛异常：** 返回 `None` 或 0，调用方容易忘记判断，也会把"没有数据"和"价格恰好是 0"混为一谈；未知 symbol 抛 `KeyError`，key 存在但那个时间没数据抛 `LookupError`。
- **会多花一个测试用例的边界：** 同一 `(symbol, ts)` 覆盖；`as_of` 早于第一笔；区间内只有一笔时开高低收相同；区间内没数据；`t0 > t1`；`vwap` 区间内总成交量为 0；传入 `float` 金额。

**英文答法。**
- "As-of means the **last value at or before** that time, so it's a `bisect_right` minus one."
- "A missing key and a **missing time point** are different failures, so I raise different exceptions."
- "For production I'd add a **write-ahead log** and snapshot the sorted arrays to columnar storage."
