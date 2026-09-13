---
id: leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-recognition
node: bitwise-tricks.enumerate-nonempty-subsets-of-mask
type: cloze
anki: 1787272454280
tags: [concept-cloze, leetcode, recall, recognition]
---
当需要枚举一个具体集合 s（而非全集）的所有非空子集时，应使用 {{c1::sub = (sub - 1) & s}} 这一跳转公式，而不是对全集逐个整数枚举再过滤。

这避免了遍历大量不属于 s 的无效中间值。

**Evidence**

§4.2 枚举非空子集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.06%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E9%9D%9E%E7%A9%BA%E5%AD%90%E9%9B%86)
