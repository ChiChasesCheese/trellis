# pc29 Valid Tic-Tac-Toe (Extended) — report

## Summary
Part 1（LC 794 原题，3x3/K=3）与 Part 2（推广到 N×N/K 连）为一手题面；Part 3（原因码）为
**(reconstructed)**。实现阶段用暴力枚举验证时发现并修正了一个经典易错点：判断"一个人能否同时有
多条连线"不能只查两两相交，必须查全部连线是否有共同交点——这是本题唯一有意思的地方。

## Sources & confidence
HIGH（Part 1，LC 794 官方题面）；MED（Part 2，TrueInterview 同步的 Snowflake Algo 87 题清单第
29 项，聚合站，题面付费，仅预览可见）：见 `../../../catalog/raw/github_repos.md` §2/§3。Part 3
原因码为重建；"多连线需要全体共同交点"这条完整必要条件是本 kit 自己用暴力枚举纠正的。

## Approach by part
1/2. 扫描四个方向（行/列/主对角线/副对角线）收集每个人的全部 K 连线；校验落子数关系
   （`#X-#O ∈ {0,1}`）、赢了就停（赢家落子数关系更严格）、双方不能都赢、以及"多条连线必须有
   共同交点"（不是两两相交）。
3. 同样的检查顺序，命中即返回对应原因码，全部通过则 `OK`。

## Pitfalls hidden tests target
- **两两相交不等于全体共同交点**：`test_three_lines_pairwise_intersecting_but_no_common_cell_is_invalid`
  直接复现了实现阶段抓到的反例（三条线两两相交、无共同点，之前的实现误判为可达）
- 落子数关系的三种细分（总体交替、X 赢的精确关系、O 赢的精确关系）分别对应三种不同的错误码
- 全 19683 种 3×3 局面逐一对照 BFS 暴力枚举（已知可达状态数 5478，用作断言基准）
- N=4 用有界深度（`max_moves=6`）BFS 暴力枚举 + 500 组随机局面交叉验证（无界 BFS 状态数上百万，
  测试里换成有界深度以保持速度）

## Complexity & measured cost
获胜线扫描 `O(N^2 * K)`；"共同交点"检查是对每个人的全部连线做集合求交，最坏 `O(连线数 * N^2)`
（连线数在小棋盘上是常数级）。perf：30x30 棋盘、300 次查询端到端 < 2s。暴力枚举 3×3
全状态 0.04s，4×4 有界深度（6 步）1.2s，仅用于测试而非生产路径。

## Test inventory
19 tests — part1 5（含 1 穷举全部 19683 局面）· part2 4（含 1 perf、随机 500 组交叉验证）·
part3 5（含 1 io/fmt）；edge 9 · fmt 1 · perf 1 · io 3。

## Skills exercised
S07（棋盘可达性推理：把游戏规则翻译成局面的代数约束）· 对"看似正确的充分条件"保持怀疑、用暴力
枚举纠正自己实现里的 bug 的习惯 · 多方向扫描与边界的规整实现。
