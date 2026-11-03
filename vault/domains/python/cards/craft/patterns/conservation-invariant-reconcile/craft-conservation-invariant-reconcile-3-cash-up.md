---
id: craft-conservation-invariant-reconcile-3-cash-up
node: craft.patterns.conservation-invariant-reconcile
type: qa
step: 3
---
## Q
**守恒不变式与对账 · 取款机里的钞票怎么「对账」**｜架构

ATM 里的钞票会在几个地方之间移动：钞箱（cassette）、出钞口（tray）、被客户取走、回收箱。取款、超时回收、卡钞都在搬运。没有账户余额这种「总额」，怎么知道机器里的钱没有凭空多出或少掉？

## A
**要点。** 守恒式：**装入的总额 = 钞箱里的 + 出钞口里的 + 回收箱里的 + 已被客户取走的**。每一个动作都只是把钱从一个容器搬到另一个，不改变总和。对账（cash-up）就是把这几个容器的实时合计摆在一起比较，`balanced` 为假就该停机检查。它是纯只读的断言，不参与业务逻辑，所以可以随时调用。

```python
import random
from collections import Counter

DENOMS = (100, 50, 20)
total = lambda c: sum(d * n for d, n in c.items())

class Atm:
    def __init__(self, cassette):
        self.cassette, self.tray, self.collected = Counter(cassette), Counter(), 0
        self.loaded = total(cassette)
    def dispense(self, amount):
        plan, left = Counter(), amount
        for d in DENOMS:                                   # 贪心选钞
            k = min(left // d, self.cassette[d]); plan[d] = k; left -= d * k
        if left: return False
        self.cassette -= plan; self.tray += plan            # 钱从钞箱移到出钞口
        return True
    def take(self):                                        # 客户取走
        self.collected += total(self.tray); self.tray.clear()
    def cash_up(self):
        return self.loaded, total(self.cassette) + total(self.tray) + self.collected

atm = Atm(Counter({100: 5, 50: 5, 20: 10}))
rng = random.Random(3)
for _ in range(20):
    atm.dispense(rng.choice([20, 70, 120, 210, 300])); atm.take()
loaded, now = atm.cash_up()
print("装入:", loaded, " 现有(钞箱+出钞口+已取走):", now, " 守恒:", loaded == now)

atm.collected += 20                                        # 注入一个 bug：取走时多记了一张 20
loaded, now = atm.cash_up()
print("注入 bug 后: 装入", loaded, " 现有", now, " 守恒:", loaded == now)
```

20 次随机取款后，再人为多记一张已取走的 20 元：

```
装入: 950  现有(钞箱+出钞口+已取走): 950  守恒: True
注入 bug 后: 装入 950  现有 970  守恒: False
```

**为什么。** 取款机出的 bug 类型是：已经出钞但没扣钞箱、卡钞后没把钞票回到回收箱、取走后重复计数。每一种都违反守恒，但功能测试（这次取了 120 元，对吗？）全都通过。把守恒式写成断言放进每个测试的收尾，等于给所有动作加了一个共同的检查。

**怎么设计。** 移动总是一次动作里「从 A 减、往 B 加」，在同一个临界区里完成，没有「钱在路上」的中间状态；容器是同一种类型（`Cassette`），不同角色（钞箱、出钞口、回收箱）只是不同的实例，这样搬运可以复用同一个函数，守恒由函数保证。

**易错。** 面额张数降到 0 的条目要从字典里删掉：选钞算法遍历这张表，留一条「20 元：0 张」会让它把并不存在的钞票算进可用集合。
