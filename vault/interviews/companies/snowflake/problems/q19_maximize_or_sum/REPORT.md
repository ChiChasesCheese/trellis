# q19 Maximize OR-Sum — report

## Summary
2026-05 Snowflake AIML 实习 OA 一手原题：至多 k 次"某元素翻倍"，最大化整个数组的按位或（= LC 2680）。原帖作者的"全给最大元素"是错的，评论区给出反例，题面保留了这段——它就是这题的教学点。2-part：Part 1 精确值 O(n) → Part 2 k 到 10⁹ 取模 **(reconstructed)**。

## Sources & confidence
HIGH——Reddit `1t0ogu7` 逐字题面与样例 `[12,9], k=1 → 30`（2026-05-01），收割全文在 `catalog/discovery/harvest/reddit_posts_2026-09-13.json`；另有 interviewfox 回忆（LOW）。Part 2 为重建。

## Approach by part
1. 前缀 OR、后缀 OR；`max((nums[i] << k) | prefix[i] | suffix[i+1])`。
2. `k ≤ 64` 走 Part 1 再取模；`k > 64` 时被移位元素与其余元素的位不重叠，按 `(nums[i], others_i)` 字典序选下标，再 `nums[i] * pow(2, k, MOD) + others_i`。

## Pitfalls hidden tests target
- "翻倍最大元素"的反例 `[12, 9]`
- 相等最大值时要比其余元素的 OR（`[6, 1, 6]`）
- 64 附近的路径切换（随机 k ∈ [0, 80] ∪ [60, 130] 与精确值取模对比）
- 取模后的数不可比较
- 空数组 / 负 k / 越界元素 → `ValueError`
- n = 10⁵ 下两个 part 的时间

## Complexity & measured cost
O(n) 时间、O(n) 空间。编排者验证：Part 1 与"把 k 次任意拆给各元素"的穷举在 3000 组随机小输入上 0 不一致；Part 2 与精确值取模在 3000 组上 0 不一致。perf：n = 10⁵ 时 Part 1（k = 15）与 Part 2（k = 10⁹）端到端均 < 2 s。

## Test inventory
20 tests — part1 13（含 4+4 参数化、1 perf、1 io）· part2 7（含 1 perf、1 io/fmt）；edge 9 · fmt 1 · perf 2 · io 2。

## Skills exercised
S08 贪心正确性与复杂度 · 位运算与前后缀预处理 · 大数取模的比较顺序
