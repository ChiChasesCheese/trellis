---
id: leetcode-c-endlesscheng-ffmcgb-difference-array-recognition
node: arrays-hash-prefix.difference-array
type: cloze
anki: 1787272452179
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求对数组的若干个连续子区间分别整体加上某个值，且所有更新可以离线处理、最后统一输出结果时，应使用 {{c1::差分数组}} 技巧；若更新和查询交替进行则不适用，需换成 {{c2::树状数组/线段树}}。

识别信号：批量区间加、离线、最后一次性求值。

**Evidence**

举例/定义和性质

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F14.01%20-%20%E5%B7%AE%E5%88%86%E6%95%B0%E7%BB%84)
