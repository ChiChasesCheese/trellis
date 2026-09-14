---
id: leetcode-c-endlesscheng-0vinmk-shrink-window-for-longest-recognition
node: two-pointers-window.shrink-window-for-longest
type: cloze
anki: 1787268626437
tags: [concept-cloze, leetcode, recall, recognition]
---
题目要求'最长/最大的满足某条件的子数组',且窗口越长越容易破坏条件时,应使用{{c1::收缩式(越短越合法)}}的不定长滑动窗口。

右指针不断扩张窗口,一旦窗口不满足条件就用while收缩左指针直至重新合法,每轮用当前合法窗口长度更新最长答案。

**Evidence**

§2.1 越短越合法/求最长/最大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.02%20-%20%E6%94%B6%E7%BC%A9%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E9%95%BF-%E6%9C%80%E5%A4%A7%EF%BC%89)
