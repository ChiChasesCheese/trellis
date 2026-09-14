# pc20 Connect Four — report

## Summary
TrueInterview 87 题清单第 16 题（"canPlayWin"，2026-06）与第 18 题（"Design Connect Four"
LLD，2026-05）同族合并。3-part：Part 1 判定落子是否四连（一手）· Part 2 加重力按列落子
**(reconstructed)** · Part 3 完整游戏状态机 LLD **(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费）；Part 1 的 `can_play_win` 签名与格子取值为原文；
Part 2、Part 3 为重建。

## Approach by part
1. 从落子点沿横、竖、两条斜线四个方向轴，各自向两边扩展数连续同色格，任意一轴 `count>=4` 即赢。
2. 复用 Part 1：先在指定列找最下面的空格落子（原地改棋盘），再对落点跑一次 `can_play_win`。
3. `ConnectFour` 封装棋盘 + 回合 + 赢家 + 落子计数；`drop()` 每次都会切换回合（即使刚好获胜），
   游戏结束或非法列/满列时抛错且不改变状态；`is_draw()` = 棋盘落满且无赢家。

## Pitfalls hidden tests target
- 只有 3 连不算赢；坐标越界 / `player` 非法 / `board[x][y]` 与 `player` 不符 → `ValueError`
- Part 2 列已满 / 越界 → `ValueError`；落子高度必须正确（不是无脑落到最底行）
- Part 3 非法操作不改变状态（失败的 `drop()` 之后 `winner()` 仍是之前的值）
- Part 3 真平局（暴力搜索找到的落子序列，棋盘落满且没有任何四连）与"赢了同时棋盘也满"的优先级
- Part 3 小于 4×4 的棋盘在构造函数直接拒绝

## Complexity & measured cost
Part 1：O(1)（每个方向轴最多扫 3+3 格，与棋盘大小无关）。Part 2：O(rows) 找落点 + O(1) 判定。
Part 3：每步 O(1)。编排者验证：200 组随机棋盘（4–7 边长，随机撒子）与"扫描整个棋盘找含该点的
四连"独立暴力实现 0 不一致；平局用例的落子序列由暴力搜索（20 万次随机 shuffle 尝试）在
16 步全部合法且落满不四连的约束下找到。perf：500×500 全 `"a"` 棋盘的单点判定端到端 < 2 s。

## Test inventory
26 tests — part1 9（含 1 perf、1 io）· part2 5 · part3 8 · io/fmt 2；edge 12 · fmt 1 · perf 1 · io 3。

## Skills exercised
S01 网格四方向扫描 · S07 小型 OOD 状态机设计（回合、赢家、平局、非法操作不改变状态）·
把"判定"、"落子"、"整局游戏"拆成递进的三层追问。
