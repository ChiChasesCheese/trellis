---
id: tlc-kth-missing-positive-number-2-code
node: a.kth-missing-positive-number
type: qa
step: 2
---
## Q
**LC 1539 第 k 个缺失的正整数**｜写出 Python 实现

严格升序的正整数数组 `arr`（`1 <= arr.length <= 1000`，`1 <= arr[i] <= 1000`）和整数 `k`（`1 <= k <= 1000`）。返回缺失的第 `k` 个正整数，要求 `O(log n)`。

## A
**思路。** `arr[mid] - (mid + 1)` 是 `arr[mid]` 之前缺失的正整数个数，随 `mid` 单调不减。二分找第一个 `>= k` 的下标 `lo`（找不到就是 `n`），第 `k` 个缺失数是 `lo + k`。

```python
def find_kth_positive(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr)                   # 在 [0, n] 上找第一个下标 i，使 arr[i] 之前缺失的数 >= k
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) >= k:      # arr[mid] 之前缺了 arr[mid] - (mid + 1) 个正整数
            hi = mid
        else:
            lo = mid + 1
    return lo + k                          # 答案前面有 lo 个数在 arr 里：第 k 个缺失数 = k + lo
```

运行：`([2,3,4,7,11], 5)` → `9`，`([1,2,3,4], 2)` → `6`，`([2], 1)` → `1`，`([1], 1)` → `2`，`([1000], 1000)` → `1001`，`(list(range(1, 1001)), 1000)` → `2000`。

**复杂度。** 时间 `O(log n)`，约 `10` 轮；空间 `O(1)`。

**写法要点。** `hi = len(arr)` 而不是 `len(arr) - 1`，让“所有元素之前缺的都不够 `k`”也能表示为 `lo = n`；用 `lo < hi` 和 `hi = mid` 的模板找第一个满足条件的位置。Python 3.10 起可以把整个二分写成一行：`k + bisect_left(range(len(arr)), k, key=lambda i: arr[i] - i - 1)`，`range` 当作“虚拟的下标序列”，不占内存；面试里先写显式循环，再提这个。
