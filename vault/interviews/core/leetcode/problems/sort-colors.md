---
slug: sort-colors
---
## Q
**LC 75 颜色分类**｜Medium

原地把只含 `0`、`1`、`2` 的数组排好序，不用库排序，最好一趟完成。

## A
**一句话。** 荷兰国旗三指针：`low` 左边全 `0`，`high` 右边全 `2`，`mid` 扫描未知区。

```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:            # nums[mid:high+1] 还没看
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1              # 换回来的必是 1，mid 可前进
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1             # 换来的没看过，mid 不动
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 与 `2` 交换后让 `mid` 前进：`[1,2,0]` 得 `[1,0,2]`，换来的 `0` 没再检查。
- 循环条件写 `mid < high`：`high` 指的位置还没处理，要 `<=`。

**追问。**
- 有更不易错的写法吗？：两趟计数，先数各颜色个数再覆盖回数组，`O(n)` 时间 `O(1)` 空间。
- 稳定吗？：不稳定，与 `high` 交换会打乱相同值的相对顺序。
- 推广到 `k` 种颜色？：计数排序 `O(n+k)`，或按颜色区间中点递归两路划分 `O(n log k)`。

**同模式。** LC 283 移动零、LC 215 数组中的第 K 个最大元素、LC 905 按奇偶排序数组、LC 31 下一个排列
