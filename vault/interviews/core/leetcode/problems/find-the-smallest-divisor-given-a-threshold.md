---
slug: find-the-smallest-divisor-given-a-threshold
---
## Q
**LC 1283 使结果不超过阈值的最小除数**｜Medium

给正整数数组 `nums` 和阈值 `threshold`，选一个正整数除数，把每个数除以它（向上取整）后求和，要求和不超过阈值。求最小的除数。

## A
**一句话。** 除数越大和越小，具有单调性；在 `[1, max(nums)]` 上二分，找最小的满足条件的除数。

```python
def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)            # 除数取 max 时和最小（等于 n）
    while lo < hi:
        mid = (lo + hi) // 2
        # 向上取整：(x + mid - 1) // mid
        need = sum((x + mid - 1) // mid for x in nums)
        if need <= threshold:
            hi = mid                 # 够小：试更小的除数
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log max)`，空间 `O(1)`。

**易错点。**
- 向上取整写成 `x // mid`：题目是向上取整，要 `(x + mid - 1) // mid`。
- 上界取 `sum(nums)`：`max(nums)` 已足够（此时每项都是 1），更紧。
- 可行时 `lo = mid + 1`：求最小的可行值，可行就收缩上界 `hi = mid`。

**追问。**
- 这是哪一类二分？：「最小化满足条件的值」，对答案二分，判定函数单调。
- 和 LC 875 爱吃香蕉的珂珂有何关系？：几乎一样，除数 = 吃香蕉速度，阈值 = 小时数。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 1482 制作 m 束花所需的最少天数
