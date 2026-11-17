---
id: data-optional-sql-null-compare
node: data.optional
type: qa
step: 4
---
## Q
`SELECT ... WHERE region != 'US'` 为什么漏掉了 `region` 是 `NULL` 的行？“不给 region 筛选”和“筛选 region 为某值”两种查询，对 `NULL` 的行各该怎样？

## A
**NULL 与任何值比较，结果是“未知”**

- **三值逻辑**：`NULL = 'US'` 和 `NULL != 'US'` 都是未知，`WHERE` 只放行真，两种写法都滤掉这行；
- **指定了 region**：具体值匹配不到 `NULL` 行，这是合同该有的行为，要写下来；
- **没指定 region**：不加条件，`NULL` 行照常参与统计；不要写 `region IS NOT NULL` 顺手排除；
- **要把 `NULL` 当一种取值**：用 `IS NULL`，或者 `region IS NOT 'US'`（SQLite 的 `IS NOT` 把 `NULL` 当普通值比较）；
- **缺日期的行**：`WHERE day >= ?` 本来就滤掉 `NULL`，不必再写 `day IS NOT NULL`；写了反而说明作者不清楚三值逻辑。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table s (id int, region text)")
db.executemany("insert into s values (?, ?)", [(1, "US"), (2, "EU"), (3, None)])
def ids(where: str) -> list[int]:
    return [r[0] for r in db.execute(f"select id from s where {where}")]

print(ids("region != 'US'"))                 # [2]：3 号（NULL）被滤掉
print(ids("region is not 'US'"))             # [2, 3]
print(ids("region is null"))                 # [3]
```

**知识点：**缺失值的表示（Optional & Null）
