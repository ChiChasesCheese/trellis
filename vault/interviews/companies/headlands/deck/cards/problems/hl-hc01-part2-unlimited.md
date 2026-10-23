---
id: hl-hc01-part2-unlimited
node: problems.hc01-stock-trading-dp
type: qa
step: 9
---
## Q
股票次数不限（LC 122）的通用状态机转移是什么？为什么又能化简成「所有正差之和」？这个化简何时失效？

## A
把 Part 1 里买入的现金 0 换成现在的 `free`：
```
hold' = max(hold, free - p)   // 休息 或 今天买
free' = max(free, hold + p)   // 休息 或 今天卖
```
初始 `free=0`，`hold=-∞`；答案 `free`。`[7,1,5,3,6,4]` 的 free 依次 0,0,4,4,7,7。

**化简**：答案 = 所有「今天比昨天贵」的差之和。证明：方案 = 每个相邻日对持有或不持有，持有的赚 `prices[i]-prices[i-1]`（可能为负）。**上界**：所赚不超过所有正差之和；**可达**：只持有正差日对即可（连续正差合并成一笔，买最低点卖最高点）。
```java
for (int i = 1; i < n; i++) if (prices[i] > prices[i-1]) sum += prices[i] - prices[i-1];
```
这个贪心只在**次数不限、无冷却、无手续费**时成立；有任何限制必须回到状态机。面试两种都讲：先通用状态机，再说可化简并给证明。
