---
id: leetcode-c-endlesscheng-caoj45-iterate-set-bits-template
node: bitwise-tricks.iterate-set-bits
type: cloze
anki: 1787272453879
tags: [concept-cloze, leetcode, recall, template]
---
lowbit 剥离遍历集合的核心循环中，每次迭代先算出 lowbit = t & -t，再执行 {{c1::t ^= lowbit}} 清除该位，最后用 {{c2::lowbit.bit_length() - 1}} 还原出元素下标。

用异或清除已知存在的最低位是安全且高效的写法。

**Evidence**

三、遍历集合

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.04%20-%20%E9%81%8D%E5%8E%86%E4%BD%8D%E5%8E%8B%E7%BC%A9%E9%9B%86%E5%90%88%E4%B8%AD%E7%9A%84%E5%85%83%E7%B4%A0)
