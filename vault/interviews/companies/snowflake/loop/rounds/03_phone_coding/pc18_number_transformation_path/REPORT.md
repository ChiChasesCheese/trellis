# pc18 Number Transformation Path — report

## Summary
TrueInterview 87 题清单第 9 题（2026-06）："Number Transformation Path"，三操作
`add(+2)`/`sub(-2)`/`split(floor(/2))`，`transform` 一手签名与"不必最短、不可达返回 None/抛错"均为
原文。predicated on `split` 仅偶数可用（本 kit 声明的重建选择，否则永远不会不可达）。2-part：
Part 1 任意路径 · Part 2 有界 BFS 求最短 **(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费，split 定义域未给出）；Part 2 为重建。

## Approach by part
1. `a==b` 直接返回 `[a]`；奇 `a` 偶 `b` 直接判 `None`；同奇偶直接平移；偶 `a` 奇 `b` 平移到 `2b` 再
   `split` 一次。
2. 有界 BFS，上界 `2*max(a,b)+4`（由 Part 1 构造给出的可行解证明足够），队列 BFS 找最短路并回溯路径。

## Pitfalls hidden tests target
- 奇数 `a` → 偶数 `b` 两个 Part 都要 `None`（宇称推理，不是"搜索失败"）
- `a==b` 的平凡情形
- `split` 降到 `1` 之后不能再 `split`（`1` 奇）也不能再 `sub`（会变成 0）
- `a<1` 或 `b<1` → `ValueError`
- Part 2 的搜索上界必须覆盖 Part 1 构造用到的最大中间值，否则会漏解

## Complexity & measured cost
Part 1 O(|a-b|) 或 O(a+b)（视是否需要 split 而定），O(1) 额外结构；Part 2 O(bound) BFS，
`bound = 2*max(a,b)+4`。编排者验证：300 组随机 (a,b)（1–500）用通用 checker（不依赖固定答案）验证
Part 1 路径合法性；150 组用独立写的第二套 BFS（不同上界公式）交叉验证 Part 2 最短长度 0 不一致；
Part 2 结果长度 ≤ Part 1 朴素构造长度。perf：1000 组 (a, a+1) 查询端到端 < 2 s（实测约 0.2 s）。

## Test inventory
21 tests — part1 12（含 4 参数化）· part2 8（含 3 参数化）· io/fmt 3；edge 12 · fmt 1 · perf 1 · io 2。

## Skills exercised
S05 隐式图可达性（奇偶推理代替真的建图搜索）· S08 任意路径 → 有界 BFS 最短路 · 主动论证搜索上界的
充分性，而不是无脑无界 BFS。
