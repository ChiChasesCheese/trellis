# q24 Maximum Throughput — report

## Summary
TrueInterview 同步清单 #74（题名转述，无报告日期）：流水线由 n 个串联服务组成，吞吐量
是所有服务里最小的（瓶颈）；预算内升级各服务（乘法产能公式），最大化瓶颈。2-part：
Part 1 二分答案 + 独立可行性判断；Part 2 **(reconstructed)** 返回达成最优解的具体升级
方案，并用反证法论证方案瓶颈恰好等于二分找到的最优值。

## Sources & confidence
MED——GitHub 镜像转述题名，升级公式、二分实现与 Part 2 方案重建均为重建（详见
`../../catalog/raw/github_repos.md` §2/§3）。

## Approach by part
1. 对候选瓶颈 `T`，服务 i 所需最小升级次数 `x_i = max(0, ceil(T/t_i)-1)`，花费
   `x_i * cost_i`；求和跟预算比较得到 `feasible(T)`（单调不增）；对 `T` 二分找最大可行
   值。`O(n log(值域))`。
2. 用最优 `T*` 对每个服务独立算出最小升级次数，即为方案；反证法证明该方案的实际瓶颈
   恰好等于 `T*`（否则会与 `T*` 的最大可行性矛盾）。

## Pitfalls hidden tests target
- `budget=0` 时答案就是原始最小值，方案全 0
- 升级昂贵服务不划算的反例（只升级便宜服务追上瓶颈）
- 只有一个服务；所有服务吞吐量已相等
- 方案自洽性：重算出的瓶颈必须恰好等于 Part 1 答案，且总花费 `<=` 预算
- 非法输入：长度不一致、`throughput<1`、`scalingCost<1`、`budget<0`
- `n=10⁵`、数值到 `10⁶`、`budget` 到 `10¹²` 下的时间

## Complexity & measured cost
Part 1：`O(n log(值域))`。Part 2：同 Part 1 再加一次 `O(n)` 独立计算升级次数。编排者验
证：200 组随机小输入（穷举所有服务的升级次数组合）对 Part 1 0 不一致；200 组随机输入
验证 Part 2 方案自洽（重算瓶颈 == 目标值、总花费 <= 预算、目标值 == Part 1 的答案）。
perf：`n=10⁵` 大数值、`budget=10¹²` 下两个 Part 端到端均 `< 2s`。

## Test inventory
15 tests — part1 8（含 5 组参数化非法输入、1 perf、1 io）· part2 6（含 1 perf、1
io/fmt）；edge 9 · perf 2 · io 2。

## Skills exercised
二分答案（最大化最小值）· 独立可行性判断的单调性论证 · 用反证法证明构造方案的紧致性 ·
大数值下二分上界的安全估计。
