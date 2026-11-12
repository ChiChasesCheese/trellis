---
slug: sum-of-subarray-minimums
---
## Q
**LC 907 子数组的最小值之和**｜Medium

求所有连续子数组的最小值之和，模 `10^9+7`。

## A
**一句话。** 算每个元素的贡献：值 × 左延伸长度 × 右延伸长度，边界用单调栈一趟求出。

```python
def sum_subarray_mins(arr):
    stack = []                 # 下标栈，值严格递增
    total = 0
    for i, x in enumerate(arr + [0]):   # 哨兵 0 把栈弹空
        while stack and arr[stack[-1]] >= x:
            j = stack.pop()    # i 是 j 右边第一个 <= 它的数
            left = stack[-1] if stack else -1
            total += arr[j] * (j - left) * (i - j)
        stack.append(i)
    return total % (10**9 + 7)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 两侧都用严格比较：并列最小值被重复计数，`[2,2,2]` 算成 `20`，应为 `12`。
- 忘了哨兵：栈里剩下的元素没结算，漏掉延伸到末尾的子数组。

**追问。**
- 最大值之和呢？：比较方向反过来；两者相减就是极差之和（LC 2104）。
- 为什么一侧用 `>=`、另一侧用 `<`？：并列最小值只归给其中一个，保证每个子数组只算一次。

**同模式。** LC 2104 子数组范围和、LC 84 柱状图中最大的矩形、LC 739 每日温度、LC 1856 子数组最小乘积的最大值
