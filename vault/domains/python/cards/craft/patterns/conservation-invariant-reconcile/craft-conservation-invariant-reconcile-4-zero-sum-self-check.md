---
id: craft-conservation-invariant-reconcile-4-zero-sum-self-check
node: craft.patterns.conservation-invariant-reconcile
type: qa
step: 4
---
## Q
**守恒不变式与对账 · 撮合系统怎么用「全场总量不变」自检**｜写法

证券撮合里，买方付现金、卖方收现金，同时股票反向移动。成交是零和的搬运，只有入金能改变现金总额，只有建仓能改变股票总数。把这两条写成什么，才能抓到「手续费从买方扣了却没记到任何账户」这类 bug？

## A
**要点。** 提供两个只读方法：`total_cash()` 和 `total_shares(symbol)`，在随机操作序列的每一步之后检查它们等于「入金之和」和「发行总数」。这是性质测试（property-based testing）的最小形式：不检查某一笔成交的具体结果，只检查任何成交序列都不能破坏的不变量。

```python
import random

class Broker:
    def __init__(self, fee_bug):
        self.cash = {"a": 10_000, "b": 10_000, "c": 10_000}
        self.shares = {"a": 100, "b": 100, "c": 100}
        self.deposited, self.issued, self.fee_bug = 30_000, 300, fee_bug
    def trade(self, buyer, seller, qty, price):
        if buyer == seller or self.shares[seller] < qty or self.cash[buyer] < qty * price: return
        self.cash[buyer] -= qty * price; self.cash[seller] += qty * price
        self.shares[seller] -= qty; self.shares[buyer] += qty
        if self.fee_bug:
            self.cash[buyer] -= 1                     # 手续费从买方扣了，却没有记到任何账户
    def check(self):
        return (sum(self.cash.values()) == self.deposited
                and sum(self.shares.values()) == self.issued)

for bug in (False, True):
    br, rng = Broker(bug), random.Random(1)
    for step in range(1, 201):
        a, b = rng.sample(["a", "b", "c"], 2)
        br.trade(a, b, rng.randint(1, 5), rng.randint(5, 20))
        if not br.check():                            # 每一步之后都检查
            print(f"fee_bug={bug}: 第 {step} 步后守恒被破坏，总现金 {sum(br.cash.values())} != 入金 {br.deposited}"); break
    else:
        print(f"fee_bug={bug}: 200 步随机成交后守恒仍成立")
```

加入一个手续费 bug（从买方扣 1，却没有记到任何账户）后：

```
fee_bug=False: 200 步随机成交后守恒仍成立
fee_bug=True: 第 1 步后守恒被破坏，总现金 29999 != 入金 30000
```

**为什么。** 手写用例只覆盖想得到的场景，随机序列覆盖想不到的组合（部分成交、同一账户先买后卖）。守恒不变式的好处是**不需要知道正确答案**：不用算出每笔成交后每个账户应有多少，只要总量不变，就排除了一大类 bug。手续费要么真的记到「手续费账户」（那么总量守恒），要么不收。

**代价。** 守恒不能证明正确：买卖双方的价格弄反，总量照样守恒。它抓的是「凭空多出或少掉」的 bug，要配合具体结果的断言一起用。

**易错。** 读总量的方法也要拿锁：否则会读到结算做到一半的账，把正常的中间状态误报为违反守恒。
