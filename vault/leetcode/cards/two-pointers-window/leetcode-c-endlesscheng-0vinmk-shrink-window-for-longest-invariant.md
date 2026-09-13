---
id: leetcode-c-endlesscheng-0vinmk-shrink-window-for-longest-invariant
node: two-pointers-window.shrink-window-for-longest
type: cloze
anki: 1787268626538
tags: [concept-cloze, invariant, leetcode, recall]
---
收缩式滑窗的不变量是:每轮外层循环体结束时,窗口[left, right]一定处于{{c1::合法}}状态。

每轮for循环体结束时,[left, right]一定是合法的；内层while在窗口不合法时持续收缩left,不合法就必须收缩到合法为止

**Evidence**

§2.1 越短越合法/求最长/最大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.02%20-%20%E6%94%B6%E7%BC%A9%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E9%95%BF-%E6%9C%80%E5%A4%A7%EF%BC%89)
