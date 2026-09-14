---
id: leetcode-c-endlesscheng-sjfwqi-suffix-array-recognition
node: strings.suffix-array
type: cloze
anki: 1787272449180
tags: [concept-cloze, leetcode, recall, recognition]
---
题目核心是“所有后缀的字典序”或最长重复子串时，考虑 {{c1::后缀数组}}。

将所有后缀按字典序排序，并配合 rank 与 LCP，将子串字典序、重复子串和后缀相关查询转成相邻区间问题。

**Evidence**

八、后缀数组/后缀自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.08%20-%20%E5%90%8E%E7%BC%80%E6%95%B0%E7%BB%84%20%28Suffix%20Array%29)
