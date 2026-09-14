# q13 Minimum Interval to Include Each Query — report

## Summary
2023 Snowflake OA 候选人索引直接复用的 LC 1851 原题：每个 query 找最小的覆盖区间大小。Part 1 是离线排序 + 最小堆的经典懒删除扫描；Part 2 **(reconstructed)** 追加"到底是哪个区间"，需要显式定义平局规则（size 相同选 start 更小）。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #21，2023 Canada OA 索引 item #19，直链 LC 1851 https://leetcode.com/problems/minimum-interval-to-include-each-query/ （逐字复用）。Part 2 为重建。

## Approach by part
1. 区间按 `left` 排序；query 按值排序但记原始下标；用 `(size, left, right)` 最小堆，扫描时先压入所有 `left <= query` 的区间，再弹出堆顶中 `right < query` 的过期条目，剩下堆顶即最优。O((n+q) log n)。
2. 堆的排序键本身就是 `(size, start, ...)`，所以平局（size 相同）天然按 `start` 更小的排在堆顶——Part 2 直接复用同一次扫描，只是多返回 `(start, end)`。

## Pitfalls hidden tests target
- 堆里过期但未弹出的条目不会被误选（堆序性质保证）
- 平局：两个区间大小相同都覆盖 query 时必须选 `start` 更小的，不能依赖"先压入堆的碰巧排前面"
- query 命中边界值、单点区间、完全无覆盖
- 非法输入（区间长度/类型/`left>right`、非 int query）→ `ValueError`
- 空 `intervals` / 空 `queries`

## Complexity & measured cost
O((n+q) log n) 时间，O(n+q) 空间。编排者验证：Part 1 与"对每个 query 线性扫描全部区间取最小"的 O(n·q) 暴力在 400 组随机小输入上 0 不一致；Part 2 同样与平局显式判断的暴力对比 0 不一致。perf：n = q = 10⁵ 时两个 part 端到端均 < 2 s。

## Test inventory
20 tests — part1 11（含 3 参数化 worked examples、1 随机 brute-force、1 perf、1 io）· part2 7（含平局测试、随机 brute-force、1 perf、1 io/fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
离线扫描 + 最小堆懒删除的"每元素只进堆一次"摊销技巧 · 排序保持原始下标 · 显式平局规则契约。
