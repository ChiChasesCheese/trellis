---
id: data-optional-none-vs-empty
node: data.optional
type: qa
step: 2
---
## Q
销售报表对一个筛选条件没有任何匹配行时，返回的 `total` 是 `0` 还是 `None`，名单是 `[]` 还是 `None`？SQL 的 `SUM` 在这里埋了什么坑？

## A
**空是“知道是零个”，`None` 是“不知道”**

- **标量汇总要落成 0**：合同写“没有匹配行：数量、金额、人数都是 0”；调用方可以直接加减、格式化，不用判断；
- **集合要落成空容器**：`[]`、`{}`、`()`，调用方的 `for` 循环和 `len()` 不用特判；
- **`SUM` 在空集上是 `NULL`**：到 Python 就是 `None`；`COUNT` 在空集上是 `0`，`SUM`、`AVG`、`MAX` 都是 `NULL`；
- **补法**：`COALESCE(SUM(x), 0)`，在查询里一处落成 0，而不是每个调用方各自写 `or 0`；
- **`None` 留给真的“没有这个东西”**：不存在的用户、未设置的有效期。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table sale (cents int)")
q = "select count(*), sum(cents), coalesce(sum(cents), 0), max(cents) from sale"
print(db.execute(q).fetchone())                  # (0, None, 0, None)
db.execute("insert into sale values (500)")
print(db.execute(q).fetchone())                  # (1, 500, 500, 500)
```

**知识点：**缺失值的表示（Optional & Null）
