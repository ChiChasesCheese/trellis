---
slug: smallest-missing-integer-greater-than-sequential-prefix-sum
---
## Q
**LC 2996 大于等于顺序前缀和的最小缺失整数**｜Easy

最长「顺序前缀」是从 `nums[0]` 起每个数比前一个大 1 的前缀。返回不在 `nums` 中、且不小于该前缀和的最小整数。

## A
**一句话。** 先求最长顺序前缀之和，再放进集合，从这个和往上试，第一个不在集合里的就是答案。

```python
def missing_integer(nums):
    s = nums[0]
    for a, b in pairwise(nums):
        if b != a + 1:
            break                # 顺序前缀到此为止
        s += b
    seen = set(nums)
    while s in seen:
        s += 1
    return s
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 断开后继续累加后面的连续段：顺序前缀必须从下标 `0` 开始。
- 忘了答案可以等于前缀和本身：条件是「大于等于」。

**追问。**
- 为什么最多试 `n` 次？：集合只有 `n` 个数，最多挡住 `n` 个连续的候选。
- 找最小缺失正整数（LC 41）？：原地把每个数放到下标 `x - 1`，再扫一遍。

**同模式。** LC 41 缺失的第一个正数、LC 1539 第 k 个缺失的正整数
