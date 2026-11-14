---
slug: concatenate-non-zero-digits-and-multiply-by-sum-ii
---
## Q
**LC 3756 连接非零数字并乘以其数字和 II**｜Medium

数字串 `s`（长 `10^5`）和 `10^5` 个查询 `[l, r]`：把 `s[l..r]` 的非零数字连成 `x`，答案是 `x·(数字和) mod 10^9+7`。

## A
**一句话。** 前缀拼接值：`val[i]` 是前 `i` 位非零数字拼成的数，区间的 `x = val[r+1] - val[l]·10^(区间非零个数)`，像字符串哈希一样 `O(1)` 切出来。

```python
def sum_and_multiply(s, queries):
    MOD = 10**9 + 7
    n = len(s)
    val = [0] * (n + 1)    # 前缀非零数字拼成的数
    cnt = [0] * (n + 1)    # 前缀非零数字个数
    dsum = [0] * (n + 1)   # 前缀数字和
    pw = [1] * (n + 1)
    for i, ch in enumerate(s):
        d = int(ch)
        val[i + 1] = val[i]
        if d:                   # 零不接到末尾
            val[i + 1] = (val[i] * 10 + d) % MOD
        cnt[i + 1] = cnt[i] + (d > 0)
        dsum[i + 1] = dsum[i] + d
        pw[i + 1] = pw[i] * 10 % MOD
    ans = []
    for l, r in queries:
        k = cnt[r + 1] - cnt[l]          # 区间里非零个数
        x = (val[r + 1] - val[l] * pw[k]) % MOD
        ans.append(x * (dsum[r + 1] - dsum[l]) % MOD)
    return ans
```

**复杂度。** 时间 `O(n + q)`，空间 `O(n)`。

**易错点。**
- 乘的是 `10^(r-l+1)`：零不占位，指数要用区间里非零数字的个数。
- 先对 `x` 取模再求数字和：数字和要用原数字算（前缀和 `dsum`），不能从取模后的 `x` 拆。

**追问。**
- 为什么能相减？：`val[r+1] = val[l]·10^k + x`，和字符串多项式哈希的切片一模一样。
- 还要支持单点修改？：线段树存 `(拼接值, 非零个数)`，合并 `左值·10^右个数 + 右值`。

**同模式。** LC 303 区域和检索 - 数组不可变、LC 3754 连接非零数字并乘以其数字和 I、LC 2156 查找给定哈希值的子串
