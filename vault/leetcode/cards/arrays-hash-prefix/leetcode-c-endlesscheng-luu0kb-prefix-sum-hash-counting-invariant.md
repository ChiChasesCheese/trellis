---
id: leetcode-c-endlesscheng-luu0kb-prefix-sum-hash-counting-invariant
node: arrays-hash-prefix.prefix-sum-hash-counting
type: cloze
anki: 1787272457080
tags: [concept-cloze, invariant, leetcode, recall]
---
扫描到当前位置时，哈希表只应包含 {{c1::此前前缀状态}} 的频次。

哈希表记录当前前缀之前的状态频次；处理当前位置前先用旧频次贡献答案；空前缀状态已初始化

**Evidence**

一、技巧类题目：哈希表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.05%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%93%88%E5%B8%8C%E8%AE%A1%E6%95%B0)
