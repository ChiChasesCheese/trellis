---
id: leetcode-c-endlesscheng-mdfnkw-combination-precompute-template
node: math-number-theory.combination-precompute
type: cloze
anki: 1787272452079
tags: [concept-cloze, leetcode, recall, template]
---
comb 函数返回 {{c1::fac[n] * inv_f[m] * inv_f[n - m] % MOD}}，前提是 0 <= m <= n，否则返回 0。

```
MOD = 1_000_000_007
MX = 100_001  # adjust based on problem constraints

fac = [0] * MX  # fac[i] = i!
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD

inv_f = [0] * MX  # inv_f[i] = (i!)^-1
inv_f[-1] = pow(fac[-1], -1, MOD)
for i in range(MX - 1, 0, -1):
    inv_f[i - 1] = inv_f[i] * i % MOD

def comb(n, m):
    # number of ways to choose m items out of n
    if m < 0 or m > n:
        return 0
    return fac[n] * inv_f[m] * inv_f[n - m] % MOD
```

**Evidence**

附：组合数的计算

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.07%20-%20%E7%BB%84%E5%90%88%E6%95%B0%E7%9A%84%E9%98%B6%E4%B9%98%E9%80%86%E5%85%83%E9%A2%84%E5%A4%84%E7%90%86)
