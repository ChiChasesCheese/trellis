---
id: hl-hc05-batch-matcher
node: problems.hc05-market-order-book
type: qa
step: 11
---
## Q
批量撮合 `BatchMatcher.run` 的校验、汇总和溢出处理怎么做？用样例说明。

## A
`rows[i] = {side, price, qty}`，`side`：0=BUY，1=SELL；第 i 行 `id = i + 1`。步骤：**先整体校验**行（长度 ≠ 3、`side ∉ {0,1}`、`price ≤ 0`、`qty ≤ 0` → `IllegalArgumentException`，信息以 `row i`（i 从 0 起）开头；`rows == null` → NPE），再转成 `Limit` 命令复用 Part 2 的 `OrderBook.executeAll`，最后从事件流里挑出 `Trade`。

```java
List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
    if (e instanceof OrderBook.Trade t) sink.accept(t);
}).toList();
```
`mapMulti` 对每元素输出 0 个或多个结果，相当于 filter + 强转一步。

`Summary(trades, filledQty, notional, bids, asks)`：`filledQty` 成交总量（每笔只算一次）；`notional = Σ price × qty`，用 `multiplyExact` / `addExact`——价格 4×10⁹ × 数量 3×10⁹ = 1.2×10¹⁹ 超过 `long` 上限 9.22×10¹⁸，普通乘法会给出看似正常的错数，溢出抛 `ArithmeticException`；`bids / asks` 是最终盘口，全部档位，最优在前。

样例：`{{0,100,5},{1,99,3},{1,100,4},{0,101,10}}` → 成交 `(2,1,SELL,100,3)`、`(3,1,SELL,100,2)`、`(4,3,BUY,100,2)`；`filledQty = 7`，`notional = 700`；`bids = [Level(101, 8, 1)]`，`asks = []`。

20 万行约 65–85 ms。
