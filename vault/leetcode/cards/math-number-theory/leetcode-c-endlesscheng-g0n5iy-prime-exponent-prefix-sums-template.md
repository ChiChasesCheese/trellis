---
id: leetcode-c-endlesscheng-g0n5iy-prime-exponent-prefix-sums-template
node: math-number-theory.prime-exponent-prefix-sums
type: cloze
anki: 1787272477580
tags: [concept-cloze, leetcode, recall, template]
---
一维前缀和区间 [l, r] 的指数和是 {{c1::pre[r + 1] - pre[l]}}。

```
def factor_count(x, p):
    count = 0
    while x and x % p == 0:
        x //= p
        count += 1
    return count

def prefix(values, p):
    result = [0]
    for x in values:
        result.append(result[-1] + factor_count(x, p))
    return result
```

**Evidence**

数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.06%20-%20%E8%B4%A8%E5%9B%A0%E5%AD%90%E6%8C%87%E6%95%B0%E5%89%8D%E7%BC%80%E5%92%8C)
