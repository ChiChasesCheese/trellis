---
id: craft-conservation-invariant-reconcile-1-entries-sum-to-zero
node: craft.patterns.conservation-invariant-reconcile
type: qa
step: 1
---
## Q
**守恒不变式与对账 · 钱转账为什么要写成「一笔分录、两条腿、合计为零」**｜写法

转账最直接的实现是两步：`alice -= n`，再 `bob += n`。在这两行之间进程崩溃，或者其中一行因为 bug 写错了数字，会怎样？账本（ledger）里的复式记账（double-entry）怎么把这类错误变成可检测的？

## A
**要点。** 一笔分录（entry）由若干条腿（posting）组成，每条腿是一个账户的一个正负金额；规则是**每个币种上所有腿加起来必须等于 0**。这条规则在写入时就校验，不平衡的分录根本进不了日志。于是整个账本任何时刻对任一币种求和都是 0，`total(currency) == 0` 成为一个永远可以拿来自检的断言。

```python
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True)
class Posting: account: str; currency: str; amount: int      # 正 = 入，负 = 出
@dataclass(frozen=True)
class Entry: id: str; postings: tuple
class InvalidEntry(ValueError): ...

class Ledger:
    def __init__(self): self.journal = []; self.bal = defaultdict(int)
    def post(self, e):
        net = defaultdict(int)
        for p in e.postings: net[p.currency] += p.amount
        if len(e.postings) < 2 or any(net.values()):         # 每个币种各自借贷平衡
            raise InvalidEntry(f"{e.id} 不平衡: {dict(net)}")
        self.journal.append(e)                                # 校验通过才提交
        for p in e.postings: self.bal[(p.account, p.currency)] += p.amount
    def total(self, currency):                                # 守恒：永远是 0
        return sum(v for (_, c), v in self.bal.items() if c == currency)

L = Ledger()
L.post(Entry("e1", (Posting("bank", "USD", -100), Posting("alice", "USD", 100))))
L.post(Entry("e2", (Posting("alice", "USD", -30), Posting("bob", "USD", 30))))
print("余额:", dict(L.bal), " total(USD) =", L.total("USD"))
try: L.post(Entry("e3", (Posting("alice", "USD", -10), Posting("bob", "USD", 9))))
except InvalidEntry as e: print("拒绝:", e)
print("拒绝之后 total(USD) =", L.total("USD"), " 日志条数:", len(L.journal))

bal = {"alice": 100, "bob": 0}                                # 对照：两步更新，中间崩溃
def transfer_naive(n):
    bal["alice"] -= n
    raise RuntimeError("崩溃")                                # 在两步之间
    bal["bob"] += n
try: transfer_naive(30)
except RuntimeError: pass
print("两步更新崩溃后总额:", sum(bal.values()), "（凭空少了 30）")
```

实际输出（先两笔合法分录，再一笔少记了 1 的分录，最后是两步更新崩溃的对照）：

```
余额: {('bank', 'USD'): -100, ('alice', 'USD'): 70, ('bob', 'USD'): 30}  total(USD) = 0
拒绝: e3 不平衡: {'USD': -1}
拒绝之后 total(USD) = 0  日志条数: 2
两步更新崩溃后总额: 70 （凭空少了 30）
```

**为什么。** 两步更新的失败是**静默**的：总额少了 30，没有任何异常，只有对账时才可能发现。分录版本把「钱不会凭空出现或消失」从一句祝愿变成了写入时的硬校验，一笔分录要么整体生效、要么整体不生效（先校验、再提交）。入金也是一笔分录：钱从「银行」账户出、到客户账户入，银行账户的负数就是系统里存入的总额。

**代价。** 一笔业务要建模成至少两条腿；每个币种分别平衡，所以跨币种兑换需要借助中间账户（兑换账户的两条腿各在一个币种里平衡）。

**易错。** 金额用整数最小单位（分），不要用浮点：`0.1 + 0.2 != 0.3` 会让「合计为零」永远查不平。
