---
id: leetcode-c-endlesscheng-g6ktkl-enumerate-then-greedy-invariant
node: greedy-sorting.enumerate-then-greedy
type: cloze
anki: 1787272432104
tags: [concept-cloze, invariant, leetcode, recall]
---
枚举加贪心正确性的覆盖条件是：{{c1::每个全局最优解的关键状态都被枚举}}。

每个全局最优解对应至少一个被枚举的关键状态；固定枚举状态后，内层贪心保持其局部问题最优；外层比较覆盖所有可能的最优结构

**Evidence**

§1.6

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.03%20-%20%E6%9E%9A%E4%B8%BE%E5%85%B3%E9%94%AE%E7%8A%B6%E6%80%81%E5%90%8E%E8%B4%AA%E5%BF%83)
