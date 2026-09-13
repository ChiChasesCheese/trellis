---
id: leetcode-c-endlesscheng-txls3i-lis-patience-sorting-recognition
node: dp-grid-interval-string.lis-patience-sorting
type: cloze
anki: 1787272413404
tags: [concept-cloze, leetcode, recall, recognition]
---
求 LIS 长度且 n 较大时，使用 {{c1::耐心排序加二分}}。

维护每个长度的递增子序列可取得的最小末尾值；二分替换不会降低任何未来可扩展性。

**Evidence**

§4.2 最长递增子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.07%20-%20LIS%20%E4%B8%8E%E8%80%90%E5%BF%83%E6%8E%92%E5%BA%8F)
