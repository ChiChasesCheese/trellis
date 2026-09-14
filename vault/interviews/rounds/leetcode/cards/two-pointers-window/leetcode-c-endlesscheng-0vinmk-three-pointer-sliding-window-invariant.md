---
id: leetcode-c-endlesscheng-0vinmk-three-pointer-sliding-window-invariant
node: two-pointers-window.three-pointer-sliding-window
type: cloze
anki: 1787268628937
tags: [concept-cloze, invariant, leetcode, recall]
---
三指针滑动窗口的不变量是:left1和left2分别对应不同阈值,{{c1::各自独立维护窗口和,互不干扰}}。

left1和left2各自独立维护对应阈值下的窗口,互不干扰；每次right右移后,left1和left2按各自阈值单调右移,不回退

**Evidence**

五、三指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.10%20-%20%E4%B8%89%E6%8C%87%E9%92%88%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
