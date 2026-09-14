---
id: leetcode-c-endlesscheng-mdfnkw-congruence-transposition-template
node: math-number-theory.congruence-transposition
type: cloze
anki: 1787272450879
tags: [concept-cloze, leetcode, recall, template]
---
transpose_check 函数验证 a+b≡c+d (mod m) 是否等价于 {{c1::a-c≡d-b}} (mod m)。

```
def transpose_check(a, b, c, d, m):
    # verifies a+b == c+d (mod m) implies a-c == d-b (mod m)
    lhs_holds = (a + b - c - d) % m == 0
    rhs_holds = (a - c - (d - b)) % m == 0
    return lhs_holds == rhs_holds
```

**Evidence**

同余式的移项

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.03%20-%20%E5%90%8C%E4%BD%99%E5%BC%8F%E7%9A%84%E7%A7%BB%E9%A1%B9%E4%B8%8E%E5%8A%A0%E5%87%8F%E6%80%A7%E8%B4%A8)
