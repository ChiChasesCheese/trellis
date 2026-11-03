---
id: craft-lock-as-transaction-boundary-1-lock-is-the-boundary
node: craft.architecture.lock-as-transaction-boundary
type: qa
step: 1
---
## Q
**锁即事务边界 · 一把锁圈住的范围，就是别人眼里「不可分」的范围**｜架构

转账分两步：A 账户扣 30，B 账户加 30。一个线程转到一半时，对账线程去求两个账户的总额。没有数据库事务的内存实现里，怎么保证对账永远看不到「钱在半空」？如果转账中途抛了异常，又怎么保证不留下半截状态？

## A
**要点。** 临界区（critical section，持锁的那段代码）的边界就是原子性的边界：读者和写者共用同一把锁，所以任何人看到的都是整笔转账前或整笔转账后。要对付异常，临界区内部还要「先校验、后修改」，把全部可能失败的检查放在第一次写之前，写之后的部分不再失败。

```python
class Bank:
    def __init__(self, locked: bool) -> None:
        self.bal = {"A": 100, "B": 0}
        self.lock = threading.Lock() if locked else None

    def transfer(self, amount: int) -> None:
        if self.lock: self.lock.acquire()
        try:
            self.bal["A"] -= amount          # 借
            time.sleep(0.05)                 # 借和贷之间的缝隙
            self.bal["B"] += amount          # 贷
        finally:
            if self.lock: self.lock.release()

    def total(self) -> int:                  # 观察者：对账
        if self.lock:
            with self.lock:
                return sum(self.bal.values())
        return sum(self.bal.values())

for locked in (False, True):
    b = Bank(locked)
    t = threading.Thread(target=b.transfer, args=(30,)); t.start()
    time.sleep(0.01)                         # 转账进行到一半时去对账
    seen = b.total()
    t.join()
    print("有锁" if locked else "无锁", "对账看到总额", seen, "转完后", b.total())
```

实际输出：

```
无锁 对账看到总额 70 转完后 100
有锁 对账看到总额 100 转完后 100
```

**为什么。** 双式记账（double-entry ledger）的 `post` 就是这样：重复检查、借贷平衡、余额下限全在第一次写之前；注释「以下是提交：不会再失败」之后才改日志和余额，整段在一把 `RLock` 里，注释写明它「代替数据库事务」。

**代价。** 锁只给同一进程内的线程提供隔离，进程崩溃时内存状态一起丢；持久化和崩溃恢复是另一层的事。
