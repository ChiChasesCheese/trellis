---
id: cc-rules-grp-cancel-whole-group
node: rules.grouping
type: qa
---
## Q
Rule: if any record in a dispute group carries the reason `withdrawn`, none of that group's records is output — whichever came first. How do you implement it, and why can it not be a streaming filter?

## A
**Two passes: collect the cancelled key set, then emit the survivors in input order.**

```python
cancelled = {k for k, rows in groups.items()
             if any(r.reason == "withdrawn" for r in rows)}
out = [r for r in records if key(r) not in cancelled]
```

A single streaming pass cannot work because the withdrawal may arrive **after** the record it cancels — by then the original has already been printed. Two related traps: a group consisting only of a withdrawal is also dropped (there is nothing to print), and cancellation is scoped by the full group key, so the same id on another network is untouched.

## Q zh
规则：若某争议分组中有任意一条记录的原因是 `withdrawn`，该组的记录一条都不输出 —— 无论谁先到达。怎么实现？为什么不能做成流式过滤？

## A zh
**两趟：先收集被取消的 key 集合，再按输入顺序输出幸存者。**

```python
cancelled = {k for k, rows in groups.items()
             if any(r.reason == "withdrawn" for r in rows)}
out = [r for r in records if key(r) not in cancelled]
```

单趟流式行不通，因为撤回可能在它所取消的记录**之后**到达 —— 那时原记录已经打印出去了。两个相关的坑：只由一条撤回构成的组也要丢弃（没有东西可打印）；以及取消的作用域是完整的分组 key，因此另一个卡组织上的同名 id 不受影响。
