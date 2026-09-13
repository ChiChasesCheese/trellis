---
id: leetcode-c-endlesscheng-9ozfk9-largest-rectangle-histogram-recognition
node: stack-queue-monotonic.largest-rectangle-histogram
type: cloze
anki: 1787272403205
tags: [concept-cloze, leetcode, recall, recognition]
---
答案形如“区间最小高度 × 区间宽度”的最大化问题，常转成 {{c1::直方图最大矩形}}。

把每根柱子当作矩形最矮高度。找到其左右第一个严格更矮柱子后，该高度能覆盖的最大宽度已确定；也可在扫描末尾加入高度为 0 的哨兵，使弹栈时结算面积。

**Evidence**

二、矩形

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.02%20-%20%E7%9B%B4%E6%96%B9%E5%9B%BE%E6%9C%80%E5%A4%A7%E7%9F%A9%E5%BD%A2)
