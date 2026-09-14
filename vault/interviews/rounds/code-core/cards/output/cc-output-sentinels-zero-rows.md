---
id: cc-output-sentinels-zero-rows
node: output.sentinels
type: qa
---
## Q
A worker took no tasks; an account's credits and debits cancel to exactly 0.00. Print them or not?

## A
**The spec decides per part, and the two rules genuinely differ.** "Print every worker with its load" includes the zero-load worker; "list accounts with a non-zero balance" excludes the cancelling one.

- Enumerate from the **declared entity list**, not from the map of things that happened — otherwise an entity that never appeared in any event silently vanishes from the output.
- The mirror trap: a filter written as `if bal:` also drops a legitimately zero row when the rule was "print everyone", and drops a zero-cost task that should have been assigned.
- Entities mentioned only inside someone else's record (a name that appears in a list but never declares one of its own) usually count as existing with empty state — check the sentence.
- Do it once, in the renderer, so the include/exclude rule is visible next to the format ([[cc-output-formatting-one-place]]).

## Q zh
某个 worker 没接到任务；某个账户的收支恰好抵消为 0.00。打印它们吗？

## A zh
**由 spec 逐 part 决定，而这两条规则确实不同。** 「打印每个 worker 及其负载」包含零负载的 worker；「列出余额非零的账户」则排除抵消为零的那个。

- 从**声明的实体清单**枚举，而不是从「发生过的事」的映射里枚举 —— 否则从未出现在任何事件里的实体会悄悄从输出中消失。
- 镜像陷阱：写成 `if bal:` 的过滤，在规则是「打印所有人」时也会丢掉合法的零值行，还会丢掉本该被分配的零成本任务。
- 只出现在别人记录里的实体（在别人列表里被提到、但自己从未声明过）通常算作存在且状态为空 —— 去看那句话。
- 这件事只在渲染处做一次，让包含/排除规则和格式挨在一起（[[cc-output-formatting-one-place]]）。
