---
id: leetcode-c-endlesscheng-wr1mjp-gcd-lcm-factorization-and-congruence-template
node: math-number-theory.gcd-lcm-factorization-and-congruence
type: cloze
anki: 1787272475181
tags: [concept-cloze, leetcode, recall, template]
---
试除分解时，只需枚举 d 满足 {{c1::d * d <= x}}，结束后剩余 x>1 是质因子。

```
from math import gcd

def gcd_and_lcm(nums):
    g = 0
    l = 1
    for x in nums:
        g = gcd(g, x)
        l = l // gcd(l, x) * x
    return g, l

def factorize(x):
    factors = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            factors[d] = factors.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        factors[x] = 1
    return factors
```

**Evidence**

6. 数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.19%20-%20GCD%E3%80%81LCM%E3%80%81%E8%B4%A8%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3%E4%B8%8E%E5%90%8C%E4%BD%99)
