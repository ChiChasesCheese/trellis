---
id: hl-hc01-large-k
node: problems.hc01-stock-trading-dp
type: qa
step: 11
---
## Q
最多 k 笔交易的 k 可以是 `Integer.MAX_VALUE`，怎么避免 `new long[k+1]` 爆内存？复杂度是多少？

## A
每笔交易至少占两天，n 天**最多完成 n/2 笔**。所以 `k ≥ n/2` 时限制等于没有，直接退化成 Part 2：
```java
if (k == 0 || n < 2) return 0;
if (k >= n / 2) return maxProfitUnlimited(prices);
long[] free = new long[k + 1], hold = new long[k + 1];
Arrays.fill(hold, NEG);
```
这既避免 `OutOfMemoryError`，也把 O(n·k) 降成 O(n)。`k < 0` 抛 `IllegalArgumentException`；`k == 0` 或 n < 2 返回 0。

复杂度：时间 O(n·min(k, n/2))，空间 O(min(k, n/2))。n=20 万、k=50 约 3.6 ms；n=100 万、k=2 约 1.3 ms。

边界要测：`k = 0`、`k = Integer.MAX_VALUE`、`k = 1_000_000_000`、`k = n/2` 临界。C++ 里 `k+1` 在 `k=INT_MAX` 是有符号溢出（UB），同样要先 `k >= n/2` 分流。
