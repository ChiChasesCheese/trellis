---
id: tlc-find-peak-element-2-code
node: a.find-peak-element
type: qa
step: 2
---
## Q
**LC 162 寻找峰值**｜写出 Python 实现

整数数组 `nums`（长度 `1..1000`，元素在 32 位整数范围，相邻元素不相等），两端之外视为 `-∞`。返回任意一个峰值（严格大于左右邻居）的下标，要求 `O(log n)`。

## A
**思路。** 在闭区间 `[lo, hi]` 里维护「这里一定有峰」。取中点 `mid`，看它与右邻居：`nums[mid] < nums[mid + 1]` 说明在上坡，峰在右侧 `[mid + 1, hi]`；否则在下坡，峰在 `[lo, mid]`。区间缩到只剩一个下标时，它就是峰。

```python
def find_peak_element(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1          # 在闭区间 [lo, hi] 里一定还有峰值
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:  # 上坡：右边一定有峰（最坏一路爬到最右端）
            lo = mid + 1
        else:                          # 下坡：mid 自己或左边有峰（相邻不相等）
            hi = mid
    return lo
```

运行：`nums=[1,2,3,1]` → `2`，`nums=[1,2,1,3,5,6,4]（1 或 5 都对）` → `5`，`nums=[1]` → `0`，`nums=[3,2,1]（峰在最左）` → `0`，`nums=[1,2,3]（峰在最右）` → `2`，`nums=[-2**31, -2**31 + 1]` → `1`。

**复杂度。** 时间 `O(log n)`：每轮把搜索区间缩小一半；空间 `O(1)`。

**写法要点。** `while lo < hi` 配合 `hi = mid`，循环结束 `lo == hi`，直接 `return lo`，不需要事后检查；`mid = (lo + hi) // 2` 在 Python 里不会溢出（整数无限精度），不必写 `lo + (hi - lo) // 2`；比较的是 `mid` 与 `mid + 1`，因为 `lo < hi` 保证 `mid + 1 <= hi`，永不越界。标准库写法：`bisect.bisect_left(range(n - 1), True, key=lambda i: nums[i] > nums[i + 1])` 把「找一个上坡接下坡的位置」交给 `bisect`（Python 3.10+ 的 `key` 参数），区间都没有下坡时返回 `n - 1`，即最后一个元素。
