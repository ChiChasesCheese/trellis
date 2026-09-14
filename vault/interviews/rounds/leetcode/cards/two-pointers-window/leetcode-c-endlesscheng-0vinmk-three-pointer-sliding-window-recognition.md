---
id: leetcode-c-endlesscheng-0vinmk-three-pointer-sliding-window-recognition
node: two-pointers-window.three-pointer-sliding-window
type: cloze
anki: 1787268628838
tags: [concept-cloze, leetcode, recall, recognition]
---
当恰好型滑窗需要调用两次结构相同、仅阈值不同的滑窗函数时,可以合并为一次遍历的{{c1::三指针滑动窗口}}。

将两个仅阈值不同、结构相同的同向滑窗合并为一次遍历:共用同一个right指针,同时维护两个独立的左指针left1(对应阈值k)和left2(对应阈值k+1),避免调用两次solve函数。

**Evidence**

§2.3.3 恰好型滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.10%20-%20%E4%B8%89%E6%8C%87%E9%92%88%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
