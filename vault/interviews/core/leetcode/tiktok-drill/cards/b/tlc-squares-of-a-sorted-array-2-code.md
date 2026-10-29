---
id: tlc-squares-of-a-sorted-array-2-code
node: b.squares-of-a-sorted-array
type: qa
step: 2
---
## Q
**LC 977 有序数组的平方**｜写出 Python 实现

有序数组 `nums`（非递减，长度 `1 ~ 10^4`，值在 `-10^4 ~ 10^4`，可能有负数），返回各元素平方后同样非递减的新数组。要求 `O(n)` 时间。

## A
**思路。** 结果数组从最后一格开始往前填。每步比较 `nums[left]²` 和 `nums[right]²`：较大的一定是剩余元素里平方最大的，写到当前位置，对应指针向内移动一格。

```python
def sorted_squares(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    for pos in range(n - 1, -1, -1):          # 从结果的最后一格往前填
        l2, r2 = nums[left] ** 2, nums[right] ** 2
        if l2 > r2:                            # 平方最大的一定在两端之一
            result[pos] = l2
            left += 1
        else:
            result[pos] = r2
            right -= 1
    return result
```

运行：`[-4,-1,0,3,10]` → `[0, 1, 9, 16, 100]`，`[-7,-3,2,3,11]` → `[4, 9, 9, 49, 121]`，`[-5]` → `[25]`，`[-3,-2,-1]` → `[1, 4, 9]`，`[1,2,3]` → `[1, 4, 9]`。

**复杂度。** 时间 `O(n)`：每次循环确定结果的一个位置，指针各自只前进不后退；空间 `O(n)`（输出数组，不算额外空间则是 `O(1)`）。

**写法要点。** `range(n - 1, -1, -1)` 倒序遍历结果下标；`** 2` 比 `x * x` 写起来清楚，两者对整数一样快；`result = [0] * n` 预分配，避免 `append` 再 `reverse`。同样的思想也可写成「分界点 + `heapq.merge`」：`k = bisect_left(nums, 0)`，负半边 `reversed(nums[:k])` 的平方递增，非负半边平方也递增，`list(heapq.merge(neg, pos))` 两路归并，惰性、`O(n)`。
