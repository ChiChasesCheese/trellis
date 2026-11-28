---
id: mlp-design-sd01-conflict
node: design.sd01
step: 7
type: qa
---
## Q
**深挖：供应商冲突、时区与多币种**｜设计轮

"两家供应商对同一个 symbol 报了不同价格怎么办？不同交易所的收盘时间不同，怎么统一？非美元计价的价格怎么换算成基准币种？"

## A
**供应商冲突。** 按 symbol 配置主供应商和备选顺序，不做运行时投票。`GET_LATEST` 和 `GET_AS_OF` 默认用主供应商的值，其他供应商的原始记录都保留可查。后台任务持续比较各家对同一 symbol 的报价，分歧超过阈值（例如若干基点，bps，1 bp 是万分之一）就标记并告警：校验的输出是"标记加保留"，不是静默丢弃或静默选择。不要取平均：平均值是任何一家都没报过的虚构价格，还会掩盖分歧本身。

**时区与交易所日历。** 摄入时立刻把供应商给的本地时间转成 UTC，`valid_time` 只用 UTC 表达。本地收盘时间、夏令时（DST）和节假日这类日历信息作为元数据放在查询层，不掺进存储层的排序依据。按本地时间字符串存，排序和 as-of 比较就依赖字符串的时区假设，夏令时切换那几天会出错。

**多币种。** 汇率把货币对（如 GBPUSD，1 英镑等于多少美元）当作一个 symbol，走同一条摄入路径，同样有 `valid_time`、`knowledge_time` 和版本。换算时取和被换算价格同一时间点的汇率，不能用当前汇率换算历史价格，否则多币种盈亏（PnL，profit and loss）会算错。

**拆股、分红等公司行动。** 不修改原始价格历史，因为那天报告的收盘价确实是那个数；另维护一张按 symbol 和生效日期的调整因子表，需要连续可比的序列时在读取时套用。

**英文答法。**
- "I **flag** vendor disagreements above a threshold; averaging would invent a price nobody quoted."
- "Everything is stored in **UTC**; exchange calendars live in the query layer."
- "FX rates are ingested like prices, and I convert with the rate **at the same point in time**."
