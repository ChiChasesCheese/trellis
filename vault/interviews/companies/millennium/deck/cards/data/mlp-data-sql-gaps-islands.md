---
id: mlp-data-sql-gaps-islands
node: data.sql
type: qa
step: 4
---
## Q
**连续区间（gaps and islands）**｜SQL 分析查询

"一个交易员有交易的日期是 1 月 5、6、7、9、10 日。找出每一段连续的日期，以及最长的一段。"

## A
**做了什么。** 连续区间题叫 gaps and islands（断档与岛）。技巧：把日期转成整数，减去它在组内的排名；同一段连续日期里这个差恒定，一旦断档差就变，按差分组就切出每一段。

```
d      日期整数   rn   差 grp
01-05  100        1    99
01-06  101        2    99
01-07  102        3    99      → 岛一：01-05 到 01-07，3 天
01-09  104        4    100
01-10  105        5    100     → 岛二：01-09 到 01-10，2 天
```

```sql
WITH n AS (
  SELECT d,
         CAST(julianday(d) AS INTEGER)               -- 日期转整数（SQLite）
           - ROW_NUMBER() OVER (ORDER BY d) AS grp   -- 减去排名
  FROM (SELECT DISTINCT d FROM trades)               -- 先去重，否则同一天重复排名
)
SELECT MIN(d) AS start, MAX(d) AS end, COUNT(*) AS days
FROM n GROUP BY grp
ORDER BY days DESC, start LIMIT 1;                   -- 最长，并列取最早
```

- **坑：日期必须去重。** 同一天两笔交易会占两个排名，差值错位，一段连续日期被切开。
- **坑：什么算"一天"。** 现金分录那天不算交易日，先 `WHERE sym IS NOT NULL`。
- **多人时：** 窗口里加 `PARTITION BY trader`，外层 `GROUP BY trader, grp`。
- **其他数据库：** 日期整数换成 `d - ROW_NUMBER() OVER (…) * INTERVAL '1 day'`（PostgreSQL），思路相同。
- **周末：** 若周末不算断档，要用交易日历表的序号代替日期整数。

**英文答法。**
- "This is **gaps and islands**: I subtract the **row number** from the date, so each consecutive run shares one value."
- "I **deduplicate dates** first, then group by that value and take min, max and count."
- "Ties for the longest run go to the **earliest start**."
