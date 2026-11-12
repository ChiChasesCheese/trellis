---
slug: minimum-operations-to-make-the-array-increasing
---
## Q
**LC 1827 最少操作使数组递增**｜Easy

每次操作可把一个元素加 `1`。求让 `nums` 严格递增的最少操作次数。

## A
**一句话。** 从左到右一趟，每个数至少抬到「调整后的前一个数 + 1」。

```python
def min_operations(nums):
    ops = 0
    prev = nums[0]             # 调整后的前一个数
    for x in nums[1:]:
        t = max(x, prev + 1)
        ops += t - x
        prev = t
    return ops
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `prev` 记成原始的 `x`：`[1,5,2,4,1]` 得 `8`，应为 `14`。
- 目标写成 `prev` 而不是 `prev + 1`：只保证非递减，`[1,1,1]` 得 `0`，应为 `3`。

**追问。**
- 允许相等（非严格递增）？：目标改成 `max(x, prev)`。
- 为什么抬到刚好 `prev + 1` 最优？：抬得越高，后面要付的越多，所以只抬到刚好。

**同模式。** LC 945 使数组唯一的最小增量操作、LC 665 非递减数列、LC 2289 使数组按非递减顺序排列
