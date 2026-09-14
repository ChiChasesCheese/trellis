---
id: cc-output-ordering-stable-two-pass
node: output.ordering
type: qa
---
## Q
What exactly does "Python's sort is stable" buy you, and how do you use it deliberately?

## A
**Equal elements keep their relative input order — including under `reverse=True`, which does not reverse ties.** Three uses:

- "Ties → input order" needs no tie-break field at all, provided you sort *once*, starting from the input list.
- A multi-key order that no single key expresses is built by sorting **least significant key first**, then the next, ending with the most significant ([[cc-output-ordering-mixed-directions]]).
- Grouping survives: after sorting by group, the members of each group are still in input order.

Consequences to respect: never re-sort "to be safe" (a second sort on a different key destroys the first); `sorted(d.items())` is stable over insertion order, which is your first-appearance order ([[cc-toolbox-hash-insertion-order]]); and `list.sort()` mutates while `sorted()` copies — the difference matters when another index still points into the old order.

## Q zh
「Python 的排序是稳定的」到底给了你什么，怎么有意识地用它？

## A zh
**相等元素保持原有的输入相对顺序 —— 包括 `reverse=True` 时，它不会翻转并列项。** 三种用法：

- 「并列按输入顺序」根本不需要 tie-break 字段，只要你从输入列表出发**只排一次**。
- 单个 key 表达不了的多键顺序，可以先按**最次要的 key** 排、再排下一个、最后排最主要的（[[cc-output-ordering-mixed-directions]]）。
- 分组得以保留：按组排完后，每组内部仍是输入顺序。

需要注意的后果：不要为了「保险」再排一次（按另一个 key 的第二次排序会毁掉第一次）；`sorted(d.items())` 相对插入顺序是稳定的，也就是首次出现顺序（[[cc-toolbox-hash-insertion-order]]）；`list.sort()` 原地修改而 `sorted()` 复制 —— 当另一个索引仍指向旧顺序时，这个区别很要紧。
