---
id: leetcode-c-endlesscheng-iyt3ss-fast-walsh-hadamard-transform-template
node: math-number-theory.fast-walsh-hadamard-transform
type: cloze
anki: 1787272430406
tags: [concept-cloze, leetcode, recall, template]
---
XOR FWT 的逆变换每层需要乘 {{c1::2 的模逆元}}。

```
def xor_fwt(values, inverse, mod):
    n = len(values)
    step = 1
    while step < n:
        for start in range(0, n, step * 2):
            for i in range(start, start + step):
                a = values[i]
                b = values[i + step]
                values[i] = (a + b) % mod
                values[i + step] = (a - b) % mod
                if inverse:
                    inv2 = pow(2, -1, mod)
                    values[i] = values[i] * inv2 % mod
                    values[i + step] = values[i + step] * inv2 % mod
        step *= 2
    return values
```

**Evidence**

§7.5 快速沃尔什变换（FWT）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.19%20-%20%E5%BF%AB%E9%80%9F%E6%B2%83%E5%B0%94%E4%BB%80%E5%8F%98%E6%8D%A2%20FWT)
