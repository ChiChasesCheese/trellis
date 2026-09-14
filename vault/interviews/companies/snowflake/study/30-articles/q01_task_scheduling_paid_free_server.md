# q01 · Task Scheduling：一台付费机一台免费机，练的是"贪心直觉会骗你"的状态 DP

> [!tldr]
> - 这题考的是：任务按顺序到达，付费机空闲时必须接客、忙碌时可以"白嫖"免费机或排队；求最小总成本
> - 三步套路：把"付费机何时空闲"抽成状态 `free_at` → Part 1 写记忆化搜索把模型跑对 → Part 2 把状态集合压成一个 Pareto 前沿
> - 最值得带走的一个模式：**贪心会在这题上出错**——"能白嫖就白嫖"在某些输入下比"多花一点排队"更贵，必须让 DP 去比较两条路

## 1. 题目在说什么（人话版）
任务按下标顺序、逐个到达，第 `i` 个任务在"时间 `i`"到达。有一台付费机，同一时刻只能处理一个任务；
有一台免费机，处理任何任务永远只花 1 单位时间、不要钱。如果任务到达时付费机正好空闲，**必须**上付费机
（没得选）；如果付费机还在忙（有积压），**可以选**：白嫖免费机，或者排队等付费机。求把所有任务处理完的
最小总成本。

三行小例子（`cost=[1,1,1000], time=[2,1,1]`）：
```
任务0到达，付费机空闲 -> 强制付费，花 1，付费机要忙到 t=2
任务1到达(t=1)，付费机还忙(free_at=2>1) -> 有选择：免费机(省钱但会让任务2被迫强制付费+1000) / 排队(+1，但把 free_at 推到 3，任务2就能安全白嫖)
答案是 2（排队更划算），不是"能白嫖就白嫖"算出来的 1001
```

## 2. 读题：把文字变成模型
- **实体**：任务（`cost[i]`、`time[i]`）、付费机的"空闲时刻" `free_at`。没有真正的免费机状态——它永远瞬间可用。
- **输入长什么样**：`PART <1|2>` + `n` + `cost` 数组 + `time` 数组，`n` 最大 `1e5`，数值到 `1e9`，必须精确整数。
- **输出要什么**：一个整数，最小总成本。
- **状态**：处理到第 `i` 个任务时，唯一需要记住的是"付费机什么时候空闲"（`free_at`），因为它决定了下一个任务是被强制还是有选择。
- **一句话建模**：这是一个 **沿任务下标推进、状态是"付费机空闲时刻"的最短路/DP 问题**，Part 1 状态空间原样搜，Part 2 把状态集合压成一个按 Pareto 支配关系剪枝的前沿。

> [!note] 为什么选这个数据结构
> 候选方案是"纯贪心：忙的时候能白嫖就白嫖"，但 worked example 4 直接举出反例——排队反而更便宜，因为它把
> `free_at` 推得更远，让后面某个天价任务不再被强制付费。贪心行不通，只能把"两种选择各自的后续成本"都算出来
> 再比较，这就是 DP。Part 1 用 `(i, free_at)` 记忆化搜索，状态数对小规模够用；Part 2 把同一时刻所有可能的
> `free_at` 打包成一个 `{free_at: min_cost}` 的前沿字典，再用支配关系剪掉明显更差的状态。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `PART`/`n`/`cost`/`time`，调 `part1` 或 `part2`，打印一个整数。先跑通空输入 `n=0 -> 0`。
2. **Part 1 最小可用**：写 `rec(i, free_at)`：`free_at <= i` 强制付费，否则取 `min(白嫖, 排队)` 的递归结果，加 `memo` 防止重复计算。用 worked example 1/2/3 手算验证。
3. **Part 2 叠加**：把 `dict[free_at] -> min_cost` 当成一个前沿，每步先按 `free_at <= i` 分成"强制组"（合并成一个新状态）和"忙碌组"（各自分裂两个后继），再剪枝。**剪枝方向是这题最大的坑**——见下面第 7 节。
4. **收尾**：`part1`/`part2` 在随机小规模输入上必须给出完全一致的答案（交叉验证），这是本题隐藏测试明确要求的。

## 4. 代码怎么组织
```
part1(cost, time) -> int        # 记忆化搜索，状态 (i, free_at)，用于交叉验证，非大 n 就绪
part2(cost, time) -> int        # 前沿 DP + Pareto 剪枝，n=1e5 量级用
main(stdin, stdout)             # 解析 PART/n/数组，分发，打印
```
两个函数完全独立实现（不是 part2 调用 part1 的某个 helper），因为它们的复杂度类别不同——这是"用简单解交叉
验证复杂解"的典型场景：面试时先讲清楚"我要写两个独立版本，然后写个脚本互相对拍"，比只交一个"看起来对"的
版本更让面试官放心。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def part1(cost, time):
    n = len(cost)
    memo = {}
    def rec(i, free_at):
        if i == n:
            return 0
        key = (i, free_at)
        if key in memo:
            return memo[key]
        if free_at <= i:                      # 强制付费
            res = cost[i] + rec(i + 1, i + time[i])
        else:                                  # 忙碌：白嫖 vs 排队，取更便宜的
            skip = rec(i + 1, free_at)
            queue = cost[i] + rec(i + 1, free_at + time[i])
            res = min(skip, queue)
        memo[key] = res
        return res
    return rec(0, 0)

def part2(cost, time):
    frontier = {0: 0}                          # free_at -> 到达它的最小成本
    for i in range(len(cost)):
        forced_min = min((c for fa, c in frontier.items() if fa <= i), default=None)
        new_frontier = {}
        if forced_min is not None:             # 强制组合并成唯一新状态
            fa, c = i + time[i], forced_min + cost[i]
            new_frontier[fa] = min(new_frontier.get(fa, c), c)
        for fa, c in frontier.items():
            if fa > i:                          # 忙碌组分裂两个后继
                new_frontier[fa] = min(new_frontier.get(fa, c), c)
                fa2, c2 = fa + time[i], c + cost[i]
                new_frontier[fa2] = min(new_frontier.get(fa2, c2), c2)
        # 剪枝：按 free_at 降序，只留成本严格低于目前最优的状态
        pruned, best = {}, None
        for fa, c in sorted(new_frontier.items(), key=lambda kv: -kv[0]):
            if best is None or c < best:
                pruned[fa] = c
                best = c
        frontier = pruned
    return min(frontier.values()) if frontier else 0
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我先确认：任务 `i` 在时间 `i` 到达，付费机空闲用一个计数器 `free_at` 表示；`free_at<=i` 时必须
  强制上付费机，否则可以选。」
- 写 Part 1 时：「我用 `(任务下标, free_at)` 做记忆化搜索的状态，因为这两个数完全决定了后续所有决策——
  贪心在这里不成立，我先举个例子说明为什么（排队反而更便宜），所以必须让两条路都递归下去比较。」
- 写 Part 2 时：「Part 1 的状态数会随 `free_at` 的取值爆炸，我把同一时刻所有 `free_at` 打包成一个
  `{free_at: min_cost}` 的前沿，每步分强制/忙碌两组处理，再用支配关系剪枝——`free_at` 更大、成本更低或
  相等的状态，能『模拟』`free_at` 更小的状态接下来的所有强制转移，所以后者可以被剪掉。」
- 如果面试官问"为什么不是 free_at 小的占优"：「我一开始也这么以为，写完交叉验证测试才发现反了——
  `free_at` 小的状态可能会在未来某一步被强制付费而丧失选择权，`free_at` 大的状态永远至少有同样多的选择。」
- 交付时：「`part1`/`part2` 在随机小规模输入上跑了交叉验证全部一致；Part 2 的前沿大小实测会随 `n`
  近似线性增长（不只是对抗构造，均匀随机数据也会），所以整体是 `O(n·frontier_size)`，经验上接近 `O(n²)`，
  没有找到更优的已知解法，我会诚实地说这一点而不是假装它是线性的。」

## 7. 常见跑偏（方法层面，3 条）
- **把这题当纯贪心做**：一看到"免费机不要钱"就无脑白嫖，遇到 worked example 4 那种"排队更省钱"的构造
  直接算错。必须让两条路都进 DP 比较，不能凭直觉排除一条。
- **剪枝方向想反**：直觉上"`free_at` 更小、更早空闲"像是好事，但推导下来支配方向是反的——**更忙的状态
  永远有更多选择**。这个方向错了会让 Pareto 剪枝直接剪掉最优解而不报错（数值静默偏大），必须靠交叉验证
  测试才能抓住。
- **在 `time[i]=0` 或大数值（1e9 级）时引入浮点或提前近似**：这题所有中间量都必须是精确整数，`time[i]=0`
  会让 `free_at` 原地不动，可能导致下一个任务也被强制，边界要单独测。

## 8. 同族题 / 延伸
- 同一"多机调度、部分强制部分可选"的模式可以换皮成"云函数冷启动 vs 预热实例"或"人工审核 vs 自动过审"，
  核心都是"状态 = 某资源何时可用，DP 沿时间轴推进"。
- 延伸思考：如果免费机也会"忙"（题目变体提到的版本），状态要再加一维记免费机的空闲时刻，前沿会变成
  二维的 Pareto 集合，剪枝规则要重新推导。
- 练习命令：`python3 loop/mock.py start q01`
