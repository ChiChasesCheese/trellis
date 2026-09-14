---
id: leetcode-c-endlesscheng-wr1mjp-binary-search-on-answer-invariant
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272470280
tags: [concept-cloze, invariant, leetcode, recall]
---
寻找最小可行值时，若 feasible(mid) 为真，应令 {{c1::hi = mid}}。

循环中答案始终位于 [lo, hi]；对最小可行值：hi 始终包含可行答案，lo 左侧均不可行

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
