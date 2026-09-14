---
id: leetcode-c-endlesscheng-sjfwqi-minimum-rotation-recognition
node: strings.minimum-rotation
type: cloze
anki: 1788743829011
tags: [concept-cloze, leetcode, recall, recognition]
---
“任意次循环左移后字典序最小”是 {{c1::最小表示法}} 的直接信号。

在 s+s 上比较循环起点；首次失配后，较大候选及其此前缀对齐的起点都可一次排除，从而线性求最小循环同构串。

**Evidence**

五、最小表示法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.06%20-%20%E6%9C%80%E5%B0%8F%E8%A1%A8%E7%A4%BA%E6%B3%95)
