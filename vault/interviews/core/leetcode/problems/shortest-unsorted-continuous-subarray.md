---
slug: shortest-unsorted-continuous-subarray
---
## Q
**LC 581 最短无序连续子数组**｜Medium

找最短的连续子数组，把它升序排序后整个数组有序，返回其长度。

## A
**一句话。** 左扫维护前缀最大值，比它小的位置都得排，最后一个是右端；右扫同理定左端。

```python
def find_unsorted_subarray(nums):
    n = len(nums)
    start, end = 0, -1       # 有序时 end-start+1 == 0
    hi, lo = -inf, inf       # 左边最大 / 右边最小
    for i in range(n):
        if nums[i] < hi:     # 左边有更大的，i 要排
            end = i
        else:
            hi = nums[i]
        j = n - 1 - i
        if nums[j] > lo:     # 右边有更小的，j 要排
            start = j
        else:
            lo = nums[j]
    return end - start + 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只看相邻逆序对：`[1,2,4,5,3]` 得 `2`，应为 `3`，`4` 也比 `3` 大。
- 比较写成 `<=`：重复值被当成无序，`[1,1,1]` 得 `3`，应为 `0`。

**追问。**
- 最简单的写法？：`sorted(nums)` 与原数组逐位比较，取首尾不同处，`O(n log n)`。
- 单调栈怎么做？：正反各扫一遍，弹出的最小下标是左端、最大下标是右端，要 `O(n)` 额外空间。

**同模式。** LC 768 最多能完成排序的块 II、LC 769 最多能完成排序的块、LC 42 接雨水、LC 238 除自身以外数组的乘积
