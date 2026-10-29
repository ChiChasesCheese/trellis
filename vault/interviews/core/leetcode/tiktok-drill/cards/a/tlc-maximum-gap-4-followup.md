---
id: tlc-maximum-gap-4-followup
node: a.maximum-gap
type: qa
step: 4
---
## Q
**LC 164 最大间距**｜追问

面试官接着问：（1）要返回产生最大间距的那一对数？（2）数值范围很小（例如 `<= 10^6`）时有更简单的做法吗？（3）为什么不直接 `sorted`？

## A
1. **返回数对。** 扫桶时同时记录 `(prev_max, mn)`：

```python
def maximum_gap_pair(nums: list[int]) -> tuple[int, int] | None:
    n = len(nums)
    if n < 2:
        return None
    lo, hi = min(nums), max(nums)
    if lo == hi:
        return None
    size = max(1, (hi - lo) // (n - 1))
    count = (hi - lo) // size + 1
    bucket_min = [hi + 1] * count
    bucket_max = [-1] * count
    for x in nums:
        i = (x - lo) // size
        bucket_min[i] = min(bucket_min[i], x)
        bucket_max[i] = max(bucket_max[i], x)
    best, pair, prev_max = 0, None, lo
    for mn, mx in zip(bucket_min, bucket_max):
        if mx < 0:
            continue
        if mn - prev_max > best:
            best, pair = mn - prev_max, (prev_max, mn)
        prev_max = mx
    return pair
```

2. **值域小。** 用 `present = [False] * (V + 1)` 标记出现过的值，一遍扫描记录相邻出现值的差，`O(n + V)`；`V` 超过 `n` 的几十倍就不划算，回到桶方案。
3. **为什么不 `sorted`。** `sorted` 是 `O(n log n)`，不满足题目的线性要求；但 Python 的排序在 C 里实现，`10^5` 个数一般更快。实战里先给线性的桶 / 基数方案，再说明 `sorted` + `pairwise` 的取舍。

**Python 提醒**：`max(b - a for a, b in pairwise(sorted(nums)))` 在只有一个元素时 `pairwise` 为空，`max` 抛 `ValueError: max() iterable argument is empty`，要写 `max(..., default=0)`。
