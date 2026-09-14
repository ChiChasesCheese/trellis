---
id: leetcode-c-endlesscheng-mdfnkw-negative-mod-normalization-recognition
node: math-number-theory.negative-mod-normalization
type: cloze
anki: 1787272450979
tags: [concept-cloze, leetcode, recall, recognition]
---
在 C++/Java 等语言中，对负数取模可能得到负结果，此时应使用 {{c1::(x mod m + m) mod m}} 将结果规范到 [0, m-1]。

Python 的 % 对正模数天然非负，可忽略此调整。

**Evidence**

负数和减法的取模

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.04%20-%20%E8%B4%9F%E6%95%B0%E4%B8%8E%E5%87%8F%E6%B3%95%E5%8F%96%E6%A8%A1%E7%9A%84%E8%A7%84%E8%8C%83%E5%8C%96)
