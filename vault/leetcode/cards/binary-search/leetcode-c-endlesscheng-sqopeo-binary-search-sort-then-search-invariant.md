---
id: leetcode-c-endlesscheng-sqopeo-binary-search-sort-then-search-invariant
node: binary-search.binary-search-sort-then-search
type: cloze
anki: 1787272400603
tags: [concept-cloze, invariant, leetcode, recall]
---
排序操作只改变元素的{{c1::顺序}}而不改变{{c2::元素集合}}，从而为后续二分建立单调性前提。

排序不改变元素集合，只建立顺序关系供二分使用；排序开销 O(n log n) 需计入整体复杂度

**Evidence**

§1.2 进阶

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.02%20-%20%E5%85%88%E6%8E%92%E5%BA%8F%E5%86%8D%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE)
