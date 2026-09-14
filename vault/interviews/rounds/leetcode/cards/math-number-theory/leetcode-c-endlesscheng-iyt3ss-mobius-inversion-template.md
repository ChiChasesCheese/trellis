---
id: leetcode-c-endlesscheng-iyt3ss-mobius-inversion-template
node: math-number-theory.mobius-inversion
type: cloze
anki: 1787272426805
tags: [concept-cloze, leetcode, recall, template]
---
筛 μ 时，对每个质数 p 需把 p² 的倍数设为 {{c1::0}}。

```
def mobius(limit):
    mu = [1] * (limit + 1)
    is_prime = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if is_prime[p]:
            for multiple in range(p, limit + 1, p):
                is_prime[multiple] = False
                mu[multiple] *= -1
            square = p * p
            for multiple in range(square, limit + 1, square):
                mu[multiple] = 0
    return mu
```

**Evidence**

§1.11 莫比乌斯函数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.07%20-%20%E8%8E%AB%E6%AF%94%E4%B9%8C%E6%96%AF%E5%87%BD%E6%95%B0%E4%B8%8E%E6%95%B4%E9%99%A4%E5%AE%B9%E6%96%A5)
