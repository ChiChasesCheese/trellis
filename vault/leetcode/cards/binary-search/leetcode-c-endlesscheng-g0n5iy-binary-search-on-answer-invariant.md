---
id: leetcode-c-endlesscheng-g0n5iy-binary-search-on-answer-invariant
node: binary-search.binary-search-on-answer
type: cloze
anki: 1787272476580
tags: [concept-cloze, invariant, leetcode, recall]
---
求最大可行值时，循环维护的 lo 应始终是 {{c1::可行答案}}。

循环中保留一个已知可行边界和一个已知不可行边界，或维护半开搜索区间；每次根据 check(mid) 丢弃不可能成为答案的一半

**Evidence**

二分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88)
