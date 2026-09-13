---
id: leetcode-c-endlesscheng-sjfwqi-minimum-rotation-invariant
node: strings.minimum-rotation
type: cloze
anki: 1788743829110
tags: [concept-cloze, invariant, leetcode, recall]
---
最小表示法首次在偏移 k 失配时，可排除较大候选起点及其后的 {{c1::k 个对齐起点}}。

i 和 j 是尚未排除的两个候选循环起点；在首次失配 k 处较大的候选，可排除从该候选到该候选+k 的所有起点

**Evidence**

五、最小表示法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.06%20-%20%E6%9C%80%E5%B0%8F%E8%A1%A8%E7%A4%BA%E6%B3%95)
