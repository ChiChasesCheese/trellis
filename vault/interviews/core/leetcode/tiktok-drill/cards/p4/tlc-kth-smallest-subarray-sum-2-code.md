---
id: tlc-kth-smallest-subarray-sum-2-code
node: p4.kth-smallest-subarray-sum
type: qa
step: 2
---
## Q
**LC 1918 第 K 小的子数组和**｜写出 Python 实现

正整数数组 `nums`（`1 <= n <= 2 * 10^4`，`1 <= nums[i] <= 5 * 10^4`）和整数 `k`（`1 <= k <= n(n+1)/2`），返回所有非空连续子数组的和中第 `k` 小的值。要求 `O(n log S)`。

## A
**思路。** 二分答案 `x`。`count_le(x)` 用双指针数出和不超过 `x` 的子数组个数；若个数不小于 `k`，答案不超过 `x`，收缩上界；否则抬高下界。

```python
def kth_smallest_subarray_sum(nums: list[int], k: int) -> int:
    def count_le(x: int) -> int:                  # 和 <= x 的子数组个数（元素全为正，双指针）
        cnt = left = cur = 0
        for right, v in enumerate(nums):
            cur += v
            while cur > x:                        # 窗口和超标：收缩左端
                cur -= nums[left]
                left += 1
            cnt += right - left + 1               # 以 right 结尾、左端在 [left, right] 的子数组都 <= x
        return cnt

    lo, hi = min(nums), sum(nums)                 # 答案一定落在 [最小元素, 总和]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:                    # 至少 k 个子数组 <= mid：答案 <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo
```

运行：`([2,1,3], 4)` → `3`；`([3,3,5,5], 7)` → `10`；`([5], 1)` → `5`；`([2,1,3], 1)` → `1`；`([2,1,3], 6)` → `6`。

**复杂度。** 时间 `O(n log S)`：`S = sum(nums)` 最多 `10^9`，约 `30` 轮，每轮 `O(n)`；空间 `O(1)`。

**写法要点。** 二分用「`lo < hi`，满足条件时 `hi = mid`，否则 `lo = mid + 1`」这一套左边界模板，终止时 `lo == hi` 就是最小满足条件的值；内部函数 `count_le` 通过闭包使用 `nums`；`cnt = left = cur = 0` 链式初始化三个整数；`enumerate` 同时给出下标与值。Python 3.10+ 还可以写成 `lo + bisect_left(range(lo, hi + 1), k, key=count_le)`，`bisect` 对 `range` 做二分，`key` 把整数 `x` 映射成 `count_le(x)`。
