---
slug: search-insert-position
---
## Q
**LC 35 搜索插入位置**｜Easy

升序无重复数组 `nums`，找 `target` 的下标，找不到返回它应插入的位置，要求 `O(log n)`。

## A
**一句话。** 二分找第一个 `>= target` 的位置（下界），区间取左闭右开 `[lo, hi)`。

```python
def search_insert(nums, target):
    lo, hi = 0, len(nums)          # 答案可以是 len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1           # 答案在右边
        else:
            hi = mid               # mid 可能就是答案
    return lo
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- `hi` 写成 `len(nums) - 1`：取不到「插到末尾」，`([1,3,5,6], 7)` 得 `3`，应为 `4`。
- 条件写成 `nums[mid] <= target`：变成找上界，`([1,3,5,6], 5)` 得 `3`，应为 `2`。

**追问。**
- 有重复元素呢？：写法不变，返回第一个 `>= target` 的位置。
- Python 有现成函数吗？：`bisect_left(nums, target)`，语义完全相同。

**同模式。** LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 704 二分查找、LC 278 第一个错误的版本、LC 69 x 的平方根
