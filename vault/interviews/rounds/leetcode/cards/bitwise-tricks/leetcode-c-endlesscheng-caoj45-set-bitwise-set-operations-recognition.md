---
id: leetcode-c-endlesscheng-caoj45-set-bitwise-set-operations-recognition
node: bitwise-tricks.set-bitwise-set-operations
type: cloze
anki: 1787272452780
tags: [concept-cloze, leetcode, recall, recognition]
---
当问题涉及判断两个用整数表示的集合是否存在交集、并集或子集关系时，应联想到直接用 {{c1::按位与(&)/按位或(|)/按位异或(^)}} 对二进制表示运算，而不是逐元素遍历比较。

位运算在硬件层面对所有比特并行处理，效率远高于逐个比较集合元素。

**Evidence**

一、集合与集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.01%20-%20%E7%94%A8%E4%BD%8D%E8%BF%90%E7%AE%97%E5%AE%9E%E7%8E%B0%E9%9B%86%E5%90%88%E9%97%B4%E8%BF%90%E7%AE%97)
