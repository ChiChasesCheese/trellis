---
id: leetcode-c-endlesscheng-iyt3ss-gcd-lcm-modular-arithmetic-template
node: math-number-theory.gcd-lcm-modular-arithmetic
type: cloze
anki: 1787272426206
tags: [concept-cloze, leetcode, recall, template]
---
安全计算 lcm(a,b) 的形式是 abs({{c1::a // gcd(a, b) * b}})。

```
from math import gcd

def lcm(a, b):
    return 0 if a == 0 or b == 0 else abs(a // gcd(a, b) * b)

def mod_inverse(a, mod):
    if gcd(a, mod) != 1:
        return None
    return pow(a, -1, mod)
```

**Evidence**

§1.7 最小公倍数（LCM）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.05%20-%20GCD%E3%80%81LCM%E3%80%81%E4%BA%92%E8%B4%A8%E4%B8%8E%E5%90%8C%E4%BD%99)
