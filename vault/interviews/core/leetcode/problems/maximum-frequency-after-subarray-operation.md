---
slug: maximum-frequency-after-subarray-operation
---
## Q
**LC 3434 子数组操作后的最大频率**｜Medium

给子数组的所有元素加同一个 `x`（只做一次），求操作后 `k` 的最大出现次数。值域 `1..50`。

## A
**一句话。** 枚举被变成 `k` 的原值 `v`：子数组里 `v` 记 `+1`、`k` 记 `-1`，最大子数组和就是能多出来的 `k`，加上原有的 `k` 个数。

```python
def max_frequency(nums, k):
    gain = 0
    for v in set(nums):
        if v == k:
            continue
        run = 0                 # 以当前结尾的最大 (#v - #k)
        for x in nums:
            run = max(run, 0) + (x == v) - (x == k)
            gain = max(gain, run)
    return nums.count(k) + gain
```

**复杂度。** 时间 `O(50·n)`，空间 `O(1)`。

**易错点。**
- 子数组里原来的 `k` 忘了扣：加 `x ≠ 0` 后它们不再是 `k`，所以记 `-1`。
- `gain` 初值为负或不取 `0`：可以不操作（`x = 0`），多出来的至少是 `0`。

**追问。**
- 值域很大？：只枚举出现过的值，每个值只在自己的位置和 `k` 的位置上做 Kadane，总 `O(n)` 级。
- 为什么是最大子数组和？：总频率 = 全局 `k` 数 + 子数组内（`v` 数 - `k` 数），只有后一项随子数组变化。

**同模式。** LC 53 最大子数组和、LC 1749 任意子数组和的绝对值的最大值、LC 2272 最大波动的子字符串
