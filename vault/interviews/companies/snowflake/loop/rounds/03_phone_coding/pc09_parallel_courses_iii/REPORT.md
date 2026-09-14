# pc09 Parallel Courses III — report

## Summary
Onsite 一手原题 LC 2050（带权 DAG 上的最短完成时间），题号和例子逐字匹配。做成 2-part：Part 1 原题（迭代 Kahn） → Part 2 给出一条字典序最小的关键路径 **(reconstructed)**。

## Sources & confidence
MED-HIGH（fastprep.io，明确 onsite 标签，题面和例子与 LC 2050 完全一致）；Part 2 未见一手报道，按同族常见追问重建，写法参考 Stripe kit `qA09_lc2050_parallel_courses_iii`（Kahn + 关键路径回溯思路），题面/规则/测试独立编写。

## Approach by part
1. 迭代 Kahn：`finish[v] = time[v] + max(finish[u] for u in preds(v))`，每次松弛一条边就更新，入度归零才入队；`processed != n` 说明有环，抛 `ValueError`。答案是 `max(finish)`。
2. "紧邻边" `(u,v)` 满足 `finish[v] == finish[u] + time[v]`；由于 `time[v] ≥ 1`，紧邻边严格增大 `finish`，所以按 `finish` 降序处理节点时后继必然已算好。`best_suffix(v) = [v]`（若 `finish[v]` 是全局最大）否则 `[v] + min(后继的 best_suffix)`（Python 列表比较正好是字典序）。最终答案是所有真源点（入度 0）里 `best_suffix` 最小的一个。

## Pitfalls hidden tests target
- `relations` 1-based、`time` 0-based 的对齐（两个方向都测）
- 无依赖关系时答案退化为 `max(time)`
- 环检测要专门报错，不是静默返回错误答案
- 自环、越界编号、`time` 长度不符、非正耗时
- Part 2 的两种平手：不同起点打平手（取字典序小起点）、同一起点不同延伸打平手
- Part 1 在 5×10^4 长依赖链下不爆栈、2 秒内完成

## Complexity & measured cost
Part 1 O(n+m) 时间/空间，迭代实现天然不会栈溢出；n=5×10^4 长链测得 ~0.015s。Part 2 O(n+m) 加上 `min()` 列表比较的开销，最坏情况与"节点数 × 候选序列长度"相关；n=3000、稠密平手较多的随机 DAG（~1.2×10^4 条边）测得 ~0.003s，远低于 2s 预算，故未额外收紧规模。编排者用记忆化 DFS 暴力（与 Kahn 实现完全独立）在 300 组随机小 DAG 上交叉验证 `minimum_time` 和 `critical_path` 的合法性，0 不一致。

## Test inventory
24 tests — part1 14（含 4 参数化样例、1 perf、1 io）· part2 10（含 4 参数化样例、1 perf、1 io、1 fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
S05 图：拓扑排序 / DAG 最长路 DP · 迭代改写避免递归栈溢出 · 平手打破规则的确定性设计（字典序最小路径）
