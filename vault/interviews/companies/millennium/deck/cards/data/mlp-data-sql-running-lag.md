---
id: mlp-data-sql-running-lag
node: data.sql
type: qa
step: 3
---
## Q
**窗口函数：累计和与 LAG**｜SQL 分析查询

"每天的净成交量，再加上累计和，以及比前一天多多少？"

## A
**做了什么。** 聚合函数加上 `OVER (ORDER BY …)` 就成了累计（running）版本：每一行看到从开头到自己的所有行。`LAG(x)` 取上一行的 x，`LEAD(x)` 取下一行的。

```
d        net   running   prev   change
01-05    35    35        NULL   NULL
01-06     4    39        35     -31
01-07     1    40         4     -3
```

```sql
WITH daily AS (
  SELECT d, SUM(qty) AS net FROM trades GROUP BY d   -- 先压成每天一行
)
SELECT d, net,
       SUM(net) OVER (ORDER BY d)  AS running,       -- 累计和
       LAG(net)  OVER (ORDER BY d) AS prev,          -- 前一天
       net - LAG(net) OVER (ORDER BY d) AS change
FROM daily;
```

- **窗口函数在分组之后计算：** 所以可以对每天的合计再做累计；要按交易员各自累计，加 `PARTITION BY trader`。
- **LAG 第一行是 NULL：** 差值也是 NULL；需要默认值时写 `LAG(net, 1, 0)`，第三个参数是缺省值。
- **坑：默认窗口范围。** 写了 `ORDER BY` 但没写框架时，默认是"从头到当前行及所有排序值相同的行"（RANGE）；日期有重复时，累计值会把同一天的几行一次加进来，看上去重复。要逐行累计，写 `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。
- **坑：没有 ORDER BY，LAG 和累计没有意义。**

**英文答法。**
- "I **aggregate to one row per day** first, then apply window functions."
- "**SUM over ORDER BY** gives the running total, and **LAG** gives the previous day."
- "I specify **ROWS** frame explicitly so ties on the date don't change the running sum."
