---
id: leetcode-c-endlesscheng-txls3i-finite-state-machine-dp-template
node: dp-linear-knapsack.finite-state-machine-dp
type: cloze
anki: 1787272414204
tags: [concept-cloze, leetcode, recall, template]
---
原地更新股票状态前，应先保存 {{c1::旧状态}}。

```
def solve(prices):
    cash = 0
    hold = float('-inf')
    for price in prices:
        old_cash = cash
        cash = max(cash, hold + price)
        hold = max(hold, old_cash - price)
    return cash
```

**Evidence**

§6.1 买卖股票

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.09%20-%20%E7%8A%B6%E6%80%81%E6%9C%BA%20DP)
