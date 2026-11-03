---
id: craft-context-managers-for-invariants-6-scales-transaction-lease
node: craft.idioms.context-managers-for-invariants
type: qa
step: 6
---
## Q
**上下文管理器守不变量 · 从 `with lock` 到数据库事务与分布式锁租约**｜写法

进程内，`with` 保证「成败都放锁」。同样的思路搬到数据库事务、分布式锁上，有什么是进程内不用考虑、但这时必须面对的？

## A
**要点。** 骨架完全一样：进入时开始（开事务、拿锁），无异常提交，有异常回滚或释放。`sqlite3` 的连接本身就是这样的上下文管理器：`with db:` 退出时无异常就提交，有异常就回滚。

```python
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE acct (id TEXT PRIMARY KEY, bal INTEGER)")
db.execute("INSERT INTO acct VALUES ('a', 100), ('b', 0)")
db.commit()

def transfer(src, dst, amt, fail=False):
    with db:                               # 退出时：无异常提交，有异常回滚
        db.execute("UPDATE acct SET bal = bal - ? WHERE id = ?", (amt, src))
        if fail:
            raise RuntimeError("入账前崩了")
        db.execute("UPDATE acct SET bal = bal + ? WHERE id = ?", (amt, dst))

transfer("a", "b", 30)
print("成功:", db.execute("SELECT * FROM acct").fetchall())
try:
    transfer("a", "b", 50, fail=True)
except RuntimeError:
    pass
print("失败后(扣款已回滚):", db.execute("SELECT * FROM acct").fetchall())
```

实际输出：

```
成功: [('a', 70), ('b', 30)]
失败后(扣款已回滚): [('a', 70), ('b', 30)]
```

**变化。** 进程内，持有者和管理器同生共死：线程死了锁就跟着解释器退出。分布式锁里，持有者可能崩溃、卡住或被网络隔离，没人执行 `finally`，所以锁必须带**租约**（lease，有过期时间的授权）：到期自动失效，新的持有者可以接手。接手之后旧持有者可能还在干活，所以写入还要带上一个递增的令牌（fencing token），存储端拒绝旧令牌。

**代价。** 租约把「永远卡住」换成了「可能同时有两个持有者」，业务必须能容忍：幂等、或者靠令牌拒绝过期的写。事务也有限度：回滚只能撤销数据库里的写，已经发出去的邮件或扣掉的第三方账户撤不回，那要靠补偿（见 saga）。

**信号。** 看到 `acquire()` / `release()` 成对出现在不同的函数里，或者「失败后某样东西没释放」的 bug 报告。
