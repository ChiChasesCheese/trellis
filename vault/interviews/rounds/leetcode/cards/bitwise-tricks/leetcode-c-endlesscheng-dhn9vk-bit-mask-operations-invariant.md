---
id: leetcode-c-endlesscheng-dhn9vk-bit-mask-operations-invariant
node: bitwise-tricks.bit-mask-operations
type: cloze
anki: 1787272405405
tags: [concept-cloze, invariant, leetcode, recall]
---
置位、清位、翻转第 k 位分别使用 {{c1::mask | bit、mask & (full ^ bit)、mask ^ bit}}，其中 bit = 1 << k。

full 用于固定有效位宽。

**Evidence**

一、基础题

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F05.01%20-%20%E4%BD%8D%E6%8E%A9%E7%A0%81%E6%93%8D%E4%BD%9C)
