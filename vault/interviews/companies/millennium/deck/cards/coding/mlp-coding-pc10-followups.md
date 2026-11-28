---
id: mlp-coding-pc10-followups
node: coding.pc10
step: 2
type: qa
---
## Q
**SQL 小题：追问与变体**｜编程轮

五个查询写完后，面试官会抓哪些点追问？

## A
- **`NOT IN` 为什么错：** 子查询结果里混进一个 NULL（garcia 有一条 symbol 为 NULL 的现金分录），`x NOT IN (a, b, NULL)` 对不等于 a、b 的 x 得到"未知"而不是"真"，于是对任何 x 都不满足条件，查询不报错、静默返回 0 行。
- **`NOT IN` 还能怎么救：** 子查询里加 `WHERE symbol IS NOT NULL`；或者改成 `NOT EXISTS`，或 `LEFT JOIN ... WHERE 右表键 IS NULL`。`NOT EXISTS` 是逐行的相关检查，NULL 只是匹配不上，不会污染其他行。
- **驱动表选哪个：** 第五题必须从 `instruments` 出发；用 `SELECT DISTINCT symbol FROM trades` 会漏掉从没被交易过的产品。
- **汇率缺失会怎样：** `LEFT JOIN` 找不到汇率时汇率是 NULL，乘积是 NULL，`SUM` 会跳过这一行，成交额被静默漏掉而不是报错；面试里主动讲出这个陷阱是加分项。
- **想要所有长度不小于 2 的连续区间：** 去掉最后一层按 trader 取第一名的窗口，直接在 `islands` 上过滤 `len >= 2`。
- **gaps and islands 为什么成立：** 日期序号和行号都逐日加一，连续时两者之差不变；中间断一天，序号多跳一格，差值就变了，按差值分组就切出每一段。
- **索引：** `trades(symbol, trade_date)` 支撑第一题；`trades(trader, ts)` 支撑第二题；`fx_rates(currency, rate_date)` 做主键，天然支撑第三题的连接。
- **会多花一个测试用例的边界：** `trades` 为空时前四题没有输出，第五题返回全部产品；全是美元计价的 desk；并列最长连续区间取起点最早的；窗口函数需要 SQLite 3.25 以上；金额用 `ROUND` 去掉浮点噪声。

**英文答法。**
- "`NOT IN` against a subquery with a **NULL** evaluates to unknown, so it silently returns no rows."
- "The difference between the date number and the **row number** is constant inside a consecutive run."
- "A missing FX rate gives a NULL, and `SUM` **skips** it, so the amount disappears without an error."
