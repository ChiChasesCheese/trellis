---
slug: two-sum-ii-input-array-is-sorted
---
## Q
**LC 167 两数之和 II - 输入有序数组**｜Medium

非递减数组 `numbers`，找两个不同位置的数之和为 `target`，返回 1 开始的下标，只能用常数空间。

## A
**一句话。** 对撞指针，和太小左指针右移，太大右指针左移。

```python
def two_sum(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo < hi:      # 两个下标必须不同
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1     # lo 配最大的 hi 都不够：淘汰 lo
        else:
            hi -= 1     # hi 配最小的 lo 都超了：淘汰 hi
    return []
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 返回 0 开始的下标：`([2,7,11,15], 9)` 得 `[0,1]`，应为 `[1,2]`。
- 循环条件写成 `lo <= hi`：同一个元素被用两次。
- 方向写反：`s < target` 时移右指针，会漏掉答案。

**追问。**
- 要输出所有不重复的解？：移动指针时跳过相同值（见三数之和）。
- 输入无序？：哈希表一遍扫，或排序后保留原下标再对撞。

**同模式。** LC 1 两数之和、LC 15 三数之和、LC 11 盛最多水的容器、LC 653 两数之和 IV
