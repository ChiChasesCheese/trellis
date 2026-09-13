---
id: leetcode-c-endlesscheng-iyt3ss-modular-combinatorics-invariant
node: math-number-theory.modular-combinatorics
type: cloze
anki: 1787272427005
tags: [concept-cloze, invariant, leetcode, recall]
---
独立选择阶段的方案数按 {{c1::乘法原理相乘}}。

组合数满足 C(n,k)=n!/(k!(n-k)!)；x1+...+xk=n 且 xi≥0 的解数为 C(n+k-1,k-1)；模质数下逆阶乘可使组合数查询为 O(1)

**Evidence**

§2.1 乘法原理

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.08%20-%20%E7%BB%84%E5%90%88%E8%AE%A1%E6%95%B0%E3%80%81%E9%9A%94%E6%9D%BF%E6%B3%95%E4%B8%8E%E6%A8%A1%E7%BB%84%E5%90%88%E6%95%B0)
