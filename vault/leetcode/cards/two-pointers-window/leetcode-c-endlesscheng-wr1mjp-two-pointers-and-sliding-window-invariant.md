---
id: leetcode-c-endlesscheng-wr1mjp-two-pointers-and-sliding-window-invariant
node: two-pointers-window.two-pointers-and-sliding-window
type: cloze
anki: 1787272469980
tags: [concept-cloze, invariant, leetcode, recall]
---
可变窗口左缩结束后，[left, right] 应满足 {{c1::窗口合法条件}}。

窗口 [left, right] 始终满足定义的合法条件，或左缩循环结束后满足；每个元素最多进窗口和出窗口一次，因此双指针是线性的

**Evidence**

2. 技巧

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.02%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
