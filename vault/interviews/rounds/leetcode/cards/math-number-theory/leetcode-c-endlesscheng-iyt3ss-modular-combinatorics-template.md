---
id: leetcode-c-endlesscheng-iyt3ss-modular-combinatorics-template
node: math-number-theory.modular-combinatorics
type: cloze
anki: 1787272427107
tags: [concept-cloze, leetcode, recall, template]
---
模质数下，逆阶乘可由 {{c1::pow(fac[limit], mod-2, mod)}} 倒推。

```
def build_combinations(limit, mod):
    fac = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fac[i] = fac[i - 1] * i % mod
    inv_fac = [1] * (limit + 1)
    inv_fac[limit] = pow(fac[limit], mod - 2, mod)
    for i in range(limit, 0, -1):
        inv_fac[i - 1] = inv_fac[i] * i % mod
    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fac[n] * inv_fac[k] % mod * inv_fac[n - k] % mod
    return comb
```

**Evidence**

§2.2 组合计数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.08%20-%20%E7%BB%84%E5%90%88%E8%AE%A1%E6%95%B0%E3%80%81%E9%9A%94%E6%9D%BF%E6%B3%95%E4%B8%8E%E6%A8%A1%E7%BB%84%E5%90%88%E6%95%B0)
