---
id: leetcode-c-endlesscheng-mdfnkw-modular-inverse-fermat-template
node: math-number-theory.modular-inverse-fermat
type: cloze
anki: 1787272451779
tags: [concept-cloze, leetcode, recall, template]
---
mod_inverse 函数返回 {{c1::pow(b, p - 2, p)}}，div_mod 函数计算 {{c2::a * mod_inverse(b, p) % p}} 作为 a/b mod p 的结果。

```
def mod_inverse(b, p):
    # Requires p to be prime and b to not be a multiple of p (Fermat's little theorem)
    return pow(b, p - 2, p)

def div_mod(a, b, p):
    return a * mod_inverse(b, p) % p
```

**Evidence**

除法的取模

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.06%20-%20%E8%B4%B9%E9%A9%AC%E5%B0%8F%E5%AE%9A%E7%90%86%E4%B8%8E%E6%A8%A1%E9%80%86%E5%85%83%EF%BC%88%E9%99%A4%E6%B3%95%E5%8F%96%E6%A8%A1%EF%BC%89)
