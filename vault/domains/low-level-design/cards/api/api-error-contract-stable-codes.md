---
id: api-error-contract-stable-codes
node: api.error-contract
type: qa
step: 2
---
## Q
服务把数据库的唯一约束冲突翻译成 409，写法是 `if "UNIQUE constraint failed" in str(exc)`。换了数据库版本、换了驱动或者换了语言环境以后这行代码会怎样？错误映射应该挂在什么上？

## A
**按异常类型或错误码映射，不按消息文本**

- **消息文本是实现细节**：驱动升级、本地化、字段改名都会让措辞变掉，映射悄悄失效，冲突变成 500；
- **挂在类型上**：`sqlite3.IntegrityError` 这一层就能区分约束类失败；要更细，用 Python 3.11 起的 `sqlite_errorname`（如 `SQLITE_CONSTRAINT_UNIQUE`）；
- **映射集中成一张表**：异常类型到 `(status, code)`，放在适配层一处，新增一种失败只加一行；
- **表里没有的**：不要猜，让它当 500 往上走，日志里留原始异常。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table links (code text primary key)")
db.execute("insert into links values ('docs')")
def create(code: str) -> int:
    try:
        db.execute("insert into links values (?)", (code,))
        return 201
    except sqlite3.IntegrityError as exc:
        if exc.sqlite_errorname in ("SQLITE_CONSTRAINT_PRIMARYKEY", "SQLITE_CONSTRAINT_UNIQUE"):
            return 409                       # 不看 str(exc)
        raise

print(create("docs"), create("new"))
```

<details class="pt"><summary>延伸</summary>

`sqlite_errorname` 要求 Python 3.11 及以上；更早的版本只能按异常类型分。其他数据库的驱动同理：PostgreSQL 的驱动暴露 SQLSTATE 码（唯一冲突是 `23505`），MongoDB 的重复键是错误码 `11000`。

</details>

**知识点：**接口的错误契约（Error Contract）
