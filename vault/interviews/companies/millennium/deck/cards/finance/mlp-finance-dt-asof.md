---
id: mlp-finance-dt-asof
node: finance.data
step: 1
type: qa
---
## Q
**时间序列、as-of 与前视偏差**｜金融常识

"什么是 as-of 查询？前视偏差（look-ahead bias）是什么？为什么对基金这么重要？"

## A
**时间序列（time series）** 是按时间排列的一串数据，如某只股票每天的收盘价。研究、风控和回测几乎都建立在时间序列上。

**as-of 查询** 问的是"在时刻 t，最新的值是多少"，即时间不晚于 t 的最后一条记录。例如周六问某股票的价格，答案是周五的收盘价。as-of 连接（as-of join）则是把两张表按时间对齐，每一行取对方在那一刻之前最新的值，DuckDB 等引擎直接支持。

**前视偏差** 是在某个历史时刻的计算里，用到了那时还不存在的信息，例如用事后才发布的修正值、或事后才算出的因子值。这会让回测收益虚高，策略上线后表现不及预期。点时数据（point-in-time，只包含当时已知的数据）是它的解药。

**对数据工程师意味着什么。**
- **查询语义要定义清楚：** 区分价格何时生效和系统何时得知，用后者回答"当时知道什么"。
- **修正追加不覆盖：** 覆盖旧值会让同一个历史查询今天和明天答案不同。
- **风控归因依赖它：** 一旦历史查询读到事后的修正，归因就不可复现。

**英文答法。**
- "An **as-of** query returns the latest value at or before a given time."
- "**Look-ahead bias** means using information that wasn't available yet, so backtests look better than reality."
