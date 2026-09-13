---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-shrink-valid-invariant
node: two-pointers-window.count-subarrays-shrink-valid
type: cloze
anki: 1787268627136
tags: [concept-cloze, invariant, leetcode, recall]
---
该计数法的不变量是:固定right时,合法左端点构成的后缀区间共有{{c1::right - left + 1}}个。

内层while收缩直到[left, right]合法为止；固定right时,合法左端点构成后缀区间[left, right],共right-left+1个

**Evidence**

§2.3.1 越短越合法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.04%20-%20%E5%AE%9A%E9%95%BF%E6%94%B6%E7%BC%A9%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E7%9F%AD%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
