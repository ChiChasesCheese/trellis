# q25 Distance to Nearest Two — report

## Summary
TrueInterview 同步清单 #77（题名转述）：数组只含 0/1/2，对每个 1 求到最近 2 的距离，
无 2 则 -1。2-part：Part 1 一维两遍扫描（LC 542 多源 BFS 技巧在一维上的特化）；Part 2
**(reconstructed)** 二维网格版，多源 BFS 求曼哈顿距离，与 LC 542 / pc02 同族。

## Sources & confidence
MED——GitHub 镜像转述题名，二维扩展与规则细节为重建（详见
`../../catalog/raw/github_repos.md` §2/§3）。

## Approach by part
1. 从左到右扫一遍记录最近的 2，再从右到左扫一遍，两遍取较小值；`O(n)`，无需队列。
2. 把所有值为 2 的格子同时作为起点做多源 BFS（网格无障碍，BFS 层数即曼哈顿距离），按
   行优先输出所有值为 1 的格子的距离；`O(rows·cols)`。

## Pitfalls hidden tests target
- 没有 2 → 全部 -1；没有 1 → 输出为空（区分"空结果"与"全 -1"）
- 1 紧邻 2（距离 1）；1 两侧都有 2（取较小值）
- 空数组 / 空网格；网格行长不一致 → `ValueError`
- 非法值（不是 0/1/2）→ `ValueError`
- 一维 `n=10⁶`、二维 `500×500` 网格下的时间

## Complexity & measured cost
Part 1：`O(n)`。Part 2：`O(rows·cols)`。编排者验证：300 组随机一维小输入对暴力（枚举
所有 2 的位置取最小绝对差）0 不一致；150 组随机小网格对暴力（枚举所有 2 的位置取最小
曼哈顿距离）0 不一致。perf：一维 `n=10⁶`、二维 `500×500` 网格下两个 Part 端到端均
`< 2s`。

## Test inventory
19 tests — part1 9（含 1 perf、2 io）· part2 8（含 1 perf、1 io）；edge 12 · fmt 1 ·
perf 2 · io 3。

## Skills exercised
两遍扫描与多源 BFS 的等价性（同一技巧不同维度的具体形式）· 无障碍网格下曼哈顿距离与
BFS 距离的等价关系及其失效条件 · 边界情况的输出形状区分（空 vs 全 -1）。
