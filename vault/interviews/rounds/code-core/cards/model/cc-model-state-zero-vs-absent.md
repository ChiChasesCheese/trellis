---
id: cc-model-state-zero-vs-absent
node: model.entity-state
type: qa
---
## Q
`counts[acct]` on a `defaultdict(int)` returns 0 for an account nobody ever mentioned — and also inserts it. When does that matter?

## A
**Whenever the key set is itself an answer.** `defaultdict` mutates on *read*, so a membership test, an iteration over keys, or a "print one line per entity" output silently gains entities that a query invented.

```python
if acct in counts:        # a read that does not create
    ...
counts.get(acct, 0)       # a value that does not create
```

Decide separately: which entities exist (declared? seen in an event? both?) and which are printed (all of them, or only the non-zero ones — specs say both). Zero balance and no balance are different states, and graders test both.

## Q zh
在 `defaultdict(int)` 上访问 `counts[acct]`，对一个从没被提到过的账户会返回 0 —— 同时也把它插了进去。这什么时候要紧？

## A zh
**只要 key 集合本身就是答案时。** `defaultdict` 在**读**的时候就会改动自己，于是成员判断、遍历 key，或者"每个实体打印一行"的输出，会悄悄多出被查询凭空造出来的实体。

```python
if acct in counts:        # a read that does not create
    ...
counts.get(acct, 0)       # a value that does not create
```

分开决定：哪些实体存在（声明过的？在事件中出现过的？两者？）以及哪些被打印（全部，还是只打非零的 —— 两种题面都有）。余额为零和没有余额是两种不同状态，评测机两个都测。
