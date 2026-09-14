# 02 · DP 模式识别 + 状态设计

> 面向 OA（q02 q04 q05 q09）与电面（q01 的 DP 部分）。每种模式：**一眼信号 → 状态定义 → 转移 → 复杂度 → 本 kit 哪题**。
> 代码引用自 `../../problems/q*/solution.py`（可直接打开对照）。先看 `01-solving-framework.md` §3 的 120 min OA 框架，再看这份文件的算法细节。

---

## 0. 四问法（面试时说出来，任何 DP 题通用）

1. **状态**是什么？（`dp[i]` / `dp[i][j]` 表示什么，一句话）
2. **转移**是什么？
3. **初值**是什么？
4. **答案**在哪个格子？

下面五节按"计数 DP → 区间/调度 DP → 2D DP → 取模与状态压缩 → 对比：不是 DP 的计数题"排列，最后一节故意放一道**看着像 DP、其实不是**的题（q05），因为**分不清"计数"和"计数 DP"是电面最容易丢分的地方**。

---

## 1. 计数 DP：状态 = (位置, 附加约束的游程/剩余量)

**一眼信号**：「长度为 n 的字符串/序列有多少种」「连续 XX 不超过 k」「方案数取模」。

**状态定义**：`dp[j]` = 处理完前 i 个字符后，当前"违反约束的游程"长度恰好为 j 的方案数。**j 的上界就是约束本身**（这里是 k），不是 n。

**转移**（`q02` `_count_strings`）：
```python
cap = min(k, n)
dp = [0] * (cap + 1)
dp[0] = 1                          # 空串：游程长度 0
for _ in range(n):
    total = sum(dp)
    for j in range(cap, 0, -1):    # 从高位往低位移，避免覆盖 dp[j-1]
        dp[j] = dp[j - 1] * 5 % MOD    # 接一个"违反类"字符（这里是元音）
    dp[0] = total * 21 % MOD           # 接一个"安全类"字符（消费币，游程归零）
answer = sum(dp) % MOD
```

**复杂度**：O(n · min(k, n)) 时间，O(min(k, n)) 空间——**状态数被约束本身封顶**，不是被 n 封顶，这是计数 DP 与普通"逐位递推"的关键区别。

**本 kit**：`q02`（元音游程：part1 无模数、part2 mod 1e9+7 且 n ≤ 2500、part3 是相关但不同的"子串计数"问题，不要混）。

**最易错**：
- 从高位往低位移状态数组（`range(cap, 0, -1)`），否则会用本轮已更新的 `dp[j-1]` 覆盖上一轮的值。
- `dp[0]` 的桶含义是"空串"或"以安全字符结尾"，**两者要合并成一个桶**，不要拆成两个状态。
- 上界是 `min(k, n)` 不是 `k`——n 很小时不需要开到 k 那么大的数组。

---

## 2. 区间/调度 DP：排序 + 前驱查找

**一眼信号**：「不重叠的区间/通话/会议」「选一个子集使总权重最大」「加权区间调度」（区别于纯贪心的"最多能选几个不重叠区间"——这里权重不同，贪心不再对，需要 DP）。

**状态定义**：按结束时间排序后，`dp[i]` = 只考虑前 i 个（排序后）区间时的最大权重和。

**转移**（`q04` weighted interval scheduling）：
```python
ends, starts, vols = sorted_by_end(...)          # 按 (end, start) 排序
dp = [0] * (n + 1)
for i in range(1, n + 1):
    pred = bisect_right(ends, starts[i - 1], 0, i - 1)   # 最晚的不冲突前驱
    dp[i] = max(dp[i - 1], vols[i - 1] + dp[pred])        # 不选 i / 选 i
```

**复杂度**：排序 O(n log n) + 每步二分 O(log n) = **O(n log n)**（`q04` part1 是线性扫前驱的 O(n²) 保底版，part2 才是 bisect 版）。

**本 kit**：`q04`（Maximum Order Volume，LC 1235 型）。**零长度区间是隐藏陷阱**：`[start, start)` 是空区间，与任何区间都不冲突（包括"包住"它的区间），必须在做 DP 前单独摘出来累加，不能套用"end <= start"的普通判定（`q04` 的 `_split_free_and_normal`）。

**最易错**：
- 排序键必须是 `(end, start)`，只按 end 排会在 end 相同时行为未定义。
- `bisect_right` 查的是"`ends[0:i-1]` 中 `<= starts[i-1]` 的个数"，这个个数**恰好等于**合法前驱在 `dp` 数组里的下标（因为 `dp` 比 `ends`/`starts` 多一个前导的"0 个区间"状态）。
- 别忘了 `dp[i] = max(dp[i-1], ...)`——"不选当前区间"永远是一个候选转移。

**q01 也是调度 DP，但状态形状不同**：`q01`（paid/free server）的状态是 `(task index, 付费机 free_at)`，转移分"强制上付费机"和"二选一（走免费机 / 排队付费机）"两支。它属于"取模与状态压缩"一节讨论的**前沿压缩（Pareto frontier）**技巧，因为朴素状态数会爆炸——细节见第 4 节。

---

## 3. 2D DP：显式二维状态 + 常数优化

**一眼信号**：「m 个服务器/资源 × n 个时间槽/任务」「每步的转移要看上一步所有其他选择里的最优」。

**状态定义**：`dp[i][j]` = 处理完前 i 个时间槽、当前选择第 j 个服务器时的最小总成本。

**转移（朴素 O(m²n)）**（`q09` part1）：
```python
dp = [cost[j][0] for j in range(m)]
for i in range(1, n):
    ndp = [0] * m
    for j in range(m):
        best = min(dp[k] + (0 if k == j else switch_cost) for k in range(m))
        ndp[j] = cost[j][i] + best
    dp = ndp
```

**常数优化到 O(mn)**：转移只关心"上一步所有 j 里的最优值"和"次优值"（因为切换代价对所有 `k != j` 都一样，唯一需要区分的是"最优是不是恰好等于自己"）。维护 `(best1, best1_server, best2, best2_server)`，每个 `j` 的转移就从 O(m) 降到 O(1)：

```python
best1_val, best1_server = min((dp[k], k) for k in range(m))   # 概念上；实际一遍扫描维护
for j in range(m):
    prev_best = best2_val if j == best1_server else best1_val  # 排除自己那一路
    ndp[j] = cost[j][i] + prev_best + (0 if <no switch happened> else switch_cost)
```

**复杂度**：O(mn) 时间，O(m) 空间。**这是"2D DP 的常数优化"模式的典型代表**：状态还是 O(mn) 个，但每个状态的转移从 O(m) 压到 O(1)，靠的是"只有当前最优恰好是自己时才需要退而求其次"这个观察——本质上和滑窗最大值维护单调队列是同一类"缓存 top-2"技巧。

**本 kit**：`q09`（Server Selection，题面 image-only、置信度 MED，但算法很典型）。

**最易错**：
- tie-break 顺序：先"倾向不切换（stay）"再"更小服务器 index"——两条规则都要在维护 best1/best2 时体现，不是事后补。
- `switch_cost` 只有当 `k != j` 才计入，第一个时间槽永远不计切换代价。

---

## 4. 取模与状态压缩：Pareto frontier 剪枝

**一眼信号**：「朴素 DP 的状态数会随输入无界增长，但真正有用的状态其实很少」——这不是标准模板能背出来的模式，而是**发现状态之间存在支配关系**之后做的剪枝。

**q01 的状态爆炸问题**：朴素地把 `(task index, free_at)` 都当状态存，`free_at` 的取值范围没有自然上界（它由历史选择累加而成），对抗性输入下状态数不可控。

**关键洞察（支配关系）**：更大的 `free_at`（更"忙"）永远不会让未来变差——你随时可以选择"排队付费机"让自己变得更忙，模拟一个更小 `free_at` 状态被迫经历的强制付费。所以：**`free_at` 更大且花费更低或相等的状态，支配 `free_at` 更小且花费更高的状态**，可以丢弃后者。

```python
frontier: dict[int, int] = {0: 0}          # free_at -> 达到它的最小花费
for i in range(n):
    # ...按 free_at <= i（强制上付费机）和 > i（可二选一）分流，产生新候选状态...
    items = sorted(new_frontier.items(), key=lambda kv: -kv[0])   # free_at 降序
    pruned, best = {}, None
    for fa, c in items:
        if best is None or c < best:        # 只留下"比所有更大 free_at 都更便宜"的状态
            pruned[fa] = c
            best = c
    frontier = pruned
```

**复杂度**：经验上前沿大小保持有界（不是理论最坏情况的证明，而是"面试里先写 O(states) 正确版，再讲这个剪枝方向"的加分项）——**这也是 `01-solving-framework.md` §1 步骤 6 的"先写正确的暴力版，再谈优化"的直接应用**。

**本 kit**：`q01`（part1 是无剪枝的记忆化递归，仅作对拍；part2 才是前沿压缩版）。

**取模的两条纪律**（`q02` part2）：所有累加处 `% MOD`；**排序/比较大小绝不在取模后的值上做**（取模会破坏大小关系）——`q01` 的 Pareto 比较用的是真实花费，不涉及取模,这两个技巧不要混用到同一个状态里。

---

## 5. 对比：q05 是计数题，但不是 DP

**一眼信号容易被误判成 DP**：「生成 n 个数，数满足某条件的 pair 数量」——听起来像"计数 DP"，但**没有需要递推的状态**，本质是排序后双指针/二分计数。

**q05 Paint the Ceiling**：生成 n 个边长后，数满足 `sides[i] * sides[j] <= a` 的有序对 `(i, j)`（`i == j` 合法）。

```python
sides.sort()
total = 0
for x in sides:
    total += bisect_right(sides, a // x)     # 满足 x*y <= a 的 y 的个数
```

**复杂度**：排序 O(n log n) + 每个元素一次二分 = O(n log n)，n 可达 ~1e6。

**为什么不是 DP**：每个 `(i, j)` 的判定只依赖 `sides[i]` 和 `sides[j]` 两个值本身，不依赖"处理到第几个"这种顺序状态——**没有子问题重叠**，排序后二分/双指针就是最优解，套 DP 反而是过度设计。

**判定口诀**：看到"计数"先别急着想 DP——**先问有没有天然的顺序状态**（游程长度、背包容量、位置）。如果限制条件是"两两之间的某个可比较关系"而不是"沿着一个序列累积的状态"，大概率是排序 + 双指针/二分，不是 DP。

**本 kit**：`q05` 作为反例放在这里，就是要在电面里省下"想 DP 想了 5 分钟才发现不需要"的时间。
