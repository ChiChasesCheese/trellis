---
id: leetcode-c-endlesscheng-mdfnkw-negative-mod-normalization-template
node: math-number-theory.negative-mod-normalization
type: cloze
anki: 1787272451179
tags: [concept-cloze, leetcode, recall, template]
---
safe_mod 函数返回 {{c1::(x % m + m) % m}}，用于把可能为负的取模结果规范化。

```
def safe_mod(x, m):
    # Normalize a possibly-negative modulo result into [0, m-1]
    return (x % m + m) % m

def sub_mod(a, b, m):
    return safe_mod(a - b, m)
```

**Evidence**

负数和减法的取模

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.04%20-%20%E8%B4%9F%E6%95%B0%E4%B8%8E%E5%87%8F%E6%B3%95%E5%8F%96%E6%A8%A1%E7%9A%84%E8%A7%84%E8%8C%83%E5%8C%96)
