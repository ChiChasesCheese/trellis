---
id: leetcode-c-endlesscheng-wr1mjp-two-pointers-and-sliding-window-recognition
node: two-pointers-window.two-pointers-and-sliding-window
type: cloze
anki: 1787272469880
tags: [concept-cloze, leetcode, recall, recognition]
---
连续区间问题中，若右端扩张后能靠不断移动左端恢复条件，应考虑 {{c1::双指针/可变滑动窗口}}。

在连续子数组或子串上维护区间 [left, right]。固定长度窗口通常每次移动一格；可变窗口依赖单调可维护的条件，右扩后必要时左缩。

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.02%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
