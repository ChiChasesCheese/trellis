# q20 Sequential String — report

## Summary
2024 年 OA 一手转述（`JoeBao22/SDE-OA-2024`）：字符串 `s` 只能顺序读，对每个查询求最短
前缀长度使其数字多重集合覆盖查询的多重集合。**来源自带的参考解法是错的**——它把查询当
成有序子序列去匹配，而题目只关心计数。2-part：Part 1 逐查询二分前缀计数表；Part 2
**(reconstructed)** 用出现位置表把复杂度从 `O(len(q) log n)` 降到 `O(len(q))`。

## Sources & confidence
MED——GitHub 一手转述，参考实现带 bug（详见 `../../catalog/raw/github_repos.md` §1/§3）。
Part 2 为重建。

## Approach by part
1. 每个数字一张前缀计数列（`O(10n)` 预处理），查询里的每个数字在对应列上二分找到"凑够
   `need[d]` 个"所需的最短前缀长度，取所有数字里的最大值。
2. 每个数字一张出现位置列表（`O(n)` 预处理），需要第 `need[d]` 个该数字时直接索引
   `occ[d][need[d]-1]`，不再二分。

## Pitfalls hidden tests target
- 顺序匹配 vs 多重集合（`"21"`, `"12"` → `2`，不是 `-1`）
- 空查询 → `0`；空 `s` → 除空查询外全 `-1`
- 需要的数字从未出现 → `-1`
- 需要用满整个 `s`
- 某数字需要多次出现（重复计数）
- 非法输入（非数字字符）→ `ValueError`
- 两个 Part 在任意输入上必须给出相同答案

## Complexity & measured cost
Part 1：`O(10n)` 预处理 + `O(总查询长度 · log n)`。Part 2：`O(n)` 预处理 +
`O(总查询长度)`。编排者验证：300 组随机小输入对暴力（枚举前缀长度 + `Counter` 覆盖判定）
0 不一致；300 组随机输入 Part 1/Part 2 结果 0 不一致。perf：`n = 10⁵`、`m = 2×10⁴`、
总查询长度 ≈ `5×10⁵` 时两个 Part 端到端均 `< 2s`。

## Test inventory
16 tests — part1 9（含 1 perf、1 io）· part2 5（含 1 perf、1 io/fmt）；edge 9 · fmt 1 ·
perf 2 · io 2。

## Skills exercised
计数 vs 顺序的正确性论证 · 前缀单调性与二分 · 用出现位置表消去 log 因子 · 多 part 一致性
交叉验证。
