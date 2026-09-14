---
id: cc-model-sm-boolean-soup
node: model.state-machine
type: qa
---
## Q
You tracked a payment with `created`, `attempted`, `succeeded` and `refunded` booleans. Why does Part 4 break?

## A
**Four booleans describe sixteen combinations, of which four are legal — and every command has to test the right subset of them.**

`SUCCEED` must fire only from `attempted and not succeeded`; `UPDATE` only from `created and not attempted`; after `FAIL` re-opens the payment you need `attempted = False` again, and now some other check that read `attempted` is wrong.

One `state` field plus a transition table replaces all of it, makes an illegal state unrepresentable, and turns "which commands are legal here?" into one lookup. Keep booleans only for genuinely orthogonal facts — `refunded` beside `state`, not instead of it.

## Q zh
你用 `created`、`attempted`、`succeeded`、`refunded` 四个布尔值跟踪一笔付款。为什么到 Part 4 就崩了？

## A zh
**四个布尔值描述十六种组合，其中只有四种合法 —— 而每条命令都得检查其中正确的那一子集。**

`SUCCEED` 只能从 `attempted and not succeeded` 触发；`UPDATE` 只能从 `created and not attempted` 触发；`FAIL` 重新打开付款后又要把 `attempted` 置回 `False`，于是别处读 `attempted` 的某个判断就错了。

一个 `state` 字段加一张转移表可以取代这一切，让非法状态无法表示，并把「此处哪些命令合法？」变成一次查表。布尔值只留给真正正交的事实 —— `refunded` 与 `state` 并列，而不是取代它。
