---
id: cc-python-idioms-setdefault-vs-defaultdict
node: python.idioms
type: qa
---
## Q
`d.setdefault(k, []).append(x)` versus `defaultdict(list)`. What is the actual difference, and which trap does each carry?

## A
**`defaultdict` inserts on read; `setdefault` evaluates its default eagerly.**

- `defaultdict(list)` builds the missing value on **any** access, so `if d[k]:` inserts an empty list and changes what a later `for k in d` sees — and what your output contains.
- `d.setdefault(k, expensive())` calls `expensive()` on every call, even when the key is already present.
- `d.get(k, default)` never inserts: the right call when you are only inspecting.

Rule of thumb: `defaultdict` when the dict is write-heavy and you own it end to end; `setdefault` for a one-off insertion into a dict you also read; `get` everywhere else. Convert with `dict(dd)` before you print or diff it.

## Q zh
`d.setdefault(k, []).append(x)` 和 `defaultdict(list)` 的区别到底是什么？各自带着哪个陷阱？

## A zh
**`defaultdict` 在读取时插入；`setdefault` 会急切求值它的默认值。**

- `defaultdict(list)` 在**任何**访问时都会建出缺失的值，所以 `if d[k]:` 会插入一个空 list，改变之后 `for k in d` 看到的内容 —— 也就改变了你的输出。
- `d.setdefault(k, expensive())` 每次调用都会执行 `expensive()`，哪怕 key 已经存在。
- `d.get(k, default)` 永远不插入：只做查看时就该用它。

经验法则：字典写多且完全由你掌控时用 `defaultdict`；对一个也要读的字典做一次性插入时用 `setdefault`；其余场合用 `get`。打印或比对之前先 `dict(dd)` 转回来。
