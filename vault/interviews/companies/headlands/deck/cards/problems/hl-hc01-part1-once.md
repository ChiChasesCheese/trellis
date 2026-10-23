---
id: hl-hc01-part1-once
node: problems.hc01-stock-trading-dp
type: qa
step: 8
---
## Q
只能买卖一次的最大利润怎么从 O(n²) 暴力改进到 O(n)？写出核心代码，并说出最常见的错误写法。

## A
暴力：试遍所有（买入日 i，卖出日 j>i）取 `prices[j]-prices[i]` 最大值，至少是 0，约 n²/2 对，O(n²)；n=3 万要 186 ms，而线性版 0.018 ms（差约 1 万倍）。

改进：固定卖出日 j，最好的买入日是 j 之前**价格最低**的一天，而它随 j 后移边走边更新：
```java
long minSoFar = Long.MAX_VALUE, best = 0;
for (long p : prices) {
    if (p < minSoFar) minSoFar = p;
    else best = Math.max(best, p - minSoFar);
}
```
O(n) 时间、O(1) 空间。验算 `[7,1,5,3,6,4]`：minSoFar 依次 7,1,1,1,1,1，best 依次 0,0,4,4,5,5。

**常见错误**：写成「全局最大 − 全局最小」。最小值可能在最大值之后，`[10,9,8,1]` 答案是 0 不是 9。

另一视角：这是两状态 DP，`hold = max(hold, 0-p)`、`free = max(free, hold+p)`，且 `hold = -minSoFar`，Part 2、3、4 由它逐步扩展。
