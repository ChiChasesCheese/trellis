# q21 · Maximum Profit Query Selection：练的是"收益率最高不等于全局最优"

> [!tldr]
> - TrueInterview 同步清单 #54（2026-01 报告，GitHub 镜像转述）；**Part 2（预算拆给两种类型）整体是 (reconstructed)**
> - 这题考的是：预算内反复跑一种查询类型求最大利润，以及"预算能不能拆给两种类型"的陷阱
> - 三步套路：Part 1 直接算 `floor(k/d)*r` 取最大 → 构造反例证明"单选"不总最优 → Part 2 对每对类型做无界背包
> - 最值得带走的一个模式：**"只挑收益率最高的选项"不是正确贪心——收益率高但用不满预算会浪费余量，往往不如换一种搭配把预算用满**

## 1. 题目在说什么（人话版）

有 `n` 种查询类型，第 `i` 种每跑一次要花 `durations[i]` 时间、赚 `revenues[i]`。给定总时间
预算 `k`，只能选**一种**类型反复跑，跑 `floor(k / durations[i])` 次，求最大利润。

```
durations=[3,4], revenues=[4,5], k=7
只跑时长3的类型：floor(7/3)*4 = 8
只跑时长4的类型：floor(7/4)*5 = 5
答案：8
```

## 2. 读题：把文字变成模型

- **实体**：`n` 种查询类型，每种有 `(duration, revenue)`；一个共享的预算 `k`。
- **输出**：一个整数——最大利润。
- **状态**：Part 1 不需要维护状态，逐类型算完取最大值即可。
- **一句话建模**：Part 1 是 **"每种类型独立算一次收益，取最大值"**；Part 2 是 **"两种类型共享同一预算的无界背包"**。

> [!note] 为什么 Part 2 要用背包而不是继续贪心
> 直觉上会觉得"挑收益率 `revenue/duration` 最高的类型多跑几次"就是最优解。但收益率高的
> 类型如果 `duration` 较大，在固定预算 `k` 下容易"用不满"（有余量被浪费）；换成收益率
> 稍低但更容易和另一种类型拼满预算的组合，反而能拿到更高利润。这跟单纯"贪心排序"不是
> 一回事，是"恰好两种物品、数量不限"的无界背包问题。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **Part 1 最小可用**：`max((k // d) * r for d, r in zip(durations, revenues))`，一行公式，先用样例过一遍。
2. **举反例引出 Part 2**：口头给出 `durations=[3,4], revenues=[4,5], k=7` 这个反例，说明混着跑（`9`）严格优于单选（`8`）。
3. **Part 2 叠加**：对每一对类型 `(i, j)` 做一次容量为 `k` 的无界背包 DP，取所有 pair 的最优值，再跟 Part 1 的单类型最优比较取大（混着跑不一定更优）。
4. **收尾**：`k=0`、只有一种类型（Part 2 应退化为 Part 1）、`revenue=0` 的类型不能干扰其余计算。

## 4. 代码怎么组织

```
_validate(durations, revenues, k)
max_profit_single(durations, revenues, k)              # Part 1
_best_two_item_knapsack(d1, r1, d2, r2, k) -> int       # 两个"物品"任意非负组合的最大值
max_profit_two_types(durations, revenues, k)            # Part 2：枚举 pair 调用上面的 helper
part1 / part2
```
`_best_two_item_knapsack` 被 Part 2 对每一对类型复用；Part 2 本身还要跟 Part 1 的结果比较
取大，因为混着跑不一定比单选好。

## 5. 核心代码骨架

```python
def max_profit_single(durations, revenues, k):
    # Part 1：每种类型独立算一次，取最大值
    return max((k // d) * r for d, r in zip(durations, revenues))

def _best_two_item_knapsack(d1, r1, d2, r2, k):
    # 容量 k 的无界背包：两个"物品"任意非负组合的最大收益
    dp = [0] * (k + 1)
    for d, r in ((d1, r1), (d2, r2)):
        for c in range(d, k + 1):
            v = dp[c - d] + r
            if v > dp[c]:
                dp[c] = v
    return dp[k]

def max_profit_two_types(durations, revenues, k):
    # Part 2：枚举所有类型对，取跟 Part 1 比较后的最大值
    n = len(durations)
    best = max_profit_single(durations, revenues, k)
    for i in range(n):
        for j in range(i + 1, n):
            combo = _best_two_item_knapsack(
                durations[i], revenues[i], durations[j], revenues[j], k
            )
            best = max(best, combo)
    return best
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「Part 1 我先确认预算耗尽的定义是 `floor(k/duration)` 次，对吗？」
- 写 Part 1 时：「这个是 O(n)，对每种类型独立算，不需要排序。」
- 引出 Part 2 时：「如果预算能拆给两种类型，只挑收益率最高的不一定对——我举个反例……所以这是一个恰好两种物品的无界背包。」
- 交付时：「样例过了；这个复杂度是 `O(n²k)`，题面把规模限制得很小就是为了让这个复杂度可行。」

## 7. 常见跑偏（方法层面，3 条）

- 直接假设"贪心选收益率最高的类型"就是 Part 2 的答案，没有先构造反例验证。
- 忘了 Part 2 的答案要跟 Part 1 比较取大（有些输入下混着跑并不比单选好）。
- 背包 DP 写成 0/1 背包（每个物品只能选一次）而不是无界背包（每种类型可以跑任意次）。

## 8. 同族题 / 延伸

- 同一类"局部最优单选 ≠ 全局最优"的教学点：`q19`（翻倍哪个元素）、`q20`（多重集合覆盖 vs 子序列匹配的正确性论证）。
- 练习命令：`python3 drill.py start q21`
