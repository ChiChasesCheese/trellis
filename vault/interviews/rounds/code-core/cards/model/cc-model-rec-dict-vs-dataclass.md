---
id: cc-model-rec-dict-vs-dataclass
node: model.records
type: qa
---
## Q
Plain dict, tuple, `dataclass`, or a class with methods — what actually decides which one a timed-round record should be?

## A
**The operations you need, in this order:**

- **tuple** — small, fixed, never mutated, and you want it hashable or sortable: `(due_date, idx)` as a sort key, `(merchant, customer)` as a dict key.
- **dict** — the field set is driven by the input (arbitrary keys, unknown keys must survive) or you are still discovering it.
- **`@dataclass`** — three or more named fields that mutate; costs one line and buys a readable `__repr__` for debugging.
- **class with methods** — when an invariant must hold across mutations.

Choose once, at the start, from the last part's needs — converting later touches every access site.

## Q zh
普通 dict、元组、`dataclass`，还是带方法的类 —— 限时轮里到底靠什么决定记录用哪种？

## A zh
**靠你需要的操作，按此顺序判断：**

- **元组** —— 小、字段固定、从不修改，且你需要它可哈希或可排序：`(due_date, idx)` 当排序 key，`(merchant, customer)` 当 dict key。
- **dict** —— 字段集由输入决定（key 任意、未知 key 必须保留），或者你还在摸索字段。
- **`@dataclass`** —— 三个以上会变动的具名字段；只多一行，换来调试时可读的 `__repr__`。
- **带方法的类** —— 当某个不变量必须跨多次修改保持时。

一开始就按最后一部分的需要选定 —— 之后再改会动到每一处访问点。
