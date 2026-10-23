---
id: hl-hc01-replay-checker
node: problems.hc01-stock-trading-dp
type: qa
step: 15
---
## Q
`replay` 检查器怎么用 `State` 状态机逐天回放一个方案？哪些方案算非法？为什么还要写它？

## A
```java
state = switch (moves.get(day)) {          // moves: TreeMap<Integer, Move>
    case null -> state.afterRest();
    case Buy(var d)  -> { cash = Math.subtractExact(cash, prices[d]); yield state.afterBuy(); }
    case Sell(var d) -> { cash = Math.addExact(cash, prices[d] - rules.fee()); yield state.afterSell(rules); }
};
```
`State` 三个方法：`afterRest()`：`COOL→FREE`，其余不变；`afterBuy()`：只有 `FREE` 能买→`HOLD`，否则 `IllegalStateException`；`afterSell(rules)`：只有 `HOLD` 能卖，有冷却得 `COOL`，没有得 `FREE`。外层把 `IllegalStateException` 包成 `IllegalArgumentException("illegal plan")`。

**非法方案**：笔数超过 `maxTransactions`；日期 ≥ n；同一天两个动作（含同一天卖出又买入）；重叠（持有时又买）；冷却期内买入；卖出时没持有。

**为什么写**：「验证」与「计算」分开，`plan(...).profit()` 必须等于 `replay(...)`，两者错误很难恰好抵消。`replay` 的输入是任意 `Trade` 列表，不如 DP 内循环可控，所以用 `addExact` / `subtractExact`。
