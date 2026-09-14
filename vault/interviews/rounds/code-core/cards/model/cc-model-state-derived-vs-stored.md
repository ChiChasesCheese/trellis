---
id: cc-model-state-derived-vs-stored
node: model.entity-state
type: qa
---
## Q
"Is this merchant currently flagged?" — store the boolean, or recompute it from the counters?

## A
**Recompute it, unless the answer must persist beyond the inputs that produced it.**

A stored boolean is a second source of truth that must be updated at every site that touches a counter — including the reversal path, which is where it will be forgotten. `is_flagged(rec)` reading `fraud`, `total` and the threshold is always consistent and costs nothing at this scale.

The exception is genuinely *historical* state: "was ever flagged" (a sticky flag) cannot be derived from the current counters, so it must be stored — and stored as its own field, beside the derived answer rather than instead of it.

## Q zh
「这个商户当前是否被标记？」—— 存布尔值，还是从计数器现算？

## A zh
**现算，除非这个答案必须比产生它的输入活得更久。**

存下来的布尔值是第二个真相来源，凡是碰计数器的地方都得更新它 —— 包括撤销路径，而那正是会被忘掉的地方。读取 `fraud`、`total` 和阈值的 `is_flagged(rec)` 永远自洽，在这个规模下也不花什么代价。

例外是真正**历史性**的状态：「曾经被标记过」（sticky flag）无法从当前计数器推导，因此必须存 —— 而且要作为独立字段存在推导结果**旁边**，而不是取而代之。
