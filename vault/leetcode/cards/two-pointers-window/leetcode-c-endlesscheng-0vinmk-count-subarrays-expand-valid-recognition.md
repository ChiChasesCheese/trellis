---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-expand-valid-recognition
node: two-pointers-window.count-subarrays-expand-valid
type: cloze
anki: 1787268627337
tags: [concept-cloze, leetcode, recall, recognition]
---
统计满足条件的子数组个数,且条件满足'子数组越长越合法'时,应使用{{c1::越长越合法的计数滑窗}},每轮累加left。

内层while把窗口收缩到[left, right]不合法为止,则上一轮的[left-1,right]才是合法的,固定right时合法左端点构成前缀区间[0, left-1],共left个方案。

**Evidence**

§2.3.2 越长越合法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.05%20-%20%E5%AE%9A%E9%95%BF%E6%89%A9%E5%BC%A0%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E9%95%BF%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
