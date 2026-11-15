---
slug: number-of-different-subsequences-gcds
---
## Q
**LC 1819 序列中不同最大公约数的数目**｜Hard

给正整数数组 `nums`。求所有非空子序列的最大公约数一共有多少个不同的值。

## A
**一句话。** 枚举候选值 `g`：看 `nums` 中所有 `g` 的倍数，它们的最大公约数恰为 `g` 就说明存在子序列取到 `g`。

```python
def count_different_subsequence_gcds(nums):
    present = set(nums)
    mx = max(nums)
    ans = 0
    for g in range(1, mx + 1):
        d = 0
        for m in range(g, mx + 1, g):    # g 的所有倍数
            if m in present:
                d = gcd(d, m)
                if d == g:               # 倍数们的 gcd 降到 g
                    ans += 1
                    break
    return ans
```

**复杂度。** 时间 `O(M log M · log M)`（调和级数，`M` 为最大值），空间 `O(M)`。

**易错点。**
- 枚举子序列：指数级；换成"枚举答案值再验证"。
- 忘了 `d == g` 之后立刻停：多余的倍数不会让 gcd 变小，继续只是浪费。

**追问。**
- 为什么只看倍数？：gcd 为 `g` 的子序列里每个数都是 `g` 的倍数；`g` 的所有倍数的 gcd 若恰为 `g`，就能取到，若大于 `g`，任何由倍数组成的子序列 gcd 都不会是 `g`。

**同模式。** LC 2709 最大公约数遍历、LC 952 按公因数计算最大组件大小、LC 1071 字符串的最大公因子
