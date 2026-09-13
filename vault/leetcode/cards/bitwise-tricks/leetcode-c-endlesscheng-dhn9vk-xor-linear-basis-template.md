---
id: leetcode-c-endlesscheng-dhn9vk-xor-linear-basis-template
node: bitwise-tricks.xor-linear-basis
type: cloze
anki: 1787272407605
tags: [concept-cloze, leetcode, recall, template]
---
插入 x 时，遇到已存在的同最高位基向量就执行 {{c1::x ^= basis[bit]}} 来消元。

若最终 x 为 0，则它线性相关。

**Evidence**

七、线性基

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F05.08%20-%20XOR%20%E7%BA%BF%E6%80%A7%E5%9F%BA)
