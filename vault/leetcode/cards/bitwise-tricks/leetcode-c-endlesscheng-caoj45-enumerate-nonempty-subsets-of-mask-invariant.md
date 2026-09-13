---
id: leetcode-c-endlesscheng-caoj45-enumerate-nonempty-subsets-of-mask-invariant
node: bitwise-tricks.enumerate-nonempty-subsets-of-mask
type: cloze
anki: 1787272454380
tags: [concept-cloze, invariant, leetcode, recall]
---
该枚举顺序是按子集数值从大到小排列，循环在 sub 变为 {{c1::0}} 时自然终止，因此不包含空集。

如需包含空集需要额外处理终止时机（见 enumerate-subsets-including-empty）。

**Evidence**

§4.2 枚举非空子集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.06%20-%20%E6%9E%9A%E4%B8%BE%E7%BB%99%E5%AE%9A%E9%9B%86%E5%90%88%E7%9A%84%E9%9D%9E%E7%A9%BA%E5%AD%90%E9%9B%86)
