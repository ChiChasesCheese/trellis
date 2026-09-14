---
id: leetcode-c-endlesscheng-sjfwqi-z-function-recognition
node: strings.z-function-lcp
type: cloze
anki: 1787268629737
tags: [concept-cloze, leetcode, recall, recognition]
---
若要批量得到“每个后缀和整串前缀相同多长”，应计算 {{c1::Z 函数}}。

z[i] 记录 s[i:] 与 s 的最长公共前缀长度；维护最右匹配盒子即可在线性时间计算全部 z 值。

**Evidence**

二、Z 函数（后缀的前缀）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.02%20-%20Z%20%E5%87%BD%E6%95%B0%EF%BC%88%E6%89%A9%E5%B1%95%20KMP%EF%BC%89)
