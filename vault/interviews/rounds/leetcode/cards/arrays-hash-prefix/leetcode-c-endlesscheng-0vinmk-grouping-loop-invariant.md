---
id: leetcode-c-endlesscheng-0vinmk-grouping-loop-invariant
node: arrays-hash-prefix.grouping-loop
type: cloze
anki: 1787268629237
tags: [concept-cloze, invariant, leetcode, recall]
---
分组循环的不变量是:外层循环的每次迭代恰好对应{{c1::一个完整的组}},组与组之间不重叠不遗漏。

外层循环的每次迭代对应恰好一个完整的组,组之间不重叠不遗漏；内层循环结束时,i指向的是下一组的起点(或数组末尾),不属于当前组

**Evidence**

六、分组循环

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.11%20-%20%E5%88%86%E7%BB%84%E5%BE%AA%E7%8E%AF)
