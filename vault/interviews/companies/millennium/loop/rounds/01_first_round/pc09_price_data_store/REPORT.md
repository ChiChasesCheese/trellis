# pc09 Price Data Store — report

## Summary
一手报道：Millennium LEaD 第一轮 45 min 编码（LeetCode Discuss 7423863 Round 5，重开的技术轮）出现过一道 "price data design problem"，只留下题名。3-part：Part 1 时间序列价格存储（乱序写入、`latest`/`as_of`，一手题名对应）→ Part 2 区间聚合 `ohlc`/`vwap`（同一存储结构的自然延伸）→ Part 3 多币种换算（对应 QuantVault OA "multi-currency PnL"）**(reconstructed)**。三个 part 共用一个考点：用"按 `ts` 排序的列表 + 二分"而不是"只 `append` 的 dict-of-list"，因为写入天然乱序到达。

## Sources & confidence
HIGH（一手）：LeetCode Discuss 7423863（Quant Dev-Python，Round 5）"price data design problem"，仅有题名。PracHub 2026-02-12（口头技术筛）"How would you model stock price prediction?" 是同一话题的独立佐证，不是同一道编码题。QuantVault Millennium OA 题单 "multi-currency PnL" 对应 Part 3 的换算需求。Part 1/2 的具体 API 与全部 worked examples、Part 3 的 `FXTable`/`price_in_base` 设计均为按题名重建，标 (reconstructed)。

## Approach by part
1. 每个 symbol 维护一个按 `ts` 排序的列表（`bisect.insort` 插入）+ `ts -> Decimal price` / `ts -> Decimal volume` 字典。`latest` 取列表末尾；`as_of` 用 `bisect_right - 1` 找 `<= ts` 的最新一条；两者都是 O(log n)。同一 `(symbol, ts)` 重复写入直接覆盖字典值，不重复插入排序列表。
2. `ohlc`/`vwap` 用 `bisect_left`/`bisect_right` 切出 `[t0, t1]` 对应的子列表：`open`/`close` 取子列表首尾（时间序，不是插入序），`high`/`low` 取子列表价格的 max/min；`vwap` 用 `Decimal` 精确累加 `Σ(price·volume)` 和 `Σ(volume)` 再相除，总成交量为 0 时显式 `ValueError`（不是让它抛 `ZeroDivisionError`）。
3. `FXTable` 复用与 `PriceStore.as_of` 完全相同的 `_as_of_lookup` 二分函数（同一存储技巧，"symbol" 换成了货币对）。`price_in_base` 先查正向货币对（乘），查不到再查反向（除），都查不到才 `LookupError`；同币种直接短路，不碰汇率表。四舍五入只在 `_fmt`（展示层）发生一次：`quantize(Decimal("0.0001"), ROUND_HALF_UP)`；所有类方法返回的都是未舍入的精确 `Decimal`。

## Pitfalls hidden tests target
- Part 1：乱序写入后 `latest` 必须是"`ts` 最大"而不是"最后一次调用 `upsert`"（`test_worked_example_out_of_order_and_overwrite`）；同 `ts` 重复写入覆盖旧值，且旧的排序列表条目不能重复插入；`as_of` 早于最早记录 → `LookupError`，查询不存在的 symbol → `KeyError`（两种"没找到"故意分开）；`price`/`volume`/`rate` 传 `float` 一律 `ValueError`（金额不能浮点累加）；`ts` 传 `bool` 要按非法值处理（`isinstance(x, bool)` 在 Python 里也是 `isinstance(x, int)`，容易漏判）。
- Part 2：`ohlc` 的 open/close 必须按时间顺序而不是插入顺序取值（`test_ohlc_subrange_uses_time_order_not_insertion_order` 故意乱序插入验证）；`t0 > t1` 与"区间内无数据"是两种不同的失败（`ValueError` vs `LookupError`）；`vwap` 区间内有数据但总成交量为 0 是第三种失败（`ValueError`，除零）；四舍五入用 `ROUND_HALF_UP`，`1.00005 + 1.00005` 平均得到 `1.00005` 的精确值，展示层必须进位到 `1.0001` 而不是银行家舍入到 `1.0000`。
- Part 3：同币种换算不能查汇率表（用一个空 `FXTable` 验证，查了就会抛 `LookupError` 而不是拿到正确答案）；只发布反向货币对时必须用 `1/rate`；两个方向都没有汇率 → `LookupError`；`rate <= 0` → `ValueError`。

## Complexity & measured cost
`upsert` 均摊 O(1)（近似递增写入场景，`bisect.insort` 插在末尾）到 O(n)（真正乱序写入需要挪动元素）；`latest`/`as_of` O(log n)；`ohlc`/`vwap` O(log n + 命中数)。性能测试：10 万条近似递增写入的 tick（`price = 100 + i % 50` 让 high/low 可预测）+ 一次全区间 `OHLC`/`VWAP`，作为脚本端到端运行，编排者实测约 0.3–0.7 s，< 2 s 预算（见 `test_perf_100k_upserts_mostly_increasing_ts`）。

## Test inventory
`test_pc09.py`：25 个 `def test`（其中 1 个 5 组参数化，pytest 收集到 29 个测试用例，全部通过 `solution.py`）。按 marker：part1 10 def（含 1 io、1 fmt）· part2 8 def（含 1 perf、1 io、1 fmt）· part3 7 def（含 1 io）；edge 12 def · fmt 2 · perf 1 · io 3。`grep -c "def test" test_pc09.py` = 25。`solution.py` 全绿（29 passed）；`IMPL=starter` 28 failed / 1 passed（唯一通过的是空操作列表返回空列表这个平凡用例，其余全红）。

## Skills exercised
维护一个始终按 key 排序的结构以支持二分（而不是假设插入顺序 = 排序顺序）· as-of / 区间查询的二分实现（`bisect_left`/`bisect_right`）· 金额用 `Decimal`，舍入规则只在输出边界生效一次 · 区分"key 不存在"（`KeyError`）与"key 存在但这个范围没数据"（`LookupError`）两种失败模式 · 把同一套存储技巧（as-of 查找）复用到第二个领域（FX 汇率）而不是重写一遍。
