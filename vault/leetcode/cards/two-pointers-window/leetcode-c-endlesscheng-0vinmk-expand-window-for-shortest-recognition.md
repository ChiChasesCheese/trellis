---
id: leetcode-c-endlesscheng-0vinmk-expand-window-for-shortest-recognition
node: two-pointers-window.expand-window-for-shortest
type: cloze
anki: 1787268626738
tags: [concept-cloze, leetcode, recall, recognition]
---
题目要求'最短/最小的满足某条件的子数组',且窗口越长越容易满足条件时,应使用{{c1::扩张式(越长越合法)}}的不定长滑动窗口。

右指针扩张窗口直到条件满足,此时进入while尝试收缩左指针以寻找更短的合法窗口,收缩到刚好不再合法为止,过程中不断更新最短答案。

**Evidence**

§2.2 越长越合法/求最短/最小

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.03%20-%20%E6%89%A9%E5%BC%A0%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E7%9F%AD-%E6%9C%80%E5%B0%8F%EF%BC%89)
