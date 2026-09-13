---
id: leetcode-c-endlesscheng-sjfwqi-center-expansion-palindrome-invariant
node: strings.center-expansion-palindrome
type: cloze
anki: 1788743828509
tags: [concept-cloze, invariant, leetcode, recall]
---
中心扩展必须覆盖 {{c1::奇中心和偶中心}}，否则会漏掉一类回文。

每次循环结束时，当前内层区间是以该中心为中心的最长已验证回文；奇偶中心都必须枚举，才能覆盖全部回文子串

**Evidence**

三、Manacher 算法（回文串）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.04%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%E5%9B%9E%E6%96%87)
