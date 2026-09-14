---
id: cc-performance-memory-sort-key-cost
node: performance.memory
type: qa
---
## Q
You sort 10^6 records. Version A: `rows.sort(key=lambda r: (r.day, r.user, r.seq))`. Version B: the rows are already tuples `(day, user, seq, payload)` and you call `rows.sort()`. Which is cheaper, and when is A still right?

## A
**B.** `key=` calls a Python function once per element and stores all n key objects beside the list — one extra tuple and one call per record, tens of MB and ~10^6 interpreted calls at this size. A bare `sort()` compares tuples entirely in C with no allocation.

- The idiom: build the sort key *into* the record when you create it, payload last, then sort with no `key=`.
- Keep `key=` when the key is genuinely derived (case-folding, a computed rank) or when another part fixes the record's shape.
- `key=` is still far better than `functools.cmp_to_key`, which adds a wrapper object *and* a Python call per comparison.

## Q zh
你要排 10^6 条记录。版本 A：`rows.sort(key=lambda r: (r.day, r.user, r.seq))`。版本 B：行本身已经是 tuple `(day, user, seq, payload)`，直接 `rows.sort()`。哪个更省？A 什么时候仍然是对的？

## A zh
**B。** `key=` 会对每个元素调一次 Python 函数，并把全部 n 个 key 对象存在列表旁边 —— 每条记录多一个 tuple 和一次调用，在这个规模上是几十 MB 和约 10^6 次解释器调用。裸 `sort()` 完全在 C 里比较 tuple，不分配。

- 惯用法：造记录时就把排序键**做进**记录里，载荷放最后，然后不带 `key=` 排序。
- 当 key 确实是派生的（大小写折叠、算出来的名次），或者记录形状被别的 part 定死时，保留 `key=`。
- `key=` 仍远好过 `functools.cmp_to_key` —— 后者每次比较都多一个包装对象**和**一次 Python 调用。
