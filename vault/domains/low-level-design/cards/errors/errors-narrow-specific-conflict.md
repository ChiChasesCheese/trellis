---
id: errors-narrow-specific-conflict
node: errors.narrow-catch
type: qa
step: 4
---
## Q
短链服务插入重复的短码要回 409。代码里 `except sqlite3.IntegrityError` 就返回 409，够吗？数据库的锁超时和非空约束失败算不算“已被占用”？

## A
**只翻译唯一冲突，别的约束错误照常上抛**

- **`IntegrityError` 是一族约束**：主键、唯一、非空、外键、`CHECK` 都在里面，只有前两种表示“已被占用”；
- **锁超时是另一个类**：`OperationalError`，根本不是冲突，不能 `except sqlite3.Error` 一网打尽，否则繁忙时用户会看到“短码已存在”；
- **按码判断，不按消息文本**：`sqlite3` 的 `sqlite_errorname`（3.11 起）；PostgreSQL 用 SQLSTATE `23505`（唯一违反）；消息文本会随版本和语言变；
- **SQL 里同理**：`INSERT OR IGNORE` 连非空约束的失败也一起忽略（行悄悄没写进去）；`ON CONFLICT(code) DO NOTHING` 只管指定的那个冲突；
- **其余的 `IntegrityError` 重新 `raise`**：非空失败是我们的缺陷，仍是 500。

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("create table u (code text primary key, url text not null)")
db.execute("insert into u values ('a', 'x')")

def add(code, url) -> int:
    try: db.execute("insert into u values (?, ?)", (code, url))
    except sqlite3.IntegrityError as e:
        if e.sqlite_errorname.endswith(("PRIMARYKEY", "UNIQUE")): return 409
        raise                                   # 非空等：不是“已被占用”
    return 201

print(add("a", "y"), add("b", "y"))             # 409 201
try: add("c", None)
except sqlite3.IntegrityError as e: print(e.sqlite_errorname)   # SQLITE_CONSTRAINT_NOTNULL
```

**知识点：**捕获的范围（Narrow Catch）
