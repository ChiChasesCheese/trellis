---
id: cc-toolbox-sorted-key-once
node: toolbox.sorted
type: qa
---
## Q
`sorted(rows, key=f)` versus `sorted(rows, key=cmp_to_key(cmp))` — what does Python actually do in each?

## A
**`key=` is decorate–sort–undecorate: the key is computed exactly *n* times**, then tuples are compared in C. `cmp_to_key` wraps every element in an object whose `__lt__` calls back into Python on **every comparison** — that is n log n Python calls.

- So a key function that parses or re-formats (`int(s.split(",")[2])`) is affordable; the same expression inside a comparator is not.
- Prefer a tuple key always; reach for `cmp_to_key` only when the order genuinely has no tuple form ([[cc-output-ordering-cmp-to-key]]).
- `operator.itemgetter(1, 0)` and `attrgetter` are faster than the equivalent lambda and read better for plain tuples and records.
- The key is computed **before** any comparison, so it must not depend on state the sort mutates — and it must be total, or ties fall back to input order ([[cc-output-ordering-stable-two-pass]]).

## Q zh
`sorted(rows, key=f)` 与 `sorted(rows, key=cmp_to_key(cmp))` —— Python 各自实际做了什么？

## A zh
**`key=` 是「装饰—排序—还原」：key 恰好计算 *n* 次**，然后在 C 层比较 tuple。`cmp_to_key` 把每个元素包进一个对象，其 `__lt__` 在**每一次比较**时回调 Python —— 那是 n log n 次 Python 调用。

- 所以做解析或重新格式化的 key 函数（`int(s.split(",")[2])`）是负担得起的；同样的表达式放进比较器就不是。
- 永远优先 tuple key；只有当顺序确实没有 tuple 形式时才用 `cmp_to_key`（[[cc-output-ordering-cmp-to-key]]）。
- `operator.itemgetter(1, 0)` 和 `attrgetter` 比等价的 lambda 更快，对普通 tuple 和记录也更好读。
- key 在任何比较**之前**就算好，所以它不能依赖排序过程会改动的状态 —— 而且它必须是完全的，否则并列会退回输入顺序（[[cc-output-ordering-stable-two-pass]]）。
