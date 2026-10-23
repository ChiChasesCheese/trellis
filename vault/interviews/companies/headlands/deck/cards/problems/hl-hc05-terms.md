---
id: hl-hc05-terms
node: problems.hc05-market-order-book
type: qa
step: 2
---
## Q
订单簿的核心术语：tick、maker / taker、限价单、市价单、成交价、深度各是什么意思？

## A
- **tick**：最小报价单位，用整数 tick 表示价格（「10050」= 100.50 元），不用小数。
- **maker / taker**：maker 是已挂在簿上的单（被动方），taker 是新来主动去吃的单。
- **限价单**（limit）：带价格上限（买）/ 下限（卖），吃不完的部分挂簿。
- **市价单**（market）：不限价，有多少对手盘吃多少；约定吃不完的部分**作废**（IOC，立即成交否则取消）。
- **成交价**取 **maker 的价**：maker 报的是「愿意的最差价」，taker 的限价只是上限，取 maker 价让 taker 有价格改善。
- **深度**（depth）：买盘 / 卖盘各档价位上的总量，从最优价往外数 N 档；`Level(price, totalQty, orderCount)`。
- **价位**（price level）：同一价格上的所有订单；买卖盘之间的缝隙叫 spread。
- best bid < best ask 时没人能成交；`add` 不撮合时簿可以「交叉」。

**为什么价格不用 `double`**：`0.1 + 0.2 != 0.3`，二进制浮点存不准十进制小数，两个本该相等的价格会比出「不等」，订单挂在两个看起来一样的价位上，比较还要处理 epsilon。整数 tick 精确、可比较、可当数组下标。数量同理，累加用 `addExact`。
