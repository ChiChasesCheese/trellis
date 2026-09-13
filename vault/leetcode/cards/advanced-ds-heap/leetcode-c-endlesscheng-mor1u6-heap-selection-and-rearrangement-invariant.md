---
id: leetcode-c-endlesscheng-mor1u6-heap-selection-and-rearrangement-invariant
node: advanced-ds-heap.heap-selection-and-rearrangement
type: cloze
anki: 1787272421003
tags: [concept-cloze, invariant, leetcode, recall]
---
用大小 K 的小顶堆求第 K 大时，堆顶是当前保留元素中的 {{c1::最小值}}。

堆顶总是比较规则下的最优候选；保留 K 个最大值时堆大小不超过 K，堆顶是其中最小值；重排时不能立即重新选用刚使用的元素

**Evidence**

§5.3 第 K 小/大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.11%20-%20%E5%A0%86%E7%9A%84%E9%80%89%E6%8B%A9%E4%B8%8E%E9%87%8D%E6%8E%92)
