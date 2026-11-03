---
id: hi-pt-tt-double-entry-ledger-5-balance-at
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 6
---
## Q
**复式账本（类设计） · 历史余额的二分**｜追问 · 出自：复式账本（类设计） › 逐步扩展 1

`balance_at(account, currency, seq)` 怎么做到 O(log n)？

## A
**做法。** 每个账户币种维护序号列表和更新后余额列表；序号严格递增，列表天然有序。
```python
i = bisect_right(seqs, seq)
return bals[i - 1] if i else 0
```
二分找到序号不大于给定值的最后一项。读当前余额是 O(1)。
