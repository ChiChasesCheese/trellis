---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-nearest-boundary-recognition
node: stack-queue-monotonic.monotonic-stack-nearest-boundary
type: cloze
anki: 1787272402907
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要批量求每个元素一侧最近的更大或更小元素时，优先考虑 {{c1::单调栈}}。

在线性扫描数组时，维护仍可能成为后续元素最近边界的下标栈。通过弹出不满足单调关系的元素，可求每个位置左侧或右侧最近的严格更大/更小元素。

**Evidence**

一、单调栈 > §1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.01%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%B1%82%E6%9C%80%E8%BF%91%E6%94%AF%E9%85%8D%E8%BE%B9%E7%95%8C)
