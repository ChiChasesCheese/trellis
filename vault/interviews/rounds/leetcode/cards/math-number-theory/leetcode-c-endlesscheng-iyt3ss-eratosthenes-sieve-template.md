---
id: leetcode-c-endlesscheng-iyt3ss-eratosthenes-sieve-template
node: math-number-theory.eratosthenes-sieve
type: cloze
anki: 1787272425307
tags: [concept-cloze, leetcode, recall, template]
---
埃氏筛的核心是：若 is_prime[p] 为真，就按步长 {{c1::p}} 标记倍数。

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
    return [x for x in range(2, limit + 1) if is_prime[x]]
```

**Evidence**

§1.2 预处理质数（筛质数）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.02%20-%20%E5%9F%83%E6%B0%8F%E7%AD%9B%E9%A2%84%E5%A4%84%E7%90%86%E8%B4%A8%E6%95%B0)
