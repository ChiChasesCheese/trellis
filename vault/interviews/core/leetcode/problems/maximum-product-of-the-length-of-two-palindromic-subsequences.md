---
slug: maximum-product-of-the-length-of-two-palindromic-subsequences
---
## Q
**LC 2002 两个回文子序列长度的最大乘积**｜Medium

字符串 `s`（长度至多 `12`）。选两个**不相交**（下标不重叠）的回文子序列，使它们长度的乘积最大，返回这个乘积。

## A
**一句话。** 用二进制掩码表示一个子序列所选下标，先找出所有回文掩码及长度，再对每个掩码枚举其补集的子掩码，取乘积最大者。

```python
def max_product(s):
    n = len(s)
    pal = {}                              # 掩码 -> 回文长度
    for mask in range(1, 1 << n):
        t = ''.join(s[i] for i in range(n) if mask >> i & 1)
        if t == t[::-1]:
            pal[mask] = len(t)
    ans = 0
    full = (1 << n) - 1
    for a, la in pal.items():
        rest = full ^ a                    # 只能用剩下的下标
        b = rest
        while b:                           # 枚举 rest 的子掩码
            if b in pal:
                ans = max(ans, la * pal[b])
            b = (b - 1) & rest
    return ans
```

**复杂度。** 时间 `O(3^n + 2^n · n)`，空间 `O(2^n)`。

**易错点。**
- 枚举所有掩码对再判断相交：`4^n` 太慢，只枚举补集的子掩码是 `3^n`。
- 掩码对应的串不是回文也参与乘积：必须先过滤。

**追问。**
- 为什么是 `3^n`？：每个下标有三种状态，属于第一个、属于第二个、都不属于。

**同模式。** LC 78 子集、LC 1255 得分最高的单词集合、LC 1178 猜字谜
