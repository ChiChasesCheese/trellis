---
id: cc-output-ordering-mixed-directions
node: output.ordering
type: qa
---
## Q
"Highest total first, ties by merchant id ascending." Write the key. Then the spec adds "and by name *descending*" — what breaks?

## A
**Negate the numeric fields inside a tuple key:** `key=lambda r: (-r.total, r.id)`. `reverse=True` is not a substitute — it flips *every* field, including the id.

- You cannot negate a string, so a descending **string** field has no tuple-key expression. Two ways out:
  - two stable passes — sort by the least significant key first, then by the most significant with `reverse=True` (ties keep the previous pass's order, because Python's sort is stable in both directions);
  - `functools.cmp_to_key` ([[cc-output-ordering-cmp-to-key]]).
- Mapping a string to an ordinal to negate it only works for a known finite alphabet and costs more than it saves.
- `None` cannot be compared with an `int`; substitute a sentinel (`float("inf")`, `-1`, or a leading flag field) inside the key rather than filtering rows out.

## Q zh
「total 最高的在前，并列时按 merchant id 升序。」写出这个 key。然后 spec 又加上「再按 name *降序*」—— 哪里会出问题？

## A zh
**在 tuple key 里对数值字段取负：** `key=lambda r: (-r.total, r.id)`。`reverse=True` 不能替代它 —— 它会翻转*每一个*字段，包括 id。

- 字符串不能取负，所以降序的**字符串**字段没有 tuple-key 写法。两条出路：
  - 两次稳定排序 —— 先按最次要的 key 排，再按最主要的 key 加 `reverse=True` 排（并列项保持上一趟的顺序，因为 Python 的排序在两个方向上都稳定）；
  - `functools.cmp_to_key`（[[cc-output-ordering-cmp-to-key]]）。
- 把字符串映射成序号再取负，只在字母表已知且有限时可行，代价大于收益。
- `None` 不能和 `int` 比较；在 key 内部替换成哨兵值（`float("inf")`、`-1`，或前置一个标志字段），而不是把行过滤掉。
