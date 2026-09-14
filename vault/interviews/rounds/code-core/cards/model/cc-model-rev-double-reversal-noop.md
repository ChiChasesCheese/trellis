---
id: cc-model-rev-double-reversal-noop
node: model.reversal
type: qa
---
## Q
The same charge is disputed twice. What must happen, and what is the cheapest way to guarantee it?

## A
**The second dispute is a no-op — and `pop` gives you that for one keyword argument.**

```python
entry = charges.pop(cid, None)
if entry is None:
    return                # already reversed, or never existed
```

Removing the ledger entry *is* the record that the reversal happened, so no second "disputed" flag is needed and the two cases the grader tests — a repeated reversal and a reversal of an unknown id — collapse into the same branch.

The failure it prevents is silent and permanent: counters decremented twice leave `total` at −1 and every later evaluation of that merchant wrong.

## Q zh
同一笔扣款被争议了两次。必须发生什么？保证它最省事的办法是什么？

## A zh
**第二次争议是 no-op —— 而 `pop` 只用一个默认参数就给了你这个保证。**

```python
entry = charges.pop(cid, None)
if entry is None:
    return                # already reversed, or never existed
```

移除账目条目**本身**就是"撤销已发生"的记录，因此不需要第二个"已争议"标志，而评测机测的两种情形 —— 重复撤销、撤销未知 id —— 也合并成同一个分支。

它避免的失败既隐蔽又永久：计数器被减了两次，`total` 变成 −1，此后对该商户的每一次判定都是错的。
