---
id: leetcode-c-endlesscheng-luu0kb-prime-sieve-and-divisor-enumeration-invariant
node: math-number-theory.prime-sieve-and-divisor-enumeration
type: cloze
anki: 1787272461280
tags: [concept-cloze, invariant, leetcode, recall]
---
枚举 n 的因子时，只需遍历到 {{c1::sqrt(n)}}，因为因子成对出现。

筛法中合数会被其某个较小质因子标记；因子总成对出现 d 与 n//d；枚举到 sqrt(n) 已覆盖每一对因子

**Evidence**

五、数学：因子

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.19%20-%20%E7%AD%9B%E8%B4%A8%E6%95%B0%E4%B8%8E%E5%9B%A0%E5%AD%90%E6%9E%9A%E4%B8%BE)
