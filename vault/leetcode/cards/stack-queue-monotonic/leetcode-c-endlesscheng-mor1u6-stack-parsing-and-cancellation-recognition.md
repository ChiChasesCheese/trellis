---
id: leetcode-c-endlesscheng-mor1u6-stack-parsing-and-cancellation-recognition
node: stack-queue-monotonic.stack-parsing-and-cancellation
type: cloze
anki: 1787272420005
tags: [concept-cloze, leetcode, recall, recognition]
---
新输入只会处理最近一个未完成状态时，使用 {{c1::栈}}。

栈保存尚未被后续输入解决的局部状态：成对匹配、相邻抵消、嵌套结构和运算符优先级。对顶栈从两端共享容量。

**Evidence**

§3.1-§3.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.08%20-%20%E6%A0%88%E7%9A%84%E5%8C%B9%E9%85%8D%E3%80%81%E6%B6%88%E9%99%A4%E4%B8%8E%E8%A1%A8%E8%BE%BE%E5%BC%8F%E8%A7%A3%E6%9E%90)
