---
id: mlp-finance-mk-bars
node: finance.markets
step: 5
type: qa
---
## Q
**OHLC 与 VWAP**｜金融常识

"OHLC 和 VWAP 是什么？怎么从逐笔数据算出来？"

## A
**OHLC** 是一段时间的四个价格：开盘价（open，这段时间第一笔）、最高价（high）、最低价（low）、收盘价（close，最后一笔）。开盘和收盘按时间顺序取，不是按数据到达的顺序取；乱序到达的数据要先按时间排好。

**VWAP（volume-weighted average price，成交量加权平均价）** 是 `Σ(价格 × 成交量) / Σ成交量`。成交量大的价格权重大，所以它比简单平均更接近大家真正成交的平均价。执行交易时常拿 VWAP 当基准，看自己的成交价是否优于市场平均。区间内总成交量为 0 时 VWAP 没有定义，要当作错误处理，而不是返回 0。

**对数据工程师意味着什么。**
- **读时计算：** 这类 K 线可以对价格历史做无状态的读时聚合，不用把它存成可变状态。
- **要可复现：** 带上"查询时刻"时，只能用当时已知的 tick 聚合，不能用事后修正过的。
- **金额用定点十进制：** 价格和成交量用 `Decimal`，不用浮点数，只在展示时舍入。

**英文答法。**
- "**OHLC** takes open and close in **time order**, not arrival order."
- "**VWAP** is the sum of price times volume over total volume, and it's undefined with zero volume."
