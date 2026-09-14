# q09 · Server Selection with switching cost：练的是"best/second-best 把 O(m) 转移压成 O(1)"

> [!tldr]
> - **本题整体是 (reconstructed)**：原始来源只有截图，唯一恢复的文字线索是"O(m²n) 朴素解 vs O(mn) 优化解"这条复杂度约束；具体的 cost/switch_cost 设定和三个 worked example 都是作者按这条线索设计并验证过的，不是逐字复原
> - 这题考的是：`n` 个时间槽依次选一个 server 激活，切换 server 要付固定代价，求最小总代价；朴素解每格扫全部 server 是 O(m²n)，用"上一格的最优/次优"两个值就能把每格转移压到 O(1)
> - 三步套路：先写 O(m²n) 朴素 DP 验证语义 → 发现"每格只需要上一格的最优和次优"→ 把转移改成 O(1)，同时维护父指针支持路径重建

## 1. 题目在说什么（人话版）
有 `m` 个 server、`n` 个按顺序处理的时间槽。`cost[j][i]` 是"槽 `i` 让 server `j` 激活"的代价；相邻两槽
如果切换了激活的 server，要多付一次固定的 `switch_cost`（槽 0 没有"上一槽"，永远不付切换费）。每槽
恰好激活一个 server，求 `n` 个槽的最小总代价。

三行小例子：
```
m=2,n=2,cost=[[1,100],[100,1]],switch_cost=1
全程留在同一 server：1+100=101（或100+1=101）
切换一次：cost[0][0]=1 + switch_cost=1 + cost[1][1]=1 = 3   <- 更优
答案：3（即使有切换代价，切换有时仍然是最优选择）
```

## 2. 读题：把文字变成模型
- **实体**：server（`m` 个）、时间槽（`n` 个，按顺序处理）、切换代价 `switch_cost`。
- **输入长什么样**：`PART <1|2>` + `m n switch_cost` + `m` 行 `cost[j]`（每行 `n` 个数）。
- **输出要什么**：Part 1 一个整数总代价；Part 2 是 `(总代价, 每槽选的 server 下标列表)`。
- **状态**：`dp[j]` = 到当前槽为止、以 server `j` 结束时的最小总代价。转移需要"上一槽所有 server 里
  的最小值"，这正是能被压缩的部分。
- **一句话建模**：这是一个 **逐槽转移、需要跨 server 取最优的 DP**，朴素做法每格扫全部 `m` 个候选前驱
  是 O(m²n)，但因为"排除自己之后的最优值"要么是全局最优（自己不是最优时），要么是全局次优（自己就是
  最优时），只需要维护最优和次优两个值就能把每格转移降到 O(1)。

> [!note] 为什么选这个数据结构
> 关键观察：server `j` 在当前槽要么"留在自己"（代价是自己上一槽的值，不付切换费），要么"从别的 server
> 切过来"（代价是"上一槽所有 server 里、排除自己之后的最小值" + `switch_cost`）。"排除自己之后的最小值"
> 只有两种可能——如果全局最优不是自己，就是全局最优；如果全局最优正是自己，就退化成全局次优。所以只要
> 每槽维护 `(最优值, 最优者是谁, 次优值)` 这三个数，就能 O(1) 算出每个 server 的转移，不需要重新扫一遍
> 全部 `m` 个候选。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `m n switch_cost` 和 `cost` 矩阵，调 `part1`/`part2`，按格式打印。
2. **Part 1 最小可用**：`dp = [cost[j][0] for j in range(m)]`；每槽对每个 `j` 扫描全部 `k`，
   `best = min(dp[k] + (0 if k==j else switch_cost) for k in range(m))`。正确优先，O(m²n)。
3. **Part 2 叠加**：每槽先算出全局最优/次优（及最优者下标），再对每个 `j` 用 O(1) 公式算出"切换过来"
   的代价，和"留在自己"比较，按 tie-break 规则（打平优先不切换，再打平选编号最小）决定 `ndp[j]` 和它
   的前驱，同时记录父指针数组用于最后回溯路径。
4. **收尾**：`n=0`（总代价 0，assignment 为空）、`m=1`（永远不能切换）、`switch_cost=0`（每槽独立选
   最小）等边界过一遍；随机小规模下 `part1(...) == part2(...)[0]` 交叉验证。

## 4. 代码怎么组织
```
part1(m, n, cost, switch_cost) -> int                    # O(m^2 n) 朴素扫描，正确性基线
part2(m, n, cost, switch_cost) -> (int, list[int])        # O(mn) 最优/次优压缩 + 路径重建
main(stdin, stdout)                                        # 解析，分发，按格式打印
```
Part 1 保留朴素实现（不是简化版的 Part 2），因为它本身就是题目要求对比的基线，也是交叉验证 Part 2
正确性的独立实现。Part 2 内部把"算最优/次优"和"决定每个 server 的转移+记父指针"分成两段，读起来更
清楚每一步在解决什么子问题。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def part1(m, n, cost, switch_cost):           # O(m^2 n)：每格扫全部候选前驱
    if n == 0:
        return 0
    dp = [cost[j][0] for j in range(m)]
    for i in range(1, n):
        dp = [cost[j][i] + min(dp[k] + (0 if k == j else switch_cost) for k in range(m))
              for j in range(m)]
    return min(dp)

def part2(m, n, cost, switch_cost):           # O(mn)：只需要上一槽的最优/次优
    if n == 0:
        return 0, []
    dp = [cost[j][0] for j in range(m)]
    parents = []
    for i in range(1, n):
        best1_val = best2_val = float("inf")
        best1_server = best2_server = -1
        for k in range(m):                     # 一遍扫描求最优/次优（及最优者是谁）
            if dp[k] < best1_val:
                best2_val, best2_server = best1_val, best1_server
                best1_val, best1_server = dp[k], k
            elif dp[k] < best2_val:
                best2_val, best2_server = dp[k], k
        ndp, preds = [0] * m, [0] * m
        for j in range(m):
            if best1_server != j:               # 自己不是最优 -> 切换用全局最优
                switch_val, switch_pred = best1_val + switch_cost, best1_server
            else:                                # 自己就是最优 -> 切换只能用次优
                switch_val, switch_pred = best2_val + switch_cost, best2_server
            stay_val = dp[j]
            if stay_val <= switch_val:           # tie-break：打平优先不切换
                ndp[j], preds[j] = cost[j][i] + stay_val, j
            else:
                ndp[j], preds[j] = cost[j][i] + switch_val, switch_pred
        dp, parents = ndp, parents + [preds]
    total = min(dp)
    last = min(range(m), key=lambda k: dp[k])    # tie-break：打平选编号最小
    assignment = [last]
    for preds in reversed(parents):
        last = preds[last]
        assignment.append(last)
    assignment.reverse()
    return total, assignment
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认切换代价的语义：槽 0 永远免切换费，之后每次相邻槽激活的 server 变化就付一次固定
  代价；我先写朴素 O(m²n) 保证语义对，再优化。」
- 写 Part 1 时：「每格对每个候选 server，我扫描上一槽所有 server 的代价，加上是否切换的代价，取最小，
  这是最直接但 O(m) 每格的做法。」
- 写 Part 2 时：「关键观察是：排除自己之后的最优值只有两种可能——不是自己就是全局最优，是自己就退化
  成全局次优——所以我只需要维护最优和次优两个值，把每格的转移从 O(m) 降到 O(1)。」
- 如果面试官问 tie-break：「我按题面约定，代价打平时优先不切换（减少不必要的状态变化），再打平就选
  编号最小的 server，保证输出确定性。」
- 交付时：「小规模随机交叉验证 `part1==part2[0]` 全部一致；Part 2 在 m=n=1000（约 1e6 格）上做了性能
  测试，远低于 2 秒预算，Part 1 只在小规模上验证正确性，没有跑满 1000x1000 的 perf（O(m²n) 在这个
  规模下不现实，这一点在 REPORT 里诚实说明）。」

## 7. 常见跑偏（方法层面，3 条）
- **只维护"全局最优"而忘记维护"次优"**：当某个 server `j` 自己就是上一槽的全局最优时，它切换到别的
  server 的代价不能再用"全局最优"（那是它自己），必须退化成次优，漏掉这一步会让 `j` 的转移算错。
- **tie-break 顺序搞反**：题目要求"打平优先不切换"，如果写成"打平优先切换"，assignment 会和样例的
  具体路径对不上，即使总代价数字是对的。
- **忘记记录父指针就想重建路径**：Part 2 必须在每一步转移时记下"这个 server 的最优前驱是谁"，事后
  没法从 `dp` 数组反推出具体路径。

## 8. 同族题 / 延伸
- "best/second-best 压缩转移"是一个通用的 DP 优化模式，凡是"排除自己求最优"的场景都能用（比如
  "除自己以外数组最大值"类问题）。
- 延伸思考：如果 `switch_cost` 因 server 对而异（矩阵而非常数），这个 O(1) 压缩技巧会失效，需要
  换一种优化方向（比如按结构分组或接受更高复杂度）。
- 练习命令：`python3 loop/mock.py start q09`
