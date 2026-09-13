---
id: leetcode-c-endlesscheng-g6ktkl-minimum-interval-cover-invariant
node: greedy-sorting.minimum-interval-cover
type: cloze
anki: 1787272433904
tags: [concept-cloze, invariant, leetcode, recall]
---
覆盖贪心始终保持 {{c1::目标起点到 current 连续无缺口}}。

[s, current] 已被所选区间连续覆盖；扫描过的、左端点不超过 current 的区间均已纳入最远延伸比较；每次选择使 current 达到当前可达的最远右端点

**Evidence**

§2.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.09%20-%20%E6%9C%80%E5%B0%91%E5%8C%BA%E9%97%B4%E8%A6%86%E7%9B%96)
