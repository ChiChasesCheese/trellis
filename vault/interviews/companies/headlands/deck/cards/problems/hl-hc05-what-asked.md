---
id: hl-hc05-what-asked
node: problems.hc05-market-order-book
type: qa
step: 1
---
## Q
订单簿（order book）题要实现什么？四个 Part 各做什么？

## A
订单簿存放所有尚未成交的买单和卖单：买盘按价格从高到低、卖盘从低到高，同价位按先来后到排队。价格用整数 **tick**（最小报价单位），数量是整数。买盘最高价是 best bid，卖盘最低价是 best ask；买价 ≥ 最低卖价就成交。

- **Part 1 维护（不撮合）**：`add / cancel / modify / bestBid / bestAsk / depth / find / queue / size`，同价位 FIFO；
- **Part 2 撮合 + 事件**：`execute(Command) → List<Event>`，价格-时间优先；命令 `Limit / Market / Cancel / Modify`，事件 `Trade / Rested / Cancelled / Modified / Rejected`；文本接口 `parse / render / replay`；
- **Part 3 批量限价撮合**：`BatchMatcher.run(long[][] rows)`，`rows[i] = {side, price, qty}`（0=BUY，1=SELL），第 i 行 `id = i+1`，返回 `Summary(trades, filledQty, notional, bids, asks)`；
- **Part 4 性能追问**：`TickBook`，价格 `long` tick、不装箱、O(1) 按 id 撤单、稳态零分配。

考的是建模与工程判断：选对数据结构（有序 Map + 带序的队列 + id 索引）、把规则说清楚并实现一致、用 sealed 类型把结果变成穷尽的代数类型、最后回答「怎么让它更快」。

价格-时间优先（price-time priority）：价格优先，同价按到达顺序，几乎所有交易所都用。
