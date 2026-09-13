---
id: leetcode-c-endlesscheng-sqopeo-binary-search-lower-bound-invariant
node: binary-search.binary-search-lower-bound
type: cloze
anki: 1787272400305
tags: [concept-cloze, invariant, leetcode, recall]
---
lowerBound(nums, x) 返回第一个 {{c1::>= x}} 的下标；若不存在则返回 {{c2::n（数组长度）}}。

nums 非递减；lowerBound 返回第一个 >= x 的下标，不存在则为 n；<x 与 >=x 元素个数之和为 n，<=x 与 >x 同理

**Evidence**

一、二分查找 常用转化表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.01%20-%20%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E4%B8%8E%20lowerBound%20%E7%BB%9F%E4%B8%80%E8%BD%AC%E5%8C%96)
