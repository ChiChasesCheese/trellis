---
id: leetcode-c-endlesscheng-wr1mjp-prefix-suffix-and-difference-recognition
node: arrays-hash-prefix.prefix-suffix-and-difference
type: cloze
anki: 1787272470481
tags: [concept-cloze, leetcode, recall, recognition]
---
有大量“给区间统一加值，最后查看数组”的操作时，用 {{c1::差分数组}}。

把区间或多次范围操作转为预处理数组。前缀/后缀记录单侧累计信息；差分只记录区间变化，在最后一次前缀累加还原。

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.04%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E3%80%81%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%B7%AE%E5%88%86)
