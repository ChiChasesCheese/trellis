# q22 Dropped Requests — report

## Summary
TrueInterview 同步清单 #68（2025-11 报告，题名对应经典 HackerRank "Dropped Requests"）：
三条并行滑动窗口限流规则（同秒 >3、10 秒 >20、60 秒 >60）判断哪些请求被拒。核心教学点
是"窗口计数要不要含被拒的请求"这个从未被题面挑明的假设——Part 1 计入全部到达，Part 2
**(reconstructed)** 只计入被接受的，两者在连续拒绝场景下会分叉。

## Sources & confidence
MED——GitHub 镜像转述题名，具体阈值取自 HackerRank 经典版本（详见
`../../catalog/raw/github_repos.md` §2/§3）。三条阈值数字与 Part 2 语义均标注
(reconstructed)。

## Approach by part
1. 三个滑动窗口（同秒计数器 + 两个 deque），每个请求无条件加入所有窗口后再弹出过期项，
   `O(1)` 摊还判断是否超限。
2. 同样的三个滑动窗口，但只有判定"接受"的请求才真正加入窗口；判断时用"如果接受会变
   成多大"跟阈值比较，拒绝的请求不进窗口。

## Pitfalls hidden tests target
- 三条规则各自单独触发（同秒/10 秒/60 秒各设计一个只触发该条规则的输入）
- 恰好卡在阈值上不拒绝（`== 3/20/60`）
- Part 1 与 Part 2 在连续拒绝场景下必须分叉（worked example：15 个 vs 8 个被拒）
- 空输入、全部在阈值内
- 非法输入：非降序、负数时间戳
- `n = 10⁵` 密集突发下两个 Part 的时间

## Complexity & measured cost
两个 Part 均 `O(n)` 摊还（每个时间戳最多入队出队各一次）。编排者验证：80 组随机小输入对
`O(n²)` 独立重算实现（Part 1 和 Part 2 各自的暴力版本，从零扫描而非用滑动 deque）0 不一
致；额外验证 Part 2 的拒绝数在任意输入上都 `<= ` Part 1（因为窗口更小，触发条件更不容
易达到）。perf：`n = 10⁵` 密集突发输入下两个 Part 端到端均 `< 2s`。

## Test inventory
15 tests — part1 8（含 1 perf、1 io）· part2 6（含 1 perf、1 io/fmt）；edge 8 · perf 2 ·
io 2。

## Skills exercised
多条并行滑动窗口限流 · 摊还复杂度论证 · 识别并显式化题面里未言明的计数口径假设 · 用两
套独立暴力分别验证两个 Part。
