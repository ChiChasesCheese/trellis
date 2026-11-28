---
id: mlp-data-sql-null-logic
node: data.sql
type: qa
step: 6
---
## Q
**NULL 的三值逻辑与 NOT IN 陷阱**｜SQL 分析查询

"找出某交易员从没交易过的代码。他有一笔现金分录，代码为 NULL。写 `NOT IN` 为什么返回 0 行？"

## A
**做了什么。** SQL 的 NULL 表示"未知"，所以逻辑有三个值：真、假、未知。`WHERE` 只放行结果为真的行，未知和假一样被丢掉。

```
x = NULL          → 未知（NULL = NULL 也是未知）
x <> 1  (x 为 NULL) → 未知
1 NOT IN (2, NULL) → 未知   （要求 1≠2 且 1≠NULL，后者未知）
```

数据：集合 s 里有 1、2、NULL 三行。

```
s = {1, 2, NULL}      s.x NOT IN (1)        → 只有 2；NULL 行被丢
                      COUNT(*) = 3, COUNT(x) = 2, AVG(x) = 1.5   ← NULL 不参与聚合
```

```sql
-- 错：子查询结果里混进一个 NULL，对每个候选都变成"未知"，返回 0 行
SELECT symbol FROM instruments
WHERE symbol NOT IN (SELECT symbol FROM trades WHERE trader = 'garcia');

-- 对：逐行相关子查询，NULL 只是"不匹配"
SELECT i.symbol FROM instruments AS i
WHERE NOT EXISTS (SELECT 1 FROM trades AS t
                  WHERE t.trader = 'garcia' AND t.symbol = i.symbol);
```

- **坑：`NOT IN` 遇到 NULL 静默返回空。** 不报错，只是错得很安静；补救是子查询里加 `WHERE symbol IS NOT NULL`，更稳妥是 `NOT EXISTS`。
- **判断空值只能用 `IS NULL` / `IS NOT NULL`：** `= NULL` 永远不为真。
- **聚合跳过 NULL：** `AVG` 的分母不含 NULL 行；要当 0 算先 `COALESCE(x, 0)`。
- **驱动表选对：** 用 `instruments` 而不是 `SELECT DISTINCT symbol FROM trades`，否则从没被交易过的代码根本不在结果里。

**英文答法。**
- "`NOT IN` breaks if the subquery returns a **NULL**: the comparison becomes **unknown**, so I get zero rows."
- "I use **NOT EXISTS** instead, driven from the **instruments** table."
- "To test for null I use **IS NULL**, never equals."
