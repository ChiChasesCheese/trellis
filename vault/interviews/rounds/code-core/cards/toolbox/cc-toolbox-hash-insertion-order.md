---
id: cc-toolbox-hash-insertion-order
node: toolbox.hash
type: qa
---
## Q
The spec says "in order of first appearance". You already hold a dict keyed by id. What can you rely on, and what must you check?

## A
**Since Python 3.7 a dict preserves insertion order**, so first-appearance order is free — *provided the first insert really happens at first appearance*.

- Pre-seeding the dict from a declaration list makes the order that list's order, not the events'. That is often what you want; it is never what "first appearance in the event stream" means.
- `del d[k]` followed by a re-insert moves the key to the **end**; assigning to an existing key does not move it.
- A `defaultdict` inserts on read, so a stray probe adds a key in the wrong position ([[cc-toolbox-hash-defaultdict-read-creates]]).
- If the order must survive a rebuild, a filter, or a merge of two dicts, stop leaning on the dict and store an explicit sequence number in the record.

## Q zh
spec 要求「按首次出现顺序」。你已经有一个以 id 为 key 的 dict。可以依赖什么，必须检查什么？

## A zh
**从 Python 3.7 起 dict 保持插入顺序**，所以首次出现顺序是免费的 —— *前提是第一次插入确实发生在首次出现时*。

- 用声明列表预先填充 dict，会让顺序变成那个列表的顺序，而不是事件的顺序。那常常是你想要的；但它绝不是「在事件流中首次出现」的含义。
- `del d[k]` 之后再插入会把 key 移到**末尾**；对已有 key 赋值则不会移动它。
- `defaultdict` 在读时插入，所以一次多余的探测会把 key 加在错误的位置（[[cc-toolbox-hash-defaultdict-read-creates]]）。
- 如果这个顺序必须经受重建、过滤或两个 dict 的合并，就别再依赖 dict，改在记录里存一个显式的序号。
