---
id: leetcode-c-endlesscheng-0vinmk-same-direction-two-pointers-invariant
node: two-pointers-window.same-direction-two-pointers
type: cloze
anki: 1787268628337
tags: [concept-cloze, invariant, leetcode, recall]
---
同向双指针能保证O(n)复杂度的关键不变量是:left和right指针都{{c1::单调不减(不会回退)}}。

right指针单调不减；left指针单调不减；二者相对顺序始终保持left <= right

**Evidence**

§3.3 同向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.08%20-%20%E5%90%8C%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
