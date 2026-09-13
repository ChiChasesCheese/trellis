---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-shrink-valid-recognition
node: two-pointers-window.count-subarrays-shrink-valid
type: cloze
anki: 1787268627037
tags: [concept-cloze, leetcode, recall, recognition]
---
统计满足条件的子数组个数,且条件满足'子数组越短越合法'时,应使用{{c1::越短越合法的计数滑窗}},每轮累加right - left + 1。

内层while把窗口收缩到[left, right]合法为止,此时同右端点、更短的子数组[left+1,right]…[right,right]也都合法,一次性累加right-left+1个方案。

**Evidence**

§2.3.1 越短越合法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.04%20-%20%E5%AE%9A%E9%95%BF%E6%94%B6%E7%BC%A9%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E7%9F%AD%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
