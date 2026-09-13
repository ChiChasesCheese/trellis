---
id: leetcode-c-endlesscheng-mor1u6-heap-regret-lazy-and-dual-invariant
node: greedy-sorting.heap-regret-lazy-and-dual
type: cloze
anki: 1789002114219
tags: [concept-cloze, invariant, leetcode, recall]
---
懒删除堆在返回堆顶前必须先 {{c1::清理被标记删除的堆顶}}。

反悔堆保存可替换选择中最该撤销者；读取堆顶前必须清理延迟删除标记；对顶堆满足 low 的每个值不大于 high 的每个值，大小差至多一

**Evidence**

§5.6 懒删除堆

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.10%20-%20%E5%8F%8D%E6%82%94%E5%A0%86%E3%80%81%E6%87%92%E5%88%A0%E9%99%A4%E5%A0%86%E4%B8%8E%E5%AF%B9%E9%A1%B6%E5%A0%86)
