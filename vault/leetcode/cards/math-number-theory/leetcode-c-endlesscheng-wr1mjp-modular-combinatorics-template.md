---
id: leetcode-c-endlesscheng-wr1mjp-modular-combinatorics-template
node: math-number-theory.modular-combinatorics
type: cloze
anki: 1787272475479
tags: [concept-cloze, leetcode, recall, template]
---
组合数模板为 {{c1::fact[n] * inv_fact[k] * inv_fact[n-k] % MOD}}。

```
MOD = 10**9 + 7

def build_combinations(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

    return comb
```

**Evidence**

6. 数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.20%20-%20%E7%BB%84%E5%90%88%E8%AE%A1%E6%95%B0%E4%B8%8E%E6%A8%A1%E9%80%86%E5%85%83)
