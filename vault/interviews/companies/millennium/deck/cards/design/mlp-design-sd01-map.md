---
id: mlp-design-sd01-map
node: design.sd01
step: 1
type: qa
---
## Q
**这道题的地图**｜设计轮

"我们是一家多经理对冲基金（multi-manager，资金分给许多独立团队各自操盘），几十个交易团队（pod）各跑各的策略，还有一个中央风控团队汇总所有仓位算整体风险。现在每个 pod 自己写脚本接不同供应商的行情，请设计一个统一的价格数据服务。"

## A
**需求与规模。**
- **采集：** 收盘价（EOD，end of day）以文件形式由供应商每天收盘后投递；盘中价格是流式推送；供应商不止一家，同一个 symbol 可能被多家同时报价。公司全部数据文件每天 900K+ 份。
- **历史查询不能看到未来：** 回答"某个历史时刻的价格是多少"（as-of 查询，按那一刻系统已知的信息作答），修正值事后才到，不能影响此前的查询结果；风控拿它做历史归因。
- **读：** 几百个 pod 查最新价和历史价；风控对某个历史时刻做一致的价格快照。
- **衍生与多币种：** 算 OHLC 和 VWAP；换算成基准币种（base currency）时，汇率要和价格取同一时间点。
- **推送：** 价格变动主动推给订阅方，不让大家轮询。

**实体。** 价格记录：symbol、供应商、价格、币种、`valid_time`（价格在市场上生效的时刻）、`knowledge_time`（系统得知它的时刻）、版本号、指向被修正版本的指针。汇率把货币对当作一个 symbol，同样存。

**接口。** `PUT_PRICE`、`CORRECT_PRICE`（追加一条修正，不覆盖）、`GET_LATEST`、`GET_AS_OF`、`GET_BAR`、`SUBSCRIBE`。

**主路径。** 文件或流 → 归一化 → 追加写入价格历史日志 → 更新最新价缓存 → 查询服务读取，分发层尾随日志推送。

**英文答法。**
- "This is a price data service for a **multi-manager** fund: dozens of pods and one central risk system share the same market data."
- "The hard part is that **as-of queries must never see the future**, while vendors send **late corrections** that must not overwrite history."
- "So I'll make the store **bitemporal**, then walk through the API, ingestion, and failure modes."
