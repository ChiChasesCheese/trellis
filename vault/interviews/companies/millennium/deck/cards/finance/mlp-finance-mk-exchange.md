---
id: mlp-finance-mk-exchange
node: finance.markets
step: 2
type: qa
---
## Q
**交易所与交易时段**｜金融常识

"交易所（exchange）做什么？收盘价是怎么来的？不同市场时间不同，数据上要注意什么？"

## A
**交易所** 是撮合买卖订单的市场。每个交易所有自己的开盘和收盘时间、节假日和交易规则。多数股票交易所有盘前（pre-market）和盘后（after-hours）时段，成交稀少，价格更不稳。

**收盘价（closing price）** 常由收盘集合竞价（closing auction）决定：收盘前集中收集订单，一次性撮合出一个价格；供应商收盘后发来的 EOD（end of day）价格文件就是这个价。收盘价有时事后还会被供应商更正。

**不同市场的时间。** 纽约、伦敦、东京的本地时间、夏令时切换和节假日各不相同；同一个 UTC 时刻，有的市场开着，有的已收盘。

**对数据工程师意味着什么。**
- **统一用 UTC 存：** 摄入时就把本地时间转成 UTC，日历信息作为元数据放在查询层，别掺进存储排序。
- **"今天的收盘价"没有统一含义：** 要说清是哪个市场、哪个时区的收盘，否则按日期过滤会漏数据或串日。
- **EOD 是批处理：** 收盘后文件陆续到达，要处理重投、迟到和修正。

**英文答法。**
- "I store everything in **UTC** and keep exchange calendars as metadata."
- "The **closing price** comes from the closing auction, and vendors can correct it later."
