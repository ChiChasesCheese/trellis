---
id: mlp-finance-fund-leverage
node: finance.fund
step: 4
type: qa
---
## Q
**杠杆、敞口与交易前风控检查**｜金融常识

"什么是杠杆（leverage）？什么是总敞口和净敞口？下单前为什么要做风控检查？"

## A
**杠杆** 是用借来的钱或衍生品，让持仓规模超过自有资金。杠杆放大盈利，也放大亏损。

**敞口（exposure）** 描述持仓的规模：
- **多头（long）：** 买入持有，价格涨了赚钱。
- **空头（short）：** 先借入再卖出，价格跌了赚钱。
- **总敞口（gross）：** 多头市值加上空头市值的绝对值；总敞口除以自有资金就是常说的杠杆倍数。
- **净敞口（net）：** 多头市值减去空头市值，反映组合对市场涨跌的方向性暴露。

**交易前风控检查（pre-trade risk check）** 是订单发出之前，先按限额检查持仓规模、名义金额（notional，数量乘价格）、集中度和杠杆，不通过就拒单。事后发现超限已经晚了，所以检查放在下单路径上。

**对数据工程师意味着什么。**
- **检查依赖数据：** 校验用到的当前仓位、价格和汇率，必须足够新、足够准，否则会误拒或误放。
- **汇总口径：** 总敞口和净敞口要把所有币种折成同一个基准币种，再跨 pod 汇总。

**英文答法。**
- "**Gross exposure** is longs plus absolute shorts; **net** is longs minus shorts."
- "Pre-trade checks **reject orders** that would breach position or leverage limits."
