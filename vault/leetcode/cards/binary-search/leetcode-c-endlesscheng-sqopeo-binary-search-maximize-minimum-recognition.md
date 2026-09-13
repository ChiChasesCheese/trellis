---
id: leetcode-c-endlesscheng-sqopeo-binary-search-maximize-minimum-recognition
node: binary-search.binary-search-maximize-minimum
type: cloze
anki: 1787272402005
tags: [concept-cloze, leetcode, recall, recognition]
---
题目要求“选取/分配后使最小值尽可能大”时，属于{{c1::最大化最小值}}模式，本质是二分答案求{{c2::最大}}。

本质是二分答案求最大，mid 表示一个下界，check(mid) 判断是否存在方案使得所有子问题的最小值都不低于 mid，越小的下界越容易满足。

**Evidence**

§2.5 最大化最小值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.07%20-%20%E6%9C%80%E5%A4%A7%E5%8C%96%E6%9C%80%E5%B0%8F%E5%80%BC%EF%BC%88%E4%BA%8C%E5%88%86%E4%B8%8B%E7%95%8C%EF%BC%89)
