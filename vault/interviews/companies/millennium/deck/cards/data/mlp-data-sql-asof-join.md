---
id: mlp-data-sql-asof-join
node: data.sql
type: qa
step: 5
---
## Q
**as-of 关联：取不晚于当天的最新汇率**｜SQL 分析查询

"成交要换算成美元，汇率表只在部分日期有记录。某笔成交那天没有汇率，该用哪个？SQL 怎么写？"

## A
**做了什么。** as-of 关联是"对每一行，取不晚于它的时间点上最新的一条记录"，也就是 pandas `merge_asof` 的 SQL 版。用相关子查询：对每笔成交，在汇率表里找 `rate_date <= 成交日` 的最大那条。

```
fx（EUR）               成交 trades         换算后
rate_date   rate        id  date    amt     id  date    usd
01-02       1.10        1   01-05   100     1   01-05   110.0   ← 用 01-02 的 1.10
01-06       1.20        2   01-06   100     2   01-06   120.0   ← 当天有
                        3   01-01   100     3   01-01   NULL    ← 之前没有任何汇率
```

```sql
SELECT t.id, t.td,
       t.amt * (SELECT f.r
                FROM fx AS f
                WHERE f.cur = t.cur
                  AND f.rd <= t.td          -- 不晚于成交日：不看未来
                ORDER BY f.rd DESC
                LIMIT 1) AS usd             -- 其中最新的一条
FROM trades AS t;
```

- **关键是 `<=`：** 用 `<` 会漏掉当天有汇率的情形，用 `>=` 是用未来的汇率，造成前视偏差（look-ahead bias）。
- **没有更早的记录：** 子查询返回 NULL，乘积也是 NULL，`SUM` 会悄悄跳过这一行；要主动检查或用 `COALESCE` 报错。
- **坑：用等值 join 会丢行或变 NULL。** `JOIN … ON f.rd = t.td` 在没有汇率的日子找不到配对。
- **规模大时：** 汇率表上建 `(cur, rd)` 的索引；也可以改成窗口函数或 PostgreSQL 的 `LATERAL`。

**英文答法。**
- "I want the **latest rate at or before** the trade date, so I use a **correlated subquery** with `rd <= trade date`, order descending, limit one."
- "I never use a **later** rate, that would be look-ahead."
- "Rows with **no earlier rate** come back NULL, and I'd flag them."
