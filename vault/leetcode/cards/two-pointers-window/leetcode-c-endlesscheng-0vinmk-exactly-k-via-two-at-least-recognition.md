---
id: leetcode-c-endlesscheng-0vinmk-exactly-k-via-two-at-least-recognition
node: two-pointers-window.exactly-k-via-two-at-least
type: cloze
anki: 1787268627636
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求统计子数组和'恰好等于k'的个数,而直接维护该条件不具有单调性时,应把问题转化为{{c1::两个'至少'问题相减}}。

把'恰好等于k'的计数问题转化为'至少k'减去'至少k+1'(或等价地'至多k'减去'至多k-1'),这样只需实现一个具有单调性的solve函数并调用两次,无需为'恰好'单独写逻辑。

**Evidence**

§2.3.3 恰好型滑动窗口

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.06%20-%20%E6%81%B0%E5%A5%BD%E5%9E%8B%E6%BB%91%E7%AA%97%E7%9A%84%E5%AE%B9%E6%96%A5%E5%88%86%E8%A7%A3)
