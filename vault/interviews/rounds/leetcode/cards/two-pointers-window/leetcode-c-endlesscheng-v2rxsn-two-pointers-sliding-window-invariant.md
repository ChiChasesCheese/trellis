---
id: leetcode-c-endlesscheng-v2rxsn-two-pointers-sliding-window-invariant
node: two-pointers-window.two-pointers-sliding-window
type: cloze
anki: 1787272462779
tags: [concept-cloze, invariant, leetcode, recall]
---
滑动窗口收缩循环结束后，[left, right] 必须 {{c1::满足窗口约束}}。

窗口 [left, right] 始终满足约束，或收缩后重新满足；每个指针只单调前进，因此总移动次数是线性的

**Evidence**

一、技巧类题目：双指针、滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.01%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
