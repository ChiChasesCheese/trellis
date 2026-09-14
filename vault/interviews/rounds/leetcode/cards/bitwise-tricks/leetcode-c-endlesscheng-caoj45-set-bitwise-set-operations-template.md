---
id: leetcode-c-endlesscheng-caoj45-set-bitwise-set-operations-template
node: bitwise-tricks.set-bitwise-set-operations
type: cloze
anki: 1787272452980
tags: [concept-cloze, leetcode, recall, template]
---
在 Python 中判断集合 a 是否为集合 b 的子集应写成 (a & b) == a，注意 {{c1::& 的运算符优先级低于 ==}}，必须加括号，否则会先执行 {{c2::b == a}} 的比较再与 a 做按位与，导致逻辑错误。

许多语言中位运算符优先级都低于比较运算符，这是常见的位运算陷阱。

**Evidence**

一、集合与集合 注3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.01%20-%20%E7%94%A8%E4%BD%8D%E8%BF%90%E7%AE%97%E5%AE%9E%E7%8E%B0%E9%9B%86%E5%90%88%E9%97%B4%E8%BF%90%E7%AE%97)
