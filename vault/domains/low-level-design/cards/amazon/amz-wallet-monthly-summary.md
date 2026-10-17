---
id: amz-wallet-monthly-summary
node: amazon.amz-wallet
type: qa
step: 6
tags: [grown]
---
## Q
在钱包设计里，月度汇总怎么算？有什么不变量可以自检？

## A
期初余额 = 本月开始前所有分录的变动额之和；本月按类型（存入、取出、手续费、税）分组求和；期末 = 期初 + 本月合计。自检不变量：期末必须等于账户当前余额（本月是最后一个月时）。汇总只读流水，不改任何数据，所以可以重复算、随时算。
```python
def summary(self, acct, start, end):
    entries = self._entries[acct]
    opening = sum(e.delta for e in entries if e.ts < start)
    by_kind = Counter()
    for e in entries:
        if start <= e.ts < end:
            by_kind[e.kind] += e.delta
    return opening, dict(by_kind), opening + sum(by_kind.values())
```
