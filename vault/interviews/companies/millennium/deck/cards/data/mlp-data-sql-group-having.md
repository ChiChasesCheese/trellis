---
id: mlp-data-sql-group-having
node: data.sql
type: qa
step: 1
---
## Q
**GROUP BY 与 HAVING**｜SQL 分析查询

"每个交易员成交额是多少？只看成交笔数不少于 3 笔的交易员。WHERE 和 HAVING 放哪个？"

## A
**做了什么。** `GROUP BY` 把行按列值分组，每组聚合成一行。执行顺序是 FROM → WHERE → GROUP BY → HAVING → SELECT：`WHERE` 在分组前筛行，`HAVING` 在分组后筛组。

```
trader  sym   qty  px         trader  n  value
al      AAPL   10  150        al      3  3608
al      MSFT    5  300   →    bo      3  3631
al      AAPL   -4  152
bo      AAPL   20  150        （共 6 行，每人 3 笔，都过了 HAVING）
bo      VOD     8   70
bo      VOD     1   71
```

```sql
SELECT trader,
       COUNT(*)                 AS n,
       SUM(ABS(qty) * px)       AS value   -- 成交额与买卖方向无关，取绝对值
FROM trades
WHERE sym IS NOT NULL           -- 分组前：去掉现金分录
GROUP BY trader
HAVING COUNT(*) >= 3;           -- 分组后：按聚合结果筛
```

- **坑：聚合条件写进 WHERE 会报错。** `WHERE COUNT(*) >= 3` 不合法，因为分组还没发生。
- **坑：SELECT 里的非聚合列必须出现在 GROUP BY。** 否则标准 SQL 报错，个别数据库返回任意一行，结果不稳定。
- **`COUNT(*)` 与 `COUNT(列)`：** 前者数行，后者不数该列为 NULL 的行。
- **`SUM` 遇到整组都是 NULL 时返回 NULL**，不是 0；需要 0 时写 `COALESCE(SUM(x), 0)`。

**英文答法。**
- "I **filter rows** with WHERE first, then **group by** trader."
- "The condition on the count goes in **HAVING**, because it applies after grouping."
- "I use the **absolute quantity**, since notional doesn't depend on direction."
