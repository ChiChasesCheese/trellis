---
id: leetcode-c-endlesscheng-mdfnkw-fast-exponentiation-recognition
node: math-number-theory.fast-exponentiation
type: cloze
anki: 1787272451279
tags: [concept-cloze, leetcode, recall, recognition]
---
计算 x^y mod m 且指数 y 很大（如 1e9 级别）时，不能逐次相乘，应使用{{c1::快速幂}}（二进制幂）在 O(log y) 时间内完成。

计算 x^y mod m 时不能对指数直接取模；当指数在 64 位整数范围内，应使用快速幂——把指数按二进制分解，通过反复平方把复杂度从 O(y) 降到 O(log y)。Python 可直接用内置 pow(x, y, m)。这是除法取模求逆元的必要工具。

**Evidence**

快速幂练习

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.05%20-%20%E5%BF%AB%E9%80%9F%E5%B9%82%EF%BC%88%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%B9%82%EF%BC%89)
