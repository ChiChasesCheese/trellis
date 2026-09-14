# q17 Remove Stones to Minimize the Total — report

## Summary
Snowflake OA 题池（FastPrep 汇总）复用的 LC 1962 原题：k 次操作每次对半削减当前最大堆，求总量。因为规则本身就规定了"选最大"，贪心正确性是天然的，真正考的是最大堆的高效实现。Part 2 **(reconstructed)** 把它包装成一个 add/apply 在线服务，堆和操作可以任意穿插。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #39，FastPrep OA 题池，"Easy, Heap/Greedy"，最近报告 2024-12，LC-exact，对应 LC 1962 https://leetcode.com/problems/remove-stones-to-minimize-the-total/ 。Part 2 为重建。

## Approach by part
1. 用取负数模拟的最大堆；k 次循环每次弹出最大值，减去其一半（下取整）后推回；堆顶已为 0 时提前终止（全零，操作不再改变任何东西）。O(n + k log n)。
2. `StoneStream` 把同一个最大堆和滚动维护的 `total` 保留在对象状态里；`add` 均摊 O(log n) 插入，`apply(k)` 复用 Part 1 的循环但作用于当前堆，返回时直接读 `total`（不重新求和）。

## Pitfalls hidden tests target
- `k=0` 是无操作；`k` 远超收敛所需时提前停止而不是傻循环
- 堆值收敛到不动点（`1` 减半仍是 `1`，因为 `floor(1/2)=0`）
- 非法输入：非正整数堆、负数/非整数 `k` → `ValueError`
- 流式场景：`add` 和 `apply` 任意顺序穿插，状态必须跨调用保留
- 空堆列表 / 空流的 `apply`

## Complexity & measured cost
O(n + k log n) 时间、O(n) 空间。编排者验证：Part 1 与"每次重新排序取最大"的独立暴力（非堆实现）在 300 组随机小输入上 0 不一致；Part 2 与同样的排序式暴力在穿插 add/apply 的 80 组随机操作序列上 0 不一致。perf：n=10⁵、k=10⁵ 两个 part 端到端均 < 2 s。

## Test inventory
21 tests — part1 11（含 3 参数化 worked examples、4 参数化非法输入、1 随机 brute-force、1 perf、1 io）· part2 8（含穿插一致性随机测试、非法输入、1 perf、1 io/fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
最大堆的标准应用（反复取最大+更新）· "规则已固定选择、只考数据结构效率"的贪心变体识别 · 在线服务化：批处理算法包装成跨调用保留状态的长期对象。
