---
id: leetcode-c-endlesscheng-mdfnkw-fast-exponentiation-invariant
node: math-number-theory.fast-exponentiation
type: cloze
anki: 1787272451379
tags: [concept-cloze, invariant, leetcode, recall]
---
快速幂的核心不变量：将指数 y 用{{c1::二进制}}分解，每一位对应对 x 的一次{{c2::平方}}，只在该位为 1 时才把当前 x 乘入结果。

x^y mod m 可以把 y 表示为二进制，只需 O(log y) 次乘法计算完成；指数本身不能直接对 m 取模（除非用扩展欧拉定理降幂）

**Evidence**

除法的取模

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.05%20-%20%E5%BF%AB%E9%80%9F%E5%B9%82%EF%BC%88%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%B9%82%EF%BC%89)
