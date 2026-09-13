---
id: leetcode-c-endlesscheng-caoj45-lowbit-and-bit-library-functions-template
node: bitwise-tricks.lowbit-and-bit-library-functions
type: cloze
anki: 1787272453580
tags: [concept-cloze, leetcode, recall, template]
---
在 Python 中计算集合 s（整数表示）的元素个数应调用 {{c1::s.bit_count()}}，计算最小元素则应先取 lowbit 再调用 {{c2::bit_length() - 1}}。

这些库函数均为 O(1) 时间复杂度。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.03%20-%20lowbit%20%E8%BF%90%E7%AE%97%E4%B8%8E%E9%9B%86%E5%90%88%E4%BF%A1%E6%81%AF%E5%BA%93%E5%87%BD%E6%95%B0)
