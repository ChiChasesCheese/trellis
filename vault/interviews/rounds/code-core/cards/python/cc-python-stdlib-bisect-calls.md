---
id: cc-python-stdlib-bisect-calls
node: python.stdlib
type: qa
---
## Q
A sorted list of timestamps. You need the insertion point, "how many are ≤ t", "how many fall in [lo, hi]", and to keep the list sorted as items arrive. Which `bisect` calls, exactly?

## A
```python
import bisect
i = bisect.bisect_left(xs, t)    # first index with xs[i] >= t
j = bisect.bisect_right(xs, t)   # first index with xs[j] >  t
count_le  = bisect.bisect_right(xs, t)
in_range  = bisect.bisect_right(xs, hi) - bisect.bisect_left(xs, lo)   # lo <= x <= hi
bisect.insort(xs, t)             # insert in order: O(log n) search, O(n) shift
```

- `bisect_left` finds the first element **not less than** `t`; `bisect_right` the first **greater**. They differ only on exact hits — which is exactly where an inclusive-versus-exclusive boundary lives.
- Python 3.10+ accepts `key=`. Neither function works on a descending list — negate the values instead.

## Q zh
一个有序的时间戳列表。你需要插入位置、「有多少个 ≤ t」、「有多少个落在 [lo, hi]」，以及在新项到达时保持列表有序。具体用哪些 `bisect` 调用？

## A zh
```python
import bisect
i = bisect.bisect_left(xs, t)    # 第一个满足 xs[i] >= t 的下标
j = bisect.bisect_right(xs, t)   # 第一个满足 xs[j] >  t 的下标
count_le  = bisect.bisect_right(xs, t)
in_range  = bisect.bisect_right(xs, hi) - bisect.bisect_left(xs, lo)   # lo <= x <= hi
bisect.insort(xs, t)             # 有序插入：查找 O(log n)，移动 O(n)
```

- `bisect_left` 找第一个**不小于** `t` 的元素；`bisect_right` 找第一个**大于**的。两者只在精确命中时不同 —— 而闭区间与开区间的边界正好就在那里。
- Python 3.10+ 支持 `key=`。两者都不适用于降序列表 —— 请把值取负。
