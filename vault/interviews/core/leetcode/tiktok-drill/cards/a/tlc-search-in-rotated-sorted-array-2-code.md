---
id: tlc-search-in-rotated-sorted-array-2-code
node: a.search-in-rotated-sorted-array
type: qa
step: 2
---
## Q
**LC 33 搜索旋转排序数组**｜写出 Python 实现

`nums` 是升序且值互不相同的数组旋转后的结果，`1 <= nums.length <= 5000`，`-10^4 <= nums[i] <= 10^4`，`-10^4 <= target <= 10^4`。返回 `target` 的下标，不存在返回 `-1`，要求 `O(log n)`。

## A
**思路。** 标准的 `lo <= hi` 二分。每轮取中点：命中就返回；否则判断哪半有序（`nums[lo] <= nums[mid]` 为左半），若 `target` 落在这半的值域内就收缩到这半，否则收缩到另一半。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                  # 左半 [lo, mid] 是有序的
            if nums[lo] <= target < nums[mid]:     # target 落在有序的左半里：去左边
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                      # 否则右半 [mid, hi] 一定有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

运行：`[4,5,6,7,0,1,2], 0` → `4`；`[4,5,6,7,0,1,2], 3` → `-1`；`[1], 0` → `-1`；`[1], 1` → `0`；`[3,1], 1` → `1`；`[5,1,3], 5` → `0`。

**复杂度。** 时间 `O(log n)`：每轮区间减半；空间 `O(1)`。

**写法要点。** 使用 `lo <= hi` 的闭区间写法，收缩时 `hi = mid - 1` / `lo = mid + 1`，区间每轮严格缩小，不会死循环；`nums[lo] <= nums[mid]` 的等号处理 `lo == mid` 的情形；链式比较 `nums[lo] <= target < nums[mid]` 一行表达"落在左半值域"；Python 的整数不会溢出，`(lo + hi) // 2` 安全，在 C++ / Java 里要写 `lo + (hi - lo) // 2`。
