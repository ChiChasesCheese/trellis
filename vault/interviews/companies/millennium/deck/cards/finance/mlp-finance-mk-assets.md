---
id: mlp-finance-mk-assets
node: finance.markets
step: 1
type: qa
---
## Q
**资产类别与代码**｜金融常识

"基金交易哪些资产？股票、债券、外汇各是什么？一个 symbol 代表什么？"

## A
**主要资产类别。**
- **股票（equity）：** 公司的所有权份额，在交易所挂牌交易。
- **固定收益（fixed income，利率产品）：** 债券等，按约定付息还本，价格对利率敏感。
- **外汇（FX）：** 一种货币兑另一种货币的汇率，货币对写成 `EURUSD`，表示 1 欧元等于多少美元。
- **商品（commodity）：** 原油、黄金等。
- **期货与期权（derivatives，衍生品）：** 价格由标的资产派生的合约，期货约定未来某日按约定价买卖，期权是买卖的权利。

大基金通常按资产类别分交易台（desk），例如股票台、利率台、外汇台。

**symbol 与币种。** symbol（代码，如股票的 ticker）标识一个可交易的产品；每个产品有自己的计价币种。同一家公司在不同交易所上市，代码和币种可能不同；代码还会改名，所以要靠参考数据（见下一部分）稳定地识别它。

**对数据工程师意味着什么。**
- **不同资产数据形状不同：** 股票有成交和报价，外汇没有统一的中央交易所，债券的价格常常是报价而不是连续成交。
- **多币种是常态：** 不同产品用不同币种计价，汇总前要换成同一个基准币种。

**英文答法。**
- "Desks are split by **asset class**: equities, rates, FX, and so on."
- "Every instrument has its own **quote currency**, so we convert to a base currency before aggregating."
