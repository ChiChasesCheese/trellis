---
id: craft-lock-as-transaction-boundary-2-what-the-lock-becomes
node: craft.architecture.lock-as-transaction-boundary
type: qa
step: 2
---
## Q
**锁即事务边界 · 内存里的每把锁在生产里对应什么**｜架构

幂等转账的内存实现里有两把锁：`_mu` 保护「键表」，`_money` 保护「检查余额 + 扣款 + 存结果」。换成数据库后这两把锁分别变成什么？为什么说写代码时就该想清楚这个对应关系？

## A
**要点。** 每把锁都能对应一个生产机制：`_mu` 保护的占键动作对应唯一约束（`PRIMARY KEY (client, key)`，插入失败 = 别人已占）；`_money` 对应账户行锁，或者包住整个转账的数据库事务；`with lock` 的范围对应 `BEGIN … COMMIT`。事先说清楚对应关系，等于提前知道上线后哪些保证由谁提供。

```python
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE keys (client TEXT, key TEXT, result TEXT, PRIMARY KEY (client, key));
CREATE TABLE bal (acct TEXT PRIMARY KEY, amt INTEGER);
INSERT INTO bal VALUES ('A', 100), ('B', 0);
""")

def transfer(client: str, key: str, amount: int, fail_midway: bool = False) -> str:
    try:
        with db:                              # 事务边界 = 原来的 with lock
            db.execute("INSERT INTO keys VALUES (?, ?, NULL)", (client, key))   # 唯一约束占键
            db.execute("UPDATE bal SET amt = amt - ? WHERE acct = 'A'", (amount,))
            if fail_midway:
                raise RuntimeError("崩在借和贷之间")
            db.execute("UPDATE bal SET amt = amt + ? WHERE acct = 'B'", (amount,))
            db.execute("UPDATE keys SET result = 'ok' WHERE client = ? AND key = ?", (client, key))
        return "ok"
    except sqlite3.IntegrityError:
        return "键已被占"                           # 等价于 _keys 里 key 已存在

try:
    transfer("c1", "k1", 30, fail_midway=True)
except RuntimeError as e:
    print("失败:", e, db.execute("SELECT * FROM bal").fetchall(), db.execute("SELECT count(*) FROM keys").fetchone())
print(transfer("c1", "k1", 30), db.execute("SELECT * FROM bal").fetchall())
print(transfer("c1", "k1", 30), db.execute("SELECT * FROM bal").fetchall())
```

SQLite 内存库里，先让第一次转账崩在中间，再用同一个键成功转一次，再重复一次，实际输出：

```
失败: 崩在借和贷之间 [('A', 100), ('B', 0)] (0,)
ok [('A', 70), ('B', 30)]
键已被占 [('A', 70), ('B', 30)]
```

**为什么。** 崩溃回滚后连占键的行也一起撤销，所以重试能重新来过；这正是「键 + 结果 + 扣款在同一个事务里」的价值。

**代价。** 跨库、跨服务的转账不再有单个事务可用，要靠两阶段提交（2PC）或补偿（saga）；内存里想当然的原子性到这里没有了。
