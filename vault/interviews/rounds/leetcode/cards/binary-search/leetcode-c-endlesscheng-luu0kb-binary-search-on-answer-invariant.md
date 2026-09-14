---
id: leetcode-c-endlesscheng-luu0kb-binary-search-on-answer-invariant
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272456179
tags: [concept-cloze, invariant, leetcode, recall]
---
求最小可行值时，若 feasible(mid) 为真，应保留 {{c1::左半边（high = mid）}}。

循环中保留尚未排除的最优答案；判定函数对二分方向具有单调性；每轮严格缩小搜索区间

**Evidence**

一、技巧类题目：二分答案

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.02%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
