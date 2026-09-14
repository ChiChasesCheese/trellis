---
id: leetcode-c-endlesscheng-luu0kb-monotonic-stack-and-contribution-invariant
node: stack-queue-monotonic.monotonic-stack-and-contribution
type: cloze
anki: 1787272460379
tags: [concept-cloze, invariant, leetcode, recall]
---
单调栈中元素被弹出时，当前下标就是它的 {{c1::右侧第一个破坏单调性的边界}}。

栈中下标对应的值保持单调；新元素弹出栈顶时，确定了被弹元素的右边界；边界定义中的严格与非严格比较必须成对设计以去重

**Evidence**

四、数据结构：单调栈

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.16%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E4%B8%8E%E8%B4%A1%E7%8C%AE%E6%B3%95)
