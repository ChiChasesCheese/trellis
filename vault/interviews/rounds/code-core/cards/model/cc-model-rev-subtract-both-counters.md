---
id: cc-model-rev-subtract-both-counters
node: model.reversal
type: qa
---
## Q
`DISPUTE ch_7` must undo an earlier `CHARGE`. Your merchant record holds `total` and `fraud`. What does the undo need, and what does it do?

## A
**A ledger of what the original event did, keyed by its id — then the undo is the exact inverse.**

```python
charges[cid] = (acct, is_fraud)          # written by CHARGE
...
acct, was_fraud = charges.pop(cid)       # DISPUTE
rec = accounts[acct]
rec["total"] -= 1
if was_fraud: rec["fraud"] -= 1
reevaluate(rec)
```

Every counter the original incremented must be decremented — decrementing `total` and forgetting `fraud` leaves a merchant with more fraud than charges. Popping the entry rather than deleting it later gives you double-reversal protection for free. See [[cc-model-rev-double-reversal-noop]].

## Q zh
`DISPUTE ch_7` 必须撤销更早的一笔 `CHARGE`。你的商户记录里有 `total` 和 `fraud`。撤销需要什么，做什么？

## A zh
**一本以事件 id 为 key、记录原事件做了什么的账 —— 然后撤销就是它的精确逆运算。**

```python
charges[cid] = (acct, is_fraud)          # written by CHARGE
...
acct, was_fraud = charges.pop(cid)       # DISPUTE
rec = accounts[acct]
rec["total"] -= 1
if was_fraud: rec["fraud"] -= 1
reevaluate(rec)
```

原事件递增过的每一个计数器都必须递减 —— 只减 `total` 而忘了 `fraud`，会让商户的欺诈数超过总数。用 pop 取出条目而不是稍后再删，还免费获得了防重复撤销的能力。见 [[cc-model-rev-double-reversal-noop]]。
