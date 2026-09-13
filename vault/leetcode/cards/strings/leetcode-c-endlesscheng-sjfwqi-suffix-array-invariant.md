---
id: leetcode-c-endlesscheng-sjfwqi-suffix-array-invariant
node: strings.suffix-array
type: cloze
anki: 1787272449280
tags: [concept-cloze, invariant, leetcode, recall]
---
后缀数组 sa 满足 {{c1::s[sa[0]:] <= s[sa[1]:] <= ...}} 的字典序关系。

sa 按后缀字典序递增，rank[sa[i]] 等于 i；倍增第 k 轮按长度 2^k 前后两半 rank 排序

**Evidence**

八、后缀数组/后缀自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.08%20-%20%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84%20%28Suffix%20Array%29)
