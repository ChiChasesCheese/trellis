# pc12 Top Two Users by Total Purchase Amount — report

## Summary
fastprep.io 一手 Easy 电面题（按用户求和取 top two）。做成 3-part：Part 1 原题 → Part 2 按天分组 top-k **(reconstructed)** → Part 3 流式更新 + 退款 + 任意时刻查询 **(reconstructed)**。

## Sources & confidence
MED（fastprep.io，Easy/Phone Screen，2026-06 报告）；Part 2/3 未见一手报道，按聚合排名类暖场题最常见追问方向重建。

## Approach by part
1. 金额一律用字符串切分成"整数部分 + 两位小数"转成整数分，绝不经过 `float`；哈希表按用户累加，按 `(-总额, 用户名)` 排序取前二。
2. 按日期分组后复用 Part 1 的求和/排序逻辑，`k` 截断到该天参与排名的用户数以内。
3. 事件流顺序处理：金额更新（允许负数）累加进运行总额，`QUERY` 事件对当前哈希表排序取前二并记入快照列表；退款可以让总额变负，但该用户仍在候选池里参与比较。

## Pitfalls hidden tests target
- 金额格式必须是"整数.两位小数"，否则 `ValueError`（`"5"`、`"5.001"`、`"5.1"` 都要拒绝）
- Part 1/2 里出现负数金额要拒绝（这两个 part 没有退款语义）；Part 3 则必须接受负数
- 打平按用户名升序（例 1 的 bob/carol、例 3 的 alice/bob 都是同额打平）
- 大量小额度累加不能有浮点误差（1000 笔 0.10 必须恰好等于 10000 分）
- Part 2 的 `k = 0`（日期仍要出现，只是列表为空）
- Part 3 在任何购买之前查询（空快照）、没有任何 QUERY（返回空列表）
- Part 3 退款把总额打到负数后依然参与排名

## Complexity & measured cost
Part 1/2 均 O(记录数 + 排序)；Part 3 每次 QUERY 是 O(用户数 log 用户数) 全量重排，10 万事件、2000 个用户、约 0.1% 概率触发 QUERY 的随机流实测 < 2s。编排者用 `decimal.Decimal` 独立实现的暴力求和在 200/150 组随机小输入上分别交叉验证 Part 1 和 Part 3 的运行总额与排名，0 不一致。

## Test inventory
27 tests — part1 11（含 2 样例、6 参数化格式错误、1 perf 无、1 io）· part2 6（含 1 样例、1 fmt、1 io）· part3 10（含 1 样例、1 fmt、1 perf、1 io）；edge 15 · fmt 2 · perf 1 · io 3。

## Skills exercised
S06 计数/聚合哈希 + 确定性排序 tie-break（与 pc03、pc11 同一类考法）· 货币整数化处理，规避浮点累加误差 · 流式状态维护与"任意时刻查询"的接口设计
