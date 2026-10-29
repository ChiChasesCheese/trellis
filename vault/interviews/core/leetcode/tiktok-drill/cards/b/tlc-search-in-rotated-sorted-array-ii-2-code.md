---
id: tlc-search-in-rotated-sorted-array-ii-2-code
node: b.search-in-rotated-sorted-array-ii
type: qa
step: 2
---
## Q
**LC 81 搜索旋转排序数组 II**｜Medium · 字节高频｜写出 Python 实现

非降序数组（值可重复）被旋转后得到 `nums`（`1 <= nums.length <= 5000`，`-10^4 <= nums[i] <= 10^4`），判断 `target`（`-10^4 <= target <= 10^4`）是否在其中，返回布尔值。

## A
**思路。** 二分区间 `[lo, hi]`，`mid` 命中就返回 `True`。三个端点值都相等时无法判断方向，两端各缩一格。否则若 `nums[lo] <= nums[mid]`，左半有序：`target` 在 `[nums[lo], nums[mid])` 里就找左半，否则找右半；反之右半有序，对称处理。

```python
def search(nums: list[int], target: int) -> bool:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:      # 看不出哪半边有序：两端各缩一格（mid 不是 target）
            lo, hi = lo + 1, hi - 1
        elif nums[lo] <= nums[mid]:                # 左半 [lo, mid] 有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                      # 右半 [mid, hi] 有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

运行：`[2,5,6,0,0,1,2]` 找 `0` → `True`，找 `3` → `False`；`[1,0,1,1,1]` 找 `0` → `True`；`[1]` 找 `0` → `False`。

**复杂度。** 平均 `O(log n)`，最坏 `O(n)`（几乎全相同的值）；空间 `O(1)`。

**写法要点。** 链式比较 `nums[lo] == nums[mid] == nums[hi]` 和 `nums[lo] <= target < nums[mid]` 把区间判断写成一行，读起来像数学区间；`lo, hi = lo + 1, hi - 1` 元组赋值；`(lo + hi) // 2` 在 Python 里不会溢出，C++ / Java 要写 `lo + (hi - lo) // 2`；返回布尔值，不需要下标。
