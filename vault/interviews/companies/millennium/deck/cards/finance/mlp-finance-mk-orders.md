---
id: mlp-finance-mk-orders
node: finance.markets
step: 3
type: qa
---
## Q
**订单、订单簿与买卖价差**｜金融常识

"市价单和限价单有什么区别？什么是订单簿（order book）和买卖价差（bid-ask spread）？"

## A
**订单类型。**
- **市价单（market order）：** 按当前最好的价格立刻成交，保证成交，不保证价格。
- **限价单（limit order）：** 指定最差可接受的价格，保证价格，不保证成交；没成交的就在订单簿里排队。

**订单簿** 是交易所里按价格排好的未成交限价单：买方出价从高到低（bid，买价），卖方要价从低到高（ask，卖价）。最高买价和最低卖价叫最优报价。成交就是买单和卖单的价格交叉匹配。每次成交称为一笔成交（trade 或 fill）。

**买卖价差（bid-ask spread）** 是最低卖价减最高买价。你想立刻买，就按卖价成交；想立刻卖，就按买价成交，来回一圈就付出了价差，这是交易成本的一部分。价差越窄，流动性越好。

**中间价（mid price）** 是买价和卖价的平均，常用作"当前价格"的近似。

**对数据工程师意味着什么。**
- **"价格"要问清楚是哪一个：** 最近成交价、买价、卖价还是中间价，不同口径算出的盈亏不同。
- **订单簿数据量大：** 每次报价变化都是一条更新，存储和回放要考虑规模。

**英文答法。**
- "A **limit order** guarantees the price but not the fill; a **market order** guarantees the fill."
- "The **spread** is the lowest ask minus the highest bid, and crossing it is a trading cost."
