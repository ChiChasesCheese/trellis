---
id: craft-conservation-invariant-reconcile-2-cache-reconcile-under-lock
node: craft.patterns.conservation-invariant-reconcile
type: qa
step: 2
---
## Q
**守恒不变式与对账 · 余额缓存漂移以后，怎么用账本纠正，而不把正确的值改坏**｜写法

数字钱包里，每个账户有一个缓存的余额（读得快），真相是只增不减的分录账本。缓存可能因为 bug、崩溃恢复而漂移。设计一个 `reconcile(account)`：用账本重新推导，不一致就纠正缓存。这个函数里「推导」放在拿锁之前还是之后？

## A
**要点。** 账本是被信任的一方，缓存只是它的投影，漂移了就被账本覆盖。关键细节：**推导必须在持有账户锁时做**。转账是在持有账户锁时同时改账本和缓存的，所以锁内读到的两边一定同步。如果先在锁外推导、再拿锁去比较，推导完到拿锁之间若插进一笔转账，缓存已经变了而你手里是旧的推导值，会把一个正确的缓存「纠正」成过期值。

```python
import threading

class Account:
    def __init__(self): self.lock = threading.Lock(); self.balance = 0     # 缓存的余额

class Wallet:
    def __init__(self):
        self.entries = []                                 # 账本：只增不减，真相
        self.acct = {"a": Account(), "b": Account()}
    def derived(self, who): return sum(d for w, d in self.entries if w == who)
    def move(self, src, dst, n):
        s, d = self.acct[src], self.acct[dst]
        with s.lock, d.lock:                              # 账本与缓存在同一个持锁区里一起改
            self.entries += [(src, -n), (dst, n)]
            s.balance -= n; d.balance += n
    def reconcile(self, who) -> bool:
        a = self.acct[who]
        with a.lock:                                      # 推导必须在锁内
            derived = self.derived(who)
            if a.balance == derived: return False         # 一致就什么都不做
            a.balance = derived                           # 账本是被信任的一方
            return True

w = Wallet(); w.move("a", "b", 50); w.move("a", "b", 20)
print("正常:", w.acct["b"].balance, w.derived("b"), " reconcile 纠正了吗:", w.reconcile("b"))
w.acct["b"].balance += 1000                               # 模拟缓存漂移（某个 bug 或崩溃恢复）
print("漂移后缓存:", w.acct["b"].balance, " 账本推导:", w.derived("b"))
print("reconcile 纠正了吗:", w.reconcile("b"), " 缓存现在:", w.acct["b"].balance)
print("账本总和(应为 0):", sum(d for _, d in w.entries))
```

实际输出（正常对账什么都不改；人为把缓存加 1000 后再对账）：

```
正常: 70 70  reconcile 纠正了吗: False
漂移后缓存: 1070  账本推导: 70
reconcile 纠正了吗: True  缓存现在: 70
账本总和(应为 0): 0
```

**为什么。** 返回「是否发生了纠正」而不是静默修复，调用方（定时任务）才能统计并告警：偶尔纠正一次可以容忍，持续纠正说明有 bug 在制造漂移，应当去找它而不是继续补。

**代价。** 每次推导是 O(该账户的分录数)；长期账户要用「检查点余额 + 之后的分录」加速。缓存存在的理由是读多写少的热路径，对账是后台的、低频的。

**易错。** 纠正方向永远是账本覆盖缓存；绝不能反过来，否则一个缓存里的 bug 会写进真相。
