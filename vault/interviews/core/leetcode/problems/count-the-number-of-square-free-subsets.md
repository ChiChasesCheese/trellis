---
slug: count-the-number-of-square-free-subsets
---
## Q
**LC 2572 无平方子集计数**｜Medium

整数数组 `nums`（每个数在 `1` 到 `30` 之间）。若一个子集的乘积不能被任何大于 `1` 的完全平方数整除，它就是"无平方子集"。求非空无平方子集的个数，对 `10^9 + 7` 取模（下标不同的子集算不同）。

## A
**一句话。** 只有 `10` 个质数 `≤ 30`：用 `10` 位掩码记录已用的质数，`dp[mask]` 为乘积质因子集合恰为 `mask` 的方案数；含平方因子的数直接跳过。

```python
def square_free_subsets(nums):
    M = 10 ** 9 + 7
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    dp = [0] * 1024
    dp[0] = 1                              # 空集
    for x in nums:
        mask, ok = 0, True
        for i, p in enumerate(primes):
            if x % (p * p) == 0:           # 含平方因子，不能选
                ok = False
                break
            if x % p == 0:
                mask |= 1 << i
        if not ok:
            continue
        for s in range(1023, -1, -1):      # 倒序，每个数只选一次
            if s & mask == 0:
                dp[s | mask] = (dp[s | mask] + dp[s]) % M
    return (sum(dp) - 1) % M               # 去掉空集
```

**复杂度。** 时间 `O(n · 2^10)`，空间 `O(2^10)`。

**易错点。**
- 正序遍历 `s`：同一个数会被选多次，要倒序（01 背包）。
- 忘了数字 `1`：`mask` 为 `0`，每个 `1` 让方案数翻倍，上面的循环自然处理。
- 最后忘了减去空集。

**追问。**
- 为什么只需要 `10` 个质数？：`30` 以内的质数只有 `2 3 5 7 11 13 17 19 23 29`。

**同模式。** LC 78 子集、LC 1994 好子集的数目
