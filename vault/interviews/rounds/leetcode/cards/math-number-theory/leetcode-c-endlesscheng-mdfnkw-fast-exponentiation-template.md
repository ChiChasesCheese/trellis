---
id: leetcode-c-endlesscheng-mdfnkw-fast-exponentiation-template
node: math-number-theory.fast-exponentiation
type: cloze
anki: 1787272451479
tags: [concept-cloze, leetcode, recall, template]
---
qpow 函数中，每轮迭代先判断 {{c1::y & 1}}，若为真则把 x 乘入 result，然后令 x = x * x % m 并 {{c2::y >>= 1}}。

```
def qpow(x, y, m):
    # Binary exponentiation: x^y mod m in O(log y) multiplications
    result = 1
    x %= m
    while y > 0:
        if y & 1:
            result = result * x % m
        x = x * x % m
        y >>= 1
    return result
```

**Evidence**

总结

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.05%20-%20%E5%BF%AB%E9%80%9F%E5%B9%82%EF%BC%88%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%B9%82%EF%BC%89)
