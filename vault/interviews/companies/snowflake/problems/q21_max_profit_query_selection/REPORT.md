# q21 Maximum Profit Query Selection — report

## Summary
TrueInterview 同步清单 #54（2026-01 报告，GitHub 镜像转述）：n 种查询类型，选一种反复跑
到预算耗尽，最大化利润。2-part：Part 1 单类型 `O(n)`；Part 2 **(reconstructed)** 预算可
拆给至多两种不同类型，是"恰两物品"的无界背包，教学点是"只挑收益率最高的类型不是正确
贪心"。

## Sources & confidence
MED——GitHub 镜像 `kevin-2023-code/Tech-Interview-Questions`，题面细节来自公开预览重建
（详见 `../../catalog/raw/github_repos.md` §2/§3）。Part 2 全部为重建。

## Approach by part
1. 对每种类型算 `floor(k/durations[i]) * revenues[i]`，取最大值。
2. 对每对类型 `(i, j)` 做容量为 `k` 的无界背包 DP（两个"物品"任意非负组合），取所有
   pair 的最优值与 Part 1 的单类型最优比较取大。刻意把规模限制在 `n ≤ 30`、`k ≤ 2000`
   使 `O(n²k)` 在秒级完成。

## Pitfalls hidden tests target
- 混着跑严格更优的反例（`[3,4],[4,5],7 → 8` vs `9`）
- 混着跑不优于单类型时两个 Part 结果相等
- `k = 0`、只有一种类型（Part 2 退化为 Part 1）
- `revenue = 0` 的类型不干扰其余计算
- 非法输入：长度不一致、`duration < 1`、`revenue < 0`、`k < 0`
- Part 1 大规模（`n=10⁵`，大数值）、Part 2 限定规模（`n≤30, k≤2000`）下的时间

## Complexity & measured cost
Part 1：`O(n)`。Part 2：`O(n² · k)`。编排者验证：500 组随机小输入 Part 1 对暴力
（同一公式直接算）0 不一致；300 组随机小输入 Part 2 对独立暴力（枚举类型 i 的跑动次
数、贪心取满剩余预算给类型 j）0 不一致；200 组随机输入验证 Part 2 结果恒 `>=` Part 1。
perf：Part 1 在 `n=10⁵` 大数值下 `< 2s`；Part 2 在 `n=30, k=2000` 下 `< 2s`。

## Test inventory
15 tests — part1 8（含 6 组参数化非法输入、1 perf、1 io）· part2 7（含 1 perf、1
io/fmt）；edge 10 · fmt 1 · perf 2 · io 2。

## Skills exercised
无界背包 DP · 贪心反例构造（收益率最高 ≠ 全局最优）· 复杂度分级设计（大规模 O(n) vs
小规模 O(n²k)）· 独立暴力交叉验证。
