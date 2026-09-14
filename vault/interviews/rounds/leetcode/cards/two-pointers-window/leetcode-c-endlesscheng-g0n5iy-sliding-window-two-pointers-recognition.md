---
id: leetcode-c-endlesscheng-g0n5iy-sliding-window-two-pointers-recognition
node: two-pointers-window.sliding-window-two-pointers
type: cloze
anki: 1787272476179
tags: [concept-cloze, leetcode, recall, recognition]
---
连续区间约束可随端点移动增量维护，且失效后收缩左端能恢复条件时，用 {{c1::滑动窗口}}。

维护一个连续区间，右指针扩张以纳入元素，左指针收缩以恢复约束；适用于窗口可增量维护且约束具有单调性的场景。

**Evidence**

双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.02%20-%20%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E5%8F%8C%E6%8C%87%E9%92%88)
