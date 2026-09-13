---
id: leetcode-c-endlesscheng-0vinmk-fixed-length-sliding-window-recognition
node: two-pointers-window.fixed-length-sliding-window
type: cloze
anki: 1787268626136
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目给定固定窗口长度k,要求统计每个长度为k的子数组/子串的聚合值时,应联想到{{c1::定长滑动窗口}}。

维护一个长度恒定为k的窗口，每轮先把right元素入队，窗口凑满k后结算答案，再把left元素出队并右移，全程只需一次遍历。

**Evidence**

§1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.01%20-%20%E5%AE%9A%E9%95%BF%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
