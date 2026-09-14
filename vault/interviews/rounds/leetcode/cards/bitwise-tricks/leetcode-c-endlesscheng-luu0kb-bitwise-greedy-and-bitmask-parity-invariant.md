---
id: leetcode-c-endlesscheng-luu0kb-bitwise-greedy-and-bitmask-parity-invariant
node: bitwise-tricks.bitwise-greedy-and-bitmask-parity
type: cloze
anki: 1787272462480
tags: [concept-cloze, invariant, leetcode, recall]
---
位掩码的第 b 位为 1 表示属性 b 当前出现了 {{c1::奇数次}}。

逐位贪心确定高位后，不会被低位决策推翻；XOR 掩码第 b 位表示属性 b 的奇偶性；两状态 XOR 表示它们之间奇偶性差异

**Evidence**

一、技巧类题目：位运算

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.23%20-%20%E4%BD%8D%E8%BF%90%E7%AE%97%E8%B4%AA%E5%BF%83%E4%B8%8E%E4%BD%8D%E6%8E%A9%E7%A0%81%E5%A5%87%E5%81%B6%E7%8A%B6%E6%80%81)
