---
slug: merge-operations-to-turn-array-into-a-palindrome
---
## Q
**LC 2422 使用合并操作将数组转换为回文序列**｜Medium

每次操作可把两个相邻元素合并成它们的和。求把正整数数组变成回文所需的最少操作数。

## A
**一句话。** 双指针从两端向中间，两端相等就各收一格，否则贪心合并较小的一端。

```python
def minimum_operations(nums):
    l, r = 0, len(nums) - 1
    left, right = nums[l], nums[r]   # 两端当前的值
    ops = 0
    while l < r:
        if left == right:            # 配成一对
            l += 1
            r -= 1
            left, right = nums[l], nums[r]
        elif left < right:           # 小的一端并入邻居
            l += 1
            left += nums[l]
            ops += 1
        else:
            r -= 1
            right += nums[r]
            ops += 1
    return ops
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 相等时只移指针、不重新取 `left`、`right`：`[4,3,2,1,2,3,1]` 得 `1`，应为 `2`。
- 合并较大的一端：只会更大，永远追不上，同一输入得 `6`。

**追问。**
- 为什么合并小的一端是对的？：元素都为正，合并只会变大，较小一端不动就永远对不上。
- 元素可为 0 或负数呢？：合并只会变大的前提不成立，贪心失效，需要重新推导。

**同模式。** LC 125 验证回文串、LC 680 验证回文串 II、LC 1616 分割两个字符串得到回文串、LC 1312 让字符串成为回文串的最少插入次数
