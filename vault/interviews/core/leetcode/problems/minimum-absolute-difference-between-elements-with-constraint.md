---
slug: minimum-absolute-difference-between-elements-with-constraint
---
## Q
**LC 2817 限制条件下元素之间的最小绝对差**｜Medium

数组 `nums` 和整数 `x`，在满足 `abs(i-j) >= x` 的下标对中，求 `abs(nums[i]-nums[j])` 的最小值。

## A
**一句话。** 从左扫 `i`，把已满足距离的 `nums[i-x]` 依次插入有序列表，二分找 `nums[i]` 的前驱和后继。

```python
def min_absolute_difference(nums, x):
    seen = []                      # 距离已 >= x 的值，升序
    best = inf
    for i in range(x, len(nums)):
        insort(seen, nums[i - x])
        v = nums[i]
        k = bisect_left(seen, v)
        if k < len(seen):
            best = min(best, seen[k] - v)      # 后继
        if k > 0:
            best = min(best, v - seen[k - 1])  # 前驱
    return best
```

**复杂度。** 时间 `O(n log n)`（`insort` 搬移最坏 `O(n²)`，实际是内存拷贝，很快），空间 `O(n)`。

**易错点。**
- 把 `nums[i]` 自己也放进候选：`[1,2,3,4], x=3` 得 `0`，应为 `3`。
- 只看后继不看前驱：`[5,3,2,10,15], x=1` 里 `2` 的最近邻 `3` 在前面，漏掉会偏大。

**追问。**
- 改成 `abs(i-j) <= x` 呢？：滑动窗口，要支持删除，用 `SortedList` 或延迟删除的堆。
- 要返回下标对？：存 `(值, 下标)` 并在更新 `best` 时记录。

**同模式。** LC 220 存在重复元素 III、LC 729 我的日程安排表 I、LC 658 找到 K 个最接近的元素
