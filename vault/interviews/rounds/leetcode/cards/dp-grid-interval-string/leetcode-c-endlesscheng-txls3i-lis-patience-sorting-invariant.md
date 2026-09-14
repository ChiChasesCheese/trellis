---
id: leetcode-c-endlesscheng-txls3i-lis-patience-sorting-invariant
node: dp-grid-interval-string.lis-patience-sorting
type: cloze
anki: 1787272413504
tags: [concept-cloze, invariant, leetcode, recall]
---
tails[l-1] 保存长度 l 的 LIS 候选的 {{c1::最小结尾值}}。

tails[l-1] 是长度 l 的递增子序列最小可能结尾；tails 始终递增，便于二分

**Evidence**

§4.2 最长递增子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.07%20-%20LIS%20%E4%B8%8E%E8%80%90%E5%BF%83%E6%8E%92%E5%BA%8F)
