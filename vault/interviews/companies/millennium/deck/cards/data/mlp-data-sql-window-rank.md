---
id: mlp-data-sql-window-rank
node: data.sql
type: qa
step: 2
---
## Q
**窗口函数：ROW_NUMBER、RANK、每组取一行**｜SQL 分析查询

"每个交易员最近的一笔交易是哪笔？成交额并列时 ROW_NUMBER、RANK、DENSE_RANK 有什么区别？"

## A
**做了什么。** 窗口函数（window function）在不压缩行数的前提下，为每一行算一个"看着同组其他行"的值。`PARTITION BY` 划分组，`ORDER BY` 决定组内顺序。

三种排名遇到并列时不同（分数 90、90、80）：

```
score  ROW_NUMBER  RANK  DENSE_RANK
90     1           1     1
90     2           1     1
80     3           3     2
```

```sql
WITH ranked AS (
  SELECT trader, sym, ts, qty, px,
         ROW_NUMBER() OVER (PARTITION BY trader
                            ORDER BY ts DESC) AS rn   -- 每人内部按时间倒排
  FROM trades
)
SELECT trader, sym, ts, qty, px
FROM ranked
WHERE rn = 1;                                          -- 每人只留最新一笔
```

- **ROW_NUMBER：** 并列也给不同号码，每组恰好一行，适合"每组取一行"。
- **RANK：** 并列同号，后面跳号（1,1,3）；**DENSE_RANK：** 并列同号，不跳号（1,1,2），适合"第 N 高的值"。
- **坑：窗口函数不能直接写进 WHERE。** 要先放进子查询或 CTE（WITH），再在外层筛 `rn = 1`。
- **坑：并列时 ROW_NUMBER 结果不确定。** 在 ORDER BY 末尾补一个唯一列（如 `trade_id`）。
- **坑：别过滤掉 NULL 行。** 如果某人最新一笔恰好是现金分录（`sym` 为 NULL），它就是答案。

**英文答法。**
- "I use **ROW_NUMBER partitioned by trader**, ordered by timestamp descending, and keep row one."
- "For ties I'd add a **tiebreaker** like the trade id."
- "If I need ties to share a rank, I switch to **RANK** or **DENSE_RANK**."
