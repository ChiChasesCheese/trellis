---
id: leetcode-c-endlesscheng-0vinmk-fixed-length-sliding-window-invariant
node: two-pointers-window.fixed-length-sliding-window
type: cloze
anki: 1787268626239
tags: [concept-cloze, invariant, leetcode, recall]
---
定长滑动窗口的核心不变量是:完成入队操作后,窗口[left, right]的长度恒等于{{c1::k}}。

完成入队后窗口[left, right]长度恒等于k；入队→(窗口满则结算)→出队 的顺序不能颠倒

**Evidence**

§1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.01%20-%20%E5%AE%9A%E9%95%BF%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3)
