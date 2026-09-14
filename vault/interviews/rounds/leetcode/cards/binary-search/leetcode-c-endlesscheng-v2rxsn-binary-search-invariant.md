---
id: leetcode-c-endlesscheng-v2rxsn-binary-search-invariant
node: binary-search.binary-search
type: cloze
anki: 1787272463079
tags: [concept-cloze, invariant, leetcode, recall]
---
求最小可行值时，二分区间始终包含 {{c1::最小可行答案}}。

循环始终保留答案所在的闭区间；check(mid) 为真时，按目标方向丢弃不可能更优的一半

**Evidence**

一、技巧类题目：二分答案

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.02%20-%20%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%E4%B8%8E%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
