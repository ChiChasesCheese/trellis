# pc23 Min Coins with Change — report

## Summary
TrueInterview 87 题清单第 23 项一手题面预览（面额固定、可多付找零、最小化硬币总数），三段规则
均超出预览细节，**(reconstructed)**：Part 1 固定 canonical 面额 + 搜索上界论证；Part 2 任意
（非 canonical）面额集合，戳破贪心；Part 3 返回具体的付款/找零硬币拆法，用 checker 而非逐字符
比对验证。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览一句可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。窗口上界、任意面额、具体拆法均为重建。

## Approach by part
1. `min_coins(x, denoms)`：标准无界零钱兑换 DP，`dp[x] = min(dp[x-d]+1 for d in denoms)`。
   `min_total_coins_fixed(n)` 在 `P ∈ [n, n+200]` 里搜索 `dp[P] + dp[P-n]` 的最小值；200 =
   `max(canonical denoms)`，用更宽窗口（5x）在 `n=0..10000` 上做了零差异的计算验证。
2. Part 2 换成任意面额集合（含贪心反例 `{1,3,4}`），窗口翻倍到 `2*max(denoms)` 留余量，同样只是
   经验上界，测试里对随机面额集合和 `{1,3,4}` 专门做了 vs. 5x 窗口的比对。
3. Part 3 复用同一个 DP 表，回溯时按"面额从大到小"确定性地拆出付款和找零两侧的具体硬币；因为最优
   拆法可能不唯一，测试用 `is_valid_optimal_breakdown` checker（验证面额合法 + 净额正确 + 总数
   等于最优值）而不是逐字符比对来判定任意实现的正确性，同时保留少量精确回归用例。

## Pitfalls hidden tests target
- Part 2 用贪心代替 DP（`{1,3,4}` 凑 `6`：贪心 3 枚，DP 2 枚）
- 窗口上界选小了（漏掉真正的最优付款方案）——`test_window_bound_matches_wider_window*`
- 面额集合无法凑出目标金额（比如全是偶数面额凑奇数）却没有正确抛 `ValueError`
- 面额输入非法（空集合、非正数）
- Part 3 具体拆法用了不在面额集合里的硬币，或净额算错，或总数不是最优（`is_valid_optimal_breakdown`
  专门覆盖这三类）
- `n = 0` 时两侧都应为空列表 / 输出 `-`

## Complexity & measured cost
`min_coins` 单次 DP 是 `O(window * |denoms|)`；`min_total_coins_fixed` 单次调用是
`O((n+window) * |denoms|)`，`n<=10000, window=200, |denoms|=6` → 约 6 万次操作，微秒级。
perf 测试：3000 次随机查询（Part 1）端到端 < 2s。

## Test inventory
27 tests — part1 8（含 6 参数化、1 perf、1 io）· part2 8（含 1 参数化×3）· part3 9（含 2 io）；
edge 12 · fmt 2 · perf 1 · io 4。

## Skills exercised
S08（零钱兑换 DP 的双向变体，贪心失效场景的识别）· 上界证明的诚实边界（非单调函数下交换论证失效，
用经验验证 + 更宽窗口测试兜底）· DP 回溯构造具体解 + checker 式测试设计（当最优解不唯一时避免逐字
符断言）。
