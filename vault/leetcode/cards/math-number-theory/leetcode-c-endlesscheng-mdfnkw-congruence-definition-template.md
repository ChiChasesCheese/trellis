---
id: leetcode-c-endlesscheng-mdfnkw-congruence-definition-template
node: math-number-theory.congruence-definition
type: cloze
anki: 1787272450579
tags: [concept-cloze, leetcode, recall, template]
---
is_congruent 函数通过判断 {{c1::(a - b) % m == 0}} 来验证两数是否模 m 同余。

```
def is_congruent(a, b, m):
    # a and b are congruent modulo m iff (a - b) is a multiple of m
    return (a - b) % m == 0
```

**Evidence**

同余

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.02%20-%20%E5%90%8C%E4%BD%99%E7%9A%84%E5%AE%9A%E4%B9%89%E4%B8%8E%E4%B9%98%E6%B3%95%E6%80%A7%E8%B4%A8)
