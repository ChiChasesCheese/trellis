---
id: tlc-binary-search-2-code
node: a.binary-search
type: qa
step: 2
---
## Q
**LC 704 二分查找**｜写出 Python 实现

升序数组 `nums`（元素互不相同，`1 <= n <= 10^4`，值在 `[-9999, 9999]`）和整数 `target`。找到则返回下标，否则返回 `-1`，时间 `O(log n)`。

## A
**思路。** 搜索区间 `[lo, hi)`，初值 `[0, n)`。取中点，`nums[mid] < target` 说明答案在右边，`lo = mid + 1`；否则答案在 `[lo, mid]`，`hi = mid`。区间为空时 `lo` 是第一个不小于 `target` 的位置，再看它是否真的等于 `target`。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                  # 搜索区间 [lo, hi)，左闭右开
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1                   # mid 太小，排除 [lo, mid]
        else:
            hi = mid                       # mid 可能就是答案，保留 [lo, mid)
    return lo if lo < len(nums) and nums[lo] == target else -1
```

运行：`([-1,0,3,5,9,12], 9)` → `4`，`([-1,0,3,5,9,12], 2)` → `-1`，`([5], 5)` → `0`，`([5], 2)` → `-1`，`([5], 9)` → `-1`；`[-9999, ..., 0]` 中查 `0` → `9999`，查 `1` → `-1`。

**复杂度。** 时间 `O(log n)`，`n = 10^4` 时约 `14` 次循环；空间 `O(1)`。

**写法要点。** `lo + (hi - lo) // 2` 在 Python 里和 `(lo + hi) // 2` 等价（整数不溢出），但在 Java / C++ 里能避免 `int` 溢出，面试里养成这个写法；只有一个判断分支 `<`，不在循环里判断相等，所以相等元素在 `hi` 一侧被保留，这套写法天然就是 `bisect_left`；循环外的 `lo < len(nums)` 防止 `target` 比所有元素都大时越界。`from bisect import bisect_left` 可以替代整个循环，但面试要求手写时用这版。
