---
id: leetcode-c-endlesscheng-sqopeo-binary-search-lower-bound-recognition
node: binary-search.binary-search-lower-bound
type: cloze
anki: 1787272400205
tags: [concept-cloze, leetcode, recall, recognition]
---
当数组已经{{c1::非递减（排序）}}，且题目问某值的第一个/最后一个位置或某比较关系的元素个数时，考虑用 {{c2::lowerBound}} 转化。

在非递减数组上用 lowerBound(nums, x) 表示第一个 >= x 的下标，通过 x 或 x+1 的偏移可统一表达 >x、<x、<=x 等边界查询及对应元素个数，<x 与 >=x 互补、<=x 与 >x 互补。

**Evidence**

一、二分查找 常用转化表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.01%20-%20%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E4%B8%8E%20lowerBound%20%E7%BB%9F%E4%B8%80%E8%BD%AC%E5%8C%96)
