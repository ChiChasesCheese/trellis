---
id: leetcode-c-endlesscheng-mor1u6-monotonic-stack-invariant
node: stack-queue-monotonic.monotonic-stack
type: cloze
anki: 1787272420406
tags: [concept-cloze, invariant, leetcode, recall]
---
单调栈中一个下标被弹出，意味着它的 {{c1::第一个失效右边界}} 已确定。

栈中下标对应的值保持指定单调性；被弹出的元素已找到第一个使其失效的右边界；下标而非仅数值可保留边界信息

**Evidence**

§3.7 单调栈

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.09%20-%20%E5%8D%95%E8%B0%83%E6%A0%88)
