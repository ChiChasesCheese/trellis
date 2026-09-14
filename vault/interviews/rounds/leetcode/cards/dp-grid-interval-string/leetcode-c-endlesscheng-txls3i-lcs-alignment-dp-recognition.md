---
id: leetcode-c-endlesscheng-txls3i-lcs-alignment-dp-recognition
node: dp-grid-interval-string.lcs-alignment-dp
type: cloze
anki: 1787272413104
tags: [concept-cloze, leetcode, recall, recognition]
---
两个序列保持相对顺序的共同部分问题，优先考虑 {{c1::LCS}}。

用两个前缀定义状态；末字符相等时同时消费，否则丢弃其中一侧并取较优结果。

**Evidence**

§4.1 最长公共子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.06%20-%20LCS%20%E5%AF%B9%E9%BD%90%20DP)
