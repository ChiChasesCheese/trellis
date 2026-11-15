---
slug: maximize-sum-of-array-after-k-negations
---
## Q
**LC 1005 K 次取反后最大化的数组和**｜Easy

一次操作可选一个下标 `i`，把 `nums[i]` 换成 `-nums[i]`（同一下标可重复选）。恰好做 `k` 次后，求数组和的最大值。

## A
**一句话。** 排序后优先翻转最小的负数；负数翻完仍有奇数次剩余，就翻一次绝对值最小的数（两次相当于没翻）。

```python
def largest_sum_after_k_negations(nums, k):
    nums.sort()
    for i in range(len(nums)):
        if nums[i] < 0 and k:        # 先翻最小的负数
            nums[i] = -nums[i]
            k -= 1
    # 还剩奇数次：翻一次绝对值最小的数
    return sum(nums) - (k % 2) * 2 * min(nums)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 次数剩下偶数还去翻：翻两次等于不翻，只需看 `k % 2`。
- 翻完负数后最小值不是绝对值最小：此时所有数都非负，`min(nums)` 就是绝对值最小的。
- `k` 用完以后还继续翻：用 `k` 控制，翻完立即停止。

**追问。**
- 为什么先翻最小的负数？：每翻一个负数，和增加 `2|x|`，越小的负数增益越大。
- 不排序能做吗？：用小根堆每次翻堆顶，`O(k log n)`。

**同模式。** LC 1029 两地调度、LC 1217 玩筹码、LC 455 分发饼干
