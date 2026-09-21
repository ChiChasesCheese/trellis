# pc01 Grouped Aggregation — report

## Summary
Millennium LEaD 第一轮实时编码，一手报道的"百万行 CSV/DataFrame 按 id 分组求和，用分块+再聚合解决"
原题。3-part：Part 1 单遍纯 Python `dict` 流式累加（一手基本解）→ Part 2 按 `chunk_size` 切块、
每块独立聚合再合并，`workers>1` 时用 `ThreadPoolExecutor` 分发（一手原追问"chunking and
re-aggregating"）→ Part 3 复合键 `(id, category)` 分组、同时算 `sum`/`count`/`max`
**(reconstructed)**。

## Sources & confidence
HIGH（一手）：LeetCode Discuss 7423863（2025-12，Quant Developer-Python，Round 3）。Part 3 为重建。

## Approach by part
1. `csv.reader` 逐行解析 `id,amount`，`dict.get(key, 0) + amount` 累加；`Decimal` 全程避免浮点。
2. 把已物化的行序列按 `chunk_size` 切块，每块跑 Part 1 的函数得到局部 `dict`，再依次
   `_merge_totals` 合并；`workers>1` 用 `ThreadPoolExecutor.map` 并行跑每块的聚合，合并顺序不影响
   结果（加法结合律）。
3. 同一遍解析里对每个 `(id, category)` 复合键维护一个 `{"sum","count","max"}` 累加器。

## Pitfalls hidden tests target
- 分块与不分块结果必须逐分（Decimal）相等，且与 `workers` 无关（`test_chunked_with_workers_matches_sequential`、
  `test_chunked_matches_streaming_for_various_chunk_sizes` 覆盖 `chunk_size ∈ {1,2,3,5,100}`）
- 负数金额（退款）能正确拉低 `sum` 但不能污染 `max`（`test_part1_negative_amounts` / worked 例 3）
- 字段数不对、`id`/`category` 为空串、`amount` 非数字，三类非法输入都必须 `ValueError`，不能悄悄跳过
  或产出脏数据
- `chunk_size <= 0`、`workers <= 0` 必须 `ValueError`，不能死循环或返回空结果
- 输出排序与两位小数格式（`"6.00"` 不是 `"6"`）——`test_part1_output_sorted_and_two_decimals` /
  `test_part3_output_sorted_by_composite_key`
- 与 `pandas.DataFrame.groupby().sum()` 的独立交叉验证（`pytest.importorskip("pandas")`，核心逻辑本身
  不依赖 pandas）

## Complexity & measured cost
每行 O(1) 摊销（`csv` 解析 + 一次 dict 查找/写入）；Part 1/Part 2 整体 O(n)，Part 2 额外的切块/合并是
O(n) + O(块数 × 每块 distinct key 数)。Part 3 同样 O(n)，每行多维护两个字段。
实测：50 万行、2000 个 distinct id、`chunk_size=50_000, workers=4` 端到端 0.76s；纯单遍
`group_sum_streaming` 0.63s（均 < 2s 预算，`test_perf_500k_rows_chunked` 断言 < 2.0s）。

## Test inventory
23 tests（`grep -c "def test"`）— part1 9（含 5 组参数化非法输入、1 io、1 pandas 交叉验证）·
part2 7（含 5 组 chunk_size 参数化、1 perf、1 io）· part3 6（含 5 组参数化非法输入、1 io）；
edge 12 · fmt 2 · perf 1 · io 3。

## Skills exercised
S03 分组累加与流式解析 · S08 复杂度/并行模式（分发-合并、结合律保证确定性）· S02 精确金额处理
（`Decimal` + 显式舍入）。
