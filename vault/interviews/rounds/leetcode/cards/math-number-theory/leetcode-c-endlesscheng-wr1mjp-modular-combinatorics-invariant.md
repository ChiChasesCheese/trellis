---
id: leetcode-c-endlesscheng-wr1mjp-modular-combinatorics-invariant
node: math-number-theory.modular-combinatorics
type: cloze
anki: 1787272475380
tags: [concept-cloze, invariant, leetcode, recall]
---
模质数 MOD 下，fact[i] 的逆元可用 {{c1::pow(fact[i], MOD - 2, MOD)}} 求得。

fact[i] = i! mod MOD；inv_fact[i] 是 fact[i] 的乘法逆元，因此 C(n,k)=fact[n]·inv_fact[k]·inv_fact[n-k]

**Evidence**

6. 数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.20%20-%20%E7%BB%84%E5%90%88%E8%AE%A1%E6%95%B0%E4%B8%8E%E6%A8%A1%E9%80%86%E5%85%83)
