---
id: leetcode-c-endlesscheng-sjfwqi-kmp-prefix-function-recognition
node: strings.kmp-prefix-function
type: cloze
anki: 1787272447305
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求在线性时间内找模式串全部出现位置，且可能有重叠匹配时，优先考虑 {{c1::KMP}}。

用模式串每个前缀的最长 border 长度，在失配时复用已匹配的信息，实现线性子串匹配。

**Evidence**

一、KMP（前缀的后缀）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.01%20-%20KMP%20%E7%AE%97%E6%B3%95%EF%BC%88%E5%89%8D%E7%BC%80%E5%87%BD%E6%95%B0%20-%20border%EF%BC%89)
