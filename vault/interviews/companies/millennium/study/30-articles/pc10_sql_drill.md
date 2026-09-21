# pc10 · SQL Drill：练的是"分组的 NULL 语义"和"NOT IN 遇 NULL 会静默清空结果"

> [!tldr]
> - 这题考的是：同一份数据、不同的问题，NULL 该不该被过滤是两回事；`NOT IN` 子查询里混进一个 NULL 会让整个查询悄悄返回空结果
> - 三步套路：先画清楚三张表怎么 join → 分组聚合和窗口函数都跑通 → gaps-and-islands 和 NOT EXISTS 是两个独立的"套路记忆点"
> - 最值得带走的一个模式：**任何"找出从未出现过的 X"的题，先问自己"NOT IN 的子查询里会不会混进 NULL"，混进就换 NOT EXISTS**

## 1. 题目在说什么（人话版）

三张表：`trades`（每笔成交）、`instruments`（每个 symbol 属于哪个 desk、用什么货币计价）、`fx_rates`（每种货币每天兑 USD 的汇率）。五道小题：

```
Part 1: 每个 symbol 每天成交了多少钱
Part 2: 每个 trader 最近一笔交易是什么
Part 3: 把所有交易换算成 USD，按 desk 汇总
Part 4: 每个 trader 连续交易的最长天数是多少天
Part 5: 有哪些 instrument 是 trader 'garcia' 从没交易过的
```

`trades` 里有一条特殊记录：`symbol` 是 `NULL`，代表一笔现金调整（不挂靠任何 instrument）。这条记录像一颗埋在数据里的地雷——五道小题对它的处理方式并不统一，这正是这道题真正在考的东西。

## 2. 读题：把文字变成模型

- **实体**：`trades`（事实表）、`instruments`（symbol 的维度）、`fx_rates`（货币的维度，按天变化）。
- **关键翻译**："每 symbol 每日成交额"是一次分组聚合；"每 trader 最新一笔"是一次"每组取一行"；"换算成 USD"是一次多表 join；"最长连续交易日"是一次 gaps-and-islands；"从未交易过"是一次集合差。
- **状态**：SQL 不需要你自己维护状态——这正是它和前面 Python 题的区别，"状态"全部由 `GROUP BY`/`PARTITION BY`/子查询表达。
- **一句话建模**：把每道小题先在纸上翻译成"我要对哪张表、按什么分组、聚合出什么"，再动笔写 SQL。

> [!note] 为什么现金分录要挑着过滤
> Part 1 问"这个 symbol 的成交额"，现金分录没有 symbol，天然不属于任何答案行，用 `JOIN instruments` 顺手排除。Part 2 问"这个 trader 最新一笔是什么"，如果这笔恰好是现金分录，那就是正确答案——过滤掉反而是错的。同一份 NULL，两种语义,两种处理方式。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：把 schema 抄一遍在草稿纸上，画出三张表怎么 join（`trades.symbol = instruments.symbol`，`instruments.currency + trades.trade_date = fx_rates.(currency, rate_date)`）。
2. **Part 1 最小可用**：`GROUP BY symbol, trade_date`，`SUM(ABS(qty) * price)`。立刻拿题面样例核对第一行。
3. **Part 2 叠加**：`ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC)`，外层 `WHERE rn = 1`。这一步不需要 join instruments——别把 Part 1 的过滤习惯带过来。
4. **Part 3 叠加**：先 join instruments 拿 desk/currency,再 `LEFT JOIN fx_rates`（不是 `JOIN`——否则 USD 计价的行会因为 fx_rates 没有 USD 记录而被整行丢弃），`CASE WHEN currency='USD' THEN 1.0 ELSE rate END` 短路。
5. **Part 4 叠加**：`julianday(date) - ROW_NUMBER() OVER (...ORDER BY date)`，这一步是记忆点，考前默写一遍。
6. **Part 5 收尾**：先写 `NOT IN` 版本让自己意识到哪里会踩 NULL 的坑,再改成 `NOT EXISTS`——面试官很吃"先写出常见错误、再自己指出为什么错"这个过程。

## 4. 代码怎么组织

```
schema.sql / seed.sql          # 三张表 DDL + 种子数据，测试从这两个文件建内存库
part1() -> str                  # 分组聚合
part2() -> str                  # 窗口函数取每组一行
part3() -> str                  # 多表 join + CASE 短路 + 按组汇总
part4() -> str                  # gaps-and-islands（三层 CTE）
part5() -> str                  # NOT EXISTS，驱动表选去重过的维度表
_connect() / main()             # 建库 + 按 PART n 执行 + 打印
```

五个函数互不调用（和前面几道 Python 题"后面的 part 复用前面的 helper"不一样）——SQL 题的复用发生在**技巧**层面（"这是同一个 as-of/分组/窗口套路"），不是代码层面。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```sql
-- Part 2：每组取一行，标准写法
WITH ranked AS (
    SELECT symbol, trader, trade_date, ts, qty, price,
           ROW_NUMBER() OVER (PARTITION BY trader ORDER BY ts DESC) AS rn
    FROM trades
)
SELECT trader, symbol, trade_date, ts, qty, price
FROM ranked WHERE rn = 1 ORDER BY trader;

-- Part 4：gaps-and-islands 的核心一行
-- 同一段连续日期内，"日期序号 - 组内排名"是常数；断档就变化，GROUP BY 它切出每一段
SELECT trader, trade_date,
       CAST(julianday(trade_date) AS INTEGER)
           - ROW_NUMBER() OVER (PARTITION BY trader ORDER BY trade_date) AS grp
FROM (SELECT DISTINCT trader, trade_date FROM trades WHERE symbol IS NOT NULL);

-- Part 5：NOT EXISTS，不怕子查询里有 NULL
SELECT i.symbol FROM instruments AS i
WHERE NOT EXISTS (
    SELECT 1 FROM trades AS t WHERE t.trader = 'garcia' AND t.symbol = i.symbol
);
```

## 6. Talking through it in the interview

- Before starting: "Let me sketch how the three tables join first — trades to instruments on symbol, instruments to fx_rates on currency and date — before I write any query."
- Writing Part 2: "I'm partitioning by trader and ordering by timestamp descending, then taking rank one — that's the standard 'one row per group' pattern instead of a correlated MAX subquery."
- Writing Part 5: "If I write this as `NOT IN`, the subquery can return a NULL — trader garcia has a cash trade with no symbol — and a `NOT IN` list containing NULL makes the whole comparison UNKNOWN for every row, so the query silently returns nothing. `NOT EXISTS` sidesteps that because it's a per-row correlated check."
- On delivery: "All five pass against the seed data; the one I'd flag as worth double-checking in production is part3 — a missing FX rate for a given day doesn't error, it just quietly drops that trade's contribution to the sum."

## 7. 常见跑偏（方法层面，3 条）

- 把 Part 1 的"join 掉 NULL symbol"这个习惯原样搬到 Part 2：Part 2 的语义是"最新一笔"，现金分录如果就是最新的,过滤掉反而是错答案——每道题先想清楚 NULL 该不该被过滤，不要复制上一题的写法。
- gaps-and-islands 记成"排序后比较相邻行的差"（自连接或 `LAG`）：能做对但代码更长；`julianday(date) - ROW_NUMBER()` 是这个套路的标准写法,考前应该能不看提示写出来。
- Part 5 想当然地写 `NOT IN`：这是 SQL 面试里最经典的陷阱之一,不是这道题独有——遇到"找出集合差"类问题,第一反应应该是"子查询会不会有 NULL"，而不是先写完再调试。

## 8. 同族题 / 延伸

- 本 kit `pc09_price_data_store`：同样是"as-of / 区间查询"的话题，但用 Python + `bisect` 实现；对照着看能看出 SQL 窗口函数和手写二分是同一类问题的两种解法。
- 练习命令：`python3 loop/mock.py start pc10`
