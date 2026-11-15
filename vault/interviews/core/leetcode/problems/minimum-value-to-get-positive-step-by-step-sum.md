---
slug: minimum-value-to-get-positive-step-by-step-sum
---
## Q
**LC 1413 逐步求和得到正数的最小值**｜Easy

给整数数组 `nums`，选一个正整数初值 `startValue`，从左到右累加 `nums`，要求每一步的累加值都不小于 `1`。求最小的 `startValue`。

## A
**一句话。** 记前缀和的最小值 `low`，起始值只需把最低点抬到 `1`，即 `1 - low`（至少为 `1`）。

```python
def min_start_value(nums):
    low = cur = 0
    for x in nums:
        cur += x
        low = min(low, cur)          # 最低的前缀和
    return 1 - low                   # 抬到最低点也不小于 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `low` 初值取很大：前缀和全为正时，`1 - low` 会是负数，`low` 要从 `0` 起，保证答案至少为 `1`。
- 忘了每一步都要大于等于 `1`：不是只看最终结果，要看前缀和的最小值。

**追问。**
- 为什么是 `1 - low`？：起始值加最低前缀和 `≥ 1`，所以起始值 `≥ 1 - low`。
- 类似的题？：LC 2304 游戏的最少生命值，也是求前缀最小值再抬到下限。

**同模式。** LC 174 地下城游戏、LC 53 最大子数组和
