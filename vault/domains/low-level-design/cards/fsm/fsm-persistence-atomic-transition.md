---
id: fsm-persistence-atomic-transition
node: fsm.persistence
type: qa
step: 3
---
## Q
到期付款要“扣款并把付款标成已完成”。进程在两步之间崩溃，重启后重试会怎样？怎么设计才安全？

## A
**状态变更和副作用写在同一个事务里**

- **分开写**：扣完款崩溃，状态还是“待付”，重启后再扣一次；反过来，状态已改而款没扣，也无人察觉；
- **同一事务**：要么两个都生效，要么都不生效，重试时一切回到崩溃前；
- **条件更新**：`where status = 'pending'` 让并发或重放的第二次更新不命中，不改任何东西；
- **事务之外的副作用**（发邮件、调外部接口）：放在提交之后，用幂等键或记录“已发送”的标志防重。

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("create table acct(bal int); insert into acct values (100);"
                 "create table pay(id text primary key, status text);"
                 "insert into pay values ('p1', 'pending');")

def settle(crash):
    with db:                                          # 一个事务
        db.execute("update acct set bal = bal - 30")
        if crash: raise RuntimeError("process died")
        db.execute("update pay set status='done' where id='p1' and status='pending'")

get = lambda: (db.execute("select bal from acct").fetchone()[0], db.execute("select status from pay").fetchone()[0])
try: settle(True)
except RuntimeError: pass
print(get()); settle(False); print(get())             # (100, 'pending') (70, 'done')
```

**知识点：**持久化与恢复（Persistence & Resume）
