---
id: mlp-finance-mk-levels
node: finance.markets
step: 4
type: qa
---
## Q
**行情数据的层级与来源**｜金融常识

"行情数据（market data）有哪些层级？供应商和交易所直连有什么区别？"

## A
**层级，从细到粗。**
- **逐笔与订单簿更新（tick 和 depth）：** 每一笔成交、每一次报价变化，数据量最大。
- **一级行情（level 1）：** 最优买价、最优卖价和最近成交。
- **二级行情（level 2）：** 订单簿多档的价格和数量，即深度。
- **K 线（bar）：** 按时间段汇总，如每分钟的开高低收（OHLC）和成交量，数据量小很多。
- **日终数据（EOD）：** 每个产品每天一条，收盘后以文件形式交付。

**来源。** 数据供应商（vendor）把多个交易所的数据整理后提供，各家字段格式不同，需要逐家适配，同一个 symbol 可能被多家同时报价；交易所直连延迟最低，但要自己处理各交易所的协议。盘中通常是流式推送，收盘后是批量文件。

**对数据工程师意味着什么。**
- **每家供应商一份解析配置：** 新增供应商应该是配置变更，而不是新代码路径。
- **文件量大：** 一家大基金每天要处理 900K+ 份数据文件，摄入要并行、幂等。
- **各层级怎么选：** 回测通常用 K 线或日终，实时风控和执行才需要逐笔。

**英文答法。**
- "**Ticks** are the most granular; **bars** and **end-of-day** files are aggregates."
- "Each vendor has its own format, so I'd make onboarding a **configuration change**."
