---
id: leetcode-c-endlesscheng-caoj45-lowbit-and-bit-library-functions-invariant
node: bitwise-tricks.lowbit-and-bit-library-functions
type: cloze
anki: 1787272453480
tags: [concept-cloze, invariant, leetcode, recall]
---
s & (s - 1) 的效果是 {{c1::清除 s 二进制表示中最低的一个 1 位}}，等价于从集合中删除最小元素。

特别地，若 s 本身是 2 的幂，该结果为 0。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.03%20-%20lowbit%20%E8%BF%90%E7%AE%97%E4%B8%8E%E9%9B%86%E5%90%88%E4%BF%A1%E6%81%AF%E5%BA%93%E5%87%BD%E6%95%B0)
