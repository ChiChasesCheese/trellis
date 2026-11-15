---
slug: check-if-a-number-is-majority-element-in-a-sorted-array
---
## Q
**LC 1150 检查一个数是否在数组中占绝大多数**｜Easy

非递减数组 `nums` 和整数 `target`。若 `target` 出现的次数超过 `n / 2`，返回 `True`。

## A
**一句话。** 有序数组里超过一半的元素必然盖住中间位置；找到 `target` 第一次出现的下标 `i`，只要 `nums[i + n // 2]` 还是 `target` 就是占多数。

```python
def is_majority_element(nums, target):
    n = len(nums)
    i = bisect_left(nums, target)      # 第一次出现的位置
    return i + n // 2 < n and nums[i + n // 2] == target
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 不判越界：`i + n // 2` 可能超出数组长度，要先比较。
- 只判 `nums[n // 2] == target`：这只说明它盖住中位，次数可能恰好不超过一半的情形要靠第二个下标判断。
- 要求「超过」一半：恰好 `n / 2` 个不算，所以向右走 `n // 2` 步还要落在 `target` 上，保证个数 `≥ n // 2 + 1`。

**追问。**
- 也可以数个数吗？：`bisect_right - bisect_left > n // 2`，同样 `O(log n)`。
- 无序数组呢？：摩尔投票或哈希计数，`O(n)`。

**同模式。** LC 169 多数元素、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置
