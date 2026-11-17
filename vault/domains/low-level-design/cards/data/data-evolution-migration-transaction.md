---
id: data-evolution-migration-transaction
node: data.evolution
type: qa
step: 3
---
## Q
预约表要加“同一用户同一场次只能有一条有效预约”的唯一约束，但线上已经有重复数据。直接加约束会怎样？迁移里修数据、加约束、记版本号的顺序和事务边界怎么定？

## A
**先修数据，再建约束；三步放在同一个事务里**

- **直接建唯一索引**：遇到重复行就失败，迁移停在一半；
- **顺序**：先去重或取消多余的行，再建约束，最后把版本号 +1；
- **同一个事务**：要么三步都做了，要么都没做；半途失败后重跑，仍然从同一个起点开始；
- **SQLite 的 DDL 可以回滚**：`CREATE INDEX` 在事务里失败就回滚；MySQL 等数据库的 DDL 会隐式提交，不能这样靠事务，要拆成可重复执行的步骤；
- **记版本号**：存在 `schema_version` 表里，迁移前检查，已经应用过的不再重复执行，且不能改动已发布的迁移，改动要新增一个迁移。

```python
import sqlite3

db = sqlite3.connect(":memory:", isolation_level=None)       # 手动控制事务
db.executescript("create table r(u, s, active); insert into r values (1,1,1),(1,1,1);"
                 "create table v(n int); insert into v values (0);")
db.execute("begin")
db.execute("update r set active = 0 where rowid not in (select min(rowid) from r where active group by u, s)")
db.execute("create unique index one_active on r(u, s) where active")   # 数据已修，建约束成功
db.execute("update v set n = 1")
db.execute("commit")
print(db.execute("select n, (select count(*) from r where active) from v").fetchone())
```

**知识点：**字段演进（Schema Evolution in Code）
