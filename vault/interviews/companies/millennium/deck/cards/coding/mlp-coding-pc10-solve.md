---
id: mlp-coding-pc10-solve
node: coding.pc10
step: 1
type: qa
---
## Q
**SQL 小题：题与解**｜编程轮

三张表：`instruments(symbol, desk, currency)` 是产品清单（desk 是交易台），`trades(trade_id, symbol, trader, trade_date, ts, qty, price)` 是成交（`qty` 正为买、负为卖；`symbol` 为 NULL 的是现金调整分录），`fx_rates(currency, rate_date, rate_to_usd)` 是每日汇率。写五个查询：一，每个 symbol 每天的成交额；二，每个 trader 最新的一笔；三，换算成美元后按 desk 汇总成交额；四，每个 trader 最长的连续交易日；五，trader `garcia` 从没交易过的产品。

## A
**一句话思路。** 一，分组聚合；二，窗口函数 `ROW_NUMBER` 在每组里取第一行；三，`JOIN` 加 `LEFT JOIN` 汇率表；四，连续区间用"日期序号减行号恒定"分组（gaps and islands）；五，用 `NOT EXISTS`，不用 `NOT IN`。每题都要先想 NULL 该不该算：第一题要排除现金分录，第二题却要保留它。

```sql
-- 1. 每 symbol 每日成交额：JOIN instruments 顺带排除 symbol 为 NULL 的现金分录
SELECT t.symbol, t.trade_date, ROUND(SUM(ABS(t.qty) * t.price), 2) AS notional
FROM trades t JOIN instruments i ON i.symbol = t.symbol
GROUP BY t.symbol, t.trade_date
ORDER BY t.symbol, t.trade_date;

-- 2. 每个 trader 最新一笔：窗口函数在每个 trader 内按时间倒序编号，取 1
--    这里不过滤 NULL：现金分录若是他最新的一笔，它就是答案
WITH ranked AS (
  SELECT trader, symbol, trade_date, ts, qty, price,
         ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC) AS rn
  FROM trades)
SELECT trader, symbol, trade_date, ts, qty, price FROM ranked WHERE rn = 1 ORDER BY trader;

-- 3. 换算成美元，按 desk 汇总：美元计价的 CASE 短路，不要求汇率表里有 USD 一行
SELECT i.desk,
       ROUND(SUM(ABS(t.qty) * t.price *
             CASE WHEN i.currency = 'USD' THEN 1.0 ELSE fx.rate_to_usd END), 2) AS usd_notional
FROM trades t
JOIN instruments i ON i.symbol = t.symbol
LEFT JOIN fx_rates fx ON fx.currency = i.currency AND fx.rate_date = t.trade_date
GROUP BY i.desk ORDER BY i.desk;

-- 4. 最长连续交易日（gaps and islands）
WITH days AS (
  SELECT DISTINCT trader, trade_date FROM trades WHERE symbol IS NOT NULL),  -- 现金分录那天不算交易日
numbered AS (
  SELECT trader, trade_date,
         CAST(julianday(trade_date) AS INTEGER)
           - ROW_NUMBER() OVER (PARTITION BY trader ORDER BY trade_date) AS grp  -- 连续日期内恒定，断档就变
  FROM days),
islands AS (
  SELECT trader, MIN(trade_date) AS s, MAX(trade_date) AS e, COUNT(*) AS len
  FROM numbered GROUP BY trader, grp),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY trader ORDER BY len DESC, s) AS rn FROM islands)  -- 并列取最早
SELECT trader, s, e, len FROM ranked WHERE rn = 1 ORDER BY trader;

-- 5. garcia 没交易过的产品：从 instruments 出发（含从未被交易的），用 NOT EXISTS
SELECT i.symbol FROM instruments i
WHERE NOT EXISTS (SELECT 1 FROM trades t WHERE t.trader = 'garcia' AND t.symbol = i.symbol)
ORDER BY i.symbol;
```

**复杂度。** 第一、三题一次扫描加分组；第二、四题多一次按分区排序，O(n log n)；第五题配合 `trades(trader, symbol)` 索引，每个产品一次索引查找。

**边写边讲。**
- "I join to `instruments` so the cash entries with a **NULL symbol** drop out; for latest-trade I keep them on purpose."
- "`ROW_NUMBER` over a partition is the direct way to **pick one row per group**."
- "I use `NOT EXISTS` because `NOT IN` with a **NULL** in the subquery silently returns nothing."
