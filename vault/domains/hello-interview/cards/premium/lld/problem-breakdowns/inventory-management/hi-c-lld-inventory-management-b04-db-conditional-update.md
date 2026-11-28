---
id: hi-c-lld-inventory-management-b04-db-conditional-update
node: lld.problem-breakdowns.inventory-management.beyond
type: qa
step: 1
---
## Q
**库存管理 · 拓展：持久化后，调拨由数据库来保证**｜拓展 · 追问

库存存进关系数据库之后，内存里的锁就不管用了（多进程、多机器）。扣减和调拨怎么写才不超卖、不丢货？

## A
**模式。** 条件更新（conditional update）：把"判断"和"修改"合成一条 SQL，由数据库的行锁保证原子；多步操作放在一个事务里。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE stock (wh TEXT, pid TEXT, qty INTEGER CHECK (qty >= 0), PRIMARY KEY (wh, pid))")
db.executemany("INSERT INTO stock VALUES (?,?,?)", [("EAST", "w", 7), ("WEST", "w", 0)])
db.commit()


def transfer(db: sqlite3.Connection, pid: str, src: str, dst: str, qty: int) -> bool:
    try:
        with db:                                 # 一个事务：块内任何异常都整体回滚
            # 条件更新：判断和扣减在同一条语句里，数据库自己保证原子，不存在"先查后改"的窗口
            cur = db.execute("UPDATE stock SET qty = qty - ? WHERE wh = ? AND pid = ? AND qty >= ?",
                             (qty, src, pid, qty))
            if cur.rowcount != 1:
                raise LookupError("insufficient")
            db.execute("INSERT INTO stock VALUES (?,?,?) ON CONFLICT(wh, pid) DO UPDATE SET qty = qty + ?",
                       (dst, pid, qty, qty))
        return True
    except LookupError:
        return False


assert transfer(db, "w", "EAST", "WEST", 5)
assert not transfer(db, "w", "EAST", "WEST", 10)             # 库存不足：整个事务回滚
assert dict(db.execute("SELECT wh, qty FROM stock")) == {"EAST": 2, "WEST": 5}
```
- **条件更新：** `UPDATE … SET qty = qty - n WHERE … AND qty >= n`，检查和扣减是同一条语句，数据库保证不会有别人插在中间；`rowcount` 为 0 说明库存不足。这相当于内存版里"锁内检查并扣"。
- **事务：** `with db:` 在块正常结束时提交，抛异常时整体回滚，所以源仓库扣了而目的仓库没加的中间状态不会落库。
- **`CHECK (qty >= 0)`：** 约束是最后一道防线，即使应用有 bug 也不会写出负库存。
- **死锁在数据库里依旧存在：** 两个事务以相反顺序更新（东、西）两行会互等；和内存里一样，按固定顺序更新（先小 ID 后大 ID），或遇到死锁错误时重试整个事务。SQLite 同一时刻只有一个写者，演示不出来，换成 PostgreSQL、MySQL 才会遇到。
- **告警的位置：** 回调不能在事务里执行；事务提交后再发，更稳妥的是写入一张"待发送"表（发件箱，outbox），由单独的进程发送，避免"库存改了但通知没发出"。
- **何时不用：** 单进程内存系统，仓库锁足够。
