---
id: hl-ld02-trading-basics
node: problems.ld02-trading-ood
type: qa
step: 2
---
## Q
限价单、tick、成交（fill）、仓位、已实现 / 未实现盈亏分别是什么？多头和空头的盈亏怎么统一计算？

## A
- **限价单**（limit order）：带方向（BUY / SELL）、数量、限价（买单「最高出这个价」，卖单「最低收这个价」）；成交价可以比限价**更好**，不能更差。
- **tick**：价格最小变动单位，价格存成整数个 tick（AAPL 150.25 美元、tick 0.01 美元 → 15,025）。
- **成交**（fill）：订单的一部分或全部被对手方接走；一张订单可分多次成交（部分成交）。
- **仓位**（position）：净持有数量，买入为正（**多头 long**），卖空为负（**空头 short**）。
- **已实现盈亏**（realized PnL）：已平掉部分赚了多少；**未实现盈亏**：没平部分按当前市价（mark price）估算。

统一：`盈亏 = 方向 × (现价 − 开仓价) × 数量`，多头 +1、空头 −1（`Side.sign()`：BUY=+1，SELL=−1）。例：多头买 10 股@100，市价 120 → 未实现 +200；空头卖 10 股@100，市价 120 → −200（价格涨了空头亏）。`Position.unrealizedPnl(markPx)`：多头 `netQty*mark − openCost`，空头 `openCost − |netQty|*mark`，flat → 0。

**为什么不用 `double` 表示钱**：`0.1 + 0.2 = 0.30000000000000004`，几十万笔成交每笔带点误差就对不上；更要命的是重放——运算顺序不同得到不同 `double`，两次结果不逐位相等，事件溯源的核心保证就破了。整数加减乘精确且满足结合律。

**溢出**：`long` 范围 ±9.22×10¹⁸，`px × qty` 超过时 Java 默默回绕成负数；`Math.addExact(big, 1)` 抛 `ArithmeticException`。风控里特别危险：名义金额溢出成负数的订单会「小于上限」被放行。所以用 `multiplyExact/addExact`，溢出在风控里当拒绝。

手算：风控单笔最多 1000 股、仓位最多 3000，参考价 100。#1 买 100@100 通过，PENDING；Ack → WORKING；`Fill(#1, exec 10, 60, 99)` → PARTIALLY_FILLED，仓位多 60、成本 5940；`Fill(exec 11, 40, 100)` → FILLED，仓位 100、成本 9940；#2 卖 100 限价 101，Ack，`Fill(exec 12, 100, 105)`：FIFO 先平 60@99 赚 360，再平 40@100 赚 200，已实现 560，仓位回 0；#3 买 5000 → QTY_LIMIT，REJECTED。
