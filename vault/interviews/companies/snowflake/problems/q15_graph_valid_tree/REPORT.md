# q15 Graph Valid Tree — report

## Summary
2023 Snowflake OA 候选人索引直接复用的 LC 261 原题：判断无向图是否连通且无环（一棵树）。Part 1 用并查集一次性判定；Part 2 **(reconstructed)** 把它变成在线维护——边一条条到达，每条边加入后汇报是否仍无环、还剩几个连通分量，是并查集的自然在线场景。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #17，2023 Canada OA 索引 item #15，直链 LC 261 https://leetcode.com/problems/graph-valid-tree/ （逐字复用）。Part 2 为重建。

## Approach by part
1. 先检查边数是否恰为 `n-1`（必要条件，快速剪枝）；再用路径压缩 + 按秩合并的并查集逐条合并边端点，任何一条边两端点已同集合即成环判否；全部处理完后分量数应为 1。
2. 同一个并查集贯穿整个在线过程：每条边 `union` 失败则标记"已成环"（一旦为真永久为真，因为环不会被后续加边消除），分量数取并查集当前的 `components` 计数器，天然单调不增。

## Pitfalls hidden tests target
- 边数对但图不连通/有环的构造（三角形+孤立点、边太少/太多）
- 成环状态一旦出现就不会恢复（`test_part2_cycle_flips_acyclic_and_stays_flipped`）
- 单节点空树、零边 Part2 输出为空列表
- 非法输入：`n<1`、端点越界、自环、边格式不对、非整数 → `ValueError`
- 性能：n=10⁵ 的真实随机树

## Complexity & measured cost
O(n + m·α(n)) 时间（α 为阿克曼反函数，实践中近似常数）、O(n) 空间。编排者验证：Part 1 与 BFS 连通性检查（独立于并查集）在 300 组随机小图上 0 不一致；Part 2 与"每步重新 BFS 数分量 + 边数公式判环"的独立暴力在 150 组随机小图上 0 不一致。perf：n=10⁵ 的随机打乱树，两个 part 端到端均 < 2 s。

## Test inventory
22 tests — part1 12（含 4 参数化 worked examples、5 参数化非法输入、1 随机 brute-force、1 perf、1 io）· part2 8（含成环持久性测试、随机 brute-force、非法输入、1 perf、1 io/fmt）；edge 13 · fmt 1 · perf 2 · io 2。

## Skills exercised
并查集（路径压缩 + 按秩合并）标准实现与复杂度论证 · "边数对但不充分"的陷阱识别 · 在线维护场景下并查集相对重跑 BFS/DFS 的复杂度优势。
