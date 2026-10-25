---
id: pay-ledger-double-entry-balanced-journal-code
node: ledger.double-entry
type: qa
step: 4
---
## Q
怎么在代码里保证一笔分录一定借贷平衡？一笔 100 美元支付（手续费 2.90）的分录是什么样？

## A
用有符号整数（最小货币单位，借为正、贷为负），一笔分录内所有行之和必须为零，写入前校验。

```python
from collections import defaultdict
journal = [("customer_funds_in_transit", +10000), ("merchant_payable", -9710), ("fee_revenue", -290)]
assert sum(amt for _, amt in journal) == 0, "unbalanced journal"
bal: dict[str, int] = defaultdict(int)
for acct, amt in journal:
    bal[acct] += amt
print(dict(bal), sum(bal.values()))
try:
    bad = [("a", 100), ("b", -99)]
    assert sum(x for _, x in bad) == 0, "unbalanced journal"
except AssertionError as e:
    print("rejected:", e)
```

实际输出：

```
{'customer_funds_in_transit': 10000, 'merchant_payable': -9710, 'fee_revenue': -290} 0
rejected: unbalanced journal
```

含义：渠道应收（在途资金）借 100.00，商户应付贷 97.10，手续费收入贷 2.90。三行之和为 0；少 1 分的坏分录被直接拒绝。

**生产实现的要点**
1. 校验放在写入事务内，并在数据库层有兜底（延迟约束或触发器检查每个 journal 的和为零）。
2. 金额是整数，不是浮点。
3. 每个币种分别平衡，不能跨币种求和。
4. 一笔业务事件对应一个 journal，不允许一个 journal 只写一部分行。
