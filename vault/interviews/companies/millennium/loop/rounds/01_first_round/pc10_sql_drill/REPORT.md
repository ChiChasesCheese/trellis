# pc10 SQL Drill — report

## Summary
三条独立一手报道（1p3a thread-1079245 / 855488 / 939377）与一条 Blind 摘要共同确认 Millennium 的技术筛里混了 SQL 环节，强调"速度"，但均未留下具体题面。五道小题按"SQL 基础"考纲重建 **(reconstructed)**：Part 1 分组聚合（每 symbol 每日成交额）→ Part 2 窗口函数取每组一行（每 trader 最新一笔）→ Part 3 多表 join 换算货币按 desk 汇总 → Part 4 gaps-and-islands 求最长连续交易日 → Part 5 `NOT IN` 遇 NULL 静默返回空结果的经典陷阱，正确写法是 `NOT EXISTS`。三张表 `trades`/`instruments`/`fx_rates` 的 DDL 与种子数据在 `schema.sql`/`seed.sql`，本目录的 `conftest.py` 提供一个按这两个文件从零建库的 `db` fixture。

## Sources & confidence
MED-HIGH：1point3acres thread-1079245（Developer OA，2 h/5 题，"SQL 基础、Python decorator"）、thread-855488（Quant/FE OA，3 h/4 题，"SQL 一题挂"）、thread-939377（DS/DE OA，120 min/8 题，"1 SQL + 1 coding"）三条独立报道都确认 SQL 环节存在；Blind 摘要（"mix of Python and SQL, main thing is speed"）独立佐证。均未给出具体题面，五个小题、schema、种子数据、worked examples 全部标 (reconstructed)。

## Approach by part
1. `trades JOIN instruments` 再 `GROUP BY symbol, trade_date`：join 天然把 `symbol IS NULL` 的现金分录排除掉，不需要额外 `WHERE`；`SUM(ABS(qty) * price)` 不区分买卖方向，`ROUND(..., 2)` 消除浮点噪声。
2. `ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC)` 取每个 trader 排名第一的行；故意**不**过滤 `symbol IS NULL`，因为"最新一笔交易"如果恰好是现金分录，那就是正确答案——这一步和 Part 1 的 NULL 处理方向刻意相反,用来考察候选人是否会不假思索地复制 Part 1 的过滤逻辑。
3. `trades JOIN instruments`（拿 desk/currency）`LEFT JOIN fx_rates ON (currency, trade_date)`（拿当日汇率），`CASE WHEN currency='USD' THEN 1.0 ELSE rate END` 让 USD 计价的 instrument 不需要 `fx_rates` 里有自身货币的记录，按 `desk` 汇总。
4. `julianday(trade_date) - ROW_NUMBER() OVER (PARTITION BY trader ORDER BY trade_date)` 是 gaps-and-islands 的标准技巧：同一段连续日期内这个差值恒定；`trading_days` CTE 先用 `DISTINCT ... WHERE symbol IS NOT NULL` 排除现金分录当天，再分组、取每个 trader 最长的一段（并列取起始最早）。
5. 从 `instruments`（主键天然去重、覆盖零交易的 symbol）出发 `NOT EXISTS` 相关子查询，避免 `NOT IN` 子查询里混进 `trades.symbol IS NULL` 时整个表达式对所有候选行变 `UNKNOWN` 而静默清空结果集的经典陷阱。

## Pitfalls hidden tests target
- Part 1：现金分录（`symbol IS NULL`）绝不能出现在任何输出行（`test_part1_drops_the_null_symbol_cash_trade`）；金额必须四舍五入到 2 位小数，不能带浮点噪声。
- Part 2：`garcia` 的现金分录恰好是它最新一笔交易，输出里 `symbol` 字段必须是 `NULL`——如果候选人照搬 Part 1 的 `JOIN instruments` 思路，这一行会被误删（`test_part2_keeps_null_symbol_when_it_really_is_the_latest_trade`）；每个 trader 必须恰好一行，不能因为 `ORDER BY ts DESC` 没有唯一 tie-break 而重复或漏掉。
- Part 3：`FX` desk（只有 USD 计价的 `EURUSD`）在 `fx_rates` 完全没有 `USD` 记录的情况下也必须算对，验证 `CASE` 短路生效而不是被 `LEFT JOIN` 的 `NULL` 拖垮。
- Part 4：`sqlite3.sqlite_version_info >= (3, 25, 0)` 是窗口函数的前提，专门有一个测试断言它（而不是假设 CI/HackerRank 环境一定支持）；`garcia` 现金分录那天不能计入交易日；两段等长（`garcia` 的 01-05 与 01-07）必须取起始日期更早的一段，不能取"先算出来的那段"（依赖排序稳定性）。
- Part 5：直接在测试里写死一份"错误的" `NOT IN` 查询跑一遍，断言它在这份种子数据上返回 0 行——用真实执行结果而不是复述规则来证明陷阱确实存在；`ORPHAN`（零交易记录的 instrument）必须出现在结果里，用来验证驱动表选的是 `instruments` 而不是 `SELECT DISTINCT symbol FROM trades`。

## Complexity & measured cost
Part 1–3、5 都是单次分组/join/相关子查询，O(n log n)（排序/分组）到 O(n·m)（Part 5 的 `NOT EXISTS` 在 sqlite 里会被优化成半连接，配合 `instruments` 主键索引接近 O(n)）。Part 4 的窗口函数是 O(n log n)。性能测试：5 万条合成交易（200 个 trader，跨约 300 天，制造大量连续段与断档）灌入一个新建的内存库，执行 Part 4 的完整 SQL（窗口函数 + 三层 CTE），编排者实测远小于 2 s 预算（见 `test_perf_part4_streaks_over_50k_synthetic_trades`）。

## Test inventory
`test_pc10.py`：20 个 `def test`，全部通过 `solution.py`（20 passed）；`IMPL=starter`（每个 part 返回 `""`）16 failed / 4 passed——4 个通过的是"空表应该无输出"和"sqlite 版本检查"这类对空字符串 SQL 也恰好成立的退化用例,其余全红。按 part marker：part1 4（含 1 fmt）· part2 4（含 1 io）· part3 3 · part4 5（含 1 perf）· part5 4（含 1 io）；按辅助 marker：edge 11 · fmt 1 · perf 1 · io 2。`grep -c "def test" test_pc10.py` = 20。

## Skills exercised
分组聚合的两种典型 NULL 处理策略对比（Part 1 用 join 排除 vs Part 2 刻意保留）· 窗口函数做"每组取一行"（`ROW_NUMBER` + `PARTITION BY` + `ORDER BY ... DESC`）· 多表 join 换算货币时用 `CASE` 短路避免不必要的维表依赖 · gaps-and-islands 通用解法（日期差值分组）· `NOT IN` vs `NOT EXISTS` 在 NULL 面前的语义差异，以及用真实查询结果（而不是背书）验证这个差异。
