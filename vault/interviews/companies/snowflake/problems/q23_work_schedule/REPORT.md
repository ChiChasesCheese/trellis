# q23 Work Schedule — report

## Summary
TrueInterview 同步清单 #72（2025-07 报告）：7 字符 pattern（数字或 `?`），`?` 填
`0..dayHours` 使一周总工时等于 workHours，列出所有填法（字典序）。2-part：Part 1 回溯 +
可行性剪枝直接按字典序生成；Part 2 **(reconstructed)** 把规模放大到 pattern 长度 1000、
workHours 1e4，改用前缀和滑动窗口 DP 只计数取模。

## Sources & confidence
MED——GitHub 镜像转述题名，规则细节（回溯剪枝、DP 形状）为重建（详见
`../../catalog/raw/github_repos.md` §2/§3）。

## Approach by part
1. 从左到右回溯每个 `?` 位置，按 0..dayHours 升序尝试；用后缀固定和 + 剩余 `?` 数
   `×dayHours` 算出可达区间 `[lo,hi]`，`workHours` 不在区间内就剪枝。升序 + 从左到右
   保证生成顺序即字典序，无需排序。
2. `dp[i][s]` = 前 i 天工时和为 s 的方案数；固定天是整体平移，`?` 天是宽度
   `dayHours+1` 的滑动窗口和；用前缀和把每层的窗口和从 `O(S·dayHours)` 降到 `O(S)`，
   总体 `O(n·S)`。

## Pitfalls hidden tests target
- 无 `?` 时的直接判断（命中/不命中）
- `workHours` 等于理论最大值（唯一解：全填满）或超出理论范围（空/0）
- 字典序验证（多个 `?` 时靠左位置的取值决定整体顺序）
- 非法输入：长度不是 7、非法字符（含 `'9'`）、`workHours<0`、`dayHours` 越界
- Part 2 允许 pattern 长度超过 7（不受 Part 1"恰好一周"限制）
- 全 `?`（分支数最大）与 `n=1000,S=8000`（DP 表最大规模）下的时间

## Complexity & measured cost
Part 1：回溯 + 剪枝，实测全 `?` 长度 7、`workHours=28`（居中，解最多）本地 0.17s 生成
273127 个解；pytest 端到端 perf 断言 `< 2s`。Part 2：`O(n·S)`，实测
`n=1000, S=8000` 本地约 1.0–1.2s（含前缀和构建），pytest 端到端 perf 断言 `< 2s`。编排
者验证：150 组随机小 pattern（长度 7）对暴力枚举全部 `?` 组合 0 不一致（Part 1 与
Part 2 各自 150 组）；额外验证 Part 2 支持长度 > 7 的 pattern（对小规模暴力交叉验证）。

## Test inventory
18 tests — part1 10（含 7 组参数化非法输入、1 perf）· part2 7（含 1 perf、1 io/fmt）；
edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
回溯 + 区间可行性剪枝 · 计数 DP 与前缀和降复杂度 · 生成顺序与排序需求的对应关系 ·
小规模枚举与大规模 DP 的复杂度分级设计。
