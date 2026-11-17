---
id: testing-doubles-recording-spy
node: testing.doubles
type: qa
step: 2
---
## Q
报表接口要求「不管有多少行，查询次数不超过预算」，防止逐行再查一次（N+1 查询）。怎样在测试里数出实际发了几条查询，又不去 mock 数据库？

## A
**用真数据库，在边上装一个记录器**

- **sqlite3 自带钩子**：`connection.set_trace_callback(fn)`，每执行一条语句就调用 `fn(sql)`，参数已展开；
- **记录而不拦截**：语句照常执行，结果是真的；记录器只是旁听；
- **断言预算**：在 3 行数据和 300 行数据上各跑一遍，查询数相同；而不是写死一个具体的数字；
- **也能验绑定**：记录到的语句里能看到参数是怎样传进去的，用来确认没有拼接字符串；
- **这是 spy**：包着真实对象的替身，保留行为再多留一份记录。

```python
import sqlite3

def run(n_rows: int, per_row: bool) -> int:
    db, log = sqlite3.connect(":memory:"), []
    db.execute("create table t(x)")
    db.executemany("insert into t values (?)", [(i,) for i in range(n_rows)])
    db.set_trace_callback(log.append)                          # 从这里开始记录
    if per_row:
        for i in range(n_rows): db.execute("select x from t where x=?", (i,)).fetchone()
    else:
        db.execute("select x from t").fetchall()
    return sum(1 for s in log if s.lower().startswith("select"))

print(run(3, True), run(300, True))     # 3 300：随行数增长，N+1
print(run(3, False), run(300, False))   # 1 1：与行数无关
```

**知识点：**测试替身（Test Doubles）
