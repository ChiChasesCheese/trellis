---
id: tlc-find-k-th-smallest-pair-distance-2-code
node: b.find-k-th-smallest-pair-distance
type: qa
step: 2
---
## Q
**LC 719 找出第 k 小的距离对**｜写出 Python 实现

整数数组 `nums`（`2 <= n <= 10^4`，`0 <= nums[i] <= 10^6`）和整数 `k`（`1 <= k <= n * (n - 1) / 2`）。返回所有数对 `(nums[i], nums[j])`（`i < j`）的距离 `|nums[i] - nums[j]|` 中第 `k` 小的。要求不枚举全部数对。

## A
**思路。** 先排序。写一个 `count_at_most(d)`：右端点 `right` 向右扫，`left` 在窗口里最小值离 `nums[right]` 超过 `d` 时右移，每个 `right` 贡献 `right - left` 个合法数对。然后在 `[0, nums[-1] - nums[0]]` 上二分，找最小的 `d` 使 `count_at_most(d) >= k`。

```python
def smallest_distance_pair(nums: list[int], k: int) -> int:
    nums = sorted(nums)

    def count_at_most(d: int) -> int:           # 距离 <= d 的数对个数（双指针，O(n)）
        count = left = 0
        for right, x in enumerate(nums):
            while x - nums[left] > d:           # 窗口里最小的数离 x 太远：左端右移
                left += 1
            count += right - left               # 以 right 为右端点的合法数对：left..right-1
        return count

    lo, hi = 0, nums[-1] - nums[0]              # 答案一定落在 [0, 最大差] 里
    while lo < hi:                              # 二分"最小的 d，使得 count_at_most(d) >= k"
        mid = (lo + hi) // 2
        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**运行。** `[1,3,1]`、`k = 1` → `0`；`[1,1,1]`、`k = 2` → `0`；`[1,6,1]`、`k = 3` → `5`；`[5,5]`、`k = 1` → `0`；`[0,1000000]`、`k = 1` → `1000000`。

**复杂度。** 时间 `O(n log n + n log V)`，`V = nums[-1] - nums[0]`；空间 `O(n)`。

**写法要点。** `count_at_most` 放在函数内部，直接读取外层排好序的 `nums`，不用传参；`for right, x in enumerate(nums)` 同时拿到下标和值；`left` 是 `count_at_most` 里的局部变量，只右移不回退，所以整趟是 `O(n)`；二分用 `lo, hi = 0, 最大差` 的「左闭右闭、`lo < hi`」写法，`>= k` 时收缩 `hi = mid`，否则 `lo = mid + 1`，结束时 `lo == hi` 就是答案。Python 3.10+ 也可以写成 `bisect_left(range(V + 1), k, key=count_at_most)`，行为等价，但先把显式循环写熟，面试中更稳。
