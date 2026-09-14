---
id: leetcode-c-endlesscheng-g6ktkl-separate-identical-items-invariant
node: greedy-sorting.separate-identical-items
type: cloze
anki: 1787272432706
tags: [concept-cloze, invariant, leetcode, recall]
---
相邻不同重排可行当且仅当 {{c1::m <= n-m+1}}。

最高频值需要被其余元素形成的间隔隔开；可用的非最高频元素数为 n-m；每次删除两个不同元素都会消耗一个非最高频元素

**Evidence**

§1.8

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.05%20-%20%E7%9B%B8%E9%82%BB%E4%B8%8D%E5%90%8C%E7%9A%84%E9%A2%91%E6%AC%A1%E8%B4%AA%E5%BF%83)
