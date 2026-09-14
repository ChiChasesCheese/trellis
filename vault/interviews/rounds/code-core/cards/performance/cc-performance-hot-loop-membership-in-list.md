---
id: cc-performance-hot-loop-membership-in-list
node: performance.hot-loop
type: qa
---
## Q
`if charge_id in seen_ids:` where `seen_ids` is a list that grows to 10^5 entries. The logic is right and the performance test times out. Explain and fix.

## A
**`in` on a `list` is O(n); on a `set` or `dict` it is O(1) average.** The loop is therefore O(n²) — up to 10^10 comparisons.

```python
seen_ids = set()          # not []
if charge_id in seen_ids: ...
seen_ids.add(charge_id)
```

- The same trap: `list.index`, `list.remove`, `list.count`, and `if x not in results` used as a de-duplicator.
- `x in some_dict` and `x in some_dict.keys()` are both O(1) — a view, not a copy. `x in list(some_dict)` is O(n) *and* allocates.
- If you also need insertion order, use a `dict` with `None` values: O(1) membership and ordered iteration.

## Q zh
`if charge_id in seen_ids:`，其中 `seen_ids` 是一个会长到 10^5 项的 list。逻辑是对的，性能测试超时。解释并修复。

## A zh
**`in` 作用在 `list` 上是 O(n)；作用在 `set` 或 `dict` 上平均是 O(1)。** 于是这个循环是 O(n²) —— 最多 10^10 次比较。

```python
seen_ids = set()          # 不是 []
if charge_id in seen_ids: ...
seen_ids.add(charge_id)
```

- 同类陷阱：`list.index`、`list.remove`、`list.count`，以及拿 `if x not in results` 当去重用。
- `x in some_dict` 和 `x in some_dict.keys()` 都是 O(1) —— 那是视图，不是拷贝。`x in list(some_dict)` 既是 O(n) **又**要分配内存。
- 如果还需要插入顺序，用值为 `None` 的 `dict`：O(1) 成员判断加有序遍历。
