---
id: leetcode-c-endlesscheng-luu0kb-two-pointers-and-group-scan-invariant
node: two-pointers-window.two-pointers-and-group-scan
type: cloze
anki: 1787272456480
tags: [concept-cloze, invariant, leetcode, recall]
---
分组循环每轮结束后，i 必须指向 {{c1::上一组之后的第一个位置}}。

双指针移动不会漏掉仍可能成为答案的组合；分组循环每轮消费一个极大且不重叠的区间；下一轮从前一组结束位置开始

**Evidence**

一、技巧类题目：分组循环

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.03%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E5%88%86%E7%BB%84%E5%BE%AA%E7%8E%AF)
