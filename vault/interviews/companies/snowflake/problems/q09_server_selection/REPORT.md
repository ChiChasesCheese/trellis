# q09 Server Selection with switching cost — report

## 摘要

两个已知来源帖子都是纯截图，唯一能恢复的文字线索是一条评论给出的复杂度约束：`2<=m<=n<=1000`，
"存在 O(N²) 解法，但问怎么做到 O(m·n)"。本题把这条线索具体化为一个经典"带切换代价的序列选择" DP：
Part1 是朴素的 O(m²n)（每格扫描所有其他 server），Part2 是把每格转移压到 O(1) 的 O(mn) 解法
（只需要追踪上一列的最优/次优总代价），并且要求 Part2 额外做路径重建。这正好复刻了来源评论里提到
的复杂度落差，是我设计但对来源具名引用负责的重构。

## 来源与置信度

- https://leetcode.com/discuss/interview-question/2594968/Snowflake-or-OA-or-Server-Selection
  （2022-09-08，纯截图，评论者称未解出）
- https://leetcode.com/discuss/interview-question/2794537 （2022-11-08，"Server Selection"，纯
  截图，但一条评论给出复杂度约束原文："2 <= m <= n <= 1000... there is an O(N^2) solution, but
  how to solve in O(m*n)"）
- 索引为 2023 Canada list item #2
- 置信度：中 —— 复杂度约束是硬信息，cost 结构 / switch_cost 语义 / tie-break 规则均为设计产物，
  problem.md 里逐条标注了 (reconstructed)。三个 worked example 的 cost 和 assignment 都用独立
  脚本跑过 part1/part2 两套实现并交叉核对，不是手算臆测。

## 逐 part 思路

- **Part1**：`dp[j]` = 到当前槽为止、以 server j 结尾的最小总代价。转移时对每个 j 扫描所有
  `k != j` 取 `dp_prev[k] + switch_cost` 与 `dp_prev[j]`（留下）的最小值，再加 `cost[j][i]`。
  故意保留 O(m) 的内层扫描，作为"能写出来但不是目标复杂度"的基线。
- **Part2**：核心技巧是只维护上一槽 `dp_prev` 里的**最优值/server** 和**次优值/server**
  （一次线性扫描，`O(m)` 每槽、总 `O(mn)`）。对 server j：如果最优 server 不是 j，切换代价 =
  最优值+switch_cost；如果最优 server 正是 j（不能切换到自己），退而用次优值+switch_cost。跟
  "留下"（`dp_prev[j]`，不付切换代价）比较，**平局时优先留下**；记录每个 j 的前驱 server 用于最后
  回溯出 `assignment`。最终答案是 `min(dp)`，多个 server 打平时取**编号最小**的（`min(range(m),
  key=...)` 天然满足，Python 的 `min` 对 key 相同的第一个候选保留最小索引）。
- 路径重建：每一步记录 `preds[j]`（server j 在这一槽的前驱 server 下标），最后从 `argmin(dp)` 开始
  反向回溯拼出 `assignment`，再整体反转。

## 隐藏测试针对的坑

- **"切到自己"陷阱**：如果最优 server 就是 j 本身，必须退化用次优值，否则会算出"免费切换到自己"
  的错误结果——`test_example1_part2_cost_and_assignment` 的追踪过程专门覆盖了这一步（槽1 时
  server1 恰好是自己去年最优，触发次优分支）。
- **平局 tie-break 顺序**：`test_tie_break_prefers_not_switching_then_lowest_index` 构造了完全
  等价的两个 server + switch_cost=0，如果不优先"留下"，会在每一步都随意切换（虽然代价相同，但
  assignment 就不确定了，对不上样例）。
- `switch_cost=0` 退化为每列独立取最小（`test_switch_cost_zero_*`）——这个测例之前我自己手滑算错
  过期望值（把第0列的最小值 3 错记成 1），跑测试时立刻被 part1 的真实实现打回来（`assert 6 == 4`），
  提醒我先用代码算样例、再写断言，而不是心算。
- 极大 `switch_cost` 退化为整段粘在"行总和最小"的单一 server 上（`test_huge_switch_cost_*`）。
- `m=1`（不可能切换）、`n=0`（空 assignment，注意 stdout 第二行仍然要输出一个空行）。
- 小规模暴力枚举交叉验证：`test_randomized_cross_check_against_part1_and_brute_force` 用
  `itertools.product` 穷举所有 `m^n` 种分配方案核对 part1/part2 的代价，并且用 `assignment` 反
  推真实代价核对 part2 返回的路径确实能达成它声称的总代价（不仅代价数字对，路径本身也要自洽）。

## 复杂度与实测

Part1: O(m²n) 时间，O(m) 空间（滚动数组）。Part2: O(mn) 时间，O(mn) 空间（需要保存每一步的
`preds` 数组用于回溯；若不需要路径重建可以降到 O(m)）。

perf 测试只针对 Part2，`m=n=1000`（约 1e6 格，匹配来源约束 `m<=n<=1000`），本地实测纯函数调用
约 0.1s，经 `run_script` 子进程往返（含 Python 解释器启动开销）仍远低于 2s 预算。**没有**在满
1000×1000 规模上对 Part1 做 perf 测试 —— 本地测过 Part1 在 `m=1000, n=20`（2×10⁷ 次操作）已经
要 0.65s，线性外推到 `n=1000` 会接近 30-60s，远超预算，这是 O(m²n) 基线本身"故意慢"的设计意图，
在 REPORT 里诚实记录而不是悄悄跳过。Part1 只在 `m,n<=15` 的小规模正确性测试和交叉验证里被调用。

## 测试清单

21 个测试 —— part1: 8 个（含 1 个 io）；part2: 13 个（含 2 个 io、1 个 perf、1 个 fmt、2 个
交叉验证）；edge 8 个。全部针对 `solution.py` 通过；针对 `starter.py`（`IMPL=starter`）确认产生
17 个真实断言失败（并非 collection error），另外 4 个因 stub 返回 `(0, [])` 恰好命中 `n=0` 等边界
期望而"意外通过"。

## 技能 ids

S08（LC 原题变体 + 复杂度再压一档：O(m²n) → O(m·n) 的 best/second-best DP 优化，路径重建，
确定性 tie-break）
