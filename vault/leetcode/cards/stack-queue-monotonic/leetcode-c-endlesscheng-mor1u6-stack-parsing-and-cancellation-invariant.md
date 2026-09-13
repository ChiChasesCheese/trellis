---
id: leetcode-c-endlesscheng-mor1u6-stack-parsing-and-cancellation-invariant
node: stack-queue-monotonic.stack-parsing-and-cancellation
type: cloze
anki: 1787272420104
tags: [concept-cloze, invariant, leetcode, recall]
---
合法括号扫描中，任何前缀的未匹配左括号数必须 {{c1::不小于零}}。

栈内元素都是尚未完成匹配的状态；合法括号任意前缀深度非负，结束时深度为零；运算符栈的优先级不会违反弹栈规则

**Evidence**

§3.4 合法括号字符串（RBS）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.08%20-%20%E6%A0%88%E7%9A%84%E5%8C%B9%E9%85%8D%E3%80%81%E6%B6%88%E9%99%A4%E4%B8%8E%E8%A1%A8%E8%BE%BE%E5%BC%8F%E8%A7%A3%E6%9E%90)
