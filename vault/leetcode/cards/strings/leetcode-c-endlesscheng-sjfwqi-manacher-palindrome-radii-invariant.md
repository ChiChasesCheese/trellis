---
id: leetcode-c-endlesscheng-sjfwqi-manacher-palindrome-radii-invariant
node: strings.manacher-palindrome-radii
type: cloze
anki: 1788743828211
tags: [concept-cloze, invariant, leetcode, recall]
---
Manacher 中 i 落在当前最右回文内时，半径初值为 {{c1::min(right - i, radius[mirror])}}。

center 和 right 描述当前右边界最远的已知回文；位置 i 在 right 内时，初始半径不能超过镜像半径和 right-i 两者的较小值

**Evidence**

三、Manacher 算法（回文串）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.03%20-%20Manacher%20%E5%9B%9E%E6%96%87%E5%8D%8A%E5%BE%84)
