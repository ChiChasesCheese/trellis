---
id: cc-model-rec-mutable-vs-tuple
node: model.records
type: qa
---
## Q
You stored per-entity state as a tuple `(fraud, total)` in a dict. Part 4 must decrement one of them. What goes wrong, and what is the fix?

## A
**A tuple cannot be updated in place, so every mutation becomes a rebuild** — `counts[a] = (counts[a][0] - 1, counts[a][1] - 1)` — which is unreadable, easy to mis-order, and silently wrong the day a third field is inserted between them.

Fix: a mutable record (`dict`, `list` or `dataclass`) for anything that changes; keep tuples for the things that must be hashable or sortable. The two roles are different: a tuple is a *value* (a key, a sort key, a returned pair); a record is an *identity* whose fields change over time.

## Q zh
你把每实体状态存成 dict 里的元组 `(fraud, total)`。Part 4 需要把其中一个减一。会出什么问题？怎么修？

## A zh
**元组无法原地更新，于是每次修改都变成重建** —— `counts[a] = (counts[a][0] - 1, counts[a][1] - 1)` —— 既难读、又容易搞错顺序，而且在两者之间插入第三个字段的那天会悄悄出错。

修法：会变化的东西一律用可变记录（`dict`、`list` 或 `dataclass`）；元组留给必须可哈希或可排序的东西。两者角色不同：元组是**值**（key、排序 key、返回的一对）；记录是随时间改变字段的**身份**。
