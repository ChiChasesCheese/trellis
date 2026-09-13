---
id: leetcode-c-endlesscheng-sqopeo-binary-search-kth-smallest-largest-recognition
node: binary-search.binary-search-kth-smallest-largest
type: cloze
anki: 1787272402307
tags: [concept-cloze, leetcode, recall, recognition]
---
题目要求“第 k 小/第 k 大的值”，且能设计出关于 x 单调的计数函数时，可将其转化为{{c1::二分答案}}问题，其中第 k 小等价于求满足 count(x)>=k 的{{c2::最小}} x。

第 k 小等价于求最小的 x，使得 <= x 的元素个数至少为 k；第 k 大等价于求最大的 x，使得 >= x 的元素个数至少为 k，从而把选数问题转化为二分答案求最小/最大，k 从 1 开始计数。

**Evidence**

§2.6 第 K 小/大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.08%20-%20%E7%AC%AC%20K%20%E5%B0%8F-%E5%A4%A7%E8%BD%AC%E5%8C%96%E4%B8%BA%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
