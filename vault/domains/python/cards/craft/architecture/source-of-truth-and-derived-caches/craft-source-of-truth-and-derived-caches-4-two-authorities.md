---
id: craft-source-of-truth-and-derived-caches-4-two-authorities
node: craft.architecture.source-of-truth-and-derived-caches
type: qa
step: 4
---
## Q
**真相与派生缓存 · 取款机有两个权威：账户余额和钞箱存量**｜架构

ATM 取款要同时改两件事：银行里的账户余额（银行是权威），和机器里钞箱的存量（机器是权威）。这两件事不在同一个系统里，没有办法放进一个事务。怎么保证失败时不吞钱、也不白吐钱？

## A
**要点。** 真相不唯一时没有原子性可言，只能靠两样东西：（1）固定顺序，让失败时需要回滚的永远是本地那一半（可回滚、可控），远端那一半留到最后才动；（2）一条守恒不变量随时可验。取款顺序是：先从钞箱留钞 → 再请银行扣账 → 最后交到出钞口；失败时放回钞箱，银行没动。

```python
class BankDown(Exception): ...

class Atm:
    def __init__(self, bank_fail: bool) -> None:
        self.loaded = 100                      # 装钞总额
        self.cassette, self.tray, self.collected = 100, 0, 0
        self.bank_balance = 500                # 银行的账：另一个权威
        self.bank_fail = bank_fail

    def withdraw(self, amount: int) -> None:
        self.cassette -= amount                # 1. 本地先留钞：回滚干净
        try:
            if self.bank_fail:
                raise BankDown
            self.bank_balance -= amount        # 2. 再请银行扣账
        except BankDown:
            self.cassette += amount            # 失败只回滚本地那一半
            raise
        self.tray += amount                    # 3. 最后才交到出钞口

    def balanced(self) -> bool:                # 对账：钞票守恒
        return self.loaded == self.cassette + self.tray + self.collected

for fail in (True, False):
    a = Atm(fail)
    try:
        a.withdraw(40)
    except BankDown:
        pass
    print("银行故障" if fail else "银行正常", "钞箱", a.cassette, "出钞口", a.tray,
          "银行余额", a.bank_balance, "守恒", a.balanced())
```

装钞 100、银行余额 500，取 40，银行故障与正常各一次，实际输出：

```
银行故障 钞箱 100 出钞口 0 银行余额 500 守恒 True
银行正常 钞箱 60 出钞口 40 银行余额 460 守恒 True
```

**为什么。** 钞票一旦交到出钞口就收不回来，所以这一步必须最后做；而银行扣账可以用一笔冲正（reversal）抵消，所以放在中间。

**代价。** 如果在「银行已扣、交钞之前」机器掉电，本地回滚不到，只能靠流水和事后对账修复，这是「顺序加补偿」比事务弱的地方。
