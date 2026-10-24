---
id: tlc-patterns-binary-search-4-index
node: patterns.binary-search
type: qa
step: 4
---
## Q
**二分查找（Binary Search）｜在下标上二分：旋转数组、最小值、峰值、只出现一次的数**

这些「不完全有序」的数组怎样判断答案在哪一半？写出 LC 33 和 LC 153 的二分，并指出 `<` 与 `<=` 的区别。

## A
关键：每次比较 `mid` 与端点，**确定哪一半是有序的 / 答案不可能在哪一半**。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:          # 左半 [lo, mid] 有序（<= 处理 lo == mid）
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                              # 右半 [mid, hi] 有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

def find_min(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:           # 断点在右半，最小值在 (mid, hi]
            lo = mid + 1
        else:
            hi = mid                       # 最小值在 [lo, mid]
    return nums[lo]
```

运行：`search([4,5,6,7,0,1,2], 0)` → `4`，`search(..., 3)` → `-1`，`search([3,1], 1)` → `1`；`find_min([3,4,5,1,2])` → `1`，`find_min([2,1])` → `1`。

- `<=` 的意义：当 `lo == mid`（区间只剩两个元素）时左半只有一个元素，也算有序。把 `nums[lo] <= nums[mid]` 误写成 `<`，`search([3, 1], 1)` 返回 `-1`，正确是 `1`。
- **峰值**（LC 162）：比较 `nums[mid]` 与 `nums[mid+1]`，上坡则峰在右（`lo = mid + 1`），否则在 `[lo, mid]`；`lo < hi` 终止时 `lo` 即峰。
- **有序数组中唯一的单个数**（LC 540）：让 `mid` 落到偶数下标，若 `nums[mid] == nums[mid+1]`，前半成对完整，单个数在右，`lo = mid + 2`，否则 `hi = mid`。
