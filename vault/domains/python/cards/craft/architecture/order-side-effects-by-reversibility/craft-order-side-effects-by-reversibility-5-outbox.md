---
id: craft-order-side-effects-by-reversibility-5-outbox
node: craft.architecture.order-side-effects-by-reversibility
type: qa
step: 5
---
## Q
**副作用按可逆性排序 · 数据库事务里能发邮件吗：从两阶段提交到 outbox**｜架构

下单要写订单表，还要发确认邮件。在数据库事务里直接发邮件，事务回滚时邮件已经发出去了；先提交再发，进程在两者之间崩了就丢邮件。在分布式系统里这个排序问题怎么解？

## A
**要点。** 同一条原则的放大：两阶段提交（2PC）的准备阶段先做可回滚的，最后统一提交；outbox 模式把「要发的邮件」写成同一事务里的一行记录（可回滚的数据库写入），提交之后由另一个进程读出来真正去发。不可逆的动作被推迟到事务提交之后，代价是它变成至少一次投递。

```python
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE orders (id TEXT PRIMARY KEY, status TEXT);
CREATE TABLE outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, msg TEXT, sent INTEGER DEFAULT 0);
""")
sent_mail: list[str] = []

def place_order(oid: str, fail: bool = False) -> None:
    with db:                                             # 一个本地事务
        db.execute("INSERT INTO orders VALUES (?, 'PAID')", (oid,))
        db.execute("INSERT INTO outbox (msg) VALUES (?)", (f"确认邮件 {oid}",))   # 只是一行：可回滚
        if fail:
            raise RuntimeError("提交前失败")

def relay(crash_before_mark: bool = False) -> None:      # 提交之后，另一个进程投递
    for row_id, msg in db.execute("SELECT id, msg FROM outbox WHERE sent = 0").fetchall():
        sent_mail.append(msg)                            # 不可撤销的副作用，最后才做
        if crash_before_mark:
            raise RuntimeError("发完邮件、标记之前崩了")
        with db:
            db.execute("UPDATE outbox SET sent = 1 WHERE id = ?", (row_id,))

try:
    place_order("o1", fail=True)
except RuntimeError:
    pass
relay()
print("订单失败回滚后发出的邮件:", sent_mail)

place_order("o2")
try:
    relay(crash_before_mark=True)
except RuntimeError:
    pass
relay()                                                  # 重启后再投递
print("崩溃重试后发出的邮件:", sent_mail)
```

先让订单在提交前失败再投递；再下一单、投递时崩在标记之前、重启后再投递，用 SQLite 实际输出：

```
订单失败回滚后发出的邮件: []
崩溃重试后发出的邮件: ['确认邮件 o2', '确认邮件 o2']
```

**为什么。** 回滚的订单连邮件记录一起消失，不会发出「幽灵邮件」；代价是崩溃那一单发了两次，所以收件方（或邮件服务）要靠幂等键去重，投递方保证至少一次。

**信号。** 一个事务里想调用外部系统（发消息、调接口、发短信）时，先问能不能改成「在事务里记下意图，提交之后再执行」。
