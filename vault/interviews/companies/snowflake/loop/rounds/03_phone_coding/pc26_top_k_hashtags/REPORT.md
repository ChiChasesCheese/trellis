# pc26 Top K Hashtags — report

## Summary
一手预览只给出 Part 1（去重用户数热度排名，降序+字典序打平取 top k）。Part 2 流式类
`add`/频繁`top(k)`、Part 3 滑动时间窗（闭区间，相对最大时间戳）均为 **(reconstructed)**，是聚
合排名类问题最常见的两个追问方向。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览一句原题面可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。流式类与滑动窗口为重建。

## Approach by part
1. `dict[tag -> set[user]]` 一次遍历分组去重，排序键 `(-len(set), tag)`，切片前 k。
2. `HashtagCounter` 维护同样的 `dict[tag -> set[user]]`（这是任何正确实现都绕不开的最小状
   态）；`top(k)` 每次对全部 tag 重新排序，`O(T log T)`——诚实讨论了这不是渐进最优（真正最优需要
   按热度分桶的有序结构，`O(log T)` 更新/`O(k + log T)` 查询），但面试时间通常不允许写出来。
3. 滑动窗口用**闭区间** `[max_ts - window_seconds, max_ts]`（而不是开区间/`ts > cutoff`），
   这样 `window_seconds = 0` 才能正确保留 `ts == max_ts` 的事件；这是这道重建题里最容易写错的
   边界，问题原来的草稿曾用 `>` 而不是 `>=`，被 `test_window_zero_keeps_only_max_ts` 抓出来并
   修正为 `>=`。

## Pitfalls hidden tests target
- 同一用户重复发同一 tag 只算一次（不能用纯计数代替去重集合）
- 热度打平按 tag 字典序升序
- Part 3 输入不保证按时间排序，`max_ts` 必须扫描全体而不是假设最后一条最新
- Part 3 `window_seconds = 0` 的闭区间边界（这题本身在实现时踩过一次坑，见上）
- Part 2 从未调用 `top()` 时输出 `-`

## Complexity & measured cost
Part 1：`O(n)` 分组 + `O(T log T)` 排序（`n` = 事件数，`T` = 不同 tag 数）。Part 2 每次 `add`
`O(1)`，每次 `top(k)` `O(T log T)`（讨论了更优设计但未实现）。Part 3：`O(n)` 过滤 + `O(T log T)`
排序。perf：10 万条事件端到端 < 2s。

## Test inventory
23 tests — part1 7（含 1 perf、1 io）· part2 6（含 1 io）· part3 8（含 1 io/fmt）；
edge 12 · fmt 1 · perf 1 · io 3。

## Skills exercised
S06（计数/聚合哈希 + 确定性排序 tie-break，与 pc11、pc12、pc03 同一类考法）· 去重 vs 计数的区分
· 滑动窗口边界的闭/开区间选择与验证 · 对"渐进最优但实现成本高"的设计能不能诚实讲清楚。
