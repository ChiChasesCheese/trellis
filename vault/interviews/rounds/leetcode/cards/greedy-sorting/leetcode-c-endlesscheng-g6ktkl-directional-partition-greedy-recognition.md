---
id: leetcode-c-endlesscheng-g6ktkl-directional-partition-greedy-recognition
node: greedy-sorting.directional-partition-greedy
type: cloze
anki: 1787272431705
tags: [concept-cloze, leetcode, recall, recognition]
---
原顺序不能改变且答案由若干连续合法段组成时，尝试 {{c1::单向扫描、在最早合法或最早必要处切分}}。

无法排序时，固定从左到右或从右到左扫描；每一步尽早完成一个合法局部目标或切段，并将剩余部分化为同类子问题。

**Evidence**

§1.4-§1.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.02%20-%20%E5%8D%95%E5%90%91%E6%89%AB%E6%8F%8F%E4%B8%8E%E5%88%87%E5%88%86%E8%B4%AA%E5%BF%83)
