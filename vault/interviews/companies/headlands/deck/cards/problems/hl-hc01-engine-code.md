---
id: hl-hc01-engine-code
node: problems.hc01-stock-trading-dp
type: qa
step: 13
---
## Q
Part 4 里 `maxProfit` 和 `plan` 共用的引擎 `run` 怎么写？为什么开头要把旧值存进局部变量？

## A
```java
for (int j = bound; j >= 0; j--) {
    int src = unbounded ? j : j - 1;
    long oldHold = hold[j], oldFree = free[j], oldCool = cool[j];
    long buy  = src >= 0 ? free[src] - p : NEG;
    long sell = oldHold + p - fee;
    int bits = 0;
    if (buy > oldHold) { hold[j] = buy; bits |= 1; } else hold[j] = oldHold;
    if (rules.cooldown()) {
        cool[j] = sell;
        if (oldCool > oldFree) { free[j] = oldCool; bits |= 2; } else free[j] = oldFree;
    } else {
        if (sell > oldFree) { free[j] = sell; bits |= 2; } else free[j] = oldFree;
    }
    if (how != null) how[i * w + j] = (byte) bits;
}
```
要点：
- 开头保存 `oldHold / oldFree / oldCool`，之后无论先写谁，其他转移用的都是昨天的值。
- `unbounded`（`maxTransactions ≥ n/2`）时 j 这一维压成 1 格，买入读同格 `free[j]`。
- 严格 `>`：平局选休息，避免净利润为 0 的废交易。
- `how == null` 时不记录，所以 `maxProfit`（传 null）和 `plan`（传数组）共用同一引擎，答案必然一致。
- 终点：没股票的两种情形（`free` 与 `cool`）取现金多的，不会停在 `HOLD`。
