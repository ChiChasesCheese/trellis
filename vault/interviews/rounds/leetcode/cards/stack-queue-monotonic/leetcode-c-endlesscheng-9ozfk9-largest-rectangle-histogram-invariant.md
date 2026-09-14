---
id: leetcode-c-endlesscheng-9ozfk9-largest-rectangle-histogram-invariant
node: stack-queue-monotonic.largest-rectangle-histogram
type: cloze
anki: 1787272403304
tags: [concept-cloze, invariant, leetcode, recall]
---
直方图扫描到更矮柱子时，被弹出柱子的 {{c1::右边界}} 已经确定为当前位置。

栈中柱高单调递增。；读到更矮柱子时，被弹出的柱子已确定右边界 i。；弹出高度 h 的下标 mid 后，新栈顶是左侧第一个更矮柱子，宽度为 i - stack[-1] - 1。

**Evidence**

二、矩形

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.02%20-%20%E7%9B%B4%E6%96%B9%E5%9B%BE%E6%9C%80%E5%A4%A7%E7%9F%A9%E5%BD%A2)
