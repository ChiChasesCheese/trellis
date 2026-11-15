---
slug: smallest-missing-non-negative-integer-after-operations
---
## Q
**LC 2598 执行操作后的最大 MEX**｜Medium

整数数组 `nums` 和整数 `value`。可以对任意元素任意次地加上或减去 `value`。求操作后数组的最大 MEX（缺失的最小非负整数）。

## A
**一句话。** 元素模 `value` 的余数不变，每个元素能变成同余的任意整数；统计各余数的个数，依次放 `0, 1, 2, …`，第 `i` 个数消耗一个余数为 `i % value` 的元素，缺了就是 MEX。

```python
def find_smallest_integer(nums, value):
    cnt = Counter(x % value for x in nums)
    mex = 0
    while cnt[mex % value]:
        cnt[mex % value] -= 1      # 用掉一个同余的元素
        mex += 1
    return mex
```

**复杂度。** 时间 `O(n)`，空间 `O(value)`。

**易错点。**
- 负数取模：Python 里 `x % value` 已非负，其他语言要补成非负余数。
- 把余数当成具体的值去匹配：任何同余的元素都能变成目标，只用统计个数。

**追问。**
- 为什么一个一个试就够？：MEX 最多是 `n`，循环最多 `n` 步。

**同模式。** LC 41 缺失的第一个正数、LC 763 划分字母区间（Partition Labels）、LC 55 跳跃游戏
