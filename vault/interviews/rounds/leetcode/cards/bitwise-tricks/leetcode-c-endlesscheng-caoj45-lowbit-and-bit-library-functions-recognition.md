---
id: leetcode-c-endlesscheng-caoj45-lowbit-and-bit-library-functions-recognition
node: bitwise-tricks.lowbit-and-bit-library-functions
type: cloze
anki: 1787272453380
tags: [concept-cloze, leetcode, recall, recognition]
---
看到需要反复剥离整数二进制表示的最低位 1（例如逐一取出集合最小元素）时，应联想到 {{c1::lowbit = s & -s}} 这一固定写法。

lowbit 技巧广泛用于树状数组和集合最小元素提取。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.03%20-%20lowbit%20%E8%BF%90%E7%AE%97%E4%B8%8E%E9%9B%86%E5%90%88%E4%BF%A1%E6%81%AF%E5%BA%93%E5%87%BD%E6%95%B0)
