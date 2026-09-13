---
id: leetcode-c-endlesscheng-0vinmk-opposite-direction-two-pointers-invariant
node: two-pointers-window.opposite-direction-two-pointers
type: cloze
anki: 1787268628038
tags: [concept-cloze, invariant, leetcode, recall]
---
相向双指针的循环终止条件是当left {{c1::>= right}}(即两指针相遇或交叉)时停止。

循环条件为left < right；每轮至少移动一个指针,保证最终left >= right时终止

**Evidence**

§3.2 相向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.07%20-%20%E7%9B%B8%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
