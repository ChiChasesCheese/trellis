---
slug: first-missing-positive
---
## Q
**LC 41 缺失的第一个正数**｜Hard

未排序整数数组 `nums`，找出没出现的最小正整数。要求 `O(n)` 时间、`O(1)` 额外空间。

## A
**一句话。** 答案在 `[1, n+1]`：把数组当哈希表，循环排序把每个 `x` 换到下标 `x-1`，第一个站错位的下标加一就是答案。

```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= (x := nums[i]) <= n and nums[x - 1] != x:
            # x 已固定目标下标，交换不会改变它
            nums[i], nums[x - 1] = nums[x - 1], x
    for i, x in enumerate(nums):
        if x != i + 1:
            return i + 1
    return n + 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 一行元组交换 `nums[i], nums[nums[i]-1] = ...`：先改了 `nums[i]`，第二个下标用了新值，`[3,4,-1,1]` 死循环。
- 不判目标位置是否已是 `x`：重复值 `[1,1]` 与自己无限交换。
- 条件先取 `nums[nums[i]-1]` 再判范围：`-1`、`0` 或超大值越界，要让 `1 <= nums[i] <= n` 在前。

**追问。**
- 为什么是 `while` 不是 `if`？：换回来的数可能仍在 `[1,n]`，还没归位。
- 不许改输入怎么办？：放进 `set` 从 `1` 数起，`O(n)` 空间。

**同模式。** LC 268 丢失的数字、LC 287 寻找重复数、LC 442 数组中重复的数据、LC 448 找到所有数组中消失的数字
