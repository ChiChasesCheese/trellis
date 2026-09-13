---
id: leetcode-c-endlesscheng-g0n5iy-two-stack-editor-invariant
node: stack-queue-monotonic.two-stack-editor
type: cloze
anki: 1787272481079
tags: [concept-cloze, invariant, leetcode, recall]
---
对顶栈中 right 的栈顶应是 {{c1::光标右侧最近字符}}。

left 从左到右存储光标左侧文本；right 的栈顶是光标右侧最近字符；left 与反转后的 right 拼接为完整文本

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.18%20-%20%E5%AF%B9%E9%A1%B6%E6%A0%88%E5%85%89%E6%A0%87%E6%A8%A1%E6%8B%9F)
