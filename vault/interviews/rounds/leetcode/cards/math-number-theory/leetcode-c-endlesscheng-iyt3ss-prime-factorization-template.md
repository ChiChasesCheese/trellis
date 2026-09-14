---
id: leetcode-c-endlesscheng-iyt3ss-prime-factorization-template
node: math-number-theory.prime-factorization
type: cloze
anki: 1787272425606
tags: [concept-cloze, leetcode, recall, template]
---
试除分解后若 x > 1，必须追加 {{c1::(x, 1)}}。

```
def factorize(x):
    result = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            exponent = 0
            while x % d == 0:
                x //= d
                exponent += 1
            result.append((d, exponent))
        d += 1
    if x > 1:
        result.append((x, 1))
    return result

def factorial_prime_exponent(n, p):
    total = 0
    while n:
        n //= p
        total += n
    return total
```

**Evidence**

§1.3 质因数分解

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.03%20-%20%E8%B4%A8%E5%9B%A0%E6%95%B0%E5%88%86%E8%A7%A3%E4%B8%8E%E9%98%B6%E4%B9%98%E6%8C%87%E6%95%B0)
