---
id: leetcode-c-endlesscheng-g0n5iy-two-stack-editor-recognition
node: stack-queue-monotonic.two-stack-editor
type: cloze
anki: 1787272480980
tags: [concept-cloze, leetcode, recall, recognition]
---
文本操作围绕可移动光标，且需频繁左右移动时，用 {{c1::对顶栈}}。

把光标左、右两侧分别存入两个栈；插入、删除和移动只操作栈顶，从而避免字符串中间操作的线性搬移。

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.18%20-%20%E5%AF%B9%E9%A1%B6%E6%A0%88%E5%85%89%E6%A0%87%E6%A8%A1%E6%8B%9F)
