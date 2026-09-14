---
id: cc-python-stdlib-itertools-calls
node: python.stdlib
type: qa
---
## Q
You need consecutive runs of equal keys, running totals, adjacent pairs and all unordered pairs. Which `itertools` calls — and what is the precondition that silently ruins the first one?

## A
```python
from itertools import groupby, accumulate, pairwise, combinations, chain
for key, grp in groupby(rows, key=lambda r: r.merchant):   # rows MUST be sorted by key
prefix = list(accumulate(values, initial=0))               # leading 0, length n+1
for a, b in pairwise(xs):                                  # consecutive pairs (3.10+)
for a, b in combinations(xs, 2):                           # every unordered pair
flat = list(chain.from_iterable(lists))                    # flatten one level
```

- **`groupby` groups only *adjacent* equal keys.** Unsorted input yields many one-element groups and no error — sort by the same key first, or use a `defaultdict`.
- `grp` is a one-shot iterator that is invalidated when you advance to the next group; materialize it with `list(grp)` if you need it twice.

## Q zh
你需要相同键的连续段、running total、相邻对、以及所有无序对。用哪些 `itertools` 调用 —— 以及什么前置条件会悄悄毁掉第一个？

## A zh
```python
from itertools import groupby, accumulate, pairwise, combinations, chain
for key, grp in groupby(rows, key=lambda r: r.merchant):   # rows 必须先按该 key 排序
prefix = list(accumulate(values, initial=0))               # 前置 0，长度 n+1
for a, b in pairwise(xs):                                  # 相邻对（3.10+）
for a, b in combinations(xs, 2):                           # 所有无序对
flat = list(chain.from_iterable(lists))                    # 展平一层
```

- **`groupby` 只把*相邻*的相同键归为一组。** 未排序的输入会产生一堆单元素分组且不报错 —— 先按同一个 key 排序，或改用 `defaultdict`。
- `grp` 是一次性迭代器，一旦推进到下一组就失效；需要用两次就 `list(grp)` 物化它。
