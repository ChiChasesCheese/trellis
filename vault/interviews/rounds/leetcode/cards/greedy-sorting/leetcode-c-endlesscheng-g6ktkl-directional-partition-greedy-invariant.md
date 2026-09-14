---
id: leetcode-c-endlesscheng-g6ktkl-directional-partition-greedy-invariant
node: greedy-sorting.directional-partition-greedy
type: cloze
anki: 1787272431807
tags: [concept-cloze, invariant, leetcode, recall]
---
切分贪心扫描到位置 i 时，i 左边应保持 {{c1::已合法划分且段数最优}}。

扫描位置之前的前缀已被合法划分且段数最优；当前累计状态只描述尚未结束的一段；在最早合法位置切分不会减少后缀的可行选择

**Evidence**

§1.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.02%20-%20%E5%8D%95%E5%90%91%E6%89%AB%E6%8F%8F%E4%B8%8E%E5%88%87%E5%88%86%E8%B4%AA%E5%BF%83)
