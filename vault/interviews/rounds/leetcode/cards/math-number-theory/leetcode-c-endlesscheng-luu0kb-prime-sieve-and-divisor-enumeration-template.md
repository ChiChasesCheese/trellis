---
id: leetcode-c-endlesscheng-luu0kb-prime-sieve-and-divisor-enumeration-template
node: math-number-theory.prime-sieve-and-divisor-enumeration
type: cloze
anki: 1787272461380
tags: [concept-cloze, leetcode, recall, template]
---
埃氏筛对质数 p 标记合数时，从 {{c1::p * p}} 开始即可。

```
def prime_sieve(limit):
    is_prime = [True] * (limit + 1)
    if limit >= 0:
        is_prime[0] = False
    if limit >= 1:
        is_prime[1] = False
    for value in range(2, int(limit ** 0.5) + 1):
        if is_prime[value]:
            for multiple in range(value * value, limit + 1, value):
                is_prime[multiple] = False
    return is_prime
```

**Evidence**

五、数学：埃氏筛

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.19%20-%20%E7%AD%9B%E8%B4%A8%E6%95%B0%E4%B8%8E%E5%9B%A0%E5%AD%90%E6%9E%9A%E4%B8%BE)
