---
id: leetcode-c-endlesscheng-g0n5iy-prefix-suffix-heaps-invariant
node: advanced-ds-heap.prefix-suffix-heaps
type: cloze
anki: 1787272479580
tags: [concept-cloze, invariant, leetcode, recall]
---
维护前缀最小 k 项时，堆中应保留 {{c1::当前前缀的 k 个最小元素}}。

扫描到 i 时，堆中恰为该前缀或后缀最优的 k 个元素；维护的 sum 始终等于堆内元素和

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.13%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%A0%86%E9%80%89%E6%8B%A9)
