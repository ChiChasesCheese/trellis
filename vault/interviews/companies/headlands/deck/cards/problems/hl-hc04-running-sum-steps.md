---
id: hl-hc04-running-sum-steps
node: problems.hc04-queue-mean-snapshot
type: qa
step: 2
---
## Q
队列均值从最笨解法到最终方案的改进链是什么？朴素版慢在哪、错在哪？

## A
**最笨**：`ArrayDeque<Long>`，`getMean` 每次遍历求和。`push/pop` O(1)，`getMean` O(n)。队列长 2 万、20 万次 push、约 10 万次 `getMean`，约 20 亿次加法，实测 **2604 ms**；改进后的 `QueueMean` 同序列只要 **3 ms**。

**改进链**：
1. **维护总和**：`push` 时 `sum += x; size++`，`pop` 时 `sum -= x; size--`，`getMean = sum / size`，全 O(1)；新问题：`sum` 若是 `double` 会漂移。
2. **总和用整数**：整数加减精确；新问题：`long` 溢出，`push(MAX), push(MAX)` 后 `sum = -2`。
3. **128 位总和**：两个 `long`（`hi`、`lo`）拼成。
4. **`ArrayDeque<Long>` 换 `long[]` 环形缓冲**：避免装箱、指针追逐、GC 压力。
5. **返回精确均值**：约分分数 `record Mean(BigInteger numerator, long denominator)`，另给最接近的 `double`。

不写 `Math.addExact`：题目要的是「算对」，不是「报错」。累加器一旦转成 `BigInteger` 就不再转回的实现，性能会塌；128 位没有这个问题。
