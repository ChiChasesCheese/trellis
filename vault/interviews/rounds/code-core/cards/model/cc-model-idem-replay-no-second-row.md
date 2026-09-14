---
id: cc-model-idem-replay-no-second-row
node: model.idempotency
type: qa
---
## Q
A ledger prints one signed row per movement. What does a replayed request contribute to that list?

## A
**Nothing — a replay is not a movement.** The row list is the sequence of state changes, and a replay by definition changed no state.

Same for a rejected request: an over-refund that was refused produces no row, does not consume the refund cap, and does not advance a running net.

Practical shape: emit the row inside the branch that actually mutates, never in the command dispatcher.

```python
if not apply_payment(...):    # returns False for replay/reject
    return
rows.append(("payment", pid, amount, net))
```

## Q zh
一个账本对每次资金变动打印一行带符号的记录。被重放的请求给这个列表贡献什么？

## A zh
**什么都不贡献 —— 重放不是一次变动。** 行列表是状态变化的序列，而重放按定义没有改变任何状态。

被拒绝的请求同理：一次被拒的超额退款不产生行、不消耗退款额度、也不推进滚动净额。

实践形态：把生成行的语句放在**真正发生修改**的分支里，绝不放在命令分派处。

```python
if not apply_payment(...):    # returns False for replay/reject
    return
rows.append(("payment", pid, amount, net))
```
