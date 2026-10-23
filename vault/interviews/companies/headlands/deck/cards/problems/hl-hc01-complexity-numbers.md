---
id: hl-hc01-complexity-numbers
node: problems.hc01-stock-trading-dp
type: qa
step: 18
---
## Q
买卖股票各个 Part 的时间、空间复杂度和实测量级是多少？真正会超时的写法有哪些？

## A
n = 天数，k = 笔数上限，K = min(k, n/2)：
- `maxProfitBrute`：O(n²) 时间、O(1) 空间；n=3,000 约 2.0 ms，n=30,000 约 **186 ms**。
- `maxProfitOnce`：O(n)、O(1)；n=30,000 约 **0.018 ms**，n=100 万约 0.6 ms。暴力对线性差约 1 万倍。
- `maxProfitUnlimited`：O(n)、O(1)；n=100 万约 2.1 ms。
- `maxProfitAtMost`：O(n·K) 时间，O(K) 空间；n=20 万、k=50 约 3.6 ms。
- `maxProfit`（冷却 + 手续费、不限次数）：O(n)；n=100 万约 3.4 ms。
- `plan`：O(n·K) 时间、O(n·K) 字节决策表；n=10 万、冷却 + 手续费约 0.8 ms。

参考解离 2 秒预算有三个数量级余量。真正会超时的是：暴力 O(n²)、对大 k 做 O(n·k)、每天 `new` 数组的写法。

更优渐近：O(nk) 有 O(n log n) 解法（拆成波谷-波峰段，利用边际收益递减 / 凹性，用堆合并），知道方向即可，通常不要求写出。
