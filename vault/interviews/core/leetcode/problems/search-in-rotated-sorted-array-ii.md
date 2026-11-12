---
slug: search-in-rotated-sorted-array-ii
---
## Q
**LC 81 搜索旋转排序数组 II**｜Medium

非降序数组（值可重复）在某处被旋转，判断 `target` 是否在其中。

## A
**一句话。** 二分时判断哪一半有序，看 `target` 是否在有序半边的值域内；两端与中点相等时看不出，就两端各缩一格。

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo, hi = lo + 1, hi - 1      # 无法判断，缩两端
        elif nums[lo] <= nums[mid]:      # 左半有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                            # 右半有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

**复杂度。** 时间 平均 `O(log n)`、最坏 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏掉三者相等就缩的分支：`[1,0,1,1,1]` 找 `0`，左半被当成有序而丢掉，返回 `False`，应为 `True`。
- 左半有序写成 `<` 而不是 `<=`：`[3,1]` 找 `1` 时 `lo == mid`，右半被当成有序，返回 `False`。

**追问。**
- 为什么最坏 `O(n)`？：`[1,1,1,2,1,1]` 这类数组断点在哪边无法判断，只能逐个排除。
- 求最小值（LC 154）？：`nums[mid] == nums[hi]` 时 `hi -= 1`，同样最坏 `O(n)`。

**同模式。** LC 33 搜索旋转排序数组、LC 153 寻找旋转排序数组中的最小值、LC 154 寻找旋转排序数组中的最小值 II、LC 34 在排序数组中查找首尾位置
