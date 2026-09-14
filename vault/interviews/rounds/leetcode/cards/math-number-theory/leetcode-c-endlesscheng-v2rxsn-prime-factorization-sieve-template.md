---
id: leetcode-c-endlesscheng-v2rxsn-prime-factorization-sieve-template
node: math-number-theory.prime-factorization-sieve
type: cloze
anki: 1787272468580
tags: [concept-cloze, leetcode, recall, template]
---
埃氏筛标记质数 p 的倍数时，从 {{c1::p * p}} 开始。

```
def sieve(limit):
    is_prime = [True] * (limit + 1)
    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return is_prime
```

**Evidence**

五、数学：质数筛法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.20%20-%20%E8%B4%A8%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3%E4%B8%8E%E7%AD%9B%E6%B3%95)
