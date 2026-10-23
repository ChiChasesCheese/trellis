---
id: hl-hc01-dp-fib-ladder
node: problems.hc01-stock-trading-dp
type: qa
step: 3
---
## Q
动态规划（dynamic programming, DP）是什么？用斐波那契说明朴素递归、记忆化、自底向上表、滚动数组四步演进。

## A
DP = 把大问题拆成一串小问题，小问题答案存起来反复用，不重复算。

斐波那契 `fib(n) = fib(n-1) + fib(n-2)`：
- 朴素递归：`fib(3)` 被反复重算，`fib(40)` 约 3.3 亿次调用，`fib(50)` 约 400 亿次——病根是**重叠子问题**。
- 记忆化（memoization）：算过的存进 `memo[]`，每个 `fib(i)` 只算一次，O(n)。
- 自底向上表（tabulation）：`f[1]=1; for i: f[i]=f[i-1]+f[i-2]`，不用递归。
- 滚动数组（rolling array）：只依赖前两项，留两个变量，空间 O(n)→O(1)。

```java
long a = 0, b = 1;
for (int i = 2; i <= n; i++) { long c = a + b; a = b; b = c; }
```
DP 的形状：找小问题 → 写**转移**（小问题间的关系）→ 定起点 → 按依赖顺序填 → 答案是某一格。相关术语：**最优子结构**（大问题最优解由小问题最优解拼成）。别的题里「小问题」和「关系」要自己发明。
