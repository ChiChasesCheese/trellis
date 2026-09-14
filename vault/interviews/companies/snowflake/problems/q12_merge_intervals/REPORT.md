# q12 Merge Intervals — report

## Summary
2023 Snowflake OA 候选人索引直接复用的 LC 56 原题，无任何本地化改编。Part 1 排序+一次扫描合并重叠/相接区间；Part 2 **(reconstructed)** 把它包装成一个 add/snapshot 流，模拟"占用时段不断注册，随时要看合并视图"的场景。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #19，2023 Canada OA 索引 item #17，直链 LC 56 https://leetcode.com/problems/merge-intervals/ （逐字复用）。Part 2 为重建。

## Approach by part
1. 校验每个区间；按 `(start, end)` 排序；遍历时若 `start <= 当前合并区间.end` 就并入（取 `max(end)`），否则开新区间。
2. `IntervalStream` 只在 `add` 时缓冲一个 `[start, end]` 副本；`snapshot()` 直接调用 Part 1 的合并函数处理全部已缓冲区间，返回值是新列表（调用方修改不影响内部状态）。

## Pitfalls hidden tests target
- 首尾相接算重叠（`[1,4],[4,5]` → `[1,5]`），但差 1 不相接不合并——brute force 用两两重叠判断 `a.start<=b.end and b.start<=a.end`，不能用"整数点覆盖染色"（那会把相接但不重叠的区间误判为连续）
- 完全嵌套、完全重复
- 非法区间（长度、类型、`start>end`）→ `ValueError`，流的 `add` 同样校验
- `snapshot()` 返回值被调用方 mutate 不能污染内部状态
- 未排序输入、负数边界

## Complexity & measured cost
Part 1：O(n log n) 排序 + O(n) 扫描。Part 2：`add` 均摊 O(1)，`snapshot` O(m log m)（m 为已加入区间数）。perf：n = 10⁵ 时 Part 1 一次合并、Part 2 在 10 万次 add 中穿插 4 次 snapshot，均 < 2 s。

## Test inventory
24 tests — part1 14（含 5 参数化 worked examples、1 随机 brute-force、1 perf、1 io）· part2 8（含随机穿插一致性检查、1 perf、1 io/fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
排序+扫描的区间合并范式 · 精确边界定义（重叠 vs 相接 vs 相邻不重叠）· 流式/增量场景的摊销设计（写多读少）。
