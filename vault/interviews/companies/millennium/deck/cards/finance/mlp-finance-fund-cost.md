---
id: mlp-finance-fund-cost
node: finance.fund
step: 5
type: qa
---
## Q
**交易成本、基点与结算**｜金融常识

"策略的收益为什么要扣交易成本？bps 是什么？交易之后的结算（settlement）是什么？"

## A
**交易成本（transaction cost）** 包括佣金、买卖价差（买价和卖价的差）和市场冲击（你的单子自己把价格推动了）。滑点（slippage）是预期成交价和实际成交价的差。成本不扣掉，回测里赚钱的策略实盘可能亏钱，所以评估策略要看"扣完成本后"的夏普。

**基点（bps，basis point）** 是万分之一，1 bp 是 0.01%，10 bps 是 0.10%。成本、价差、分歧都习惯用 bps 表达。

**结算（settlement）** 是交易达成后现金和证券真正换手。美国股票现在是 T+1，也就是成交日后一个工作日完成。"只计入已结算资金"（good funds）的做法，是只把真正到账的钱算作可用。结算属于后台，对账不平就要查是哪一笔没有对上。

**对数据工程师意味着什么。**
- **口径统一：** 同一笔成本在研究、风控、对账里要用同一个定义，否则各方的数对不上。
- **对账是日常：** 后台数据处理要求每一笔都能核对，不匹配的要标记保留，不能静默丢弃。

**英文答法。**
- "**10 bps** is 0.10 percent; I'd always judge a strategy **net of costs**."
- "**Settlement** is when cash and securities actually change hands, typically T plus one."
