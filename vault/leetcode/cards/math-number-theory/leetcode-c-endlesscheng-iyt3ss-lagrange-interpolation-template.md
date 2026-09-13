---
id: leetcode-c-endlesscheng-iyt3ss-lagrange-interpolation-template
node: math-number-theory.lagrange-interpolation
type: cloze
anki: 1787272430703
tags: [concept-cloze, leetcode, recall, template]
---
第 i 项分母是所有 j≠i 的 {{c1::(x_i-x_j) 的乘积}}。

```
def lagrange(xs, ys, target, mod):
    total = 0
    n = len(xs)
    for i in range(n):
        numerator = 1
        denominator = 1
        for j in range(n):
            if i != j:
                numerator = numerator * (target - xs[j]) % mod
                denominator = denominator * (xs[i] - xs[j]) % mod
        total = (total + ys[i] * numerator * pow(denominator, -1, mod)) % mod
    return total
```

**Evidence**

§7.6 拉格朗日插值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.20%20-%20%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E6%8F%92%E5%80%BC)
