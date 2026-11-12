---
slug: tt-sorted-array-more-than-n-over-3
---
## Q
**有序数组中出现次数超过 n/3 的数**｜Medium

非递减有序整数数组 `nums`，升序返回所有出现次数大于 `n / 3` 的数，要求时间低于 `O(n)`。例：`[1,1,2,4,4]` → `[1,4]`。

## A
**一句话。** 令 `step = n // 3`，满足条件的值至少占 `step + 1` 个连续下标，必含某个 `step` 的倍数下标，只验证这至多 5 个候选，每个用两次二分数次数。

```python
def more_than_third(nums):
    n = len(nums)
    step = n // 3       # 次数 > n/3，即至少 step + 1 次
    ans = []
    # 候选：每隔 step 取一个下标上的值
    for v in sorted({nums[i] for i in range(0, n, step)}):
        cnt = bisect_right(nums, v) - bisect_left(nums, v)
        if 3 * cnt > n:     # 整数比较，不用浮点
            ans.append(v)
    return ans
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 「大于」写成「大于等于」：`[1,1,2,2,3,3]` 每个值恰好 `n / 3` 次，应为 `[]`，写成 `>=` 得 `[1,2,3]`。
- 只检查一个位置：`[1,1,2,4,4]` 只看 `nums[n // 3]` 漏掉 `4`，超过 `n/3` 的值最多两个。

**追问。**
- 超过 `n/k` 怎么办？：`step = n // k`，候选仍每隔 `step` 取一个，总成本 `O(k log n)`。
- 数组无序、要求 `O(n)` 时间 `O(1)` 空间？：Boyer–Moore 多数投票推广，维护 `k - 1` 个候选再验证（LC 229）。

**同模式。** LC 229 多数元素 II、LC 169 多数元素、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 1150 检查数字是否为排序数组中的多数元素
