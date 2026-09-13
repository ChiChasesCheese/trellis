---
id: leetcode-c-endlesscheng-sqopeo-binary-search-minimize-maximum-recognition
node: binary-search.binary-search-minimize-maximum
type: cloze
anki: 1787272401704
tags: [concept-cloze, leetcode, recall, recognition]
---
题目要求“分组/分配后使每组的最大值尽可能小”时，属于{{c1::最小化最大值}}模式，本质是二分答案求{{c2::最小}}。

本质是二分答案求最小，mid 表示一个上界（盖子），check(mid) 判断该上界能否压住所有子问题的最大值，越大的上界越容易满足。

**Evidence**

§2.4 最小化最大值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.06%20-%20%E6%9C%80%E5%B0%8F%E5%8C%96%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8A%E7%95%8C%EF%BC%89)
