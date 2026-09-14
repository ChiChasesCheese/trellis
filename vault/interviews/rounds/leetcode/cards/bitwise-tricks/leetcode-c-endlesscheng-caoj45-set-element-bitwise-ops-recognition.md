---
id: leetcode-c-endlesscheng-caoj45-set-element-bitwise-ops-recognition
node: bitwise-tricks.set-element-bitwise-ops
type: cloze
anki: 1787272453080
tags: [concept-cloze, leetcode, recall, recognition]
---
当需要判断整数 i 是否属于位压缩集合 s 时，应使用 {{c1::(s >> i) & 1}} 而不是遍历集合逐一比较。

右移 i 位把目标位移到最低位，再与 1 做按位与即可读出该位的值。

**Evidence**

二、集合与元素

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F16.02%20-%20%E9%9B%86%E5%90%88%E4%B8%8E%E5%8D%95%E4%B8%AA%E5%85%83%E7%B4%A0%E7%9A%84%E4%BD%8D%E8%BF%90%E7%AE%97)
