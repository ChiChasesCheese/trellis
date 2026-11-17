---
id: debugging-prevent-safe-data-fix
node: debugging.prevent
type: qa
step: 4
---
## Q
缺陷已经把几十条线上订单的状态写坏了，需要写一段脚本修数据。怎么保证这次修复本身不会闯新祸，事后又怎么证明修对了？

## A
**默认只预演；先写变更记录再改；改完用独立的检查验证**

- **预演（dry run）为默认**：先只读，打印“会改几行、哪几行”；行数和你的预期不符，就停下，不要执行；
- **先写变更记录，再改数据**：把旧值写进审计表（同一个事务里），出了问题能还原，也能事后说清“改过什么”；
- **用事务包起来**：全部成功才提交，中途出错整体回滚，不留下改了一半的状态；
- **改完验证**：用另一条独立的查询确认“不该再有坏数据”，且“没改的行没变”；
- **节奏**：先在副本或少量数据上做，再放大；一次别改太多，出错时影响面小。

```python
import sqlite3

def fix(db, apply=False):
    bad = db.execute("SELECT id, status FROM o WHERE status='canceled'").fetchall()
    print("将修改", len(bad), "行：", bad)                  # 预演：先看清范围
    if not apply: return
    with db:                                              # 一个事务
        db.executemany("INSERT INTO audit VALUES(?, ?)", bad)           # 先记旧值
        db.execute("UPDATE o SET status='cancelled' WHERE status='canceled'")
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE o(id, status)"); db.execute("CREATE TABLE audit(id, old)")
db.executemany("INSERT INTO o VALUES(?, ?)", [(1, "canceled"), (2, "active")])
fix(db); fix(db, apply=True)
print(db.execute("SELECT status, COUNT(*) FROM o GROUP BY status").fetchall())
# [('active', 1), ('cancelled', 1)]：坏值清零，没改的行没动
```

**知识点：**防止复发（Prevent Recurrence）
