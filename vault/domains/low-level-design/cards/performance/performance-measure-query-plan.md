---
id: performance-measure-query-plan
node: performance.measure-first
type: qa
step: 3
---
## Q
销售报表接口有一个可选的 region 过滤，SQL 写成 `WHERE (:r IS NULL OR region = :r)`，这样一条语句就能处理“有”和“没有”两种情况。`region` 上明明有索引，为什么查询还是慢？不猜，怎么确认？

## A
**慢查询别猜，看数据库的执行计划**

- **`EXPLAIN QUERY PLAN`** 说明数据库打算怎么执行：`SCAN` 是整表扫描，`SEARCH ... USING INDEX` 是走索引；
- **“参数为空就不过滤”的写法让优化器无法提前选索引**：语句是固定的，计划要同时适用于有参数和没参数两种情况，所以退回整表扫描；
- **按有没有过滤条件拼出不同的 SQL**：有 region 时用 `WHERE region = ?`，没有时不加 `WHERE`；条件拼接的是固定的列名片段，值仍然用 `?` 绑定，不会有注入；
- **确认后再量时间**：计划变了、耗时也要下降才算数；
- **区分度越高，差距越大**：下面的 8 个地区每个占 1/8，只差约 1.5 倍；区分度是千分之一时，整表扫描和索引查找的差距要大得多。

实测（3.11，SQLite 3.53.1，本机，20 万行、8 个地区，`region` 有索引，查某一个地区的合计）：

| 写法 | 执行计划 | 耗时 |
|---|---|---|
| `(? IS NULL OR region = ?)` | `SCAN s` | 3.1 ms |
| `region = ?` | `SEARCH s USING INDEX ix (region=?)` | 2.1 ms |

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE s(id INTEGER PRIMARY KEY, region TEXT, amt INT)")
db.execute("CREATE INDEX ix ON s(region)")
for q, args in (("SELECT SUM(amt) FROM s WHERE (? IS NULL OR region = ?)", ("A", "A")),
                ("SELECT SUM(amt) FROM s WHERE region = ?", ("A",))):
    print(db.execute("EXPLAIN QUERY PLAN " + q, args).fetchall()[0][3])
# SCAN s
# SEARCH s USING INDEX ix (region=?)
```

代码只演示两种写法的执行计划；“按有没有过滤条件拼不同语句”就是第二条那种固定写法，由调用方选择用哪一条。

**知识点：**先测量（Measure First）
