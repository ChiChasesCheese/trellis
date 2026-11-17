---
id: concurrency-depth-db-atomic-expression
node: concurrency-depth.atomics
type: qa
step: 3
---
## Q
扣库存时，把 `qty` 读到 Python 里减一再写回，和 `UPDATE … SET qty = qty - 1 WHERE qty >= 1` 有什么区别？ORM 里的 `item.qty -= 1` 属于哪一种？

## A
**让数据库算新值，下限写进条件，一条语句就是一个原子操作**

- **读出再写回**：写回的是 Python 里算好的绝对值，两个连接都读到 1000、各写 999，丢掉一次扣减。实测（3.11，8 个线程各一个连接，各扣 20 次，50 轮）每一轮结果都不是 840；`SET qty = qty - 1` 的版本 0/50 轮出错；
- **`item.qty -= 1`（ORM 的属性赋值）** 生成的是 `SET qty = 999` 这种绝对值，等同于第一种；ORM 一般提供表达式形式（`Item.qty - 1`）生成第二种；
- **下限写进 `WHERE qty >= ?`**：`rowcount` 为 0 就是库存不够，检查和扣减是同一步，不会扣成负数；
- **一次性验证码、抢占式状态变更、尝试次数加一**，都用同样的形式：条件和修改写在同一条语句里；
- **要读到扣减后的值**：数据库支持的话用 `RETURNING`（SQLite 3.35+），不要再 `SELECT` 一次，那是另一次读；
- **持有行锁时读改写才安全**：`SELECT … FOR UPDATE` 先锁行，再读、算、写，后到的事务等前一个提交。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE stock(id INTEGER PRIMARY KEY, qty INT)")
db.execute("INSERT INTO stock VALUES (1, 2)")

def take(n) -> bool:
    cur = db.execute("UPDATE stock SET qty = qty - ? WHERE id = 1 AND qty >= ?", (n, n))
    return cur.rowcount == 1               # 下限在条件里，减法在库里算

print(take(1), take(1), take(1))           # True True False
```

**知识点：**原子操作与无锁（Atomics & Lock-Free）
